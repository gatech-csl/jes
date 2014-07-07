# -*- coding: utf-8 -*-
"""
jes.gui.commandwindow.prompt
============================
This is provided to JES client code, for asking questions to the user.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import sys
from threading import Semaphore

class PromptService(object):
    def __init__(self):
        self.semaphore = Semaphore(0)
        self.commandWindow = None
        self.response = None

    def setCommandWindow(self, window):
        self.commandWindow = window

    def requestInput(self, prompt):
        if self.commandWindow is None:
            raise RuntimeError("Command window hasn't registered itself")
        if prompt is None:
            prompt = ''

        self.commandWindow.prompt(prompt, 'standard-output', self.respond, 'standard-input')
        self.semaphore.acquire()

        if self.response is None:
            raise KeyboardInterrupt
        else:
            res = self.response
            self.response = None
            return str(res)

    def respond(self, value):
        self.response = value
        self.semaphore.release()


promptService = PromptService()

