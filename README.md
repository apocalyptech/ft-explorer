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

Simply run `ft-explorer.py` and it should do its thing.

The data from UCP FilterTool 2.2 is bundled with the application, so there is
no need to copy anything over.  The app will load any file in the
`resources/BL2/dumps` and `resources/TPS/dumps` directories which start with
"`Resource - `" and has a `.txt` or `.txt.xz`
*([lzma/lzma2 compression](https://en.wikipedia.org/wiki/Xz))* extension.

Feel free to add your own dump files in there, if what you're looking for
isn't already bundled with FilterTool.  I've added a very small amount of
extra data inside the BL2 file `Resources - FTExplorerAdditions.txt.xz`.

This is only tested on Linux, though I've had reports of it working fine
on Windows as well.  It uses Python 3 and PyQt5 to do its stuff.  If running
on Windows or OSX, be sure to have those installed, and launch it from a
terminal/commandline of some sort to see any errors which might pop up.

Status
------

![Main Window](screenshot.png)

This is a pretty quick-and-dirty app, and is unlikely to see much in the
way of feature improvements, or concessions to platforms other than Linux,
mostly because I assume I'm probably the only person who'll ever use it.
If there's Actual Interest from other folks, I'm guessing I could be
convinced to spend some more effort on it.

Some things which are at least somewhat likely to happen:

* Selecting between B2 and TPS data
* Remember settings between runs (which toggles are active, etc)

Some things which are less likely to happen:

* Proper packaging *(for any platform)*
* Searching
* Fancy icons and stuff in the tree

Credits
-------

The bundled pre-dumped object data is taken from UCP FilterTool, by
[LightChaosman](https://www.youtube.com/channel/UCgJ6TA5sZ_Rwc1LPDYbQT1Q), and
is included with their gracious consent.

License
-------

This is licensed under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).
See [COPYING.txt](COPYING.txt).

The "Dark Theme" is Michell Stuttgart Faria's
[QDarkGray Stylesheet](https://github.com/mstuttgart/qdarkgray-stylesheet)
with a few custom modifications.  QDarkGray Stylesheet is itself a rework of
Colin Duquesnoy's [QDarkStyleSheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet).
It is available under the [MIT License](qdarkgraystyle/COPYING.txt).

Redistribution of the bundled data in the `resources` directory should be
cleared with LightChaosman first.  Try the
[Shadow's Evil Hideout discord channel](https://discord.gg/0YjZxbVBS9b3bXUS).
