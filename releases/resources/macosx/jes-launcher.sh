#!/bin/sh

##################################################################################
#                                                                                #
# jes-launcher.sh                                                                #
#                                                                                #
# A shell script for launching JES on Mac OS X.                                  #
# Part of it is based on Tobias Fischer's Universal Java Application Stub,       #
# but it has been heavily specialized to JES.                                    #
#                                                                                #
#       https://github.com/tofi86/universalJavaApplicationStub                   #
#                                                                                #
##################################################################################
# Tobias' license:                                                               #
#                                                                                #
# The MIT License (MIT)                                                          #
#                                                                                #
# Copyright (c) 2014 Tobias Fischer                                              #
#                                                                                #
# Permission is hereby granted, free of charge, to any person obtaining a copy   #
# of this software and associated documentation files (the "Software"), to deal  #
# in the Software without restriction, including without limitation the rights   #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      #
# copies of the Software, and to permit persons to whom the Software is          #
# furnished to do so, subject to the following conditions:                       #
#                                                                                #
# The above copyright notice and this permission notice shall be included in all #
# copies or substantial portions of the Software.                                #
#                                                                                #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  #
# SOFTWARE.                                                                      #
#                                                                                #
##################################################################################


# Where are we?

PRG=$0

while [ -h "$PRG" ]; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '^.*-> \(.*\)$' 2>/dev/null`
    if expr "$link" : '^/' 2> /dev/null >/dev/null; then
        PRG="$link"
    else
        PRG="`dirname "$PRG"`/$link"
    fi
done


# Identify things in the bundle.

ContentsMacOS=`dirname "$PRG"`
Contents=`dirname "$ContentsMacOS"`

JES_BASE="$Contents/Resources/Java"
JES_HOME="$JES_BASE/jes"

InfoPlistFile="$Contents/Info.plist"

# read the program name from CFBundleName
CFBundleName=`/usr/libexec/PlistBuddy -c "print :CFBundleName" ${InfoPlistFile}`

# read the icon file name
CFBundleIconFile=`/usr/libexec/PlistBuddy -c "print :CFBundleIconFile" ${InfoPlistFile}`


# See if there's a user configuration file...

JESCONFIGDIR="$HOME/Library/Application Support/JES"

if test -f "$JESCONFIGDIR/JESEnvironment.sh"; then
    source "$JESCONFIGDIR/JESEnvironment.sh"
fi


# Find the Java to use.

# first check environment variable "$JES_JAVA_HOME"
if [ -n "$JES_JAVA_HOME" ]; then
    JAVA="$JES_JAVA_HOME/bin/java"

# then check system variable "$JAVA_HOME"
elif [ -n "$JAVA_HOME" ]; then
    JAVA="$JAVA_HOME/bin/java"

# otherwise check "/usr/libexec/java_home" symlinks
elif [ -x /usr/libexec/java_home ]; then
    JAVA="`/usr/libexec/java_home`/bin/java"

# otherwise check Java standard symlink (old Apple Java)
elif test -h /Library/Java/Home; then
    JAVA="/Library/Java/Home/bin/java"

# fallback: public JRE plugin (Oracle Java)
else
    JAVA="/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java"
fi


# ...Did we find one?

if [ ! -x "$JAVA" ]; then
    # display error message with applescript
    osascript -e "tell application \"System Events\" to display dialog \"Error launching ${CFBundleName}!\n\nYou need to have Java installed on your Mac!\nVisit http://java.com for more information.\" with title \"${CFBundleName}\" buttons {\"OK\"} default button 1 with icon path to resource \"${CFBundleIconFile}\" in bundle (path to me)"

    # exit with error
    exit 1
fi


# Where's our Java code?

JARS="$JES_BASE/dependencies/jars"

CLASSPATH="$JES_HOME/classes.jar"

CLASSPATH="$CLASSPATH:$JARS/jython-2.5.3.jar"
CLASSPATH="$CLASSPATH:$JARS/junit.jar"
CLASSPATH="$CLASSPATH:$JARS/jmf.jar"
CLASSPATH="$CLASSPATH:$JARS/jl1.0.jar"
CLASSPATH="$CLASSPATH:$JARS/AVIDemo.jar"
CLASSPATH="$CLASSPATH:$JARS/jMusic1.6.4.jar"
CLASSPATH="$CLASSPATH:$JARS/jmusic-instruments.jar"


# Where's our Python code?

PYTHONHOME="$JES_BASE/dependencies/jython"

PYTHONPATH="$JES_HOME/python"


# Where should the Jython cache live?

PYTHONCACHE="$HOME/Library/Caches/JES/jython-cache"

mkdir -p $PYTHONCACHE


# What about JESConfig.properties?

JESCONFIG=$JESCONFIGDIR/JESConfig.properties

mkdir -p "$JESCONFIGDIR"


# Enable drag & drop to the dock icon.

export CFProcessPath="$0"


# All right, time to actually run it!

exec "$JAVA" \
    -classpath "$CLASSPATH" \
    -Xdock:icon="$CONTENTS/Resources/${CFBundleIconFile}" \
    -Xdock:name="${CFBundleName}" \
    -Dfile.encoding="UTF-8" \
    -Djes.home="$JES_HOME" \
    -Djes.configfile="$JESCONFIG" \
    -Dpython.home="$PYTHONHOME" \
    -Dpython.path="$PYTHONPATH" \
    -Dpython.cachedir="$PYTHONCACHE" \
    -Dapple.laf.useScreenMenuBar=true \
    ${JES_JAVA_MEMORY:--Xmx512m} ${JES_JAVA_OPTIONS} \
    JESstartup "$@"

