# -*- coding: utf-8 -*-
"""
jes.gui.components.threading
============================
Utilities for dealing with multithreading and the Swing EDT.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from functools import wraps
from java.lang import Runnable
from javax.swing import SwingUtilities

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


def invokeLater(fn, *args, **kwargs):
    task = FunctionCall(fn, args, kwargs)
    SwingUtilities.invokeLater(task)


def invokeThreadsafe(fn, *args, **kwargs):
    if SwingUtilities.isEventDispatchThread():
        return fn(*args, **kwargs)
    else:
        task = FunctionCall(fn, args, kwargs)
        SwingUtilities.invokeAndWait(task)
        return task.getResult()


def threadsafe(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        return invokeThreadsafe(fn, *args, **kwargs)

    return decorated


def runnable(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        return FunctionCall(fn, args, kwargs)

    return decorated

