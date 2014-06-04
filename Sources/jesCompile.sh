#!/bin/sh

jars=".:../jars/jython.jar:../jars/jmf.jar:../jars/jl1.0.jar:../jars/junit.jar:../jars/customizer.jar:../jars/mediaplayer.jar:../jars/AVIDemo.jar"

export CLASSPATH=$jars

javac -target 1.5 *.java -cp $jars
javadoc *.java -d javadoc
