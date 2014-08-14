# -*- coding: utf-8 -*-
"""
jes.tools.vardebug
==================
This contains a debug window, and a controller for a debug window.

:copyright: (C) 2002 Jason Ergle, Claire Bailey, David Raines, Joshua Sklare;
            (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import sys
import time
from java.awt.event import ActionListener
from javax import swing

### Useful type names

INTEGER     = type(30).__name__
BOOLEAN     = type(True).__name__
LONG        = type(30L).__name__
FLOAT       = type(2.0).__name__
COMPLEX     = type(1.0j).__name__
STRING      = type("Hello").__name__
TUPLE       = type(()).__name__
LIST        = type([]).__name__
DICTIONARY  = type({}).__name__
SET         = type(set()).__name__
NONE        = type(None).__name__

TYPE_SORT_ORDER = {
    INTEGER:    1,
    BOOLEAN:    1,
    NONE:       1,
    LONG:       1,
    COMPLEX:    1,
    STRING:     1,
    TUPLE:      1,
    LIST:       1,
    DICTIONARY: 1
}

TYPE_SORT_DEFAULT = 2

IMPROVED_TYPE_NAMES = {
    NONE:       'None'
}


### Columns

NAME_COL = 0
TYPE_COL = 1
VALUE_COL = 2


### The debug window

DEBUG_WINDOW_TITLE = 'JES Watcher Window #%s - %H:%M:%S'
DEBUG_WINDOW_SIZE = (400, 400)
CLOSE_BUTTON_CAPTION = 'Close'

VAR_L_NAME_COL_CAPTION = 'Local Variables'
VAR_G_NAME_COL_CAPTION = 'Command Area Variables'

VAR_TYPE_COL_CAPTION = 'Type'
VAR_VALUE_COL_CAPTION = 'Value'


class DebugWindow(swing.JFrame, ActionListener):
    def __init__(self, localVars, globalVars, windowNumber, varsToFilter):
        """
        Creates the layout of the window.
        """
        self.varsToFilter = set(varsToFilter)

        now = time.localtime(time.time())
        self.title = time.strftime(DEBUG_WINDOW_TITLE, now)
        self.title = self.title % windowNumber
        self.size = DEBUG_WINDOW_SIZE
        self.contentPane.setLayout(swing.BoxLayout(self.contentPane,
                                                   swing.BoxLayout.Y_AXIS))

        # Create panels and button, and place them on the frame
        closeButton = swing.JButton(CLOSE_BUTTON_CAPTION, actionListener=self)

        bottomPanel = swing.JPanel()
        bottomPanel.add(closeButton)

        localPane = self.buildTablePane(VAR_L_NAME_COL_CAPTION, localVars)
        globalPane = self.buildTablePane(VAR_G_NAME_COL_CAPTION, globalVars)

        self.contentPane.add(localPane)
        self.contentPane.add(globalPane)
        self.contentPane.add(bottomPanel)

        self.setDefaultCloseOperation(1)
        self.setVisible(1)

    def buildTablePane(self, caption, varDict):
        # Create the list.
        varList = [
            [name, self.getTypeName(value), value]
            for name, value in varDict.items()
            if name not in self.varsToFilter
        ]

        # Sort them all.
        varList.sort(key=self.orderRow)

        # Fix the type names.
        for row in varList:
            if row[TYPE_COL] in IMPROVED_TYPE_NAMES:
                row[TYPE_COL] = IMPROVED_TYPE_NAMES[row[TYPE_COL]]

        # Create a table model.
        headers = [caption, VAR_TYPE_COL_CAPTION, VAR_VALUE_COL_CAPTION]
        tableModel = swing.table.DefaultTableModel(varList, headers)

        # Create the actual table.
        table = swing.JTable(tableModel)
        table.getColumnModel().getColumn(0).setPreferredWidth(1)

        # Wrap it in a ScrollPane.
        return swing.JScrollPane(table)

    def getTypeName(self, value):
        return type(value).__name__

    def orderRow(self, row):
        return (TYPE_SORT_ORDER.get(row[TYPE_COL], TYPE_SORT_DEFAULT),
                row[NAME_COL])

    def actionPerformed(self, event):
        actionCommand = event.getActionCommand()

        if actionCommand == CLOSE_BUTTON_CAPTION:
            self.setVisible(0)


### Launcher

class DebugWindowLauncher(object):
    def __init__(self, varsToFilter):
        self.count = 1
        self.varsToFilter = varsToFilter

    def __call__(self):
        frame = sys._getframe(1)
        localVars = frame.f_locals.copy()
        globalVars = frame.f_globals.copy()

        DebugWindow(localVars, globalVars, self.count, self.varsToFilter)
        self.count += 1

