#!/bin/sh
# Launches JES in place on Linux, with Java auto-detection or user-defined path.

# Get the directory where the script is located
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Check if java_path file exists and contains a valid Java path
if [ -f "$SCRIPT_DIR/java_path" ]; then
    JAVA_HOME=$(cat "$SCRIPT_DIR/java_path")
    if [ ! -d "$JAVA_HOME" ] || [ ! -x "$JAVA_HOME/bin/java" ]; then
        echo "Error: The Java path in '$SCRIPT_DIR/java_path' is invalid or does not point to a valid Java installation!"
        exit 1
    fi
    echo "Using Java from 'java_path' file: $JAVA_HOME"
else
    # Auto-detect Java 8 if no java_path file exists
    JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))  # Get the parent directory of the java binary
    if [ -z "$JAVA_HOME" ]; then
        echo "Error: Java is not installed on your system, and no 'java_path' file was found!"
        exit 1
    fi

    # Check if it's Java 8
    JAVA_VERSION=$("$JAVA_HOME/bin/java" -version 2>&1 | head -n 1)
    if [[ "$JAVA_VERSION" =~ "1.8" ]]; then
        echo "Using Java 8 from $JAVA_HOME"
    else
        echo "Error: The detected Java version is not Java 8. Found: $JAVA_VERSION"
        echo "If you have Java 8 installed, create a file named 'java_path' and put the Java directory there."
        exit 1
    fi
fi

# Set JAVA binary path
JAVA="$JAVA_HOME/bin/java"

# Check if the JAVA binary is executable
if [ ! -x "$JAVA" ]; then
    echo "Error: Java is not installed or not executable at $JAVA_HOME!"
    exit 1
fi

# Where are we?
PRG=$0

while [ -h "$PRG" ]; do
    link=$(readlink "$PRG")
    if expr "$link" : '^/' >/dev/null; then
        PRG="$link"
    else
        PRG="$(dirname "$PRG")/$link"
    fi
done

JES_BASE=$(dirname "$PRG")
JES_HOME="$JES_BASE/jes"

# Set up classpath
JARS="$JES_BASE/dependencies/jars"
CLASSPATH="$JES_HOME/classes.jar"

for jar in "$JARS"/*.jar; do
    CLASSPATH="$CLASSPATH:$jar"
done

# Python setup
PYTHONHOME="$JES_BASE/dependencies/jython"
PYTHONPATH="$JES_HOME/python:$JES_BASE/dependencies/python"

# Cache and config directories
PYTHONCACHE="${XDG_CACHE_HOME:-$HOME/.cache}/jes/jython-cache"
mkdir -p "$PYTHONCACHE"

JESCONFIGDIR="${XDG_CONFIG_HOME:-$HOME/.config}/jes"
mkdir -p "$JESCONFIGDIR"
JESCONFIG="$JESCONFIGDIR/JESConfig.properties"

# Run JES
exec "$JAVA" \
    -classpath "$CLASSPATH" \
    -Dfile.encoding="UTF-8" \
    -Djes.home="$JES_HOME" \
    -Djes.configfile="$JESCONFIG" \
    -Dpython.home="$PYTHONHOME" \
    -Dpython.path="$PYTHONPATH" \
    -Dpython.cachedir="$PYTHONCACHE" \
    ${JES_JAVA_MEMORY:--Xmx512m} \
    JESstartup "$@"
