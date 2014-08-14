JES: Jython Environment for Students
====================================
JES is a development environment designed for [Media Computation][].
It allows students to use the Python programming language (specifically,
Jython, which is a version of Python implemented in Java) to manipulate
images, sounds, and videos.

[Media Computation]: http://mediacomputation.org/

JES is incorporated in "Introduction to Computing and Programming in Python:
A Multimedia Approach," by Mark Guzdial and Barbara Ericson. Dr. Guzdial
is the project leader, and the project has been worked on by many people
over the years (as seen in the `jes/help/JESCopyright.txt` file).

JES is Free Software, made available under the GNU General Public License.
This means that everyone may use JES, free of charge, and share it with
anyone. Everyone can also make changes to JES and share those changes.
You can read the full license information in the `jes/help/JESCopyright.txt`
file.


Running JES
-----------
The easiest way to run JES is with a downloadable package,
which you can find at <https://github.com/gatech-csl/jes/releases>.
Each of them includes its own `JESReadme.txt` with instructions.

If you're working on JES, or you just want to run the latest development
version:

1.  Download a Java Development Kit and Apache Ant.
2.  Use Git to clone the JES repository, or download a .zip file of the
    repository.
3.  Build JES by running `ant`.
4.  Run the `jes.sh` shell script if you're on Mac or Linux,
    or the `jes.bat` batch file if you're on Windows.


What's in the repository
------------------------
The `build.xml` is used by developers to launch JES and run all of its tests.
It contains instructions for Apache Ant (http://ant.apache.org/).
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

* `dependencies/python`: Python libraries used by JES.

* `dependencies/jmusic-instruments`: Instrument classes to use with the
  bundled copy of jMusic. This contains the Java source files and class files,
  but JES actually imports them from a JAR file in `dependencies/jars`.

The `tests` folder contains Python programs that test different parts of JES
to make sure we wrote them according to the specifications.
You can run these from inside JES by opening the `TestExecute.py` file,
but it's much easier to just use `ant test`.

The `releases` folder is where JES releases (like ZIP files, Windows
installers, or Mac applications) are built. You can build them by running
`ant release`, and they appear directly inside the `releases` folder.

* The `releases/build-releases.xml` file contains the Ant instructions for
  building each kind of release. (Ant considers it part of `build.xml`,
  so you can't run it by itself.)

* The `releases/resources` folder contains files that get included as part
  of the releases, like README files or platform-specific installers.

* The `releases/stage` folder is used by Ant to arrange all the files for the
  releases before it actually zips them all up.

If you just run `ant release`, it generates a "snapshot release" suitable
for testing. If you want to build proper releases, build Windows installers,
or sign the released JAR files, there are instructions in
`working-on-jes/building-releases.md`.

The `demos` folder contains programs you can run to try out JES.

The `working-on-jes` folder contains articles written by the JES developers
about how JES works, and how you can even contribute to it!

