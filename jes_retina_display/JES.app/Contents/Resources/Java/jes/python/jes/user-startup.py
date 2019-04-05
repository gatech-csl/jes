# -*- coding: utf-8 -*-
"""
jes/user-startup.py
===================
This file is executed to provide the initial namespace for JES.
(It has a dash in the name _specifically_ so it won't be importable.)

:copyright: (C) 2002 Jason Ergle, Claire Bailey, David Raines, Joshua Sklare;
            (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import sys
from java.io import File
from math import (acos, asin, atan, ceil, cos, exp, floor, log, log10,
                  pow, sin, sqrt, tan, pi)
from media import *
from os import sep as pathSep

# Provide a hatch into JES for debugging.

def debugJES():
    from jes.program import JESProgram
    if hasattr(JESProgram, 'activeInstance'):
        return JESProgram.activeInstance
    else:
        raise RuntimeError("JESProgram instance did not register itself")


# Override Python's normal exit instructions.
# This makes exit and exit() both print instructions for exiting.

import JESVersion
from java.lang import System
from jes.util.interactive import SystemMessage

if System.getProperty('os.name').find('Mac') != -1:
    quit = exit = SystemMessage('Press Command + Q or select "Exit" from the "File" menu to exit JES')
else:
    quit = exit = SystemMessage('Press Ctrl + Q or select "Exit" from the "File" menu to exit JES')

version = SystemMessage(JESVersion.getMessage())

del JESVersion
del System
del SystemMessage


# Figure out which variables to filter out.

from jes.tools.vardebug import DebugWindowLauncher
showVars = DebugWindowLauncher(['showVars'] + [name for name in vars().keys()])
del DebugWindowLauncher
del name

