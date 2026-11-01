#!/usr/bin/env python3
"""Adds the peak of every note / drum hit to manifest.json ("pk"), so the player can balance them. Flags silent slots.
Usage: python3 tools/stats.py v1"""
import json, os, subprocess, sys, array
D = sys.argv[1]; SR = 22050
man = json.load(open(os.path.join(D, 'manifest.json')))
bad = []
for name, f in man['files'].items():
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', os.path.join(D, name + '.mp3'), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    a = array.array('h', raw); n = len(f.get('notes') or f.get('hits'))
    pk = []
    for i in range(n):
        seg = a[int((i * f['slot']) * SR): int((i + 1) * f['slot'] * SR)]
        p = max((abs(x) for x in seg), default=0) / 32768; pk.append(round(p, 3))
        if p < 0.02: bad.append((name, i))
    f['pk'] = pk
json.dump(man, open(os.path.join(D, 'manifest.json'), 'w'), indent=1)
print('silent or nearly silent slots:', bad)
