JES @release@ for Linux
==========================
@introductiontext@

Requirements
------------
This is the Linux package of JES. It works on all Linux distributions
and other kinds of Unix (including Mac OS X, though an OS X-specific package
is also available).

To run JES, you first need a Java Runtime Environment to be installed.
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

All of JES's other dependencies are included in this ZIP file.
You just need a working Java Runtime Environment.


Running JES
-----------
To start JES, just run the `jes.sh` shell script file. You should be able to
run it just by double-clicking on it in your file manager.

If not, open your Terminal or Terminal Emulator program (see above),
and `cd` to the directory where you unzipped JES (it probably won't be
this exact folder):

    cd Downloads/jes-@release@-linux

Then, you can run the shell script with:

    sh jes.sh


JES Development
---------------
JES's homepage is on @homepagehost@, at <@homepage@>.
You can keep track of JES development, download the latest version,
report issues, or even contribute your own code to JES!

