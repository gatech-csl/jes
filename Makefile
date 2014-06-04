# Makefile for building and running JES

ROOT:=$(CURDIR)
#JAVA_HOME=/home/timmy/java/jdk1.5.0_09
JAVA=$(JAVA_HOME)/bin/java
#given by env:
#JAVAC=$(JAVA_HOME)/bin/javac
JAVADOC=$(JAVA_HOME)/bin/javadoc
JAVACFLAGS="-Xlint:all"

ifndef $(JAVAC)
	JAVAC=$(JAVA_HOME)/bin/javac
endif

## CLASSPATH="$(ROOT)/jars/jython.jar:$(ROOT)/jars/jmf.jar:$(ROOT)/jars/jl1.0.jar:$(ROOT)/jars/junit.jar:$(ROOT)/Sources/"

CLASSPATH="$(shell sh ./list-jars.sh):$(ROOT)/Sources/"

JYTHONPATH="$(ROOT)/jython-2.2.1"
JYTHONCLASSNAME="org.python.util.jython"
CACHEPATH="$(ROOT)/cache"

JESSCRIPT="$(ROOT)/Sources/JESProgram.py"
TESTSCRIPT="TestExecute.py"
TESTDIR="$(ROOT)/Sources/Tests"

JAVACLASSES=$(shell find Sources/ -name '*.java' -print | sed  's/\.java/\.class/')
JAVADOCOUTPUT=$(shell find Sources/ -name '*.java' -print | sed 's/Sources/Sources\/javadoc/' | sed  's/\.java/\.html/')
JAVASOURCEFILES=Sources/*.java

all: .firsttimebuilding classes javadoc

.firsttimebuilding:
	touch .firsttimebuilding
	@echo '###################################'
	@echo '# This is your first time bulding #'
	@echo '# make sure your JAVA_HOME is set #'
	@echo '###################################'
	@echo "JAVA_HOME = " $(JAVA_HOME)
	@echo "JAVA = " $(JAVA)
	@echo "JAVAC = " $(JAVAC)
	@echo "JAVADOC = " $(JAVADOC)
	@echo "CLASSPATH = " $(CLASSPATH)

classes: $(JAVACLASSES)

javadoc: $(JAVADOCOUTPUT)

%.class : %.java
#	$(JAVAC) $(JAVACFLAGS) -classpath $(CLASSPATH) $<
	$(JAVAC) -classpath $(CLASSPATH) $<


pretendclean:
	find Sources/ -name '*.class' -exec echo rm -f {} \;

zip:
	cd .. && rm -f jes.zip && zip -r jes jes -x \*.svn\*

linuxzip:
	cd .. && rm -f jes-linux.zip && zip -r jes-linux jes -x \*.svn\* \*.bat\* \*.exe\* \*win-jre\*

clean:
	rm -f .firsttimebuilding
	find Sources/ -name '*.class' -exec rm -f {} \;

fast:
	$(JAVAC) -classpath $(CLASSPATH) $(JAVASOURCEFILES)

$(JAVADOCOUTPUT): $(JAVASOURCEFILES)
	$(JAVADOC) -classpath $(CLASSPATH) -d Sources/javadoc $(JAVASOURCEFILES)

tests: $(JAVACLASSES)
	cd $(TESTDIR) && $(JAVA) -Xmx512m -Dpython.home=$(JYTHONPATH) -classpath $(CLASSPATH) \
                                 $(JYTHONCLASSNAME) $(TESTSCRIPT) $(JYTHONPATH)

# run: .firsttimebuilding classes
# 	$(JAVA) -Xmx512m -Dpython.home=$(JYTHONPATH) -classpath $(CLASSPATH) $(JYTHONCLASSNAME) $(JESSCRIPT)

run: .firsttimebuilding classes
	echo $(CACHEPATH)
	$(JAVA) -Xmx512m -Djython.cachedir=$(CACHEPATH) -Dpython.home=$(JYTHONPATH) -classpath $(CLASSPATH) JESstartup

