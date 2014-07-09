# -*- coding: utf-8 -*-
"""
jes.gui.commandwindow.pane
==========================
This CommandWindowPane class is responsible for providing a line-editing
system on top of the command window.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from jes.gui.swingutil import makeAction
from java.awt import Color
from javax.swing import JTextPane, KeyStroke
from javax.swing.event import DocumentListener

key = KeyStroke.getKeyStroke


class CommandWindowPane(JTextPane):
    """
    The pane has two responsibilities in the editing system: to interpret
    line-editing keystrokes, and to allow the controller to lock the
    pane down from input.
    """
    def __init__(self, controller, doc):
        self.controller = controller
        self.setStyledDocument(doc)
        self.setBackground(Color.BLACK)
        self.setCaretColor(Color.WHITE)

        self.standardKeymap = self.getKeymap()

    def setKeymap(self, keymap):
        # Swing keeps jacking up our keymap. This is designed to ensure that
        # a JES-able keymap always gets set, regardless of who's calling this.
        if keymap is None:
            JTextPane.setKeymap(self, self.standardKeymap)
        elif keymap.getName().endswith("ForJES"):
            JTextPane.setKeymap(self, keymap)
        else:
            commandKeymap = self.addKeymap(keymap.getName() + "ForJES", keymap)

            commandKeymap.addActionForKeyStroke(key('ENTER'), makeAction(self._enter))
            commandKeymap.addActionForKeyStroke(key('UP'), makeAction(self._up))
            commandKeymap.addActionForKeyStroke(key('DOWN'), makeAction(self._down))

            JTextPane.setKeymap(self, commandKeymap)

    def _enter(self):
        self.controller.submit()

    def _up(self):
        doc = self.getStyledDocument()
        newText = doc.history.moveUp()
        if newText is not None:
            doc.setResponseText(newText)
            self.setCaretPosition(doc.getLength())

    def _down(self):
        doc = self.getStyledDocument()
        newText = doc.history.moveDown()
        if newText is not None:
            doc.setResponseText(newText)
            self.setCaretPosition(doc.getLength())

