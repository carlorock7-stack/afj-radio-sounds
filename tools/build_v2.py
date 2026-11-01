#!/usr/bin/env python3
"""Builds folder v2/ of the AFJ Radio sounds: real recorded instruments with dynamics layers and alternating takes.

Sources (all free; see ATTRIBUTION.md):
  - maistro-sounds v2 (CC0 1.0): instruments from Karoryfer Lecolds and Versilian Studios libraries
  - Greg Sullivan's Wurlitzer EP200 (CC BY 3.0, credit required)
  - Fischer TR-808 samples via kringel-samples (CC0 1.0)
Only single notes and single hits are taken. Each instrument layer becomes ONE mono mp3 with one note per `slot`
seconds; each drum kit becomes one mp3 with every hit at each dynamics layer and take. manifest.json describes them.

Usage: python3 tools/build_v2.py <maistro-sounds clone> <E-Pianos clone> <kringel-samples clone> v2
(partial clones are fine: the needed files are fetched in one go)."""
import json, math, os, re, subprocess, sys, array, tempfile
import numpy as np
MA, EP, KR, OUT = sys.argv[1:5]
SR = 44100
os.makedirs(OUT, exist_ok=True)
tmp = tempfile.mkdtemp()

def man(inst): return json.loads(subprocess.check_output(['git', '-C', MA, 'show', 'HEAD:v2/%s/manifest.json' % inst]))
def fetch(repo, paths):
    if paths: subprocess.run(['git', '-C', repo, 'checkout', 'HEAD', '--'] + sorted(set(paths)), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def pcm(path, gain_db=0.0, length=None):
    """decode to mono float array at SR"""
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-af', 'volume=%.2fdB' % gain_db, '-f', 's16le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    return a[:int(length * SR)] if length else a
def place(slots, slot):
    """notes in fixed slots, each faded out before the next"""
    n = int(slot * SR); out = np.zeros(n * len(slots), dtype=np.float32)
    for i, s in enumerate(slots):
        seg = np.array(s[:n - int(0.02 * SR)], dtype=np.float32)
        fade = min(len(seg), int(0.08 * SR))
        if fade: seg[len(seg) - fade:] *= np.linspace(1, 0, fade, dtype=np.float32)
        out[i * n: i * n + len(seg)] = seg
    return out
def write(samples, name, norm):
    a = np.clip(samples * norm * 32767, -32767, 32767).astype(np.int16)
    w = os.path.join(tmp, name + '.raw'); a.tofile(w)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', w, '-c:a', 'libmp3lame', '-b:a', '64k', os.path.join(OUT, name + '.mp3')], check=True)
def peak(xs): return float(np.max(np.abs(xs))) if len(xs) else 0.0
def rms1(xs): seg = xs[:SR]; return float(np.sqrt(np.mean(seg * seg))) if len(seg) else 0.0
def kc(r): return r['keycenter'] if r['keycenter'] is not None else r['lokey']

# name: (maistro instrument, articulation or None, lowest, highest, velocity targets, slot seconds)
PITCHED = {
    'piano': ('piano', 'natural', 33, 96, [50, 110], 3.0), 'fmep': ('epiano-fm', None, 36, 96, [45, 110], 2.6), 'clav': ('clav-fm', None, 40, 84, [60, 115], 1.6),
    'organ': ('organ-drawbar', None, 36, 90, [100], 2.6), 'vibes': ('vibraphone', 'soft', 53, 88, [60, 115], 2.8),
    'cleangtr': ('guitar-electric', None, 40, 84, [55, 110], 2.6), 'nylon': ('guitar-nylon', None, 38, 84, [100], 2.8), 'steel': ('guitar-steel', None, 40, 83, [100], 2.6),
    'ukulele': ('ukulele', None, 52, 84, [100], 1.8), 'fbass': ('bass-finger', 'sustain', 26, 60, [55, 110], 2.2), 'upright': ('bass-upright', 'sustain', 26, 58, [100], 2.2),
    'altosax': ('sax-alto', None, 52, 80, [60, 115], 2.6), 'tenorsax': ('sax-tenor', 'sustain', 45, 82, [60, 115], 2.6), 'trumpet': ('trumpet', 'sustain', 55, 84, [60, 115], 2.4),
    'mutetpt': ('trumpet', 'harmon', 55, 84, [60, 115], 2.4), 'trombone': ('trombone', 'sustain', 36, 65, [60, 115], 2.4), 'flute': ('flute', 'vibrato', 60, 96, [60, 115], 2.4),
    'harmonica': ('harmonica', 'sustain', 60, 90, [100], 2.4), 'accordion': ('accordion', None, 47, 79, [100], 2.4), 'violin': ('violin', 'sustain', 55, 93, [60, 115], 2.6),
    'strings': ('strings-violins', 'sustain', 55, 86, [60, 115], 3.0), 'cellos': ('strings-cellos', 'sustain', 36, 66, [60, 115], 3.0),
}
# drum kits: hit -> (instrument, GM key, articulation or None); velocity targets and takes per kit
HITS = {'kick': 36, 'snare': 38, 'rim': 37, 'clap': 39, 'hat': 42, 'ohat': 46, 'pedal': 44, 'ride': 51, 'tom': 45, 'tomhi': 48, 'surdo': 41}
KITS = {'kit2_vintage': ('drums-vintage', None), 'kit2_garage': ('drums-garage', 'sticks'), 'kit2_jazz': ('drums-jazz', 'sticks'), 'kit2_brush': ('drums-brush', 'brush'), 'kit2_rock': ('drums-rock', 'sticks')}
PERC = {'conga': 63, 'congalo': 64, 'congamute': 62, 'bongo': 60, 'bongolo': 61, 'agogo': 67, 'cabasa': 69, 'shaker': 82, 'guiro': 73, 'clave': 75, 'wood': 76,
        'tamb': 54, 'cowbell': 56, 'cajon': 86, 'cajonslap': 87, 'djembe': 88, 'clap': 39, 'triangle': 81}
DVEL, TAKES, DSLOT = [40, 80, 120], 2, 1.1

def pick(R, key, vel, art, take=1):
    c = [r for r in R if kc(r) == key and r['lovel'] <= vel <= r['hivel'] and (art is None or r.get('articulation') in (art, None)) and r.get('trigger', 'attack') == 'attack']
    if not c: return None
    t = [r for r in c if r.get('seqPosition', 1) == take] or c
    return t[0]

out = {'v': 2, 'files': {}}
jobs = []   # (name, kind, [(path, gain)], meta)
for name, (inst, art, lo, hi, vels, slot) in PITCHED.items():
    m = man(inst); R = m['regions']
    keys = sorted(set(kc(r) for r in R if lo <= kc(r) <= hi and (art is None or r.get('articulation') in (art, None))))
    chosen = []
    for k in keys:
        if not chosen or k - chosen[-1] >= 3: chosen.append(k)
    layers = []
    for v in vels:
        regs = [pick(R, k, v, art) for k in chosen]
        layers.append(regs)
    ok = [i for i, k in enumerate(chosen) if all(L[i] for L in layers)]
    chosen = [chosen[i] for i in ok]; layers = [[L[i] for i in ok] for L in layers]
    jobs.append((name, 'pitched', inst, m.get('gainDb', 0), chosen, layers, vels, slot))
for name, (inst, art) in KITS.items():
    m = man(inst); R = m['regions']
    cells = []
    for h, key in HITS.items():
        for v in DVEL:
            for t in range(1, TAKES + 1):
                cells.append((h, v, pick(R, key, v, art, t) or pick(R, key, v, None, t)))
    jobs.append((name, 'kit', inst, m.get('gainDb', 0), cells))
m = man('percussion'); R = m['regions']
cells = []
for h, key in PERC.items():
    for v in DVEL:
        for t in range(1, TAKES + 1):
            cells.append((h, v, pick(R, key, v, None, t)))
jobs.append(('perc2', 'kit', 'percussion', m.get('gainDb', 0), cells))

# fetch every file needed, in one go
need = []
for j in jobs:
    if j[1] == 'pitched':
        for L in j[5]:
            need += ['v2/%s/%s' % (j[2], r['file']) for r in L]
    else:
        need += ['v2/%s/%s' % (j[2], c[2]['file']) for c in j[4] if c[2]]
print('fetching', len(set(need)), 'files'); fetch(MA, need)

for j in jobs:
    if j[1] == 'pitched':
        name, _, inst, g0, notes, layers, vels, slot = j
        tracks = []
        for L in layers:
            tracks.append(place([pcm(os.path.join(MA, 'v2', inst, r['file']), g0 + r.get('volumeDb', 0), slot) for r in L], slot))
        norm = 0.9 / max(peak(t) for t in tracks)
        ent = {'slot': slot, 'notes': notes, 'layers': []}
        for li, t in enumerate(tracks):
            fn = name if len(tracks) == 1 else '%s_%d' % (name, li)
            write(t, fn, norm)
            ent['layers'].append({'f': fn, 'v': round(((vels[li] + vels[li + 1]) / 2 if li + 1 < len(vels) else 127) / 127, 3), 'loud': round(sum(rms1(t[int(i * slot * SR):]) for i in range(len(notes))) / len(notes) * norm, 4)})
        out['files'][name] = ent
        print(name, len(notes), 'notes x', len(tracks), 'layers', sum(os.path.getsize(os.path.join(OUT, l['f'] + '.mp3')) for l in ent['layers']) // 1024, 'KB')
    else:
        name, _, inst, g0, cells = j
        segs = [pcm(os.path.join(MA, 'v2', inst, c[2]['file']), g0 + c[2].get('volumeDb', 0), DSLOT) if c[2] else [] for c in cells]
        t = place(segs, DSLOT); norm = 0.9 / max(peak(t), 1e-6); write(t, name, norm)
        hits = list(dict.fromkeys(c[0] for c in cells))
        pk = [round(peak(s) * norm, 3) for s in segs]
        out['files'][name] = {'slot': DSLOT, 'hits': hits, 'vels': [round(v / 127, 3) for v in DVEL], 'takes': TAKES, 'pk': pk}
        print(name, len(hits), 'hits', os.path.getsize(os.path.join(OUT, name + '.mp3')) // 1024, 'KB', 'missing:', sorted(set(c[0] for c in cells if not c[2])))

# Wurlitzer EP200 (CC BY 3.0, Greg Sullivan): its sfz maps notes and dynamics (pp, mp, f, ff)
sfz = open(os.path.join(EP, 'Wurlitzer EP200', 'Wurlitzer EP200.sfz'), errors='ignore').read()
regs = []; grp = {}
for hdr, body in re.findall(r'<(\w+)>([^<]*)', sfz):
    kv = dict(re.findall(r'(\w+)=([^\s<]+)', body))
    if hdr in ('group', 'master', 'global'): grp = kv; continue
    if hdr != 'region': continue
    kv = dict(grp, **kv)
    if 'sample' in kv:
        regs.append({'f': kv['sample'].replace('\\', '/').replace('$EXT', 'flac'), 'key': int(kv.get('pitch_keycenter', kv.get('key', 0))), 'lovel': int(kv.get('lovel', 1)), 'hivel': int(kv.get('hivel', 127)), 'tune': float(kv.get('tune', 0)), 'vol': float(kv.get('volume', 0))})
wv = [55, 100]   # the mp and f layers; each keeps the notes it was recorded at
wl = []
for v in wv:
    seen = {}
    for r in regs:
        if r['lovel'] <= v <= r['hivel'] and 33 <= r['key'] <= 92 and r['key'] not in seen: seen[r['key']] = r
    wl.append([seen[k] for k in sorted(seen)])
fetch(EP, ['Wurlitzer EP200/Samples/' + r['f'] for L in wl for r in L])
tracks = [place([pcm(os.path.join(EP, 'Wurlitzer EP200', 'Samples', r['f']), r['vol'], 2.8) for r in L], 2.8) for L in wl]
norm = 0.9 / max(peak(t) for t in tracks); ent = {'slot': 2.8, 'notes': [r['key'] for r in wl[0]], 'layers': []}
for li, t in enumerate(tracks):
    write(t, 'wurli_%d' % li, norm)
    ent['layers'].append({'f': 'wurli_%d' % li, 'v': [0.6, 1][li], 'notes': [r['key'] for r in wl[li]], 'loud': round(sum(rms1(t[int(i * 2.8 * SR):]) for i in range(len(wl[li]))) / len(wl[li]) * norm, 4)})
out['files']['wurli'] = ent; print('wurli', [len(L) for L in wl], 'notes per layer')

# TR-808 one-shots (CC0, Fischer, via kringel-samples)
K8 = {'kick': 'bd', 'snare': 'sd', 'clap': 'cp', 'hat': 'hh', 'ohat': 'oh', 'rim': 'rim', 'tom': 'lt', 'tomhi': 'ht', 'cowbell': 'cb', 'shaker': 'sh'}
segs = [pcm(os.path.join(KR, 'Fischer808', f + '.wav'), 0, DSLOT) for f in K8.values()]
t = place(segs, DSLOT); norm = 0.9 / peak(t); write(t, 'kit2_808', norm)
out['files']['kit2_808'] = {'slot': DSLOT, 'hits': list(K8), 'vels': [1], 'takes': 1, 'pk': [round(peak(s) * norm, 3) for s in segs]}
out['lead'] = 0.0
json.dump(out, open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)
print('total', sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) // 1024, 'KB')
