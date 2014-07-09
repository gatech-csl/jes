# -*- coding: utf-8 -*-
"""
jes.gui.commandwindow.history
=============================
This object manages histories of input in the command window.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import CommandDocumentListener

class CommandHistory(CommandDocumentListener.InputBuffer):
    """
    This holds a set of independent input histories, and manages when commands
    are stored and retrieved.

    Normally, it's in the "closed" state, which means it's not doing anything.
    To activate it, call the `start` method with a history group.
    (All history groups are independent.) If you don't want to give history
    access to the current input, provide `None`.

    Whenever the user's command changes, call `setCurrentInput` with the
    new text. If the user is on the partial command line, it will be updated
    so that up/down work as expected. If the user is in the history, there
    will be no effect.

    When the user presses up or down, call `moveUp` or `moveDown`.
    Returning `None` means nothing happened, so you can beep at the user if
    you like. Otherwise, the current position is updated and the text at
    that position is returned. You should replace the user's current
    position with that command.

    When the user presses enter, get the current command, and call `commit`.
    This will enroll the new command in the history, and close it.
    (So you need to call `start` again when the user wants to enter another
    line.)

    If the prompt is cancelled, or the user resets their command, call
    `close`. This will reset the history to the closed state, without
    changing anything.
    """
    def __init__(self):
        self.historyGroups = {}
        self.historyGroup = None
        self.history = None

        self.partialInput = None
        self.currentIndex = None
        # self.currentInput is initialized in Java.

    def close(self):
        self.historyGroup = None
        self.history = None

        self.partialInput = None
        self.currentInput = None
        self.currentIndex = None

    def start(self, historyGroup):
        self.currentInput = ''

        if historyGroup is not None:
            self.historyGroup = historyGroup
            self.history = self.historyGroups.setdefault(historyGroup, [])

            self.partialInput = ''
            self.currentIndex = len(self.history)

    def isActive(self):
        return self.currentInput is not None

    def moveUp(self):
        if self.history is None:
            return None

        return self.moveTo(self.currentIndex - 1)

    def moveDown(self):
        if self.history is None:
            return None

        return self.moveTo(self.currentIndex + 1)

    def moveTo(self, index):
        if self.history is None or index < 0 or index > len(self.history):
            # Trying to move over the stack boundaries. Return.
            return None
        else:
            self.savePartial()
            if index == len(self.history):
                # Moving to the partial-input line.
                self.currentInput = self.partialInput
            else:
                # Moving to a line of history.
                self.currentInput = self.history[index]
            self.currentIndex = index
            return self.currentInput

    def savePartial(self):
        if self.currentIndex == len(self.history):
            self.partialInput = self.currentInput

    def commit(self):
        if self.currentInput is not None:
            text = self.currentInput

            if self.history is not None:
                self.history.append(text)
            self.close()

            return text

