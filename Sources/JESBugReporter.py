# JES- Jython Environment for Students
# Copyright (C) 2002-2007 the JES team 
# See JESCopyright.txt for full licensing information
# This class, Copyright 2007, Alex Rudnick
# 5/13/09: Changes for redesigning configuration writing from python to java -Buck

import JESConfig
import java.awt as awt
import java.util as util
import java.awt.Event as Event
import java.awt.event.KeyEvent as KeyEvent
import java.lang as lang
import java.net as net
import javax.swing as swing
import java.io as io
import os

import JESConstants

import httplib, urllib, base64

COMMAND_SEND = "Send Report"
COMMAND_CANCEL = "Cancel"

BUGREPORTMESSAGE = """<html>If you find any problems with JES, or if anything
breaks unexpectedly, we'd love to know! You can report bugs and send feature requests
to us using our development website on Google Code.  Click the button below to
open your web broswer and submit your report.  Thank you for your feedback! </html>"""


class JESBugReporter(swing.JFrame):

    def __init__(self):
        self.contentPane.layout = swing.BoxLayout(self.contentPane,
            swing.BoxLayout.Y_AXIS)
	
	message = swing.JLabel(BUGREPORTMESSAGE)
	message.setAlignmentX(awt.Component.CENTER_ALIGNMENT)

        self.add(message)

        self.add(swing.Box.createVerticalStrut(10))

     
        buttonbox = swing.Box(swing.BoxLayout.X_AXIS)
        self.sendbutton = swing.JButton(COMMAND_SEND,
            actionPerformed=self.actionPerformed)
        self.cancelbutton = swing.JButton(COMMAND_CANCEL,
            actionPerformed=self.actionPerformed)
        buttonbox.add(self.sendbutton)
        buttonbox.add(self.cancelbutton)

        #self.add(swing.Box.createVerticalStrut(10))
        self.add(buttonbox)

        buttonbox.setAlignmentX(awt.Component.CENTER_ALIGNMENT)
        
        self.pack()

        self.size = (300, 175)
	self.setLocationRelativeTo(None)
        self.show()

    def actionPerformed(self, event):
        import java.awt.Desktop as Desktop
	import java.net.URI as URI

        cmd = event.getActionCommand()

        if cmd == COMMAND_SEND:
            Desktop.getDesktop().browse(URI("http://code.google.com/p/mediacomp-jes/issues/list"))

        self.setVisible(0)
        self.dispose()


