# -*- coding: utf-8 -*-
"""
jes.gui.commandwindow
=====================
The primary interface class for the command window. The rest of JES
uses this class to deal with the command window without worrying about
the structure.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from .document import CommandDocument
from .history import CommandHistory
from .pane import CommandWindowPane
from .prompt import promptService
from jes.gui.components.actions import methodAction
from jes.gui.components.threading import threadsafe
from media import * # Debugging

class CommandWindowController(object):
    """
    Encapsulates the command window GUI, editing logic, and history.
    """
    def __init__(self):
        self._history = CommandHistory()
        self._document = CommandDocument(self._history)
        self._textpane = CommandWindowPane(self, self._document)
        self._callback = None
        promptService.setCommandWindow(self)

    def getTextPane(self):
        return self._textpane

    @threadsafe
    def setFontSize(self, size):
        self._document.setFontSize(size)

    @threadsafe
    def setTheme(self, name):
        self._document.setTheme(name)

    @threadsafe
    def requestFocus(self):
        self._textpane.requestFocus()

    @threadsafe
    def display(self, text, style):
        """
        Writes text to the command window. If the command window is in
        prompt mode, it prints it, then repeats the prompt.

        :param text:    The text to print.
        :param style:   The name of the style to print it in.
        """
        if self._document.inputLimit is not None:
            offset = self._getCursorOffset()
            self._document.suspendPrompt()
            self.display(text, style)
            self._document.resumePrompt()
            self._restoreCursorOffset(offset)
        else:
            self._document.append(text, style)

    def isInPrompt(self):
        """
        Indicates whether the command window is in prompt mode.

        :return:    `True` or `False`.
        """
        return self._history.isActive()

    @threadsafe
    def prompt(self, promptText, promptStyle, responseCallback, responseStyle, historyGroup=None):
        """
        Puts the command window in prompt mode. This displays the indicated
        prompt, and waits for the user to respond.

        :param promptText:          The text to display before the input.
        :param promptStyle:         The name of the style to use for the
                                    prompt text.
        :param responseCallback:    A callable that will be invoked when the
                                    user presses enter, with the text they
                                    entered. If the prompt is cancelled, this
                                    will be called with `None` instead.
        :param responseStyle:       The name of the style to use for the
                                    user's response.
        :param historyGroup:        If provided, the command history from this
                                    group will be available, and the entered
                                    command will be saved in the history
                                    before the callback is invoked.
        """
        if self._callback is not None or self._history.isActive():
            raise Exception("A prompt is already activated")

        self._callback = responseCallback
        self._history.start(historyGroup)
        self._document.openPrompt(promptText, promptStyle, responseStyle)
        self._textpane.setEditable(True)
        self._textpane.setCaretPosition(self._document.getLength())

    @threadsafe
    def cancelPrompt(self):
        """
        If the command window is in prompt mode, this will cancel the prompt.
        Any user-entered input will remain, but the response callback will
        be called with `None` instead of the text.
        """
        self._textpane.setEditable(False)
        if self._document.inputLimit is not None:
            self._document.closePrompt()
        if self._history.isActive():
            self._history.close()
            if self._callback is not None:
                self._callback(None)
        self._callback = None

    @threadsafe
    def submit(self):
        """
        This is called when the ENTER key is pressed on the editor control.
        """
        self._textpane.setEditable(False)

        if self._document.promptText is not None:
            self._document.closePrompt()

        cb = self._callback
        self._callback = None

        if self._history.isActive():
            text = self._history.commit()
            if cb is not None:
                cb(text)
            else:
                raise Exception("A prompt is None.")

    @methodAction(name="Clear command window")
    @threadsafe
    def clearScreen(self):
        """
        Clears the command window. This can be executed at any time, and
        if the command window is in prompt mode, the prompt and user input
        will be redisplayed after the user has finished entering text.
        """
        if self._document.inputLimit is not None:
            offset = self._getCursorOffset()
            self._document.suspendPrompt()
            self._document.clear()
            self._document.resumePrompt()
            self._restoreCursorOffset(offset)
        else:
            self._document.clear()

    def _getCursorOffset(self):
        return self._document.getLength() - self._textpane.getCaretPosition()

    def _restoreCursorOffset(self, offset):
        length = self._document.getLength()
        newPosition = length - offset

        if newPosition >= self._document.inputLimit:
            self._textpane.setCaretPosition(newPosition)
        else:
            self._textpane.setCaretPosition(length)

