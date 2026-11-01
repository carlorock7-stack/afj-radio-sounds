# AFJ Radio sounds

Recorded single notes of real instruments for **AFJ Radio** on [aurorafj.org](https://aurorafj.org) (`radio.js` in the
site's repository). The site loads them through the free jsDelivr CDN:

`https://cdn.jsdelivr.net/gh/carlorock7-stack/afj-radio-sounds@<commit>/v1/<name>.mp3`

(`<commit>` is the commit id written in `RD_SND_BASE` in `radio.js`: a fixed commit never changes, so cached copies stay right.)

- **Source and licence**: rendered from the FluidR3Mono General MIDI soundfont, MIT licence. See `ATTRIBUTION.md` and `LICENSE`.
- **What is inside**: one mp3 per instrument with one note every 3 semitones, `slot` seconds apart (the player shifts the
  pitch to the notes in between), and one mp3 per drum kit with one hit per slot. `v1/manifest.json` lists the notes or
  hits of every file, their loudness and peaks. Only single notes and hits: every melody, chord and rhythm is composed
  by AFJ's code.
- **Versions**: the site pins a commit, so a commit never changes. New instruments or kits may be added to `v1/`
  (render only them: `python3 tools/render.py FluidR3Mono_GM.sf3 v1 <name,name>`); never change or delete an existing
  file there (re-recorded sounds go in a new folder, `v2/`). Then point `RD_SND_BASE` in `radio.js` at the new commit.
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
| `kit_electronic` | 30 drum hits |

## v2: real instruments

Built by `tools/build_v2.py` from free libraries (CC0 and one CC BY 3.0 instrument; see `ATTRIBUTION.md`): two or three
dynamics layers per instrument (`<name>_0.mp3` soft, `_1` hard…), and two takes of each drum hit at three dynamics.
The site prefers v2 and uses v1 for the instruments v2 does not have.

| File | Contents |
|---|---|
| `accordion` | 10 notes × 1 dynamics layers |
| `altosax` | 10 notes × 2 dynamics layers |
| `cellos` | 9 notes × 2 dynamics layers |
| `clav` | 12 notes × 2 dynamics layers |
| `cleangtr` | 15 notes × 2 dynamics layers |
| `fbass` | 12 notes × 2 dynamics layers |
| `flute` | 10 notes × 2 dynamics layers |
| `fmep` | 16 notes × 2 dynamics layers |
| `harmonica` | 7 notes × 1 dynamics layers |
| `kit2_808` | 10 hits × 1 dynamics × 1 takes |
| `kit2_brush` | 11 hits × 3 dynamics × 2 takes |
| `kit2_garage` | 11 hits × 3 dynamics × 2 takes |
| `kit2_jazz` | 11 hits × 3 dynamics × 2 takes |
| `kit2_rock` | 11 hits × 3 dynamics × 2 takes |
| `kit2_vintage` | 11 hits × 3 dynamics × 2 takes |
| `mutetpt` | 6 notes × 2 dynamics layers |
| `nylon` | 15 notes × 1 dynamics layers |
| `organ` | 14 notes × 1 dynamics layers |
| `perc2` | 18 hits × 3 dynamics × 2 takes |
| `piano` | 18 notes × 2 dynamics layers |
| `steel` | 15 notes × 1 dynamics layers |
| `strings` | 10 notes × 2 dynamics layers |
| `tenorsax` | 10 notes × 2 dynamics layers |
| `trombone` | 7 notes × 2 dynamics layers |
| `trumpet` | 9 notes × 2 dynamics layers |
| `ukulele` | 7 notes × 1 dynamics layers |
| `upright` | 11 notes × 1 dynamics layers |
| `vibes` | 11 notes × 2 dynamics layers |
| `violin` | 10 notes × 2 dynamics layers |
| `wurli` | 12 notes × 2 dynamics layers |
