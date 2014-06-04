JES: Jython Environment for Students
====================================
JES is a development environment designed for [Media Computation][].
It allows students to use the Python programming language (specifically,
Jython, which is a version of Python implemented in Java) to manipulate
images, sounds, and videos.

[Media Computation]: http://coweb.cc.gatech.edu/mediaComp-teach

JES is incorporated in "Introduction to Computing and Programming in Python:
A Multimedia Approach," by Mark Guzdial and Barbara Ericson. Dr. Guzdial
is the project leader, and the project has been worked on by many people
over the years (as seen in the `JESCopyright.txt` file).


What's in the repository
------------------------
Matthew Frazier (<https://github.com/leafstorm>) is currently rebuilding
and cleaning up the repository as part of a migration from Google Code to
GitHub. The repository layout is likely to change significantly during this
process, but he'll try to keep this up to date. (If he doesn't, email him to
complain.)

A few of the folders contain files that JES needs to run:

* `Sources`: The code for JES itself, which is a mix of Java and Jython.

* `images`: Pictures that are part of JES (like the logo and buttons).

* `jython-2.2.1`: A copy of Jython, which JES uses to run Python programs.

* `jars`: All of JES's Java dependencies, as JAR files.

* `JESHelp`: Help files explaining how to use JES.
  (The `JESIntro.txt` and `JESAPIHelp.html` files in the main folder
  are also part of the help.)

* The main folder contains a few different ways to launch JES:
  `jes.bat`, `JES.exe`, `JES.sh`, `splash.bat`, and `Makefile`.
  (`list-jars.sh` is used by `JES.sh` and `Makefile`.)
  These may or may not work...

The rest are just extra documentation:

* `demos`: Example programs for JES. (More are available from the Media
  Computation Web site.)

* `Release Build Tools`: Instructions for building JES projects,
  and some stuff used by the `JES.exe` Windows launcher.

