#!/bin/sh
# Launches JES in place on Mac and Linux.

# Where are we?
JES_BASE="$(dirname $(readlink -f $0))"
JES_HOME="$JES_BASE/jes"


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


# Where's our Python code?
PYTHONHOME="$JES_BASE/dependencies/jython"

PYTHONPATH="$JES_HOME/python"


# Where should the Jython cache live?
if test -d "$HOME/Library/Caches"; then
    PYTHONCACHE="$HOME/Library/Caches/JES/jython-cache"
else
    PYTHONCACHE="$HOME/.cache/jes/jython-cache"
fi

mkdir -p $PYTHONCACHE


# What about JESConfig.properties?
JESCONFIGNAME=JESConfig.properties

if test -d "$HOME/Library/Application Support"; then
    JESCONFIG="$HOME/Library/Application Support/JES/$JESCONFIGNAME"
else
    JESCONFIG="$HOME/.config/jes/$JESCONFIGNAME"
fi

mkdir -p "$(dirname "$JESCONFIG")"


# All right, time to actually run it!

"$JAVA" -classpath "$CLASSPATH" \
    -Djes.home="$JES_HOME" \
    -Djes.configfile="$JESCONFIG" \
    -Dpython.home="$PYTHONHOME" \
    -Dpython.path="$PYTHONPATH" \
    -Dpython.cachedir="$PYTHONCACHE" \
    -Dapple.laf.useScreenMenuBar=true \
    ${JES_JAVA_MEMORY:--Xmx512m} ${JES_JAVA_OPTIONS} \
    JESstartup "$@"

