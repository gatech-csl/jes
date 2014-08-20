# Launching JES

The JES startup process actually operates in three stages.

1.  The "launcher" is a platform-dependent shell script that sets up the
    Java environment (including system properties and the classpath).

2.  The `JESstartup` class is launched as soon as the environment is
    available. It processes "debugging-type" command line arguments,
    such as `--help`, `--version`, `--jython`, and `--check-threads`.
    It also displays the splash screen.

3.  The `jes/__main__.py` Python module is responsible for creating the JES
    user interface and related stuff. It can also interpret some command-line
    arguments.


## Standard Launchers

Right now, there are three standard launchers:

* The Windows generic launcher (`jes.bat` in the repository base)
* The Linux/Mac OS X generic launcher (`jes.sh` in the repository base)
* The Mac OS X .app launcher (`releases/resources/macosx/jes-launcher.sh`)

The two generic launchers assume that they live in the same directory
as the `jes` and `dependencies` directories. This means they can launch JES
directly from a source code checkout (after you build, of course!), and the
release process makes sure that Windows and Linux builds have a compatible
structure.

(As an aside, the `JES.exe` file included in the Windows build just calls
`jes.bat` with any command line arguments it was provided. It mostly exists
so that we can have a pretty icon and not have a Command Prompt window appear
every time the user starts JES. However, it makes all the standard output and
error disappear, so if you need to debug JES, you'll need to invoke `jes.bat`
specifically.)

