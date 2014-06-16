# Launching JES

Launching JES is a somewhat involved process. While it boils down to
"launch the `JESstartup` class," many Java system properties need to be set
in order for Jython and JES to find everything they need. You set a Java
property on the command line by passing an option that looks like:

    -Dproperty.name=property.value


## Java Classpath (-cp)

The Java classpath controls where Java loads classes from.
JES contains a bunch of Java classes, whose source code lives in the
`jes/java` folder. It also contains a few JAR's, which are ZIP files full
of compiled classes. All of JES's JAR's were written by other people,
and they live in `dependencies/jars`.

When launching JES, all the JAR's need to be on the classpath, and so do
all of the JES classes.

The classpath is different from other properties, because it's set using a
`-cp` option, like:

    -cp one.jar:another.jar:classes


## Python Home/Path (python.home and python.path)

These properties control where Jython finds `.py` files to load.
JES's own Python code lives in `jes/python`, but it also needs to load the
Python standard library, because Jython's JAR file doesn't contain the
library.

So, `python.home` needs to be set to the directory that the bundled copy of
Jython lives in, and `python.path` needs to be set to the directory that
contains JES's Python code.


## Python Cache Directory (python.cachedir)

Jython uses this directory to store information about where all the Java
packages live. If you don't have this set, it uses a directory in
`dependencies/jython` instead, which could cause permission issues.
It's probably best to put the location in the user's home directory, in the
place suggested by the operating system.

Warning: If you set `python.cachedir` to a directory that doesn't exist,
Jython will use `dependencies/jython/cachedir` anyway. Make sure the directory
exists before you use it.


## JES Home (jes.home)

This property is used by JES itself to find its files.
(Specifically, the images it uses in its UI, and its help files.)
It will look for `python`, `images`, `help`, and `javadoc` subdirectories,
so the easiest thing to do is use the `jes` directory.


## JES Config File (jes.configfile)

This property will *eventually* be used as the location of the JESConfig.txt
file. It's not implemented yet, though!

This file isn't really human-editable, so you should store it somewhere
"behind the scenes" in the user's home directory


## Options for JESstartup

There are a couple of options you can pass to the JESstartup class.
These do require all the above properties to be set.
Pass `--properties`, and it will print all the system properties and exit.
Pass `--shell`, and it will open a Python interactive prompt in your console,
instead of starting JES.

Both of these options can be passed to `jes.sh` and `JES.bat`.

