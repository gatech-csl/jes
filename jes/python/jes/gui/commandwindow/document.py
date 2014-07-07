# -*- coding: utf-8 -*-
"""
jes.gui.commandwindow.document
==============================
This Document class controls how the text in the command window changes.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
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
        self.filter = CommandDocumentFilter(self)
        self.setDocumentFilter(self.filter)

        self.listener = CommandDocumentListener(self)
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
        self.setResponseText(self.history.getCurrentInput())

    def suspendPrompt(self):
        """
        Stops allowing user input and moves the caret to the next line,
        so content can be printed to the command window by the program
        without restriction.
        """
        if self.promptText is None:
            raise Exception("A prompt is not being displayed!")

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


class CommandDocumentFilter(DocumentFilter):
    """
    This protects system-level text from modification.
    When the document is displaying a prompt, this will protect any text
    before the prompt from being edited. When the document is not displaying
    a prompt, any edits are allowed (so find a way to protect it from
    the user).
    """
    def __init__(self, doc):
        self.doc = doc

    def insertString(self, bypass, offset, string, attr):
        limit = self.doc.inputLimit

        if limit is None:
            bypass.insertString(offset, string, attr)
        elif offset >= limit:
            responseStyle = self.doc.getStyle(self.doc.responseStyle)
            string = string.replace('\t', JESConstants.TAB)
            bypass.insertString(offset, string, responseStyle)
        else:
            debug("Inserting %r denied at %r (limit is %r)", string, offset, limit)

    def replace(self, bypass, offset, length, string, attr):
        limit = self.doc.inputLimit
        if limit is None:
            bypass.replace(offset, length, string, attr)
        else:
            responseStyle = self.doc.getStyle(self.doc.responseStyle)
            endOffset = offset + length
            string = string.replace('\t', JESConstants.TAB)

            if offset >= limit and endOffset >= limit:
                bypass.replace(offset, length, string, responseStyle)
            elif offset < limit and endOffset >= limit:
                bypass.replace(limit, length - (limit - offset), string, responseStyle)
            else:
                debug("Replacing %r at %r:%r with %r denied (limit is %r)", self.doc.getText(offset, length), offset, length, string, limit)

    def remove(self, bypass, offset, length):
        limit = self.doc.inputLimit
        if limit is None:
            bypass.remove(offset, length)
        else:
            endOffset = offset + length

            if offset >= limit and endOffset >= limit:
                bypass.remove(offset, length)
            elif offset < limit and endOffset >= limit:
                bypass.remove(limit, length - (limit - offset))
            else:
                debug("Removing %r at %r:%r denied (limit is %r)", self.doc.getText(offset, length), offset, length, limit)


class CommandDocumentListener(DocumentListener):
    """
    This listener is responsible for keeping the CommandHistory up to date
    with the current status. Whenever the document changes, if a prompt is
    displayed, it grabs the slice after the prompt and tosses it to the
    document history.
    """
    def __init__(self, doc):
        self.doc = doc

    def update(self, event):
        limit = self.doc.inputLimit
        if limit is not None:
            length = self.doc.getLength()
            inputText = self.doc.getText(limit, length - limit)
            self.doc.history.setCurrentInput(inputText.rstrip('\n'))

    def changedUpdate(self, event):
        self.update(event)

    def insertUpdate(self, event):
        self.update(event)

    def removeUpdate(self, event):
        self.update(event)

