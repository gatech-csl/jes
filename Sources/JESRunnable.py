#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare

#See JESCopyright.txt for full licensing information

from java.lang import Runnable
from javax.swing import JOptionPane

################################################################################
# JESRunnable
#
# a runnable object which update the command window, displaying the new results
# from the execution of the user's code.
################################################################################

class JESRunnable( Runnable ):

######################################################################
# init
# interpreter: the JESInterpreter object that this runnable updates
# output: a string, the output from the user's code
# errRec: a JESExceptionRecord object, only defined if an excption occured.
#         created from the exception information and stack trace returned
#         by sys.exc_info()
######################################################################
    def __init__(self,interpreter, output, errRec, mode):
        self.interpreter = interpreter
        self.output = output
        self.mode = mode

        if errRec != None:
            self.errMsg = errRec.getExceptionMsg()
            self.errLine = errRec.getLineNumber()
        else:
            
            self.errMsg = ''
            self.errLine = None
        
######################################################################
# run
#
# the method that does all of the updating work.
# this method should ALWAYS be called from within the same thread
# that the GUI executes in.
######################################################################

    def run(self):
        
        if self.output != '' and self.output != None:
            self.interpreter.sendOutput( self.output )
        if self.errMsg != '' and self.errMsg != None:
            self.interpreter.sendOutput( self.errMsg )

        if self.errLine != None:
            self.interpreter.program.gui.editor.showErrorLine(self.errLine)


        self.interpreter.program.gui.commandWindow.restoreConsole(self.mode)
        self.interpreter.program.gui.setRunning( 0 )
        self.interpreter.program.gui.stopWork()
        self.interpreter.program.gui.editor.document.removeLineHighlighting()
        self.interpreter.program.gui.editor.editable = 1
	
	# needed for midi note playing
	import JavaMusic

        try:
            JavaMusic.cleanUp()
        except:
            menuBar = self.interpreter.program.gui.getJMenuBar()
            mediaMenu = menuBar.getMenu(menuBar.getMenuCount() - 2)
            if mediaMenu.getText() == 'MediaTools':
                # the above is merely for sanity checking...
                #if mediaMenu.getItem(0).isEnabled():
                if self.interpreter.program.gui.soundErrorShown == 0:
                    # we don't want to keep bombarding the user with messages!
                    # mediaMenu.getItem(0).setEnabled(0)
                    self.interpreter.program.gui.soundErrorShown = 1
                    msg = 'Sound card initialization failed!\n\n'
                    msg += 'You will not be able to use this functionality during the\n'
                    msg += 'current session of JES. Please make sure your sound card\n'
                    msg += 'is not currently being used by another program and restart\n'
                    msg += 'JES.'
                    JOptionPane.showMessageDialog(self.interpreter.program.gui,
                                                  msg, 'Sound Error', JOptionPane.ERROR_MESSAGE)
            
	if self.interpreter.debug_mode:
	    self.interpreter.debugger.endExecution()
