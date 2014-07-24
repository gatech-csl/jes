# -*- coding: utf-8 -*-
"""
jes.bridge.terpactions
======================
These actions connect to the interpreter and debugger, allowing GUI elements
to connect directly to interpreter-related actions.

This was created because InterpreterControl *used* to have these actions,
but it created a chicken-and-egg where TerpControl needs the GUI, but
GUI needs the interpreter actions.

(In JES, "terp" is short for "interpreter," not "terrapin.")

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from jes.gui.components.actions import PythonAction
from jes.gui.components.threading import threadsafe


def addInterpreterActions(terp):
    """
    Adds actions to an Interpreter and its Debugger. These include:

    * stopAction, for stopping the interpreter while running.
    * toggleDebuggerAction, for turning the debugger on/off as appropriate.
    * enableDebuggerAction, which just turns it on.
    * disableDebuggerAction, which just turns it off.
    """
    terp.stopAction = PythonAction(terp.stopThread,
        name="Stop", enabled=False
    )
    terp.toggleDebuggerAction = PythonAction(terp.toggleDebugMode,
        name="Watcher", enabled=True
    )
    terp.enableDebuggerAction = PythonAction(terp.setDebugMode, True,
        name="Show watcher", enabled=True
    )
    terp.disableDebuggerAction = PythonAction(terp.setDebugMode, False,
        name="Hide watcher", enabled=False
    )

    terp.debuggerActions = (
        terp.toggleDebuggerAction,
        terp.enableDebuggerAction, terp.disableDebuggerAction
    )

    terp.beforeRun.connect(lockControls)
    terp.afterRun.connect(unlockControls)
    terp.onDebugSet.connect(updateDebugSettings)

    updateDebugSettings(terp, debugMode=terp.debugMode)


@threadsafe
def lockControls(terp, **_):
    terp.stopAction.enabled = True
    for act in terp.debuggerActions:
        act.enabled = False


@threadsafe
def unlockControls(terp, **_):
    terp.stopAction.enabled = False
    for act in terp.debuggerActions:
        act.enabled = True


@threadsafe
def updateDebugSettings(terp, debugMode, **_):
    if debugMode:
        terp.enableDebuggerAction.enabled = False
        terp.disableDebuggerAction.enabled = True
    else:
        terp.enableDebuggerAction.enabled = True
        terp.disableDebuggerAction.enabled = False

