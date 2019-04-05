# -*- coding: utf-8 -*-
"""
jes.__main__
============
Powers up JES.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""

# Super early startup

from jes.platform.macosx import installOpenHandler, setDockIcon
setDockIcon()


# Now, actually start loading stuff

import JESstartup
import sys
from jes.program import JESProgram

def usageError():
    JESstartup.showHelp()
    sys.exit(1)


# Manually process the command-line options

if len(sys.argv) < 2:
    mode = 'editor'
    filename = None
elif len(sys.argv) == 2:
    mode = 'editor'
    filename = sys.argv[1]
else:
    usageError()


# Start it!

mainJESProgram = JESProgram(filename)
installOpenHandler(mainJESProgram)

