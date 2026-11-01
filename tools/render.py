#!/usr/bin/env python3
"""Renders the AFJ Radio instrument files from the FluidR3Mono General MIDI soundfont (MIT licence, see ATTRIBUTION.md).

Each instrument becomes ONE mp3 file holding single notes, one every `slot` seconds (notes every 3 semitones over the
range AFJ Radio uses; the player shifts the pitch to the notes in between). Each drum kit becomes one mp3 with one hit per
slot. manifest.json lists, per file: the slot length, the MIDI notes (or drum hits) in order, and a loudness gain.
Only single notes and single drum hits are recorded: no melodies, no loops, no phrases.

Usage: python3 tools/render.py <path to FluidR3Mono_GM.sf3> <output folder>   (needs fluidsynth and ffmpeg)
"""
import json, os, struct, subprocess, sys, tempfile, wave, array, math

SF, OUT = sys.argv[1], sys.argv[2]
SR = 44100

# name: (bank, program, lowest, highest, hold seconds, slot seconds). Chosen for the instruments each genre is played with.
# No voices: the soundfont's choir, "oohs" and voice presets are left out on purpose.
INST = {
    # keys and mallets
    'piano': (0, 0, 36, 84, 2.6, 3.1), 'mellowpiano': (8, 0, 36, 84, 2.6, 3.1), 'ep': (0, 4, 40, 82, 2.6, 3.1), 'fmep': (0, 5, 43, 84, 2.6, 3.1),
    'organ': (0, 16, 41, 80, 2.6, 2.9), 'clav': (0, 7, 45, 75, 1.4, 1.8), 'vibes': (0, 11, 53, 89, 2.4, 3.0), 'marimba': (0, 12, 53, 89, 1.2, 1.6),
    'kalimba': (0, 108, 55, 86, 1.6, 2.0), 'celesta': (0, 8, 60, 96, 1.6, 2.1), 'musicbox': (0, 10, 60, 96, 1.8, 2.3),
    # guitars and plucked strings
    'nylon': (0, 24, 40, 79, 2.6, 3.1), 'steel': (0, 25, 43, 84, 2.4, 2.9), 'twelve': (8, 25, 52, 88, 2.4, 2.9), 'mandolin': (16, 25, 55, 88, 1.6, 2.0),
    'ukulele': (8, 24, 55, 84, 1.6, 2.0), 'jazzgtr': (0, 26, 40, 82, 2.4, 2.9), 'cleangtr': (0, 27, 40, 84, 2.4, 2.9), 'funkgtr': (8, 28, 45, 76, 0.8, 1.1),
    'overdrive': (0, 29, 40, 84, 2.4, 2.8),
    # basses
    'upright': (0, 32, 28, 55, 2.0, 2.4), 'fbass': (0, 33, 28, 55, 2.0, 2.4), 'fretless': (0, 35, 28, 55, 2.0, 2.4), 'slap': (0, 36, 28, 55, 1.6, 2.0),
    'synthbass': (8, 38, 28, 55, 1.8, 2.1),
    # leads: horns, reeds, winds, bowed
    'trumpet': (0, 56, 55, 84, 2.4, 2.8), 'mutetpt': (0, 59, 55, 84, 2.4, 2.8), 'altosax': (0, 65, 52, 84, 2.4, 2.8), 'tenorsax': (0, 66, 45, 79, 2.4, 2.8),
    'flute': (0, 73, 60, 96, 2.4, 2.8), 'panflute': (0, 75, 60, 93, 2.4, 2.8), 'harmonica': (0, 22, 55, 84, 2.4, 2.8), 'violin': (0, 40, 55, 91, 2.4, 2.8),
    'accordion': (0, 21, 48, 84, 2.4, 2.8), 'italianacc': (8, 21, 48, 84, 2.4, 2.8), 'bandoneon': (0, 23, 48, 81, 2.4, 2.8),
    # sections and pads
    'strings': (0, 48, 41, 84, 2.8, 3.3), 'slowstrings': (0, 49, 41, 84, 2.8, 3.3), 'tremstrings': (0, 44, 48, 84, 2.6, 3.0), 'pizz': (0, 45, 48, 84, 1.0, 1.4),
    'synthstrings': (0, 50, 41, 84, 2.8, 3.3), 'warmpad': (0, 89, 41, 84, 2.8, 3.4), 'brass': (0, 61, 48, 80, 2.0, 2.4),
}
# drum hits: name -> (GM note, velocity)
HITS = [('kick', 36, 112), ('kicksoft', 36, 70), ('snare', 38, 112), ('ghost', 38, 45), ('clap', 39, 105), ('rim', 37, 100),
        ('hat', 42, 95), ('hatsoft', 42, 50), ('ohat', 46, 90), ('pedal', 44, 80), ('ride', 51, 90), ('tom', 45, 100), ('tomhi', 48, 100), ('surdo', 41, 105),
        ('conga', 63, 100), ('congalo', 64, 100), ('congamute', 62, 90), ('bongo', 60, 100), ('bongolo', 61, 100), ('timbale', 65, 100), ('agogo', 67, 90),
        ('cabasa', 69, 90), ('shaker', 70, 95), ('guiro', 73, 90), ('clave', 75, 100), ('wood', 76, 100), ('tamb', 54, 90), ('cowbell', 56, 90),
        ('brushtap', 38, 50), ('swirl', 40, 70)]
