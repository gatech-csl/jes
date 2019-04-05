# -*- coding: utf-8 -*-
"""
jes.gui.commandwindow.pane
==========================
This CommandWindowPane class is responsible for providing a line-editing
system on top of the command window.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from jes.gui.components.actions import PythonAction
from java.awt import Color, Toolkit
from java.awt.datatransfer import DataFlavor
from java.awt.event import FocusListener
from javax.swing import JTextPane, KeyStroke
from javax.swing.event import DocumentListener
from javax.swing.text import Utilities

key = KeyStroke.getKeyStroke


class CommandWindowPane(JTextPane, FocusListener):
    """
    The pane has two responsibilities in the editing system: to interpret
    line-editing keystrokes, and to allow the controller to lock the
    pane down from input.
    """
    def __init__(self, controller, doc):
        self.controller = controller
        self.setStyledDocument(doc)
        self.updateTheme(doc)
        doc.onThemeSet.connect(self.updateTheme)
        self.addFocusListener(self)

        self.standardKeymap = self.getKeymap()

    def updateUI(self):
        # Update the default font, if necessary,
        # when the look and feel changes.
        JTextPane.updateUI(self)
        doc = self.getStyledDocument()
        if hasattr(doc, 'setTheme'):
            # Sometimes, we don't have a CommandWindowDocument here.
            doc.setTheme(doc.themeName)

    def updateTheme(self, doc, **_):
        self.setBackground(doc.getBackgroundColor())
        self.setCaretColor(doc.getDefaultTextColor())

    def setKeymap(self, keymap):
        # Swing keeps jacking up our keymap. This is designed to ensure that
        # a JES-able keymap always gets set, regardless of who's calling this.
        if keymap is None:
            JTextPane.setKeymap(self, self.standardKeymap)
        elif keymap.getName().endswith("ForJES"):
            JTextPane.setKeymap(self, keymap)
        else:
            commandKeymap = self.addKeymap(keymap.getName() + "ForJES", keymap)

            commandKeymap.addActionForKeyStroke(key('HOME'), PythonAction(self._home))
            commandKeymap.addActionForKeyStroke(key('shift HOME'), PythonAction(self._shifthome))
            commandKeymap.addActionForKeyStroke(key('ENTER'), PythonAction(self._enter))
            commandKeymap.addActionForKeyStroke(key('UP'), PythonAction(self._up))
            commandKeymap.addActionForKeyStroke(key('DOWN'), PythonAction(self._down))

            JTextPane.setKeymap(self, commandKeymap)

    def _home(self):
        doc = self.getStyledDocument()
        caret = self.getCaretPosition()
        if doc.inputLimit is not None and caret >= doc.inputLimit:
            self.setCaretPosition(doc.inputLimit)
        else:
            pos = Utilities.getRowStart(self, caret)
            self.setCaretPosition(pos)

    def _shifthome(self):
        doc = self.getStyledDocument()
        caret = self.getCaretPosition()
        if doc.inputLimit is not None and caret >= doc.inputLimit:
            self.moveCaretPosition(doc.inputLimit)
        else:
            pos = Utilities.getRowStart(self, caret)
            self.moveCaretPosition(pos)

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

    def paste(self):
        # Should we even try to paste?
        doc = self.getStyledDocument()
        if doc.inputLimit is None:
            return

        textToPaste = getContentToPaste(self)

        if not textToPaste:
            return

        # Grab the first line of the text, if there's multiple lines.
        index = textToPaste.find('\n')
        if index != -1:
            textToPaste = textToPaste[:index]

        if not textToPaste:
            return

        # Determine where to put the text, and type!
        # (We let the DocumentFilter determine the final location.)
        start, end = self.getSelectionStart(), self.getSelectionEnd()

        if start == end:
            doc.insertString(self.getCaretPosition(), textToPaste, None)
        elif end > start:
            self.replaceSelection(textToPaste)

    def focusGained(self, event):
        self.caret.visible = True

    def focusLost(self, event):
        self.caret.visible = False


def getContentToPaste(forComponent):
    clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
    clipContents = clipboard.getContents(forComponent)

    for flavor in clipContents.getTransferDataFlavors():
        if DataFlavor.stringFlavor.equals(flavor):
            return clipContents.getTransferData(flavor)

    return None