The .app launcher is only used in `JES.app` bundles for OS X. It operates
slightly differently than the rest because it has to work with the `.app`
directory structure. (Specifically, `jes` and `dependencies` live in
the bundle's `Contents/Resources/Java` instead of right next to the launcher.)

All three of them allow arguments to be passed, which will be forwarded on to
the `JESstartup` class.


### Customizing Java

All of the launchers assume that Java is installed system-wide,
except for the Windows launcher, which looks for a JRE in
`dependencies/jre-win32`. You can tell the launchers to use a specific JRE
by setting the `JES_JAVA_HOME` environment variable.

(The system `JAVA_HOME` environment variable will also be consulted,
but `JES_JAVA_HOME` will only apply to JES, *and* it will override the
bundled JRE on Windows if necessary.)

Just a warning: `JAVA_HOME` should be set to the directory where Java is
installed, *not* the actual Java executable!

By default, JES will only allocate 512 MB of heap. This is controlled by the
`JES_JAVA_MEMORY` environment variable, which contains JVM memory options
(`-Xmx512m` by default.) You can override this.

If you need to define system properties or otherwise customize Java,
you can provide additional options to pass to Java using the
`JES_JAVA_OPTIONS` environment variable.

If you want an easy way to set these environment variables for JES
without having to deal with your system configuration, you can create
a `JESEnvironment.sh` or `JESEnvironment.bat` file, that sets environment
variables. This file lives in the same directory as `JESConfig.properties`.

On Linux or Mac, a `JESEnvironment.sh` file might look like:

    JES_JAVA_HOME=/usr/lib/custom-java
    JES_JAVA_MEMORY=-Xmx2048m

On Windows, a `JESEnvironment.bat` file might look like:

    set JES_JAVA_HOME=C:\Program Files\Super Java
    set JES_JAVA_MEMORY=-Xmx2048m


## Debugging Options for JESstartup

There are a couple of options you can pass to the launchers, which will be
interpreted by the `JESstartup` class.

* Pass `--help` to print a list of options instead of starting JES.

* Pass `--version` to print version information instead of starting JES.

* Pass `--properties` to print all the system properties
  instead of starting JES.

* Pass `--jython` to start a Jython process instead of JES.
  All arguments after the `--jython` (such as a `-c PYTHON` option or
  a script filename) are used as Jython options.

* Pass `--debug-keys` to print debugging information each keypress
  as it is delivered to Java.

* Pass `--check-threads` to print a stack trace whenever a thread other than
  the Event Dispatch Thread causes the GUI to change.
  (This won't catch all threading bugs, but it will catch many of them.)

* Pass `--python-verbose=<level>` to set the Jython verbosity level.
  This can be `error`, `warning`, `message`, `comment`, or `debug`
  (for example, `--python-verbose=comment`).


## The Environment Created by the Launchers

In order for JES to find what it needs, the launchers set a large number
of Java system properties and other things. You set a Java
property on the command line by passing an option that looks like:

    -Dproperty.name=property.value

before you pass the class name (`JESstartup`).


### Java Classpath (-cp)

The Java classpath controls where Java loads classes from.
Usually, these are JAR files -- ZIP files full of compiled classes.
JES contains a bunch of Java classes, whose source code lives in the
`jes/java` folder. Ant compiles them into a JAR named `jes/classes.jar`.

It also contains several JAR's written by other people, which live in
`dependencies/jars`. When launching JES, its own JAR needs to be on the
classpath, as well as all the JAR's in `dependencies/jars`.

And finally, every plugin JAR has to be included on the classpath, because
Java has no easy way to activate JARs at runtime. Add every `*.jar` file
from the user, system, and built-in plugin directories, in order.
(See below for detail on where those are.)

The classpath is different from other properties, because it's set using a
`-cp` option, like:

    -cp jes/classes.jar:one.jar:another.jar

If you need to add more JAR's, just put them in `dependencies/jars`,
and the launchers and Ant will start loading them automatically.


### Python Home/Path (python.home and python.path)

These properties control where Jython finds `.py` files to load.
JES's own Python code lives in `jes/python`, and there is some extra code
in `dependencies/python`, but it also needs to load the Python
standard library, because Jython's JAR file doesn't contain the library.

So, `python.home` needs to be set to the directory that the bundled copy of
Jython lives in, and `python.path` needs to include `jes/python` and
`dependencies/python`.


### Python Cache Directory (python.cachedir)

Jython uses this directory to store information about where all the Java
packages live. If you don't have this set, it uses a directory in
`dependencies/jython` instead, which could cause permission issues.
It's probably best to put the location in the user's home directory, in the
place suggested by the operating system.

Warning: If you set `python.cachedir` to a directory that doesn't exist,
Jython will use `dependencies/jython/cachedir` anyway. Make sure the directory
exists before you use it.


### JES Home (jes.home)

This property is used by JES itself to find its files.
(Specifically, the images it uses in its UI, and its help files.)
It will look for `python`, `images`, `help`, and `javadoc` subdirectories,
so the easiest thing to do is use the `jes` directory, which the
standard launchers do.


### JES Config File (jes.configfile)

This property is the path to the JES configuration file, including its
name (which is usually `JESConfig.properties`). This is where JES keeps all
the user settings which need to remain across restarts.

Most of the time users don't really need to see it or edit it.
So you should store it somewhere "behind the scenes" in the user's
home directory. (If it's left out, JES will put it *directly*
in the user's home directory, which may annoy people. I know it annoys me.)


### JES Plugin Directories (jes.plugins.user, .system, .builtin)

These properties are used by the plugin installer to determine what it can
do with plugins. They point to directories where the plugins live.
`jes.plugins.system` and `jes.plugins.builtin` are purely informational,
but `jes.plugins.user` indicates a directory that JES *should* have write
access to, where it can add and delete `.jar` files.

`.user` is for plugins downloaded by the user theirselves. It should live
in the user's home directory, near the configuration file.

`.system` is for plugins added by the system adminstrator. If JES has just
been unpacked some random place, it should be the `plugins` directory
next to `jes` and `dependencies`. If JES was installed at the system level
and the standard directory tree might not exist, it should be somewhere
that the system administrator traditionally installs software.

`.builtin` is for plugins built into this copy of JES. They live in
`$JES_HOME/builtin-plugins`. Right now, the release system doesn't actually
have a way to pack built-in plugins into the release archives, but that will
change soon.

