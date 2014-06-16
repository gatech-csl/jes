#!/bin/sh
# Launches JES in place on Mac and Linux.

# Where are we?
JES_BASE="$(dirname $(readlink -f $0))"
JES_HOME="$JES_BASE/jes"


# What Java should we use?
if test -z "$JAVA_HOME"; then
    JAVA=java
else
    JAVA="$JAVA_HOME/java"
fi


# Where's our Java code?
JARS="$JES_BASE/dependencies/jars"

CLASSPATH="$JES_HOME/classes"

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


# What about JESConfig.txt?
if test -d "$HOME/Library/Application Support"; then
    JESCONFIG="$HOME/Library/Application Support/JES/JESConfig.txt"
else
    JESCONFIG="$HOME/.config/jes/JESConfig.txt"
fi

mkdir -p "$(dirname "$JESCONFIG")"


# All right, time to actually run it!

java -classpath "$CLASSPATH" \
    ${JAVA_MEMORY:--Xmx512m} \
    -Djes.home="$JES_HOME" \
    -Djes.configfile="$JESCONFIG" \
    -Dpython.home="$PYTHONHOME" \
    -Dpython.path="$PYTHONPATH" \
    -Dpython.cachedir="$PYTHONCACHE" \
    JESstartup "$@"

