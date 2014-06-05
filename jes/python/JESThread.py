#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information
#5/20/03: Added a call to JESProgram's loadSuccess on load success. -AdamW

import JESStdOutputBuffer
import JESExceptionRecord
import JESRunnable
import threading
import traceback
import JESDebugger
import StringIO
import sys
from code import compile_command
import java.lang.System
from java.lang import Thread
import javax.swing as swing

debug = 0

class JESThread(Thread):
################################################################################
# Function name: __init__
# Parameters:
#     -code: string of code that will be executed.
#     -interpreter: instance of the JESInterpretor object that is creating this
#                   object.
# Return:
#     An instance of the JESThread class.
# Description:
#     Creates a new instance of the JESThread class
################################################################################
    def __init__(self, code, interpreter, mode):
	self.mode = mode
        global debugFile

        if self.mode == 'run' or self.mode == 'debug':
            self.fileText = code
        else:
            self.fileName = code
        self.interpreter = interpreter
        self.contextForExecution = interpreter.contextForExecution
        self.outputBuffer = None
        self.errMsg = None
        self.excRecord = None
        self.debugger = interpreter.debugger
	
################################################################################
# Function name: run
# Description:
#     Begins running the Jython code that was passed into the JESThread instance
#     upon creation.  The code will run until all of it has been executed,
#     an exeption occurs, or stopPython is called.
################################################################################
    def run(self):
        #print 'running thread in', self.mode, 'mode'
        self.initialize()
        try:
            #print "JESTHREAD " + Thread.currentThread().getName()
            if self.mode == 'run':
                code = compile_command(self.fileText)
                exec code in self.contextForExecution
            elif self.mode == 'debug':
                code = compile_command(self.fileText)
                self.debugger.run(code, self.contextForExecution)
                self.mode = 'run'  # this is so that the command window will reset back to
                                   # run mode
                
            elif self.mode == 'load':
                ## NO MAGIC. (alexr)
                execfile(self.fileName, self.contextForExecution)
                self.interpreter.program.loadSuccess()
                
                # the following block subtracts the added identifiers of the last load
                # from the current context
                # for key in self.contextForExecution.keys():
                #     if key in self.interpreter.currentLoadedFileKeys:
                #         del self.contextForExecution[key]
                # 
                # # now we load the file into an empty context, well, not empty, we need the stuff
                # # in preprocessing

                # origContext = self.interpreter.contextAfterPreprocessing.copy()
                # tempContext = self.interpreter.contextAfterPreprocessing.copy()
                # execfile(self.fileName,tempContext)

                # # java.lang.System.out.println(tempContext)

                # # now repopulate the current context. The problem is that
                # # we blew away all of our renamed variables.
                # for key in tempContext.keys():
                #     if(not self.contextForExecution.has_key(key)):
                #         self.interpreter.currentLoadedFileKeys.insert(0, key)

                #     ## if it was in the original context, don't bother
                #     ## overwriting it. We might've changed it, right?
                #     if(key in origContext.keys()):
                #         continue
                #     else:
                #         self.contextForExecution[key] = tempContext[key]

                ## Mark suggests we try running without this loop. WCPGW?
                ## (alexr)
                # check the new identifiers against the current context
                # for key in tempContext.keys():
                #     if self.contextForExecution.has_key(key):
                #         # redefining identifier, see if value is different
                #         if self.contextForExecution[key] == tempContext[key]:
                #             # already in the context, do nothing
                #             pass
                #         else:
                #             # warn user get yes or no answer
                #             promptResult = swing.JOptionPane.showConfirmDialog(
                #                 self.interpreter.program.gui,
                #                 'a definition with the name ' + key + ' has already been defined.',
                #                 'Are you sure you want to override?',
                #                 swing.JOptionPane.YES_NO_OPTION)
                #             change = (promptResult == swing.JOptionPane.YES_OPTION)
                #             if change:
                #                 self.interpreter.currentLoadedFileKeys.insert(0, key)
                #                 self.contextForExecution[key] = tempContext[key]
                #     else:
                #         self.interpreter.currentLoadedFileKeys.insert(0, key)
                #         self.contextForExecution[key] = tempContext[key]
		
                #Code has been successfully executed, notify the program:

            elif self.mode == 'preprocessing':

                execfile(self.fileName,self.contextForExecution)
                self.interpreter.contextAfterPreprocessing = self.contextForExecution.copy()
		
	    else:
		execfile(self.fileName,self.contextForExecution)
                
            #Include these lines to actually exit on a sys.exit() call
            #except SystemExit, value:
            #   raise SystemExit, value

        except:

            if self.mode == 'preprocessing':
                # probably bad design here
                # if we see an error in the preprocessing file, we print
                # an error message and die
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.preprocessingFailed(exc_type,
                                         exc_value,
                                         exc_traceback)
            else:
                if self.mode == 'debug':
                    self.interpreter.debugger.running = 0
                self.mode = 'run'
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.excRecord = JESExceptionRecord.JESExceptionRecord(self.interpreter.program.filename,\
                                                                       self.interpreter.program)
                self.excRecord.setFromUserCode(exc_type,exc_value, exc_traceback)
                if debug:
                    print 'exception from JESThread.run()'
                    import traceback
                    traceback.print_exc()


        
        self.threadCleanup()

