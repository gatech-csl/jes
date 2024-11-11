JES 6.0 for Linux
============================================================
JES is a development environment designed for [Media Computation][].
It allows students to use the Python programming language (specifically,
Jython, which is a version of Python implemented in Java) to manipulate
images, sounds, and videos.

[Media Computation]: http://mediacomputation.org/

JES is incorporated in "Introduction to Computing and Programming in Python:
A Multimedia Approach," by Mark Guzdial and Barbara Ericson. Dr. Guzdial
is the project leader, and the project has been worked on by many people
over the years (as seen in the `JESCopyright.txt` file).

JES is Free Software, made available under the GNU General Public License.
This means that everyone may use JES, free of charge, and share it with
anyone. Everyone can also make changes to JES and share those changes.
You can read the full license information in the `JESCopyright.txt` file.


Requirements
------------
This is the Linux package of JES. It works on all Linux distributions


To run JES, you first need a Java Runtime Environment to be installed.
Open your Terminal or Terminal Emulator program (on many Linux versions,
this will be in your "Applications" menu in the "Accessories" category),
and run this command to see if you have Java installed:

    java -version

It should print output that looks like:

    java version "1.8.0"

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

    cd Downloads/jes-6.0-linux

Then, you can run the shell script with:

    sh jes.sh

If the script is unable to automatically detect the Java 8 path on your system, you can manually
specify it by creating a java_path file in the root directory of your JES installation.

   touch java_path

Inside the java_path file, specify the full path to your Java 8 installation.
For example, if your Java 8 installation is located at '/usr/lib/jvm/java-1.8.0-openjdk'
you can add it to the java_path file like this:

    echo "/usr/lib/jvm/java-1.8.0-openjdk" > java_path

Adding JES to Your Menu
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

    rm ${XDG_DATA_HOME:-$HOME/.local/share}/applications/jes.desktop


JES Development
---------------
JES's homepage is on GitHub, at <https://github.com/gatech-csl/jes>.
You can keep track of development, download the latest version,
report issues, or even contribute your own code to JES!
