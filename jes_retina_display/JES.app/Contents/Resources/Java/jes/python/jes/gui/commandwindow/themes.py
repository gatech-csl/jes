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
from jes.util.collections import OrderedDict

###
### STYLE FLAGS
###

#: No flags.
NO_STYLES = 0

#: Sets the text to monospace instead of the default proportional font.
MONOSPACE = 1 << 0

Theme = namedtuple('Theme', ('backgroundColor', 'defaultStyle', 'styles'))


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

THEMES = OrderedDict()

THEMES['Standard on Black'] = Theme(
    Color.BLACK,
    (MONOSPACE, Color.WHITE),
    {
        'python-code':      (MONOSPACE,         Color(0xaacdf3)),   # Light blue
        'python-prompt':    (MONOSPACE,         Color(0x27d3c7)),   # Teal
        'python-return':    (MONOSPACE,         Color(0xedd400)),   # Gold
        'python-traceback': (MONOSPACE,         Color(0xff5c58)),   # Red
        'standard-input':   (MONOSPACE,         Color(0x8ae234)),   # Green
        'standard-output':  (MONOSPACE,         Color(0xffffff)),   # White
        'standard-error':   (MONOSPACE,         Color(0xfe8df2)),   # Pink
        'system-message':   (MONOSPACE,         Color(0xff9b41)),   # Orange
    }
)

THEMES['Standard on White'] = Theme(
    Color.WHITE,
    (MONOSPACE, Color.BLACK),
    {
        'python-code':      (MONOSPACE,         Color(0x204a87)),   # Dark blue
        'python-prompt':    (MONOSPACE,         Color(0x158ba0)),   # Teal
        'python-return':    (MONOSPACE,         Color(0xa98b07)),   # Spicy brown mustard
        'python-traceback': (MONOSPACE,         Color(0xcc0000)),   # NC State red (Go Wolfpack!)
        'standard-input':   (MONOSPACE,         Color(0x11aa00)),   # Green
        'standard-output':  (MONOSPACE,         Color(0x000000)),   # Black
        'standard-error':   (MONOSPACE,         Color(0xb31296)),   # Fuschia
        'system-message':   (MONOSPACE,         Color(0xcf5101)),   # Burnt orange
    }
)


THEMES['Old JES (Yellow on Black)'] = Theme(
    Color.BLACK,
    (NO_STYLES, Color.YELLOW),
    {
        'python-prompt':    (MONOSPACE,         Color.YELLOW),
    }
)


THEMES['White on Black'] = Theme(
    Color.BLACK,
    (MONOSPACE, Color.WHITE),
    {}
)


THEMES['Black on White'] = Theme(
    Color.WHITE,
    (MONOSPACE, Color.BLACK),
    {}
)


# See http://www.sron.nl/~pault/colourschemes.pdf

THEMES['Colorblind-Friendly on White'] = Theme(
    Color.WHITE,
    (MONOSPACE, Color.BLACK),
    {
        'python-code':      (MONOSPACE,         Color(0x114477)),   # Blue
        'python-prompt':    (MONOSPACE,         Color(0x117777)),   # Teal
        'python-return':    (MONOSPACE,         Color(0x777711)),   # Gold
        'python-traceback': (MONOSPACE,         Color(0x771122)),   # Red
        'standard-input':   (MONOSPACE,         Color(0x117744)),   # Green
        'standard-output':  (MONOSPACE,         Color(0x000000)),   # Black
        'standard-error':   (MONOSPACE,         Color(0x771155)),   # Purple
        'system-message':   (MONOSPACE,         Color(0x774411)),   # Orange
    }
)


THEMES['Colorblind-Friendly on Black'] = Theme(
    Color.BLACK,
    (MONOSPACE, Color.WHITE),
    {
        'python-code':      (MONOSPACE,         Color(0x77AADD)),   # Blue
        'python-prompt':    (MONOSPACE,         Color(0x77CCCC)),   # Teal
        'python-return':    (MONOSPACE,         Color(0xDDDD77)),   # Gold
        'python-traceback': (MONOSPACE,         Color(0xDD7788)),   # Red
        'standard-input':   (MONOSPACE,         Color(0x88CCAA)),   # Green
        'standard-output':  (MONOSPACE,         Color(0xFFFFFF)),   # White
        'standard-error':   (MONOSPACE,         Color(0xCC99BB)),   # Purple
        'system-message':   (MONOSPACE,         Color(0xDDAA77)),   # Orange
    }
)


THEME_NAMES = THEMES.keys()
DEFAULT_THEME_NAME = THEME_NAMES[0]

