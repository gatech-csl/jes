Building JES Releases
=====================
The JES release process is 98% automated, using [Apache Ant][].
This includes simple .tar.gz and .zip files for Linux and Windows,
.app packages for Mac OS X, and even .exe installers for Windows (using
[Nullsoft Scriptable Install System][]).

[Apache Ant]: http://ant.apache.org/
[Nullsoft Scriptable Install System]: http://nsis.sourceforge.net/

At its simplest, you can create packages by running:

    ant release

This will create a `releases/jes-5.0-snapshot` directory. It will include:

* `jes-5.0-snapshot-linux.tar.gz`: A .tar.gz file for Linux or UNIX.
  Just unpack it and run `jes.sh`.

* `jes-5.0-snapshot-macosx.zip`: A .zip file which contains a `JES.app`
  package for Mac OS X. It should work on any Mac of any CPU architecture.

* `jes-5.0-snapshot-windows-java-included.zip`:
  A .zip file for Windows, including a Java Runtime Environment for JES.
  Just unzip it and double-click `JES.exe`.

* `jes-5.0-snapshot-windows-java-required.zip`:
  A .zip file for Windows, just like the `java-included` ZIP file but
  without the JRE. (This makes it much smaller.)

* `jes-5.0-snapshot-testkit.zip`: A package containing the JES test suite
  and demos, to use for testing.

* `index.html`: A Web page with a list of all the releases.
  If you want, you can just upload this entire directory to the Internet,
  and this file will include instructions and links so people can
  download the release they need.

But, there are some other options you can set to make full-featured releases.


Full Versions
-------------
The `-snapshot` in `jes-5.0-snapshot` means that this is just a development
snapshot, without any particular role in the release hierarchy.
The 5.0 is listed at the top of `build.xml`.

To make a new alpha, beta, or final release, you can follow this procedure:

1.  Make sure you can build Windows installers and signed JARs (described
    later in this document) as part of a snapshot release.

2.  Check to make sure the version's information is recorded in
    `JESCopyright.txt` and `JESChangelog.txt` in the `jes/help` directory.

3.  Run `git status` to make sure you don't have any uncommitted changes
    or untracked files that might get included in the release.

4.  Run `ant release -Drelease=<suffix> -Dsign=true` for a pre-release.
    (For example, alpha 1 would use `-Drelease=a1`, and beta 4 would use
    `-Drelease=b4`). This will create a directory `jes-5.0a1`, with all
    of the files being labeled `jes-5.0a1-platform.zip` instead of having
    `-snapshot`.

    If it's a final release, run `ant release -Drelease= -Dsign=true`
    (with nothing after the equals sign on `-Drelease`!).
    This will create a directory `jes-5.0`, with all the files being
    labeled `jes-5.0-platform.zip`.

5.  Test the release!

6.  Create a new Git tag for the release, using (for example) `git tag 5.0b1`
    or `git tag 5.1`. Then, push it using `git push --tags`.

7.  Go onto GitHub or whatever other Web site we may be using, and upload
    the packages from the release directory.

8.  If you just made a final release, decide what the next version number
    is going to be (if you just made 5.1, it will probably either be
    5.1.1 or 5.2), and write that in the `jes.version` property in
    `build.xml`. You can always change it later if you need to, this is just
    to make sure that snapshots don't have the version you just released
    on them anymore.


build.properties file
---------------------
Some of the more advanced features of the build system require per-machine
configuration. To avoid having to put it on the command line every time you
build, you can put these properties in a `build.properties` file that
lives in the same directory as `build.xml`.

Any property you can use with `-D` on the command line can be put in the
properties file. However, you should only include properties that you would
want to put on every build. (So, definitely not `release`.)
Mine looks like:

    makensis=makensis
    # (There's no .exe because I'm on Linux)
    sign=true
    signing.key=csltest
    signing.keypass=not putting my real password here
    signing.storepass=ditto

You can technically override any property in `build.xml` or
`releases/build-releases.xml` with this file, but you really shouldn't.
We want to make sure everyone can build the packages in the same way.

If you want to override something in your `build.properties`, you can do it
with `-D` like normal.


Windows Installers (NSIS)
-------------------------
JES builds its Windows installers using NSIS, the Nullsoft Scriptable Install
System. The cool thing about NSIS is that it runs from a script file, without
you needing to configure things manually each time, and that it runs both
on Windows and also on Linux.

You don't need NSIS to build Windows .zip file releases, just the .exe
installers. So, you can still work on JES even without having NSIS installed.
But all final releases should have an .exe installer.

On Windows, you can get NSIS from its Web site, http://nsis.sourceforge.net/.
On Linux, it may be in your distribution's package manager (on Fedora 20,
it's called `mingw32-nsis`), but if not, you'll need to Google around a bit.

Once you have NSIS installed, you need to tell Ant where it is. You do this
with the `makensis` system property. On Windows, you can put a line like this
(depending on where you installed NSIS) in your `build.properties` file:

    makensis=C:\\Program Files\\NSIS\\makensis.exe

On Linux, it's usually just called `makensis`, so you can probably do this:

    makensis=makensis

The created Windows installer will be named `jes-5.0-snapshot-windows.exe`.


JAR Signing
-----------
JAR signing was introduced for JES 5.0 at the request of the US Military
Academy at West Point. Because West Point is run by the Army, they have very
strict security requirements for their software, including that all JAR
files be cryptographically signed.

The JES build process doesn't generate keys for you - it just assumes they
live in a keystore file named `releases/keystore.jks`. You can generate a
self-signed key by running:

    keytool -genkey -keystore releases/keystore.jks -alias [pick a short name]

It'll ask you for a password for the keystore file, a password for the key
itself, and some information about yourself to write on the key.
Information on how to get your certificates signed or do other things is
found in the Java documentation.

Once you have a key in the keystore, you can just add a couple of parameters
to your `ant release` command to build a set of signed JARs:

    -Dsign=true -Dsigning.key=[the name you picked earlier]

Ant will ask you for the password for the store and for the key itself,
then make signed copies of all the JARs. The JARs will be stored in
`release/jes-5.0-snapshot/jes-5.0-snapshot-jars`.

You can define the `signing.key` property in `build.properties`, as well as
`signing.keystore` to use a different keystore, and `signing.storepass` and
`signing.keypass` to avoid needing to enter the passwords on each build.

