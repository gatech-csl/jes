# -*- coding: utf-8 -*-
"""
jes.gui.dialogs.intro
=====================
The "intro" dialog, which displays the JESIntroduction.txt file.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from __future__ import with_statement

import JESResources
import JESVersion
from java.awt import BorderLayout
from javax.swing import JTextPane, JScrollPane, JButton
from jes.gui.components.actions import methodAction
from .controller import BasicDialog, DialogController

class IntroDialog(BasicDialog):
    INFO_FILE = JESResources.getPathTo("help/JESIntroduction.txt")

    WINDOW_TITLE = "Welcome to %s!" % JESVersion.TITLE
    WINDOW_SIZE = (400, 300)

    def __init__(self):
        super(IntroDialog, self).__init__()

        # Open the text file and make a text pane
        textPane = JTextPane()
        textPane.editable = False

        scrollPane = JScrollPane(textPane)
        scrollPane.preferredSize = (32767, 32767)   # just a large number

        with open(self.INFO_FILE, 'r') as fd:
            infoText = fd.read().decode('utf8').replace(
                "@version@", JESVersion.VERSION
            )
            textPane.text = infoText

        # Load the scroll pane into the layout
        self.add(scrollPane, BorderLayout.CENTER)

        # Make an OK button
        self.okButton = JButton(self.ok)
        self.buttonPanel.add(self.okButton)

    @methodAction(name="OK")
    def ok(self):
        self.visible = False


introController = DialogController("Introduction", IntroDialog)

