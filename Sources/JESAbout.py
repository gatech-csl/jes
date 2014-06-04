#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information

import JESConstants
import java.awt as awt
import java.lang as lang
import javax.swing as swing

ABOUT_TITLE = 'About JES'
OK_BUTTON_CAPTION = 'OK'
ABOUT_WINDOW_SIZE = (500,600)
COPYRIGHT_FILE = 'JESCopyright.txt'

class JESAbout(swing.JFrame, awt.event.ActionListener):
################################################################################
# Function name: __init__
# Returns:
#     An instance of the JESAbout class.
# Description:
#     Creates an instance of the JES about window class.
################################################################################
    def __init__(self):
        self.size = ABOUT_WINDOW_SIZE
        self.title = ABOUT_TITLE
        self.setLocationRelativeTo(None)
        self.contentPane.setLayout(swing.BoxLayout(self.contentPane,
                                                   swing.BoxLayout.Y_AXIS))

        copyrightInfoArea = swing.JTextPane()
        copyrightInfoArea.setEditable(0)

        #Load copyright information from the JES copyright file
        copyrightFile = open(COPYRIGHT_FILE, 'r')
        copyrightInfoArea.text = copyrightFile.read()
	copyrightInfoArea.setCaretPosition(0)
        copyrightFile.close()

        okButton = swing.JButton(OK_BUTTON_CAPTION, actionListener=self)

        topPane = swing.JScrollPane(copyrightInfoArea)
        topPane.setPreferredSize(awt.Dimension(lang.Short.MAX_VALUE,
                                               lang.Short.MAX_VALUE))
        bottomPanel = swing.JPanel()
        bottomPanel.add(okButton)
        self.contentPane.add(topPane)
        self.contentPane.add(bottomPanel)

################################################################################
# Function name: actionPerformed
# Parameters:
#      -event: event that was performed.
# Description:
#      Catches events that occur in a JESAbout window.  If the OK button was
#      pressed, then the window is closed (just hidden, but not destroyed).
################################################################################
    def actionPerformed(self, event):
        actionCommand = event.getActionCommand()
        if actionCommand == OK_BUTTON_CAPTION:
            self.setVisible(0)
