# -*- coding: utf-8 -*-
"""
jes.gui.swingutil
=================
Utilities for dealing Swing and its many problems, such as event listeners
and threading.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import sys
import traceback
from functools import wraps
from java.lang import Runnable
from javax.swing import Action, AbstractAction, SwingUtilities

def debug(text, *formats):
    if formats:
        text = text % formats
    elif not isinstance(text, basestring):
        text = str(text)
    print >>sys.__stderr__, "#", text
    if text.endswith("!"):
        traceback.print_stack()


###
### SWING ACTION MANAGEMENT
###

class PythonAction(AbstractAction):
    """
    This is a simple Swing Action that invokes a Python callback.
    """
    def __init__(self, callback):
        self.callback = callback
        self.setEnabled(True)

    def actionPerformed(self, event):
        self.callback()


def makeAction(callback):
    """
    Wraps a callable in a PythonAction.
    """
    if isinstance(callback, PythonAction):
        return callback
    elif callable(callback):
        return PythonAction(callback)
    else:
        raise TypeError("Actions can only be created from Python callables")


###
### SWING THREADING
###

class FunctionCall(Runnable):
    def __init__(self, fn, args, kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.started = False
        self.done = False
        self.rv = None
        self.exc = None

    def run(self):
        if self.started:
            raise RuntimeException("Task was already started once")

        self.started = True
        try:
            self.rv = self.fn(*self.args, **self.kwargs)
        except object, exc:
            self.exc = exc
        finally:
            self.done = True

    def getResult(self):
        if not self.done:
            raise RuntimeException("Task has not yet finished")
        elif self.exc:
            raise self.exc
        else:
            return self.rv


def threadCheck(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if not SwingUtilities.isEventDispatchThread():
            raise RuntimeError("Not on the AWT event dispatch thread")
        return fn(*args, **kwargs)

    return decorated


def threadsafe(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if SwingUtilities.isEventDispatchThread():
            return fn(*args, **kwargs)
        else:
            task = FunctionCall(fn, args, kwargs)
            SwingUtilities.invokeAndWait(task)
            return task.getResult()
    return decorated


def runnable(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        return FunctionCall(fn, args, kwargs)
    return decorated