KITS = {'kit_standard': 0, 'kit_room': 8, 'kit_power': 16, 'kit_808': 25, 'kit_jazz': 32, 'kit_brush': 40}
DRUM_SLOT, DRUM_HOLD = 1.2, 0.25

def vlq(n):
    out = [n & 0x7F]; n >>= 7
    while n: out.insert(0, (n & 0x7F) | 0x80); n >>= 7
    return bytes(out)

def midi(events, path):
    """events: [(seconds, bytes)]; 120 bpm, 480 ticks per beat -> 960 ticks per second"""
    trk, last = b'', 0
    trk += vlq(0) + b'\xff\x51\x03' + (500000).to_bytes(3, 'big')
    for t, data in sorted(events, key=lambda x: x[0]):
        tick = int(round(t * 960)); trk += vlq(tick - last) + data; last = tick
    trk += vlq(960) + b'\xff\x2f\x00'
    with open(path, 'wb') as f:
        f.write(b'MThd' + struct.pack('>IHHH', 6, 0, 1, 480) + b'MTrk' + struct.pack('>I', len(trk)) + trk)

def render(mid, wav):
    subprocess.run(['fluidsynth', '-ni', '-q', '-g', '0.5', '-R', '0', '-C', '0', '-r', str(SR), '-F', wav, SF, mid], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def mono_stats(wav, slot, n):
    """peak and loudness (RMS of the first second of each note) of a rendered file"""
    with wave.open(wav) as w:
        ch, frames = w.getnchannels(), w.readframes(w.getnframes())
    a = array.array('h', frames); m = [(a[i] + a[i + 1]) / 2 if ch == 2 else a[i] for i in range(0, len(a), ch)]
    peak = max(abs(x) for x in m) / 32768
    rms = []
    for i in range(n):
        seg = m[int(i * slot * SR): int((i * slot + 1.0) * SR)]
        rms.append(math.sqrt(sum(x * x for x in seg) / max(1, len(seg))) / 32768)
    return peak, rms

def encode(wav, mp3, peak):
    gain = 0.9 / peak if peak > 0 else 1
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-ac', '1', '-af', 'volume=%.4f' % gain, '-c:a', 'libmp3lame', '-b:a', '64k', mp3], check=True)
    return gain

os.makedirs(OUT, exist_ok=True)
man = {'v': 1, 'source': 'FluidR3Mono_GM (MIT licence)', 'files': {}}
tmp = tempfile.mkdtemp()
for name, (bank, prog, lo, hi, hold, slot) in INST.items():
    notes = list(range(lo, hi + 1, 3))
    ev = [(0, bytes([0xB0, 0, bank])), (0, bytes([0xB0, 32, 0])), (0.001, bytes([0xC0, prog]))]
    for i, n in enumerate(notes):
        ev += [(0.05 + i * slot, bytes([0x90, n, 100])), (0.05 + i * slot + hold, bytes([0x80, n, 0]))]
    ev.append((0.05 + len(notes) * slot, bytes([0xB0, 123, 0])))
    mid, wav = os.path.join(tmp, name + '.mid'), os.path.join(tmp, name + '.wav')
    midi(ev, mid); render(mid, wav)
    peak, rms = mono_stats(wav, slot, len(notes))
    g = encode(wav, os.path.join(OUT, name + '.mp3'), peak)
    loud = sum(r * g for r in rms) / len(rms)
    man['files'][name] = {'slot': slot, 'notes': notes, 'loud': round(loud, 4)}
    print(name, len(notes), 'notes', os.path.getsize(os.path.join(OUT, name + '.mp3')) // 1024, 'KB')
for name, kit in KITS.items():
    ev = [(0, bytes([0xC9, kit]))]
    for i, (h, n, v) in enumerate(HITS):
        ev += [(0.05 + i * DRUM_SLOT, bytes([0x99, n, v])), (0.05 + i * DRUM_SLOT + DRUM_HOLD, bytes([0x89, n, 0]))]
    mid, wav = os.path.join(tmp, name + '.mid'), os.path.join(tmp, name + '.wav')
    midi(ev, mid); render(mid, wav)
    peak, rms = mono_stats(wav, DRUM_SLOT, len(HITS))
    g = encode(wav, os.path.join(OUT, name + '.mp3'), peak)
    man['files'][name] = {'slot': DRUM_SLOT, 'hits': [h[0] for h in HITS], 'loud': [round(r * g, 4) for r in rms]}
    print(name, len(HITS), 'hits', os.path.getsize(os.path.join(OUT, name + '.mp3')) // 1024, 'KB')
# every file starts with the first note at 0.05 s; the page finds the exact start after decoding (mp3 adds a short silence)
man['lead'] = 0.05
with open(os.path.join(OUT, 'manifest.json'), 'w') as f: json.dump(man, f, indent=1)
