#!/bin/sh
# Launches JES in place on Mac and Linux.

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

JES_BASE=`dirname "$PRG"`
JES_HOME="$JES_BASE/jes"

InfoPlistFile="$JES_BASE/Info.plist"

# read the program name from CFBundleName
CFBundleName=`/usr/libexec/PlistBuddy -c "print :CFBundleName" ${InfoPlistFile}`

# read the icon file name
CFBundleIconFile=`/usr/libexec/PlistBuddy -c "print :CFBundleIconFile" ${InfoPlistFile}`

# See if there's a user configuration file...

if test -d "$HOME/Library/Application Support"; then
    JESCONFIGDIR="$HOME/Library/Application Support/JES"
    JES_USER_PLUGINS="$HOME/Library/Application Support/JES/Plugins"
else
    JESCONFIGDIR="${XDG_CONFIG_HOME:-$HOME/.config}/jes"
    JES_USER_PLUGINS="${XDG_DATA_HOME:-$HOME/.local/share}/jes/plugins"
fi

if test -f "$JESCONFIGDIR/JESEnvironment.sh"; then
    source "$JESCONFIGDIR/JESEnvironment.sh"
fi



# What Java should we use?

if ! test -z "$JES_JAVA_HOME"; then
    JAVA="$JES_JAVA_HOME/bin/java"
elif ! test -z "$JAVA_HOME"; then
    JAVA="$JAVA_HOME/bin/java"
else
    JAVA="`/usr/libexec/java_home  -v 1.8`/bin/java"
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

for jar in "$JARS"/*.jar; do
    CLASSPATH="$CLASSPATH:$jar"
done

# Where's our Python code?

PYTHONHOME="$JES_BASE/dependencies/jython"

PYTHONPATH="$JES_HOME/python:$JES_BASE/dependencies/python"


# Do we have any plugins to load?
# User plugins:
JES_USER_PLUGINS="$HOME/Library/Application Support/JES/Plugins"

if test -d "$JES_USER_PLUGINS"; then
    for jar in "$JES_USER_PLUGINS"/*.jar; do
        CLASSPATH="$CLASSPATH:$jar"
    done
fi

# System plugins:

JES_SYSTEM_PLUGINS="$JES_BASE/plugins"

if test -d "$JES_SYSTEM_PLUGINS"; then
    for jar in "$JES_SYSTEM_PLUGINS"/*.jar; do
        CLASSPATH="$CLASSPATH:$jar"
    done
fi

# Built-in plugins:

JES_BUILTIN_PLUGINS="$JES_HOME/builtin-plugins"

if test -d "$JES_BUILTIN_PLUGINS"; then
    for jar in "$JES_BUILTIN_PLUGINS"/*.jar; do
        CLASSPATH="$CLASSPATH:$jar"
    done
fi

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
    -Xdock:icon="${CFBundleIconFile}" \
    -Xdock:name="${CFBundleName}" \
    -Dfile.encoding="UTF-8" \
    -Djes.home="$JES_HOME" \
    -Djes.configfile="$JESCONFIG" \
    -Djes.plugins.user="$JES_USER_PLUGINS" \
    -Djes.plugins.system="$JES_SYSTEM_PLUGINS" \
    -Djes.plugins.builtin="$JES_BUILTIN_PLUGINS" \
    -Dpython.home="$PYTHONHOME" \
    -Dpython.path="$PYTHONPATH" \
    -Dpython.cachedir="$PYTHONCACHE" \
    -Dapple.laf.useScreenMenuBar=true \
    ${JES_JAVA_MEMORY:--Xmx512m} ${JES_JAVA_OPTIONS} \
    JESstartup "$@"

