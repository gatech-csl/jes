# -*- coding: utf-8 -*-
"""
jes.gui.dialogs.controller
==========================
This manages the display of dialog boxes.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from java.awt import BorderLayout
from javax.swing import JFrame, JPanel
from jes.gui.components.actions import methodAction

class BasicDialog(JFrame):
    WINDOW_TITLE = "Dialog Box"
    WINDOW_SIZE = (600, 600)

    def __init__(self):
        super(BasicDialog, self).__init__()

        self.setLocationRelativeTo(None)
        self.title = self.WINDOW_TITLE
        self.size = self.WINDOW_SIZE
        self.contentPane.layout = BorderLayout()

        self.buttonPanel = JPanel()
        self.add(self.buttonPanel, BorderLayout.PAGE_END)


class DialogController(object):
    """
    This object manages dialog boxes which should only have one instance.
    The `show` method is an action that will display the dialog.

    :param caption: The text to use as the action name.
    :param factory: A callable (which can be a class) that creates the dialog.
    :param args:    Arguments for the factory.
    :param kwargs:  Keyword arguments for the factory.
    """
    def __init__(self, caption, factory, *args, **kwargs):
        self.show.name = caption
        self.dialogFactory = factory
        self.args = args
        self.kwargs = kwargs

        self.dialog = None

    @methodAction
    def show(self):
        if self.dialog is not None:
            self.dialog.visible = True
        else:
            self.dialog = self.dialogFactory(*self.args, **self.kwargs)
            self.dialog.visible = True

