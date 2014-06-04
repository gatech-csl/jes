#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information

import JESConstants
import JESRunnable
import JESExceptionRecord
import JESThread
import sys, os
import threading
import traceback
import string
import StringIO
import JESDebugger
from code import compile_command
from java.lang import Thread

class JESInterpreter:
################################################################################
# Function name: __init__
# Parameters:
#     -program - the running instance of JESProgram
# Description: 
#     Creates an instance of JESInterpreter
################################################################################
    def __init__(self, program):
        self.program = program
        self.contextForExecution = {}
        self.contextAfterPreprocessing = {}
        self.interpreterLock = threading.Lock()
        self.interpreterCondition = threading.Condition(self.interpreterLock)
        self.isLoading = "false"
        self.currentLoadedFileKeys = []
        self.debug_mode = 0
        self.debugger = JESDebugger.JESDebugger(self)
        
        # self.preprocessing must run before buildVarsToHighlight to avoid a
        # deadlock
        self.preProcessingWorked = self.preprocessing()

        self.varsToHighlight = self.buildVarsToHighlight()

    def getVarsToHighlight(self):
        return self.varsToHighlight
    
    def buildVarsToHighlight(self):
        
        varsToHighlight = {}
        
        self.interpreterLock.acquire()

        # this will wait until JESPreprocessing has been executed

        while not self.contextForExecution:
            self.interpreterCondition.wait()
            

        for key in self.contextForExecution.keys():
            varsToHighlight[key] = 1

        self.interpreterLock.release()
        return varsToHighlight

        

################################################################################
# Function name: preprocessing
# Description: 
#     Loads the preprocessing file into the user's interpreter
################################################################################
    def preprocessing(self):
        try:
            preproc = JESConstants.PRE_PROCESSING_FILE

            if(not os.path.exists(preproc)):
                preproc = "Sources/" + preproc

            self.runFile(preproc, 'preprocessing')

            return 'true'
        except:
            import sys
            a,b,c = sys.exc_info()
            import traceback
            traceback.print_exception(a,b,c)
            return None
            
            
            
            
################################################################################
# Function name: runCommand
# Parameters:
#     -compiledCode: the user's text, but compiled by the compile_command
#                    command
# Description:
#     Provides external classes the ability to start execution of user text.
#     This method calls gui's setRunning(runBool) method and then sends text to
#     the Jython interpreter. If the command generates an error or output, this
#     method calls sendOutput().
################################################################################
    def runCommand(self, text):
        if self.debug_mode:
            if self.debugger.running:
                self.debugCommand(text)
            else:
                self.run(text, 'debug')
        else:
            self.run(text, 'run')
            
            
    def run(self, text, mode):
        jesThread = JESThread.JESThread(text, self, mode)
        self.jesThread = jesThread
        jesThread.start()

    def debugCommand(self, text):
        self.debugger.runCommand(text)
        
    def runFile(self,fileName, mode='load'):
        self.run(fileName, mode)
        
        
################################################################################
# Function name: load
# Parameters:
#     -fileText - the text to be loaded
# Description: 
#     Loads the user's code into the context of the command window's
#     interpreter.  reloads the preprocessing code, and if that succeds, loads
#     the user's code.  uses loadHelper to perform the loading.
################################################################################
    def load(self, fileName):


        # a previous version called
        # code.compile_command() here.  but the jython version
        # of that instruction does not properly identify all
        # syntax exceptions.  Now we run the code in its own thread,
        # and seperate syntax errors from other exceptions later

        #self.runCommand(fileText,'load')
        self.runFile(fileName,'load')
        
        
################################################################################
# Function name: sendOutput
# Parameters: 
#     responseText: the text to be sent
# Description: 
#     Sends text to the UI where the user can see it
################################################################################
    def sendOutput(self, responseText):
        self.program.sendTextToCommandWindow(responseText)

################################################################################
# FunctionName: sendError
# Description:
#     Called when user code throws an exception.  It sends an error message to
#     the command window.
################################################################################
    def sendError(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        msg = self.GetExceptionDescription( exc_type )
        self.sendOutput(msg)

################################################################################
# Function name: stopThread
# Description: 
#     Stops a running thread of user code
################################################################################
    def stopThread(self):
        
        self.jesThread.stop()


    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        self.program.gui.refreshDebugState()
