#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information

import JESDebugWindow
import threading

class JESDebugWindowWrapper:
################################################################################
# Function name: __init__
# Return:
#     An instance of the JESDebugWindowWrapper class.
# Description:
#     Creates an instance of the JESDebugWindowWrapper class.
################################################################################
    def __init__(self, varsToFilter):
        self.count = 1
        self.lock = threading.Lock()
        self.varsToFilter = varsToFilter

################################################################################
# Function name: show
# Parameters:
#     -varsToDisplay: A dictionary.  Presumably the variables to be displayed.                    .
# Description: 
#     To make a debug window visible   
################################################################################
    def show(self, localVars, globalVars):
        self.lock.acquire()

        count = self.count
        self.count = self.count + 1

        JESDebugWindow.JESDebugWindow( localVars, globalVars, count, self.varsToFilter)
        self.lock.release()


