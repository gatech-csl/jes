#Jes- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information

import javax.swing as swing

class JESAction(swing.AbstractAction):
################################################################################
# Function name: __init__
# Parameters:
#     -name: a name for the Action
# Return:
#     An instance of the JESAction class.
# Description:
#     Creates a new instance of the JESAction.
################################################################################
    def __init__(self, name):
        self.name = name
        self.action = name
        self.enabled = 1

################################################################################
# Function name: actionPerformed
# Parameters:
#     -event: event object that represents action that occured
# Description:
#     This function is called when an event occurs.
################################################################################
    def actionPerformed(self, event):
        self.action()			

