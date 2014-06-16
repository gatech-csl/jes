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
The easiest way to run JES is with a downloadable package,
but unfortunately those haven't been built for JES 5 yet.
Each of them includes its own `README.txt` with instructions.

If you're working on JES, or you just want to run the latest development
version, you will need to download a Java Development Kit and Apache Ant.
The first step is to build JES: just run `ant`.
Then, you can run the `jes.sh` shell script on Mac or Linux,
or `jes.bat` on Windows.


What's in the repository
------------------------
The `build.xml` is used by developers to launch JES and run all of its tests.
It contains instructions for Apache Ant.
You can run `ant build` to build JES, `ant test` to run all the tests, and
`ant clean` to erase everything you built.

The `jes.sh` file launches JES on Mac and Linux, and `JES.bat` does the same
on Windows.

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

* `dependencies/jython`: An installation of Jython, currently version 2.5.3.
  We need to keep this around because the Jython JAR doesn't have the
  standard library.

The `tests` folder contains Python programs that test different parts of JES
to make sure we wrote them according to the specifications.
You can run these from inside JES by opening the `TestExecute.py` file,
but it's much easier to just use `ant test`.

The `packaging` folder contains files used to build the distribution packages
for each platform.

The `demos` folder contains programs you can run to try out JES.

The `working-on-jes` folder contains articles written by the JES developers
about how JES works, and how you can even contribute to it!

