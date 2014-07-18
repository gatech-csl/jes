# -*- coding: utf-8 -*-
"""
jes.gui.commandwindow.themes
============================
This contains the list of themes for the command window.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from collections import namedtuple
from java.awt import Color

###
### STYLE FLAGS
###

#: No flags.
NO_STYLES = 0

#: Sets the text to monospace instead of the default proportional font.
MONOSPACE = 1 << 0

Theme = namedtuple('Theme', ('description', 'backgroundColor', 'defaultStyle', 'styles'))


###
### THEME DATA
###

ALL_STYLES = set([
    'python-code',
    'python-prompt',
    'python-return',
    'python-traceback',
    'standard-input',
    'standard-output',
    'standard-error',
    'system-message'
])


###
### THEME DEFINITIONS
###

THEMES = {}

DEFAULT_THEME_NAME = 'Modern'

THEMES['Modern'] = Theme(
    "different colors on black",
    Color.BLACK,
    (MONOSPACE, Color(0xffffff)),
    {
        'python-code':      (MONOSPACE,         Color(0xaacdf3)),   # Light blue
        'python-prompt':    (MONOSPACE,         Color(0x729fcf)),   # Darker blue
        'python-return':    (MONOSPACE,         Color(0xedd400)),   # Gold
        'python-traceback': (MONOSPACE,         Color(0xff5c58)),   # Red
        'standard-input':   (MONOSPACE,         Color(0x8ae234)),   # Green
        'standard-output':  (MONOSPACE,         Color(0xffffff)),   # White
        'standard-error':   (MONOSPACE,         Color(0xfe8df2)),   # Pink
        'system-message':   (MONOSPACE,         Color(0xff9b41)),   # Orange
    }
)


THEMES['JES 4.3'] = Theme(
    "yellow on black",
    Color.BLACK,
    (NO_STYLES, Color.YELLOW),
    {
        'python-prompt':    (MONOSPACE,         Color.YELLOW),
    }
)


THEME_NAMES = THEMES.keys()
THEME_NAMES.sort()

