# -*- coding: utf-8 -*-
"""
jes.util.interactive
====================
Utilities for use in the interactive interpreter.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""

class SystemMessage():
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message

    def __call__(self):
        return self

