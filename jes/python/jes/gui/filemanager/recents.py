# -*- coding: utf-8 -*-
"""
jes.gui.filemanager.recents
===========================
This manages the "Open Recent Program" menu.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import JESConfig
import os.path
from java.awt.event import ActionListener
from javax.swing import JMenu, JMenuItem
from jes.gui.components.actions import PythonAction
from weakref import WeakValueDictionary

class RecentFiles(object):
    numberOfFiles = 8
    separator = u";"

    def __init__(self, fileManager):
        self.fileManager = fileManager
        fileManager.onRead.connect(self.onReadOrWrite)
        fileManager.onWrite.connect(self.onReadOrWrite)

        self.files = self.retrieveList()

        self.menu = JMenu("Open Recent Program")
        self.menuActions = WeakValueDictionary()
        self.disabledItem = JMenuItem("(No recent programs)")
        self.disabledItem.enabled = False

        self.fillMenu()

    ### Maintaining the menu

    def onReadOrWrite(self, fileManager, filename, **_):
        try:
            self.files.remove(filename)
        except ValueError:
            if len(self.files) >= self.numberOfFiles:
                # Remove enough files that there's a spare slot.
                self.files = self.files[:self.numberOfFiles - 1]

        self.files.insert(0, filename)
        self.storeList(self.files)
        self.fillMenu()

    def fillMenu(self):
        self.menu.removeAll()
        if self.files:
            for filename in self.files:
                action = self.menuActions.get(filename)
                if action is None:
                    action = PythonAction(self.fileManager.readAction, filename,
                                          name=filename)
                    self.menuActions[filename] = action
                self.menu.add(action)
        else:
            self.menu.add(self.disabledItem)

    ### Writing filenames

    def retrieveList(self):
        joined = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_RECENT_FILES)
        if not joined:
            return []
        else:
            return [fn for fn in joined.split(self.separator) if os.path.isfile(fn)]

    def storeList(self, files):
        joined = self.separator.join(files)
        JESConfig.getInstance().setStringProperty(JESConfig.CONFIG_RECENT_FILES, joined)

