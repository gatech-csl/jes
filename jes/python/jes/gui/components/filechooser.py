# -*- coding: utf-8 -*-
"""
jes.gui.filemanager.filechooser
===============================
A more Pythonic Swing JFileChooser.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import os.path
from java.io import File
from javax.swing import JFileChooser, JOptionPane
from javax.swing.filechooser import FileFilter

"""
I'm just going to add some notes about the JFileChooser under GTK+ here.
If you're running the GTK+ Look and Feel, it appears Oracle
cares about you as much as they care about anyone else who uses one of
their open source projects, which is to say, enough to make it
technically "work" so that the cost of forking is higher than the cost
of just keeping on using it, but not enough that it's actually pleasant
to use.

For example, the GTK+ JFileChooser looks like something out of Windows 3.1.
To make it worse, the file filters are broken...they put the toString()
output in the dropdown instead of the description
(OpenJDK bug: https://bugs.openjdk.java.net/browse/JDK-8029536).
And if you try to override it by plugging in the Metal UI, it breaks.

The AWT FileDialog displays beautifully under GTK+, but we can't use it
because its API doesn't expose all the methods we need.
So, after reading way too much JDK source code trying to find workarounds,
I've officially given up. You should probably just use Metal.
"""


### Filtering filenames

class ExtensionFileFilter(FileFilter):
    def __init__(self, extensions, name=None):
        if isinstance(extensions, basestring):
            self.extensions = set([extensions])
        else:
            self.extensions = set(extensions)

        extList = ", ".join("." + ext for ext in sorted(self.extensions))
        if name:
            self._descr = "%s (%s)" % (name, extList)
        else:
            self._descr = "%s files" % extList

    def getDescription(self):
        return self._descr

    def accept(self, candidate):
        if candidate.isDirectory():
            return True

        basename = candidate.getName()
        dotIndex = basename.rfind('.')
        if dotIndex == -1:
            extension = ''
        else:
            extension = basename[dotIndex + 1:]

        return extension in self.extensions


### Actual FileChooser class

class FileChooser(JFileChooser):
    """
    A more Pythonic JFileChooser.
    """
    def __init__(self, location=None, **kwargs):
        super(FileChooser, self).__init__(**kwargs)
        self._validator = None
        if location is not None:
            self.setLocation(location)

    ### Starting Points

    def setLocation(self, location):
        if os.path.isfile(location):
            self.selectedFile = File(location)
        elif os.path.isdir(location):
            self.currentDirectory = File(location)

    ### Validation

    def getValidator(self):
        """
        Returns the validator function currently in use, or `None`.
        """
        return self._validator

    def setValidator(self, val):
        """
        Assigns a validator function, which receives the chosen file path
        while the dialog is still open. It can display any dialogs it needs
        to, then either accept the path by returning it, or return `None`
        to make the user select something else.
        """
        self._validator = val

    validator = property(getValidator, setValidator)

    def approveSelection(self):
        if self._validator is not None:
            chosenFile = self.selectedFile
            chosenPath = chosenFile.path
            validatedPath = self._validator(chosenPath)
            if validatedPath is None or validatedPath is False:
                return
            elif validatedPath is True:
                pass
            elif validatedPath != chosenPath:
                self.selectedFile = File(validatedPath)

        JFileChooser.approveSelection(self)

    ### Filtering

    def addExtensionFilter(self, extensions, name=None):
        fileFilter = ExtensionFileFilter(extensions, name)
        self.addChoosableFileFilter(fileFilter)
        self.setFileFilter(fileFilter)

    def setExtensionFilter(self, extensions, name=None):
        self.resetChoosableFileFilters()
        self.addExtensionFilter(extensions, name)
        self.acceptAllFileFilterUsed = False

    ### Result interpretation

    def chooseFile(self, parent, text):
        return self._getResult(self.showDialog(parent, text))

    def chooseFileToOpen(self, parent):
        return self._getResult(self.showOpenDialog(parent))

    def chooseFileToSave(self, parent):
        return self._getResult(self.showSaveDialog(parent))

    def _getResult(self, code):
        if code == JFileChooser.APPROVE_OPTION:
            return self.selectedFile.path
        else:
            return None

