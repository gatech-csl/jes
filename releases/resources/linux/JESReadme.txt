@title@ @release@ for Linux
============================================================
@introductiontext@

Requirements
------------
This is the Linux package of @title@. It works on all Linux distributions
and other kinds of Unix (including Mac OS X, though an OS X-specific package
is also available).

To run @title@, you first need a Java Runtime Environment to be installed.
Open your Terminal or Terminal Emulator program (on many Linux versions,
this will be in your "Applications" menu in the "Accessories" category),
and run this command to see if you have Java installed:

    java -version

It should print output that looks like:

    java version "1.7.0_55"
    OpenJDK Runtime Environment (fedora-2.4.7.4.fc20-x86_64 u55-b13)
    OpenJDK 64-Bit Server VM (build 24.51-b03, mixed mode)

Many of the numbers will probably be different, but as long as it doesn't
print out an "unknown command" error, you're fine. If it does print out an
"unknown command" error, consult your system documentation for instructions
on how to install Java.

All of @title@'s other dependencies are included in this ZIP file.
You just need a working Java Runtime Environment.


Running @title@
-----------
To start @title@, just run the `jes.sh` shell script file. You should be able to
run it just by double-clicking on it in your file manager.

If not, open your Terminal or Terminal Emulator program (see above),
and `cd` to the directory where you unzipped JES (it probably won't be
this exact folder):

    cd Downloads/@basename@-@release@-linux

Then, you can run the shell script with:

    sh jes.sh


Adding @title@ to Your Menu
-----------------------
If you use a desktop environment like GNOME or KDE, you can put JES in your
applications menu by running the `add-to-menu.sh` shell script file.
You run it just like `jes.sh`, either by double-clicking it or by calling it
in your Terminal.

You won't see anything happen, but if you open your applications menu,
JES should appear in the "Education" and "Development" categories.
As a bonus, you'll be able to double-click .py files, and they'll open in JES.
(Your file manager has an option to change this, if you'd rather open
Python programs in another editor.)

When you delete JES, the menu entry *should* disappear on its own.
If not, run this command in your Terminal:

    rm ${XDG_DATA_HOME:-$HOME/.local/share}/applications/@basename@.desktop


@title@ Development
---------------
@title@'s homepage is on @homepagehost@, at <@homepage@>.
You can keep track of development, download the latest version,
report issues, or even contribute your own code to @title@!

