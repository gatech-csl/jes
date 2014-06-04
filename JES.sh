#!/bin/sh
# launches JES on mac and linux

#java -Xmx512m -Dpython.home="jython-2.1" \
#    -classpath ".:jython-2.1/jython.jar:Sources:$CLASSPATH" \
#    org.python.util.jython ./Sources/JESProgram.py 


jars=`sh ./list-jars.sh`

java -Xmx512m -Dpython.home="jython-2.2.1" -Dpython.cachedir="$HOME/.jes-cachedir " \
    -classpath ".:$jars:Sources:$CLASSPATH" JESstartup
