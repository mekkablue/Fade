# Fade

Glyphs.app plug-in for removing parts of glyphs beneath or beyond a certain coordinate:

![Fade](Fade.png)

After installation, *Fade* will appear in the *Filter* menu.

### Usage

* `x>250` will cut away everything right of x=250
* `x<200, y>300` will cut away everything left of x=200 and above y=300
* `y<100, y>700` will leave only shapes between y=100 and y=700

### Installation

1. Open *Window > Plugin Manager*
2. Find *Fade* and click the *Install* button
3. Restart Glyphs.app

### License

Copyright 2020 Rainer Erich Scheichelbauer (@mekkablue).
Based on sample code by Georg Seifert (@schriftgestalt) and Jan Gerner (@yanone).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
