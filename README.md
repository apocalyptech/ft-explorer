FilterTool Explorer (ft-explorer)
=================================

This is a little Python 3 / PyQt5 application to enable browsing of the
resource data used by the excellent Borderlands 2/TPS modding tool
[FilterTool](https://github.com/BLCM/BLCMods/wiki/UCP-Filter-Tool).

I threw this together because I like the way
[UE Explorer](http://eliotvu.com/portfolio/view/21/ue-explorer) lets you
browse around Borderlands objects/classes in a nice tree format, but using
UE Explorer is often a bit cumbersome: it doesn't work fantastically under
Wine *(I'm running Linux)*, it'll often require tweaks to its settings to
properly display some properties, and you've got to know or guess which UPK
file you need to look in to find what you're looking for.

Similarly, FilterTool is great for searching around and viewing Borderlands
data, because it contains an awful lot of pre-dumped class/object data
*(258MB uncompressed, in fact)*, but even though it's got an
autocomplete-like function, I often find myself missing the GUI browsing
which UE Explorer provides.

So, enter this app!  It takes the FilterTool pre-dumped data and presents
it in a tree, like UE Explorer would do.

Usage
-----

This utility requires that all of FilterTool's resource files be stored in
the `resources` directory alongside `ft-explorer.py`.  You can extract
them from `FilterTool.jar` with probably any unzip program, or with the
`jar` utility, if you're feeling fancy.

Simply run `ft-explorer.py` and it should do its thing.  It'll load any
file in the `resources` dir which starts with "`Resource - `" and has
a `.txt` extension.

This is only tested on Linux, and uses Python 3 and PyQt5 to do its stuff.
If running on Windows or OSX, be sure to have those installed, and launch
it from a terminal/commandline of some sort to see any errors which might
pop up.

Status
------

![Main Window](screenshot.png)

This is a pretty quick-and-dirty app, and is unlikely to see much in the
way of feature improvements, or concessions to platforms other than Linux,
mostly because I assume I'm probably the only person who'll ever use it.
If there's Actual Interest from other folks, I'm guessing I could be
convinced to spend some more effort on it.

Some things which are at least somewhat likely to happen:

* Ability to read resources right from the FilterTool zipfile.
* *(could we instead bundle the dumps ourselves?  Will have to inquire with
  the FilterTool folks about redistributability)*
* Selecting between B2 and TPS data
* Remember settings between runs (which toggles are active, etc)

Some things which are less likely to happen:

* Proper packaging *(for any platform)*
* Searching
* Fancy icons and stuff in the tree

License
-------

This is licensed under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).
See [COPYING.txt](COPYING.txt).

The "Dark Theme" is Michell Stuttgart Faria's
[QDarkGray Stylesheet](https://github.com/mstuttgart/qdarkgray-stylesheet)
with a few custom modifications.  QDarkGray Stylesheet is itself a rework of
Colin Duquesnoy's [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet).
It is available under the [MIT License](qdarkgraystyle/COPYING.txt).
