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


Running JES
-----------
If you're on a system with a Java development environment and a set of GNU
core utilities (including make) installed, just run:

    make run

If not...sorry, but you can't right now. I just finished reorganizing the
entire source tree, and while the `Makefile` works with the new layout,
the other launchers don't yet.


What's in the repository
------------------------
The `Makefile` is used by developers to launch JES and run all of its tests.
You can run `make run` to build JES, `make test` to run all the tests, and
`make clean` to erase everything you built.

The `JES.bat`, `JES.sh`, and `JES.exe` files launch JES on different
platforms, but as I said earlier, they don't work right now.

All the source files and resources for JES itself live in the `jes` folder:

* `jes/java`: The Java code that contains the core of JES, including the
  code that directly handles pictures, sounds, and movies.

* `jes/python`: The Python code that controls most of the user interface.

* `jes/images`: The pictures that are used by JES itself, such as the
  splash screen and the toolbar buttons.

* `jes/help`: Web pages (and a few text files) about how to use JES.

* `jes/classes`: When the Java code is compiled, the class files are placed
  here.

* `jes/javadoc`: API documentation for the Java parts of JES.
  (This isn't actually accessible from inside JES anymore, but the code
  for browsing it is still present.)

In addition, JES uses some code written by others, which we store alongside
JES in the `dependencies` folder:

* `dependencies/jars`: JAR files for a bunch of libraries the JES Java code
  uses to work with media files.

* `dependencies/jython`: An installation of Jython, currently version 2.2.1.
  We need to keep this around because the Jython JAR doesn't have the
  standard library.

The `tests` folder contains Python programs that test different parts of JES
to make sure we wrote them according to the specifications.
(You can't run these from inside JES.)

The `demos` folder contains programs you can run to try out JES.

The `working-on-jes` folder contains articles written by the JES developers
about how JES works, and how you can even contribute to it!

