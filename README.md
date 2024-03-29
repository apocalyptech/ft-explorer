FilterTool/BLCMM Explorer (ft-explorer)
=======================================

This is a little Python 3 / PyQt5 application to enable browsing of the
resource data used by the excellent Borderlands 2/TPS/AoDK modding tool
[BLCMM](https://github.com/BLCM/BLCMods/wiki/Borderlands-Community-Mod-Manager).
It was written when FilterTool was the tool for Borderlands mod management,
hence this project's name, but BLCMM has since supplanted it.

I threw this together because I like the way
[UE Explorer](http://eliotvu.com/portfolio/view/21/ue-explorer) lets you
browse around Borderlands objects/classes in a nice tree format, but using
UE Explorer is often a bit cumbersome: it doesn't work fantastically under
Wine *(I'm running Linux)*, it'll often require tweaks to its settings to
properly display some properties, and you've got to know or guess which UPK
file you need to look in to find what you're looking for.

BLCMM has some very nice object introspection capabilities as well, in its
own "Object Explorer" tool, but because it needs to be a lot more clever
with searching and the like, its interface is necessarily streamlined, and
doesn't provide a "full" tree like ft-explorer does.  Certainly the release
of BLCMM has made this app a little less vital, though.  BLCMM/Object Explorer
is quite good.

So, in the end, I personally still like using this most of the time for
looking at objects, as compared to BLCMM/OE.  Your mileage may vary, but
feel free to try it out!

Requirements
------------

This is a Python 3 + PyQt5 application.  It's been developed entirely on
Linux, but it works just fine in Windows (and should in Mac as well) so long as
you've got the necessary stuff installed, though Linux folks will have the
easiest time of it.

**Linux:** You may already have these installed via your package manager,
but if not, just use your package manger to install a package named something
like `python-pyqt5` or `pyqt5` or the like, and that should take care of it
for you.

**Windows/Mac:**
1. Install the latest Python 3.x.x version from
  [python.org](https://www.python.org/downloads/).  The latest (as of June 8, 2018) is 3.6.5.
2. Be sure to check the option that says something like "Add Python.exe to path"
  or "Add Python to environment variables" when installing.
3. Hop out to a commandline/terminal/powershell and see if running the command
  `python -V` outputs something like `Python 3.6.4`.
4. If so, try just running `pip install PyQt5` or `pip3 install PyQt5`.  If that
  seemed to work, you may be good to go at that point!
5. Just double-click on `ft-explorer.py` in an Explorer/Finder window, to launch
  it.

Usage
-----

Simply run `ft-explorer.py` and it should do its thing.  If that's not
working, try running it from a commandline/terminal/console, to see if it's
printing out any error messages.

The data from BLCMM 1.1 is bundled with the application, thanks to
LightChaosman.  There is no need to copy anything over!

Nearly all the functionality in the app is visible immediately onscreen,
but there are a couple of extra keys you can use:

* `Ctrl-G`: Go to specified object
* `Ctrl-F`: Search for text inside the current object
* `Enter`: Go to the next search result

You can add data to the resource library if you want, in the
`resources/BL2/dumps` and `resources/TPS/dumps` directories.  The files must
have the extensions `.dump.xz` or `.txt.xz` *([lzma/lzma2
compression](https://en.wikipedia.org/wiki/Xz))*.  Additionally, the utility
`generate_indexes.py` must be run whenever the data files are changed, to
update the indexes that the app uses to avoid having to load all the data
into memory at once.  Note that index generation takes quite awhile, since
I've not bothered to try optimizing it.

Included Data
-------------

FT/BLCMM Explorer bundles nearly all of the "useful" data available in
BLCMM.  We explicitly don't include the `StaticMeshes` and `WillowData`
datasets, since those aren't generally useful and are huge.  Also, most
(all?) Particle data isn't actually included in here either.  There's a
small handful of other classes which got pruned out as well, though I
wonder if I should go ahead and just add those in.

Setting the Font
----------------

FT Explorer is set to use whatever Monospace font your system considers the
default, which may not be the font you want to use in the main data area.
There's no way to set this font inside the FT Explorer GUI, but you can edit
its configuration file once it's been run once to set the font however you
like.  The location of the file will depend on your platform:

* **Windows:** `HKEY_CURRENT_USER\Software\Apocalyptech\FT Explorer.conf`
* **Mac:** `$HOME/Library/Preferences/com.Apocalyptech.FT Explorer.plist`
* **Linux:** `$HOME/.config/Apocalyptech/FT Explorer.conf`

Specifically, set the `datafont` attribute in the `[mainwindow]` section.
The font size can be specified in this file as well, though you can change
the font size in the main application by holding down `Ctrl` and using your
mouse wheel.

Status
------

![Main Window](screenshot.png)

This is a pretty quick-and-dirty app, and is unlikely to see much in the
way of feature improvements, or concessions to platforms other than Linux,
mostly because I assume I'm probably the only person who'll ever use it.
If there's Actual Interest from other folks, I'm guessing I could be
convinced to spend some more effort on it.

Some things which are at least somewhat likely to happen:

* With the most recent BLCMM data bundled, the app startup (and switching
  between games) takes a bit longer than I'd really like it to.  Take a
  look at some different indexing options to see if we can split that up
  a bit.
* See if there's a way to support doing keyboard things like shift-End to
  select a whole line, etc, without having to disable readonly mode.

Some things which are less likely to happen:

* Proper packaging *(for any platform)*
* Fancy icons and stuff in the tree
* In-text hyperlinks, like BLCMM's Object Explorer does?

Some things which are absolutely not going to happen:

* Searching *(BLCMM already does a great job at this)*

Credits
-------

The bundled pre-dumped object data for TPS is taken from BLCMM, by
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

Changelog
---------

I didn't really keep a changelog for this for the majority of its development,
since I was basically the only person to ever use the thing.  However, I
may as well start doing so anyway:

* Nov 12, 2021
  * Added support for Assault on Dragon Keep standalone

* *sometime prior to that*
  * Initial release(s)