################################################################################
# Function name: stopPython
# Description:
#     Stops the interpreter (should be used only after the run method is
#     called).
################################################################################
    def stopPython(self):
        self.outputBuffer.restoreOutput()
        outputText = self.outputBuffer.getText()

        runnable = JESRunnable.JESRunnable( self.interpreter,
                                            outputText ,
                                            '',
                                            0,
                                            self.mode)

        self.interpreter.program.gui.swing.SwingUtilities.invokeLater( runnable )
       
        self.threadCleanup()
        self.finalize()


################################################################################
# Function name: initialize
# Description:
#  Initializes the stuff to be done at the beginning of a run, and now also at the
#  beginning of any restarts, i.e. whenever the JESThread wakes up from a wait
################################################################################        
    def initialize(self):
        self.interpreter.program.gui.startWork()
        self.interpreter.program.gui.editor.editable = 0
        self.excRecord = None
        self.interpreter.interpreterLock.acquire()
        self.interpreter.program.gui.setRunning(1)
	self.interpreter.program.gui.debuggerButton.enabled = 0;
        self.errMsg = ''
                
        self.outputBuffer = JESStdOutputBuffer.JESStdOutputBuffer(sys.stdout,
                                                                  sys.stderr,
                                                                  self.interpreter)
        
        
################################################################################
# Function name: threadCleanup
# Description:
#   does local work needed to clean up after interpreting user's code, and
#   queues the work that must be done in the main thread
################################################################################
    def threadCleanup(self):
        self.outputBuffer.restoreOutput()
        outputText = self.outputBuffer.getText()
	runnable = None
        runnable = JESRunnable.JESRunnable( self.interpreter,
                                            outputText ,
                                            self.excRecord,
                                            self.mode)
        self.interpreter.program.gui.swing.SwingUtilities.invokeLater( runnable )
        
        # this if should be gotten rid of
        #if self.interpreter.interpreterCondition._is_owned():
        self.interpreter.interpreterCondition.notifyAll()
        self.interpreter.interpreterLock.release()
	self.interpreter.program.gui.debuggerButton.enabled = 1

    def preprocessingFailed(self, type, value, traceback):
        import sys
        import exceptions
        import re
        import string
        
        self.outputBuffer.restoreOutput()
        sys.stdout = sys.__stderr__
        
        # want to use a function defined in that Object
        expRec = JESExceptionRecord.JESExceptionRecord(None,None)
        
        txtStack = expRec.getExceptionInfo(traceback)
        del expRec # don't want to try and do anything with that :)
        # build incorrectly
        print "The following error has occured:"
        print "========================================"

        print type
        print value
        print txtStack 
        print "========================================"
        print "" # a blank line
        valueStr = value.__str__()
        if type == exceptions.ImportError and \
               re.search('^no module named',valueStr):


            ary = valueStr.split(' ')
            #ary = string.split(value,' ')
            file = ary[ len(ary) -1 ]
            print "The file: %s.py appears to be missing." % file
            print "You may need to reinstall JES."
            print "If that dosen't work, contact a TA"

        else:
            print "The above message means that there was a failure in loading JES."
            print "One of the files that the system needs to start was either"
            print "corrupted or missing.  Try reinstalling JES.  If that dosen't"
            print "help, contact a TA."

        sys.exit()
 
