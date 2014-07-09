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
import JESConstants
from java.awt import Color
from javax.swing.event import DocumentListener
from javax.swing.text import DefaultStyledDocument, DocumentFilter, StyleConstants
from jes.gui.swingutil import debug

class CommandDocument(DefaultStyledDocument):
    """
    This is the document subclass used for the JES command window.
    Its only responsibilities compared to a normal document are protecting
    everything written by the program up to the last prompt, and keeping
    the History up to date with what the current prompt text is.
    """
    def __init__(self, history):
        self.history = history

        self.promptText = None
        self.promptStyle = None
        self.responseStyle = None

        self.inputLimit = None

        # Set the default style
        baseStyle = self.getStyle('default')
        StyleConstants.setFontFamily(baseStyle, "Monospaced")
        StyleConstants.setBackground(baseStyle, Color.BLACK)
        StyleConstants.setForeground(baseStyle, Color(0xeeeecc))

        # Set the pretty text styles
        styleColors = {
            'python-code':      Color(0xaacdf3),    # Light blue
            'python-prompt':    Color(0x729fcf),    # Slightly darker blue
            'python-return':    Color(0xedd400),    # Gold
            'python-traceback': Color(0xff5c58),    # Red
            'standard-input':   Color(0x8ae234),    # Green
            'standard-output':  Color(0xffffff),    # White
            'standard-error':   Color(0xfe8df2),    # Pink
            'system-message':   Color(0xff9b41),    # Orange
        }

        for name, color in styleColors.items():
            style = self.addStyle(name, baseStyle)
            StyleConstants.setForeground(style, color)
            StyleConstants.setFontFamily(style, "Monospaced")

        # Install the filter and document listener
        self.filter = CommandDocumentFilter()
        self.setDocumentFilter(self.filter)

        self.listener = CommandDocumentListener(self.history)
        self.addDocumentListener(self.listener)

    def append(self, text, style):
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
        self.remove(0, self.getLength())

