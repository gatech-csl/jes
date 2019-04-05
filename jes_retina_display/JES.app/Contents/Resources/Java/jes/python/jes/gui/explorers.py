# -*- coding: utf-8 -*-
"""
jes.gui.explorers
=================
This contains menu actions for launching the explorers.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import media
from javax.swing import JOptionPane
from jes.gui.components.actions import methodAction

class Explorers(object):
    def __init__(self, parent, interpreter):
        self.parentWindow = parent
        self.interpreter = interpreter
        self.actions = [
            self.loadSoundTool,
            self.loadPictureTool,
            self.loadFrameSequencerTool
        ]

    @methodAction(name="Sound Tool...")
    def loadSoundTool(self):
        """
        Examines the user namespace for sounds,
        and presents a list for the user to pick from.
        Then, the sound is opened in the sound tool.
        """
        self._openExplorer("Sound Tool", media.openSoundTool,
                           "Sound", "sound", "sounds")

    @methodAction(name="Picture Tool...")
    def loadPictureTool(self):
        """
        Examines the user namespace for pictures,
        and presents a list for the user to pick from.
        Then, the picture is opened in the picture tool.
        """
        self._openExplorer("Picture Tool", media.openPictureTool,
                           "Picture", "picture", "pictures")

    @methodAction(name="Movie Tool...")
    def loadFrameSequencerTool(self):
        """
        Examines the user namespace for movies,
        and presents a list for the user to pick from.
        Then, the movie is opened in the frame sequencer tool.
        """
        self._openExplorer("Frame Sequencer Tool", media.openFrameSequencerTool,
                           "Movie", "movie", "movies")


    ###
    ### Internals
    ###

    def _openExplorer(self, toolName, explorer, cls, singular, plural):
        variables = self._findVariablesOfClass(cls)

        if len(variables) > 0:
            varname = self._showChoiceDialog(
                "Open %s" % toolName, "Choose a %s to examine: " % singular,
                variables.keys()
            )

            if varname is not None:
                explorer(variables[varname])
        else:
            self._showErrorDialog(
                "No %s" % plural, "There are no %s to examine." % plural
            )

    def _findVariablesOfClass(self, cls):
        variables = {}

        for name, obj in self.interpreter.namespace.items():
            if getattr(type(obj), '__name__', None) == cls:
                variables[name] = obj

        return variables

    def _showChoiceDialog(self, title, text, choices):
        return JOptionPane.showInputDialog(
            self.parentWindow, text, title, JOptionPane.INFORMATION_MESSAGE,
            None, choices, choices[0]
        )

    def _showErrorDialog(self, title, text):
        JOptionPane.showMessageDialog(
            self.parentWindow, text, title, JOptionPane.ERROR_MESSAGE
        )

