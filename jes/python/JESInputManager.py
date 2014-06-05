#JES- Jython Environment for Students
#
#JESInputManager: Code for the intermediary between the student tools
#    in media.py and the GUI components in JESCommandWindow.py.  This
#    code enables the student tools to request input on the command window
#    so that input() and raw_input() can read data.
#
#May 14 2009 Brian Dorn
#
#See JESCopyright.txt for full licensing information

from javax.swing import SwingUtilities
from java.lang import Runnable
import time


# This class implements the Borg design patter which enables us
# to ensure that all instances of the JESInputManager share
# same state.  This is necessary since media.py doesn't have
# any way to directly reference the command window.
class Borg(object):
    _state = {}
    def __new__(cls, *args, **kw):
	ob = super(Borg, cls).__new__(cls, *args, **kw)
	ob.__dict__ = cls._state
	return ob

# This class provides the interface for prompting for input on the
# command window and waiting for a return value.
class JESInputManager(Borg):
    commandWindow = None
    waitingFlag = False
    value = None

    def setCommandWindow(self, window):
	self.commandWindow = window

    def setReturnValue(self, retValue):
	self.value = retValue

    def setWaiting(self, bool):
	self.waitingFlag = bool

    def isWaiting(self):
	return self.waitingFlag;

    def readInput(self, message):
	#to be threadsafe on this call we need this to update the command window
	class outputPromptRunner(Runnable):
	    def __init__(self, cw, m):
		self.commandWindow = cw
		self.message = m
		
	    def run(self):
		#display the message and reenable the window to editing
		self.commandWindow.showText(self.message)
		self.commandWindow.setCaretPosition(self.commandWindow.document.getLength() )
		self.commandWindow.setKeymap(self.commandWindow.my_keymap)


	#--------------The Actual work goes here------------------
	
	if not message:
	    message = ""

	#first assign value to null
	self.value = None

	#note that the this interpreter thread needs to wait now
	#until a result comes back from the command window
	self.waitingFlag = True
    
	#update the command window with the ouput
	SwingUtilities.invokeAndWait(outputPromptRunner(self.commandWindow, message))

	#Now we wait for the user to input a value and press ENTER in the command window,
	#pausing a 10th of a second between checks.
	while self.waitingFlag:
		time.sleep(0.1)

	#clean up the return value to remove the prompt since the command
	#window will give us everything
	self.value = self.value[len(message):]

	#return the value to media.py
	return self.value

