# -*- coding: utf-8 -*-
"""
jes.interpreter
===============
This encapsulates a single interpreter state, for executing Python code.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from __future__ import with_statement

import sys
from .debugger import Debugger
from blinker import NamedSignal
from codeop import compile_command
from java.lang import Thread
from threading import Lock, Semaphore
from .exceptionrecord import JESExceptionRecord

class Interpreter(object):
    """
    This contains a Python interpreter state. It starts out empty,
    but ready to run code.
    """
    def __init__(self):
        self.lock = Lock()
        self.isRunning = False
        self.runningThread = None
        #self._threadLaunched = Semaphore(0)

        self.debugger = Debugger(self)
        self.debugMode = False

        self.namespace = {}
        self.initialNamespace = {}
        self.initialNames = set()

        self.beforeRun = NamedSignal('afterLock')
        self.onException = NamedSignal('onException')
        self.afterRun = NamedSignal('beforeUnlock')

        self.onDebugSet = NamedSignal('onDebugSet')

    def toggleDebugMode(self):
        """
        Flips the debug mode setting.
        """
        self.setDebugMode(not self.debugMode)

    def setDebugMode(self, mode):
        """
        Sets the debug mode to true or false.
        """
        mode = bool(mode)
        self.debugMode = mode
        self.onDebugSet.send(self, debugMode=mode)

    def initialize(self, initCode):
        """
        Create an "initial context" for the interpreter, by running code.
        The `initCode` function provided is passed the interpreter as an
        argument, and it can either manipulate its namespace dictionary
        directly, or run files or code fragments.
        """
        # Reset the context to blanks.
        self.namespace = {}
        self.initialNamespace = None
        self.initialNames = None

        # Call the function.
        initCode(self)

        # Capture the variables from the function.
        # (Lock to ensure that all the threads launched by initCode
        # have finished.)
        with self.lock:
            self.initialNamespace = self.namespace.copy()
            self.initialNames = set(self.initialNamespace.keys())

    def quickReset(self):
        """
        Restores the context that was present after the last call to
        initialize. (Changes to mutable objects will be included!)
        """
        self.namespace = self.initialNamespace.copy()

    def runFile(self, filename, setDunderFile=True):
        """
        Executes a file in the interpreter context (in a separate thread).

        (setDunderFile controls whether the __file__ variable is available.)
        """
        extraVars = {'__file__': filename} if setDunderFile else {}
        thread = ExecFileThread(self, filename, extraVars)
        return self._launchThread(thread)

    def runCodeFragment(self, fragment):
        """
        Executes some code in the interpreter context (in a separate thread).
        """
        if self.debugMode:
            return self.debugCodeFragment(fragment)
        else:
            return self.runCodeFragmentDirect(fragment)

    def runCodeFragmentDirect(self, fragment):
        """
        Executes some code in the interpreter context, without activating
        the debugger if it's enabled.
        """
        thread = ExecThread(self, fragment, {})
        return self._launchThread(thread)

    def debugCodeFragment(self, fragment):
        """
        Executes some code in the debugger, even if debug mode is disabled.
        """
        thread = DebugThread(self, fragment, {})
        return self._launchThread(thread)

    def _launchThread(self, thread):
        """
        Fires off a thread, and waits for it to acquire the interpreter
        lock before returning. This is used to serialize execution.
        """
        thread.start()
        #self._threadLaunched.acquire()
        return thread

    def stopThread(self):
        """
        Kills whatever thread happens to be running now.
        """
        if self.runningThread is None:
            raise RuntimeError("Can't stop while thread isn't running")
        self.runningThread.tryStop()


class InterpreterThread(Thread):
    def __init__(self, interpreter, extraVars):
        self.interpreter = interpreter
        self.extraVars = extraVars
        self.stopSignal = False

    def run(self):
        terp = self.interpreter

        with terp.lock:
            terp.runningThread = self
            #terp._threadLaunched.release()

            excRecord = None
            terp.namespace.update(self.extraVars)
            terp.beforeRun.send(terp, mode=self.mode)

            try:
                self.execute()
            except:
                filename = getattr(self, 'filename',
                    terp.namespace.get('__file__', '<unknown>'))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                excRecord = JESExceptionRecord(filename)
                excRecord.setFromUserCode(exc_type, exc_value, exc_traceback)
                terp.onException.send(terp, mode=self.mode, excRecord=excRecord)
            finally:
                self.cleanup()
                terp.afterRun.send(terp, mode=self.mode, excRecord=excRecord)
                terp.runningThread = None

    def cleanup(self):
        pass

    def tryStop(self):
        self.stopSignal = True
        from jes.gui.commandwindow.prompt import promptService
        promptService.commandWindow.cancelPrompt()
        self.stop()


class ExecFileThread(InterpreterThread):
    mode = 'execfile'

    def __init__(self, interpreter, filename, extraVars):
        super(ExecFileThread, self).__init__(interpreter, extraVars)
        self.filename = filename

    def execute(self):
        execfile(self.filename, self.interpreter.namespace)


class ExecThread(InterpreterThread):
    mode = 'execfragment'

    def __init__(self, interpreter, fragment, extraVars):
        super(ExecThread, self).__init__(interpreter, extraVars)
        self.fragment = fragment

    def execute(self):
        code = compile_command(self.fragment)
        if code is None:
            raise SyntaxError("You can only run one statement at once")
        exec code in self.interpreter.namespace


class DebugThread(InterpreterThread):
    mode = 'debugfragment'

    def __init__(self, interpreter, fragment, extraVars):
        super(DebugThread, self).__init__(interpreter, extraVars)
        self.fragment = fragment

    def execute(self):
        code = compile_command(self.fragment)
        if code is None:
            raise SyntaxError("You can only run one statement at once")
        self.interpreter.debugger.starting()
        self.interpreter.debugger.run(code, self.interpreter.namespace)

    def cleanup(self):
        self.interpreter.debugger.stopping()

