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
from .cpanel import DebugControlPanel
from .table import WatcherTable
from java.awt import BorderLayout
from javax.swing import JPanel, JOptionPane
from jes.gui.components.actions import methodAction
from jes.gui.components.panels import AutoScrollPane

class DebugPanel(JPanel):
    def __init__(self, gui, debugger, watcher):
        self.gui = gui
        self.debugger = debugger
        self.watcher = watcher

        # Create the components.
        # (cpanel is responsible for enabling/disabling the actions,
        # because it has to turn on/off the slider anyway.)
        self.cpanel = DebugControlPanel(debugger.interpreter, debugger, self)
        self.table = WatcherTable(watcher)

        # Assemble everything.
        self.setLayout(BorderLayout())
        self.tableScrollPane = AutoScrollPane(self.table)
        self.add(self.cpanel, BorderLayout.NORTH)
        self.add(self.tableScrollPane, BorderLayout.CENTER)

    @methodAction(name="Watch variable...")
    def watchVariable(self):
        """
        Opens a dialog, asking the user to add a variable to the watcher.
        """
        var = JOptionPane.showInputDialog(self.gui,
            "Please enter a variable to watch.", "Watcher",
            JOptionPane.INFORMATION_MESSAGE, None, None, "")
        if var is not None:
            self.watcher.addVariable(var)

    @methodAction(name="Stop watching variable...")
    def unwatchVariable(self):
        """
        Opens a dialog, asking the user to remove a variable from the watcher.
        """
        allVars = self.watcher.variablesToTrack
        if len(allVars) > 0:
            var = JOptionPane.showInputDialog(self.gui,
                "Choose a variable to stop watching.", "Watcher",
                JOptionPane.INFORMATION_MESSAGE, None, allVars, allVars[0])
            if var is not None:
                self.watcher.removeVariable(var)
        else:
            JOptionPane.showMessageDialog(self.gui,
                "There are no variables being watched.", "Watcher",
                JOptionPane.ERROR_MESSAGE)

    @methodAction(name="FULL SPEED!")
    def fullSpeed(self):
        """
        Accelerates the debugger to FULL SPEED!
        """
        self.debugger.setSpeed(self.debugger.MAX_SPEED)

