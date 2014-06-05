# JES- Jython Environment for Students
# Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
# See JESCopyright.txt for full licensing information

# Birth Date: 09/21/2004
# Creator:    Patrick Carnahan
# Team:       Ramrod 2

import os
from java.lang import String
from javax.swing import JFileChooser
from javax.swing import JOptionPane

class JESFileChooser(JFileChooser):

    #####################################################################
    # Function name: __init__
    # Return:
    # Description:
    #####################################################################
    def __init__(self):
        JFileChooser.__init__(self)

    #####################################################################
    # Function name: approveSelection
    # Description: 
    #     Verifies to the user that they actually want to overwrite an
    #     existing file before returning from the dialog.
    #####################################################################
    def approveSelection(self):
        filePath = self.getSelectedFile().getPath()
        fileName = String(self.getSelectedFile().getName())

        if fileName.matches('[_a-zA-Z0-9()~#.]+'):
            if os.path.exists(filePath):
                message = 'File "' + str(fileName) + ' exists. Overwrite?'
                result = JOptionPane.showConfirmDialog(self, message,
                                                       'Confirm Overwrite',
                                                       JOptionPane.YES_NO_OPTION)
                if result == JOptionPane.YES_OPTION:
                    JFileChooser.approveSelection(self)
            else:
                JFileChooser.approveSelection(self)
        else:
            message = 'The file name contains illegal characters. Please rename.'
            JOptionPane.showMessageDialog(self, message, 'Error', JOptionPane.ERROR_MESSAGE)

