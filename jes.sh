#!/bin/sh
# Launches JES in place on Mac and Linux.

# Where are we?

JES_BASE="$(dirname $(readlink -f $0))"
JES_HOME="$JES_BASE/jes"


# See if there's a user configuration file...

if test -d "$HOME/Library/Application Support"; then
    JESCONFIGDIR="$HOME/Library/Application Support/JES"
else
    JESCONFIGDIR="${XDG_CONFIG_HOME:-$HOME/.config}/jes"
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
    JAVA=java
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

if test -d "$HOME/Library/Caches"; then
    PYTHONCACHE="$HOME/Library/Caches/JES/jython-cache"
else
    PYTHONCACHE="${XDG_CACHE_HOME:-$HOME/.cache}/jes/jython-cache"
fi

mkdir -p $PYTHONCACHE


# What about JESConfig.properties?

JESCONFIG=$JESCONFIGDIR/JESConfig.properties

mkdir -p "$JESCONFIGDIR"


# All right, time to actually run it!

exec "$JAVA" \
    -classpath "$CLASSPATH" \
    -Dfile.encoding="UTF-8" \
    -Djes.home="$JES_HOME" \
    -Djes.configfile="$JESCONFIG" \
    -Dpython.home="$PYTHONHOME" \
    -Dpython.path="$PYTHONPATH" \
    -Dpython.cachedir="$PYTHONCACHE" \
    -Dapple.laf.useScreenMenuBar=true \
    ${JES_JAVA_MEMORY:--Xmx512m} ${JES_JAVA_OPTIONS} \
    JESstartup "$@"

