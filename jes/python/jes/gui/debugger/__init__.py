# -*- coding: utf-8 -*-
"""
jes.gui.debugger
================
This provides the GUI components of the JES watcher/debugger.
It connects to the watcher/debugger, monitoring the GUI and providing
state information.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
#from .cpanel import DebuggerControlPanel
from .table import WatcherTable, AutoScrollPane
from java.awt import BorderLayout
from javax.swing import JPanel
from jes.gui.swingutil import methodAction

class DebugPanel(JPanel):
    def __init__(self, gui, debugger, watcher):
        self.gui = gui
        self.debugger = debugger
        self.watcher = watcher

        # Create the components.
        self.table = WatcherTable(watcher)

        # Assemble everything.
        self.setLayout(BorderLayout())
        self.tableScrollPane = AutoScrollPane(self.table)
        self.add(self.tableScrollPane, BorderLayout.CENTER)

    @methodAction(name="Add variable...")
    def addVariable(self):
        """
        Opens a dialog, asking the user to add a variable to the watcher.
        """
        pass

    @methodAction(name="Remove variable...")
    def removeVariable(self):
        """
        Opens a dialog, asking the user to remove a variable from the watcher.
        """
        pass

