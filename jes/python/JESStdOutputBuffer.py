#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information

import sys
import JESUpdateRunnable

class JESStdOutputBuffer:
################################################################################
# Function name: __init__
# Return:
#     An instance of the JESStdOutputBuffer class.
# Description:
#     Creates a new instance of the JESStdOutputBuffer.
################################################################################
    def __init__(self, out,err,interpreter):
        self.text = ''
        self.out = out
        self.err = err
        self.interpreter = interpreter
        sys.stdout = self
        sys.stderr = self

################################################################################
# Function name: restoreOutput
# Description: undoes the effect of JESStdOutputBuffer
#              restores sys.stdout to the original value so that printing
#              commands again send text to the screen
#            
#
################################################################################
    def restoreOutput(self):
        sys.stdout = self.out
        sys.stderr = self.err

################################################################################
# Function name: flush
# Description: does nothing; included for compliance with the sys.stdout class
#
################################################################################
    def flush(self):
        pass

################################################################################
# Function name: write
# Parameters:
#     -newText: the new text string to be added
# Description: called by jython when text would have been sent to sys.stdout
#              our function grabs that text and appends it to a string
#
################################################################################
    def write(self, newText):
        self.text = self.text + newText

################################################################################
# Function name: getText
# Return: a string containing all the text that has been sent to sys.stdout
#
# Description: returns all the text that has been sent to sys.stdout since this
#              object was created
#
################################################################################
    def getText(self):
        return self.text


    def printNow(self,text):

        runnable = JESUpdateRunnable.JESUpdateRunnable(self.interpreter, text)
        #self.interpreter.program.gui.swing.SwingUtilities.invokeLater( runnable )
        self.interpreter.program.gui.swing.SwingUtilities.invokeAndWait( runnable )


