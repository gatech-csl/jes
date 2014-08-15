# -*- coding: utf-8 -*-
"""
jes.platform.macosx
===================
This tries to keep as much of the fancy Apple magic in one file as possible.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import os.path
from jes.gui.components.threading import invokeLater

try:
    from com.apple.eawt import Application, ApplicationAdapter
except ImportError:
    ApplicationAdapter = object
    onMacOSX = False
else:
    onMacOSX = True


class JESApplicationAdapter(ApplicationAdapter):
    """
    Even though command-line arguments are good enough for Windows and Linux,
    OS X has to use fancy proprietary Apple magic to simply open a file.
    ``:-/``
    """
    def __init__(self, program):
        self.program = program

    def handlePreferences(self, event):
        self.program.gui.openOptions()

    def handleQuit(self, event):
        self.program.gui.exit(event)

    def handleOpenFile(self, event):
        invokeLater(self.program.fileManager.readAction, event.getFilename())


def installOpenHandler(program):
    if onMacOSX:
        app = Application.getApplication()
        adapter = JESApplicationAdapter(program)
        app.addApplicationListener(adapter)
        app.setEnabledPreferencesMenu(True)
    # else, do nothing


def setDockIcon():
    if onMacOSX:
        # I don't know _why_ passing null here works.
        # My guess is that Apple somehow elects an image based on the
        # first window created, and setting it to null means
        # "ignore windows, just use the default."
        # Then the -Xdock:icon JVM option sets the default.
        app = Application.getApplication()
        if hasattr(app, 'setDockIconImage'):
            app.setDockIconImage(None)

