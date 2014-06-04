#!/bin/bash

# jars=""
# list_jars () {
#         for arg in $@; do
#                 # echo arg: $arg
#                 jars="$jars:$arg"
#         done
# }
# pwd for the full path, necessary because
# of the way the test suite is designed,
# it has to be ran in a differect working dir

# list_jars `pwd`/jars/*.jar
# echo $jars

PWD=`pwd`

JARS=""

JARS="$PWD/jars/jython.jar"
JARS="$JARS:$PWD/jars/jmf.jar"
JARS="$JARS:$PWD/jars/jl1.0.jar"
JARS="$JARS:$PWD/jars/junit.jar"
JARS="$JARS:$PWD/jars/AVIDemo.jar"

echo $JARS
