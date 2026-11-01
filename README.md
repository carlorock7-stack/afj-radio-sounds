# AFJ Radio sounds

Recorded single notes of real instruments for **AFJ Radio** on [aurorafj.org](https://aurorafj.org) (`radio.js` in the
site's repository). The site loads them through the free jsDelivr CDN:

`https://cdn.jsdelivr.net/gh/carlorock7-stack/afj-radio-sounds@v1/v1/<name>.mp3`

- **Source and licence**: rendered from the FluidR3Mono General MIDI soundfont, MIT licence. See `ATTRIBUTION.md` and `LICENSE`.
- **What is inside**: one mp3 per instrument with one note every 3 semitones, `slot` seconds apart (the player shifts the
  pitch to the notes in between), and one mp3 per drum kit with one hit per slot. `v1/manifest.json` lists the notes or
  hits of every file, their loudness and peaks. Only single notes and hits: every melody, chord and rhythm is composed
  by AFJ's code.
- **Versions**: the site points at the git tag `v1`. Never change files under a published tag; put new or changed
  sounds in a new folder and tag (`v2/`, tag `v2`) and update `RD_SND_BASE` in `radio.js`.
- **Rebuild**: `python3 tools/render.py FluidR3Mono_GM.sf3 v1 && python3 tools/stats.py v1` (needs fluidsynth and ffmpeg).

| File | Contents |
|---|---|
| `piano` | 17 notes, MIDI 36–84 |
| `mellowpiano` | 17 notes, MIDI 36–84 |
| `ep` | 15 notes, MIDI 40–82 |
| `fmep` | 14 notes, MIDI 43–82 |
| `organ` | 14 notes, MIDI 41–80 |
| `clav` | 11 notes, MIDI 45–75 |
| `vibes` | 13 notes, MIDI 53–89 |
| `marimba` | 13 notes, MIDI 53–89 |
| `kalimba` | 11 notes, MIDI 55–85 |
| `celesta` | 13 notes, MIDI 60–96 |
| `musicbox` | 13 notes, MIDI 60–96 |
| `nylon` | 14 notes, MIDI 40–79 |
| `steel` | 14 notes, MIDI 43–82 |
| `twelve` | 13 notes, MIDI 52–88 |
| `mandolin` | 12 notes, MIDI 55–88 |
| `ukulele` | 10 notes, MIDI 55–82 |
| `jazzgtr` | 15 notes, MIDI 40–82 |
| `cleangtr` | 15 notes, MIDI 40–82 |
| `funkgtr` | 11 notes, MIDI 45–75 |
| `overdrive` | 15 notes, MIDI 40–82 |
| `upright` | 10 notes, MIDI 28–55 |
| `fbass` | 10 notes, MIDI 28–55 |
| `fretless` | 10 notes, MIDI 28–55 |
| `slap` | 10 notes, MIDI 28–55 |
| `synthbass` | 10 notes, MIDI 28–55 |
| `trumpet` | 10 notes, MIDI 55–82 |
| `mutetpt` | 10 notes, MIDI 55–82 |
| `altosax` | 11 notes, MIDI 52–82 |
| `tenorsax` | 12 notes, MIDI 45–78 |
| `flute` | 13 notes, MIDI 60–96 |
| `panflute` | 12 notes, MIDI 60–93 |
| `harmonica` | 10 notes, MIDI 55–82 |
| `violin` | 13 notes, MIDI 55–91 |
| `accordion` | 13 notes, MIDI 48–84 |
| `italianacc` | 13 notes, MIDI 48–84 |
| `bandoneon` | 12 notes, MIDI 48–81 |
| `strings` | 15 notes, MIDI 41–83 |
| `slowstrings` | 15 notes, MIDI 41–83 |
| `tremstrings` | 13 notes, MIDI 48–84 |
| `pizz` | 13 notes, MIDI 48–84 |
| `synthstrings` | 15 notes, MIDI 41–83 |
| `warmpad` | 15 notes, MIDI 41–83 |
| `brass` | 11 notes, MIDI 48–78 |
| `kit_standard` | 30 drum hits |
| `kit_room` | 30 drum hits |
| `kit_power` | 30 drum hits |
| `kit_808` | 30 drum hits |
| `kit_jazz` | 30 drum hits |
| `kit_brush` | 30 drum hits |
