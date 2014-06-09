# Makefile for building and running JES.
# Note that we use relative paths throughout, to make the Makefile easier
# to debug.
# This is ONLY because make guarantees you're in the repository root when
# it runs.
# Other launchers should use absolute paths for most things,
# especially Python paths (as Python is capable of changing directories).

### MAKE MACROS

# Thanks, Eldar Abusalimov on StackOverflow! http://stackoverflow.com/a/9551487
# This variable has a space in it.
space :=
space +=

join-with = $(subst $(space),$1,$(strip $2))


### LOCATIONS OF THINGS IN THE JES SOURCE TREE

JES_HOME            := jes

JES_PYTHON_SRC      := $(JES_HOME)/python
JES_JAVA_SRC        := $(JES_HOME)/java
JES_JAVA_CLASS      := $(JES_HOME)/classes
JES_JAVADOC         := $(JES_HOME)/javadoc

JES_BUILD_STAMP     := $(JES_JAVA_CLASS)/+build-stamp

JYTHON_HOME         := $(abspath dependencies/jython)
JYTHON_MAIN         := org.python.util.jython
JYTHON_CACHE        := jython-cache

DEPENDENCY_JARS     := $(wildcard dependencies/jars/*.jar)

JES_TESTS           := tests
JES_TEST_SCRIPT     := $(JES_TESTS)/TestExecute.py
JES_TEST_OUTPUT     := $(JES_TESTS)/test-output


### ALL THE FILES WE'RE GONNA MAKE

JES_JAVA_FILES      := $(wildcard $(JES_JAVA_SRC)/*.java)


### JAVA SETTINGS

JAVA                ?= $(JAVA_HOME)/bin/java
JAVAC               ?= $(JAVA_HOME)/bin/javac
JAVADOC             ?= $(JAVA_HOME)/bin/javadoc

JAVADOC_FLAGS       ?= "-quiet"
JAVA_MEMORY         ?= -Xmx512m


### OUR JAVA OPTIONS

CLASSPATH           := $(call join-with,:,$(abspath $(DEPENDENCY_JARS)):$(abspath $(JES_JAVA_CLASS)))
JES_PROPERTIES      := -Dpython.home=$(abspath $(JYTHON_HOME)) \
                       -Dpython.path=$(abspath $(JES_PYTHON_SRC)) \
                       -Dpython.cachedir=$(abspath $(JYTHON_CACHE)) \
                       -Djes.home=$(abspath $(JES_HOME))

JES_JAVA_FLAGS      := $(JAVA_MEMORY) $(JES_PROPERTIES) -classpath $(CLASSPATH)


### TARGETS

.PHONY: all classes javadoc clean test run

all: classes javadoc

ifndef JAVA_HOME
	$(error The JAVA_HOME variable must be set, in the environment or with -D)
endif


### COMPILING OUR JAVA

classes: $(JES_BUILD_STAMP)

$(JES_BUILD_STAMP): $(JES_JAVA_FILES)
	$(JAVAC) $(JAVAC_FLAGS) -classpath $(CLASSPATH) -sourcepath $(JES_JAVA_SRC) -d $(JES_JAVA_CLASS) $(JES_JAVA_FILES)
	touch $(JES_BUILD_STAMP)


### MAKING OUR JAVADOCS

javadoc: $(JES_JAVADOC)/index-all.html

$(JES_JAVADOC)/index-all.html: $(JES_JAVA_FILES)
	$(JAVADOC) $(JAVADOC_FLAGS) -classpath $(CLASSPATH) -d $(JES_JAVADOC) $(JES_JAVA_SRC)/*


### RUNNING A JES

$(JYTHON_CACHE):
	mkdir -p $(JYTHON_CACHE)

run: classes javadoc $(JYTHON_CACHE)
	$(JAVA) $(JES_JAVA_FLAGS) JESstartup


### RUNNING THE TESTS

test: classes $(JYTHON_CACHE)
	$(JAVA) $(JES_JAVA_FLAGS) $(JYTHON_MAIN) $(JES_TEST_SCRIPT)


### CLEAN ALL THE THINGS

.PHONY: cleancode cleantest cleanjava cleanpy

clean: cleancode cleantest
cleancode: cleanjava cleanpy

cleanjava: cleanjava cleanpy cleantest
	rm -rf $(JES_JAVA_CLASS)
	mkdir -p $(JES_JAVA_CLASS)
	rm -rf $(JES_JAVADOC)
	mkdir -p $(JES_JAVADOC)

cleanpy:
	rm -f $(JES_PYTHON_SRC)/*.class
	rm -f $(JES_TESTS)/*.class
	rm -rf $(JYTHON_CACHE)

cleantest:
	rm -rf $(JES_TEST_OUTPUT)/*.*

