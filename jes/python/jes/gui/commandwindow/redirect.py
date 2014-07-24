# -*- coding: utf-8 -*-
"""
jes.gui.commandwindow.redirect
==============================
This allows standard output and error to be redirected to the command window.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import pprint
import sys

class RedirectStream(object):
    def __init__(self, window, style):
        self.window = window
        self.style = style
        self.buffer = []

    def write(self, text):
        self.buffer.append(text)
        if text.endswith('\n'):
            self.flush()

    def flush(self):
        if self.buffer:
            self.window.display(''.join(self.buffer), self.style)
            self.buffer = []


class RedirectStdio(object):
    def __init__(self, window):
        self.commandWindow = window
        self.stdout = RedirectStream(window, 'standard-output')
        self.stderr = RedirectStream(window, 'standard-error')
        self.old_streams = []

    def install(self):
        self.old_streams.append((sys.stdout, sys.stderr, sys.displayhook))
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        sys.displayhook = self.displayhook

    def uninstall(self):
        self.stdout.flush()
        self.stderr.flush()
        sys.stdout, sys.stderr, sys.displayhook = self.old_streams.pop()

    def displayhook(self, value):
        self.stdout.flush()
        if value is None:
            return

        self.commandWindow.display(repr(value) + '\n', 'python-return')
        sys.builtins['_'] = value

    def __enter__(self):
        self.install()

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.uninstall()

