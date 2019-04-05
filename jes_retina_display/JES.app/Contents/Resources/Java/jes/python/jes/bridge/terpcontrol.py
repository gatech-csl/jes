# -*- coding: utf-8 -*-
"""
jes.bridge.terpcontrol
======================
This interacts with the interpreter, to keep the GUI locked down while
the interpreter runs.

(In JES, "terp" is short for "interpreter," not "terrapin.")

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import Stoppable
import StoppableInput
import StoppableOutput
from jes.gui.commandwindow.redirect import RedirectStdio
from jes.gui.components.threading import threadsafe

class InterpreterControl(Stoppable):
    def __init__(self, gui, interpreter):
        self.gui = gui
        self.interpreter = interpreter

        self.redirect = RedirectStdio(gui.commandWindow)

        interpreter.beforeRun.connect(self.afterLock)
        interpreter.afterRun.connect(self.beforeUnlock)
        interpreter.onException.connect(self.showException)

    def stop(self):
        self.interpreter.stopThread()

    @threadsafe
    def afterLock(self, terp, mode, **_):
        self.gui.startWork()
        self.gui.setRunning(True)
        self.gui.editor.editable = False

        self.redirect.install()

        StoppableInput.setThingToStop(self)
        StoppableOutput.setThingToStop(self)

    @threadsafe
    def beforeUnlock(self, terp, mode, **_):
        StoppableInput.setThingToStop(None)
        StoppableOutput.setThingToStop(None)

        self.redirect.uninstall()

        self.gui.editor.document.removeLineHighlighting()
        self.gui.editor.editable = True
        self.gui.setRunning(False)
        self.gui.stopWork()

    @threadsafe
    def showException(self, terp, excRecord, mode, **_):
        msg = excRecord.getExceptionMsg()
        lineno = excRecord.getLineNumber()

        if msg:
            self.gui.commandWindow.display(msg, 'python-traceback')

        if lineno:
            self.gui.editor.showErrorLine(lineno)

