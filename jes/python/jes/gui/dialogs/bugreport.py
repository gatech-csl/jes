# -*- coding: utf-8 -*-
"""
jes.gui.dialogs.bugreport
=========================
The "Report a bug in JES!" dialog, which provides a link to GitHub.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from __future__ import with_statement

import JESVersion
from java.awt import BorderLayout, Desktop
from java.net import URI
from javax.swing import JTextPane, JScrollPane, JButton, JLabel
from jes.gui.components.actions import methodAction
from .controller import BasicDialog, DialogController

WEBSITE_HOST = JESVersion.ISSUES_HOST
WEBSITE_URI = URI(JESVersion.ISSUES_URL)

MESSAGE = (
    "If you find any problems in JES, or anything breaks unexpectedly, "
    "we'd love to know! You can report bugs on the JES project page at %s. "
    "Click the button below to open your Web browser and submit your report."
    "\n\n"
    "When submitting a report, first check to make sure someone else hasn't "
    "submitted the same bug. And please include this version information, "
    "so we know what to test with: "
    "\n\n"
    "%%s"
    "\n\n"
    "Thank you for your feedback!"
) % WEBSITE_HOST


class BugReportDialog(BasicDialog):
    WINDOW_TITLE = "Report a Bug"
    WINDOW_SIZE = (630, 450)

    def __init__(self):
        super(BugReportDialog, self).__init__()

        # Add a message
        textPane = JTextPane()
        textPane.editable = False

        version = "\n".join("    " + line for line in JESVersion.getMessage().splitlines())
        textPane.text = MESSAGE % version

        scrollPane = JScrollPane(textPane)
        scrollPane.preferredSize = (32767, 32767)   # just a large number

        # Load it into the layout
        self.add(scrollPane, BorderLayout.CENTER)

        # Make buttons
        self.sendButton = JButton(self.send)
        self.buttonPanel.add(self.sendButton)

        self.closeButton = JButton(self.close)
        self.buttonPanel.add(self.closeButton)

    @methodAction(name="Send a report")
    def send(self):
        Desktop.getDesktop().browse(WEBSITE_URI)
        self.visible = False

    @methodAction(name="Close")
    def close(self):
        self.visible = False


bugReportController = DialogController("Report a problem in JES!", BugReportDialog)

