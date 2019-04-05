# -*- coding: utf-8 -*-
"""
jes.gui.commandwindow.document
==============================
This Document class controls how the text in the command window changes.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import CommandDocumentFilter
import CommandDocumentListener
from .themes import THEMES, DEFAULT_THEME_NAME, ALL_STYLES, MONOSPACE, NO_STYLES
from blinker import NamedSignal
from collections import namedtuple
from java.awt import Color
from javax.swing import UIManager
from javax.swing.event import DocumentListener
from javax.swing.text import (DefaultStyledDocument, StyleConstants,
                              SimpleAttributeSet)

TranscriptLine = namedtuple('TranscriptLine', ['style', 'text'])


class CommandDocument(DefaultStyledDocument):
    """
    This is the document subclass used for the JES command window.
    Its only responsibilities compared to a normal document are protecting
    everything written by the program up to the last prompt, and keeping
    the History up to date with what the current prompt text is.
    """
    def __init__(self, history, themeName=DEFAULT_THEME_NAME):
        self.history = history

        self.promptText = None
        self.promptStyle = None
        self.responseStyle = None

        self.inputLimit = None

        # Initialize the transcripts
        self.transcripts = [[]]
        self.transcript = self.transcripts[0]

        # Set the themes
        self.onThemeSet = NamedSignal('onThemeSet')
        self.setTheme(themeName)

        # Install the filter and document listener
        self.filter = CommandDocumentFilter()
        self.setDocumentFilter(self.filter)

        self.listener = CommandDocumentListener(self.history)
        self.addDocumentListener(self.listener)

    def setTheme(self, themeName):
        """
        Updates all the existing styles, and recolors the command window
        to match the new styles if any text is present.
        """
        # Pick our fonts!
        self.defaultFontFamily = \
            UIManager.getDefaults().getFont("EditorPane.font").getFamily()
        self.monoFontFamily = 'Monospaced'

        # Check that the theme exists
        if themeName not in THEMES:
            themeName = DEFAULT_THEME_NAME

        self.themeName = themeName
        self.theme = theme = THEMES[themeName]

        # Set the default style
        baseStyle = self.getStyle('default')
        StyleConstants.setBackground(baseStyle, theme.backgroundColor)
        self._setStyle(baseStyle, theme.defaultStyle)

        # Set the pretty text styles
        existingStyles = set(self.getStyleNames())
        for name in ALL_STYLES:
            if name in existingStyles:
                style = self.getStyle(name)
            else:
                style = self.addStyle(name, baseStyle)

            styleSpec = theme.styles.get(name, (None, None))
            styleSpec = (
                (theme.defaultStyle[0] if styleSpec[0] is None else styleSpec[0]),
                (theme.defaultStyle[1] if styleSpec[1] is None else styleSpec[1])
            )
            self._setStyle(style, styleSpec)

        self._recolorDocument()
        self.onThemeSet.send(self)

    def _recolorDocument(self):
        # Reapply character styles to the text in the transcript
        offset = 0
        for styleName, text in self.transcript:
            length = len(text)
            self.setCharacterAttributes(offset, length,
                                        self.getStyle(styleName), False)
            offset += length

        # Reapply character styles to the user input
        if self.responseStyle:
            self.setCharacterAttributes(offset, self.getLength() - offset,
                                        self.getStyle(self.responseStyle),
                                        False)

    def _setStyle(self, attrSet, styleSpec):
        flags, color = styleSpec

        StyleConstants.setForeground(attrSet, color)

        if flags & MONOSPACE:
            StyleConstants.setFontFamily(attrSet, self.monoFontFamily)
        else:
            StyleConstants.setFontFamily(attrSet, self.defaultFontFamily)

    def getBackgroundColor(self):
        """
        Returns the background color that this document's editor window
        should have.
        """
        return self.theme.backgroundColor

    def getDefaultTextColor(self):
        """
        Returns the default text color. (The theme really should specify one!)
        """
        return self.theme.defaultStyle[1]

    def setFontSize(self, size):
        """
        Updates the document to have the provided font size.
        """
        # First, we need to resize all the existing text.
        attr = SimpleAttributeSet()
        StyleConstants.setFontSize(attr, size)
        self.setCharacterAttributes(0, self.getLength(), attr, False)

        # Next, ensure that new text is given the proper size.
        for name in self.getStyleNames():
            StyleConstants.setFontSize(self.getStyle(name), size)

    def append(self, text, style):
        """
        Writes text at the end of the document, in a specific style.
        """
        self.transcript.append(TranscriptLine(style, text))
        self.insertString(self.getLength(), text, self.getStyle(style))

    def openPrompt(self, promptText, promptStyle, responseStyle):
        """
        Indicates a prompt to draw on the screen, and starts displaying
        user input in response. This requires the history to have already
        been activated.
        """
        if self.promptText is not None:
            raise Exception("A prompt is currently being displayed!")

        self.promptText = promptText
        self.promptStyle = promptStyle
        self.responseStyle = responseStyle

        self.resumePrompt()

    def closePrompt(self):
        """
        Suspends the prompt, then resets it so a different prompt can be
        displayed. After this, you should either commit or close the history.
        """
        if self.promptText is None:
            raise Exception("A prompt is not being displayed!")

        self.suspendPrompt()
        self.promptText = None
        self.promptStyle = None
        self.responseStyle = None

    def resumePrompt(self):
        """
        Draws the prompt and starts allowing user input again,
        also locking the program from writing before the prompt.
        """
        if self.promptText is None:
            raise Exception("A prompt is not being displayed!")

        self.ensureNewline(self.promptStyle)
        self.append(self.promptText, self.promptStyle)

        self.inputLimit = self.getLength()
        self.filter.enable(self.inputLimit, self.getStyle(self.responseStyle))
        self.listener.enable(self.inputLimit)

        self.setResponseText(self.history.getCurrentInput())

    def suspendPrompt(self):
        """
        Stops allowing user input and moves the caret to the next line,
        so content can be printed to the command window by the program
        without restriction.
        """
        if self.promptText is None:
            raise Exception("A prompt is not being displayed!")

        inputLength = self.getLength() - self.inputLimit
        text = self.getText(self.inputLimit, inputLength)
        self.transcript.append(TranscriptLine(self.responseStyle, text))

        self.filter.disable()
        self.listener.disable()
        self.inputLimit = None
        self.ensureNewline(self.responseStyle)

    def setResponseText(self, text):
        """
        Replaces the current response text with some new text.
        """
        if self.inputLimit is None:
            raise Exception("A prompt is not being displayed!")

        offset = self.inputLimit
        self.replace(offset, self.getLength() - offset, text, self.getStyle(self.responseStyle))

    def ensureNewline(self, style):
        """
        Ensures that there's a newline at the end of the buffer,
        so that anything appended will appear at the start of the line.
        """
        length = self.getLength()
        if length != 0 and self.getText(length - 1, 1) != '\n':
            self.append('\n', style)

    def clear(self):
        """
        Erase everything in the document.
        """
        self.transcripts.append([])
        self.transcript = self.transcripts[-1]
        self.remove(0, self.getLength())

