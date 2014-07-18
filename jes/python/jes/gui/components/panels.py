# -*- coding: utf-8 -*-
"""
jes.gui.components.panels
=========================
Wrapper/helper classes that decorate panels and add functionality to them
like scrolling or hiding.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from javax.swing import JScrollPane

class AutoScrollPane(JScrollPane):
    def __init__(self, component):
        super(AutoScrollPane, self).__init__(component)
        self.lastMaximum = None
        self.verticalScrollBar.model.stateChanged = self.stateChanged

    def stateChanged(self, event):
        brmodel = event.source
        if brmodel.maximum != self.lastMaximum:
            brmodel.value = brmodel.maximum
            self.lastMaximum = brmodel.maximum

