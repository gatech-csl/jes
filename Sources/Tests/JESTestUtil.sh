#!/bin/sh

java "-Dpython.path=.:.." "-Dpython.home=../../jython-2.2.1" -cp "../../jython-2.2.1/jython.jar:..:." -Xmx384m org.python.util.jython ./TestExecute.py "../../jython-2.2.1"
