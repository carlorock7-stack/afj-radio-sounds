# Attribution and licence of the AFJ Radio instrument sounds

The files in `v1/` are single notes and single drum hits rendered from the **FluidR3Mono General MIDI soundfont**
(`FluidR3Mono_GM.sf3`, as distributed with MuseScore 2.1 / 3.6.2), with `tools/render.py` (fluidsynth, no reverb or
chorus) and encoded as mono mp3 with ffmpeg. They are released under the **MIT licence**, like the soundfont they come
from. The notices below come from the soundfont's licence file and must be kept with any copy of these files.

Only single notes and single drum hits are included: no melodies, phrases or loops. The music AFJ Radio plays is
composed by AFJ's own code (radio.js on aurorafj.org). The soundfont's voice presets (choir, "oohs", synth voice) are
not used.

---

MS_General.sf2
---

Current version: 0.1 alpha 1st March 2018

This is a fork of FluidR3Mono_GM.sf2, with many samples (eventually) being replaced and/or reprogrammed. This version of the SoundFont is an alpha work-in-progress. Information on all sample sources will be provided upon release.

FluidR3 (original version) by Frank Wen Copyright © 2000-2002

Mono conversion (FluidR3Mono) by Michael Cowgill Copyright © 2014-17

Adaptation for MS_General.sf2 by S. Christian Collins Copyright © 2018

Temple Blocks instrument provided by Ethan Winer Copyright © 2002

Drumline Percussion provided by Michael Schorsch Copyright © 2016

MS_General.sf2 is shared under the MIT license as described in COPYING, as was FluidR3Mono and FluidR3 before it. The licensing for this new collection is currently under discussion and may be subject to change before release.

The COPYING and README files from the original FluidR3GM file are now displayed here for reference.

The acknowledgements and copyright notices above must be included in any derivative work.


README
---

Fluid (R3) SoundFont

Copyright (c) 2000-2002, 2008 Frank Wen <getfrank@gmail.com>

I hereby release Fluid under the MIT license, as described in COPYING.


Thanks to Toby Smithe for helping to get Fluid included in Ubuntu.

This package, of course, is the original Release 3 of Fluid.  


Fluid was constructed in part from samples found in the public domain that I
edited/cleaned/remixed/programmed and largely from recordings of my own and
in conjunction with the people below who helped along the way:

Suren M. Seron
Scott Hanan
Steve Aupperle
Chris Gillman
Alex Taubr
Chris Prola
Andrew Klenk
Winfried Hubbe 
Dylan
Tim
Gort
Uros Katic 
Ethan Winer (http://www.ethanwiner.com) 


It's obviously been a few years since the project, but its nice to see that
people are still enjoying my work and getting good use out of it.  As always,
I'd like to hear some work done with Fluid so email me, or just email me to
say hello and tell me what is going on in the computer musician world.
Who knows, maybe I'll kick start this project again? ;)


COPYING
---

Mono version:  Copyright (c) 2014-16 Michael Cowgill 
Copyright (c) 2000-2002, 2008 Frank Wen <getfrank@gmail.com>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.



---

# v2/: real instruments (added November 2026)

`v2/` is made by `tools/build_v2.py` from these free libraries. Only single notes and single drum hits are taken
(two or three dynamics layers, and two takes of each drum hit), trimmed, converted to mono and encoded as mp3.

| Files | Source | Author | Licence |
|---|---|---|---|
| piano, fmep, clav, organ, vibes, cleangtr, nylon, steel, ukulele, fbass, upright, altosax, tenorsax, trumpet, mutetpt, trombone, flute, harmonica, accordion, violin, strings, cellos, kit2_vintage, kit2_garage, kit2_jazz, kit2_brush, kit2_rock, perc2 | [maistro-sounds](https://github.com/atscglobal-ie/maistro-sounds) v2, built from the sfzinstruments libraries of Karoryfer Lecolds (D. Smolken) and Versilian Studios (Big Rusty Drums, Unruly Drums, Swirly Drums, Virtuosity Drums, Black And Blue Basses, Sneakybass, Osiris Piano, Shinyguitar and others listed in its NOTICE.md) | Karoryfer Lecolds, Versilian Studios | CC0 1.0 (public domain dedication; credit given anyway) |
| wurli_0, wurli_1 | [Greg Sullivan's E-Pianos](https://github.com/sfzinstruments/GregSullivan.E-Pianos): Wurlitzer EP200 v1.1 | Greg Sullivan (http://www.sullivang.net/), mapped by kinwie | **CC BY 3.0**: credit required, given on the AFJ Radio page |
| kit2_808 | TR-808 one-shots by Fischer, via [kringel-samples](https://github.com/Gradigang-Solutions/kringel-samples) (from tidalcycles/sounds-tr808-fischer) | Fischer | CC0 1.0 |

Wurlitzer EP200 samples: "Wurlitzer EP200 Electric Piano" by Greg Sullivan, licensed under the Creative Commons
Attribution 3.0 Unported licence (https://creativecommons.org/licenses/by/3.0/). Changes: single notes trimmed,
converted to mono, encoded as mp3, packed into one file per dynamics layer.
