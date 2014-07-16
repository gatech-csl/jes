# -*- coding: utf-8 -*-
"""
jes.core.interpreter.watcher
============================
This plugs into the debugger and examines the values of variables at each
step.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import linecache
from blinker import NamedSignal

class _Missing(object):
    def __str__(self):
        return '-'

    def __repr__(self):
        return '-'

MISSING = _Missing()


class Record(object):
    def __init__(self, filename, lineno):
        self.filename = filename
        self.lineno = lineno
        self.line = linecache.getline(filename, lineno)
        self.variables = {}

    def getVariable(self, var):
        if var in self.variables:
            return self.variables[var]
        else:
            return MISSING

    def __str__(self):
        return "<Record on %r line %d: %r>" % (self.filename, self.lineno, self.variables)


class Watcher(object):
    def __init__(self, debugger):
        self.variablesToTrack = []
        self.records = []

        debugger.onStart.connect(self._start)
        debugger.onFrame.connect(self.recordFrame)

        self.onAddedVariable = NamedSignal('onAddedVariable')
        self.onRemovedVariable = NamedSignal('onRemovedVariable')
        self.onRecorded = NamedSignal('onRecorded')
        self.onReset = NamedSignal('onReset')

    def reset(self):
        self.records = []
        self.onReset.send(self)

    def addVariable(self, name):
        self.variablesToTrack.append(name)
        self.onAddedVariable.send(self, var=name)

    def removeVariable(self, name):
        self.variablesToTrack.remove(name)
        self.onRemovedVariable.send(self, var=name)

    def _start(self, debugger, **_):
        self.reset()

    def recordFrame(self, debugger, filename, lineno, frame, **_):
        record = Record(filename, lineno)
        for var in self.variablesToTrack:
            try:
                value = eval(var, frame.f_locals, frame.f_globals)
                record.variables[var] = value
            except:
                pass
        self.records.append(record)
        self.onRecorded.send(self, record=record)

