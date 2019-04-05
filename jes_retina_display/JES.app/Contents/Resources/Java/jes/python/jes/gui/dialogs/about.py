# -*- coding: utf-8 -*-
"""
jes.gui.dialogs.about
=====================
The "about" dialog, which displays the JESCopyright.txt and JESChangelog.txt
files.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from __future__ import with_statement

import JESResources
import JESVersion
from java.awt import BorderLayout, Component
from javax.swing import (JTabbedPane, JTextPane, JScrollPane, JButton,
                         JLabel, JPanel)
from jes.gui.components.actions import methodAction
from .controller import BasicDialog, DialogController

class AboutDialog(BasicDialog):
    INFO_FILES = (
        ("Authors/License",     JESResources.getPathTo("help/JESCopyright.txt")),
        ("Version History",     JESResources.getPathTo("help/JESChangelog.txt")),
        ("Included Software",   JESResources.getPathTo("help/JESDependencies.txt")),
    )

    WINDOW_TITLE = "About " + JESVersion.TITLE
    WINDOW_SIZE = (600, 600)

    def __init__(self):
        super(AboutDialog, self).__init__()

        # Open the files and build a tab pane
        self.tabbedPane = tabs = JTabbedPane()

        for title, path in self.INFO_FILES:
            textPane = JTextPane()
            textPane.editable = False
            scrollPane = JScrollPane(textPane)
            scrollPane.preferredSize = (32767, 32767)   # just a large number

            with open(path, 'r') as fd:
                infoText = fd.read().decode('utf8')
                textPane.text = infoText

            textPane.caretPosition = 0
            tabs.addTab(title, scrollPane)

        # Load this tabbed pane into the layout
        self.add(tabs, BorderLayout.CENTER)

        # Add a label at the top
        versionLabel = JLabel(JESVersion.TITLE + " version " + JESVersion.RELEASE)
        versionLabel.alignmentX = Component.CENTER_ALIGNMENT

        versionPanel = JPanel()
        versionPanel.add(versionLabel)
        self.add(versionPanel, BorderLayout.PAGE_START)

        # Make an OK button
        self.okButton = JButton(self.ok)
        self.buttonPanel.add(self.okButton)

    @methodAction(name="OK")
    def ok(self):
        self.visible = False


aboutController = DialogController("About %s" % JESVersion.TITLE, AboutDialog)

