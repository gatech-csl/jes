# -*- coding: utf-8 -*-
"""
jes.program
===========
This is the JESProgram class, which functions as a sort of container for
all the different components of JES. (It also has some historical leftover
code that I haven't had a chance to refactor yet.)

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial;
            (C) 2009 William Scharfnorth, Brian Dorn, and Barbara Ericson;
            (C) 2008 Brian O'Neill, William Scharfnorth, and Barbara Ericson;
            (C) 2006, 2007 Alex Rudnick, Timmy Douglas, and Barbara Ericson;
            (C) 2003 Ellie Harmon, Yu Cheung Ho, Keith McDermott,
                     Eric Mickley, Larry Olson, and Adam Wilson
            (C) 2002 Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from __future__ import absolute_import
import JESConfig
import JESResources
import os
import os.path

import string
import sys
import JavaMusic

from code import compile_command
from tokenize import TokenError
from java.lang import System
from java.lang import Thread 
from javax.swing import JOptionPane
from jes.bridge.replbuffer import REPLBuffer
from jes.bridge.terpactions import addInterpreterActions
from jes.bridge.terpcontrol import InterpreterControl
from jes.core.interpreter import Interpreter
from jes.core.interpreter.exceptionrecord import JESExceptionRecord
from jes.core.interpreter.messages import TAB_ERROR_MESSAGE
from jes.core.interpreter.watcher import Watcher
from jes.core.plugins import PluginData, PluginInstaller
from jes.gui.components.threading import threadsafe
from jes.gui.dialogs.intro import introController
from jes.gui.filemanager import FileManager
from jes.gui.mainwindow import JESUI
from jes.util.tabnanny import check as checkTabs

ERROR_LOADING_FILE = '\nThere was an error loading the file. It may not actually exist. FILENAME: '
ERROR_NO_FILE = ('\nNo file has been selected.\n '
                 'You must open a saved file, or save the opened file,\n'
                 'before clicking LOAD\n')

class JESProgram:
    def __init__(self, initialFilename=None):
        JESProgram.activeInstance = self
        self.startupTimeSec = 0

        # Install all the plugins
        self.pluginData = PluginData()
        self.pluginInstaller = PluginInstaller(self.pluginData)

        # Set up the interpreter
        self.interpreter = terp = Interpreter()
        self.debugger = terp.debugger
        self.watcher = Watcher(self.debugger)

        addInterpreterActions(terp)

        terp.initialize(self.initializeInterpreter)
        self.varsToHighlight = list(terp.initialNames)

        # Install the file manager.
        self.fileManager = FileManager()

        self.setupGUI(initialFilename)

        # Open the first Python prompt!
        self.replBuffer.startStatement()

    @threadsafe
    def setupGUI(self, initialFilename):
        self.gui = JESUI(self)
        self.gui.windowSetting(None)

        self.setHelpArray()

        self.gui.changeSkin(
            JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_SKIN))
        self.gui.show()

        if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BLOCK):
            self.gui.editor.removeBox()
        else:
            self.gui.editor.addBox()

        if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_GUTTER):
            self.gui.turnOnGutter()
        else:
            self.gui.turnOffGutter()

        # Install the bridges.
        self.terpControl = InterpreterControl(self.gui, self.interpreter)
        self.replBuffer = REPLBuffer(self.interpreter, self.gui.commandWindow)

        # Open or create the file.
        if initialFilename is None:
            self.fileManager.newFile()
        else:
            self.fileManager.readFile(initialFilename)

        # Startup complete!
        startTimeNS = System.getProperty("jes.starttimens")
        if startTimeNS is not None:
            self.startupTimeSec = (
                (System.nanoTime() - long(startTimeNS)) / 1000000000.0
            )

        # Show introduction window if settings could not be loaded (Either new
        # JES user or bad write permissions)
        config = JESConfig.getInstance()
        loadError = config.getLoadError()

        if loadError is not None:
            JOptionPane.showMessageDialog(
                self.gui,
                "Your JESConfig.properties file could not be opened!\n" +
                loadError.toString(),
                "JES Configuration",
                JOptionPane.ERROR_MESSAGE
            )
        elif config.wasMigrated():
            JOptionPane.showMessageDialog(
                self.gui,
                "Your settings were imported from JES 4.3.\n" +
                "JES doesn't use the JESConfig.txt file in " +
                "your home directory anymore, so you can delete it.",
                "JES Configuration",
                JOptionPane.INFORMATION_MESSAGE
            )
        elif not config.wasLoaded():
            introController.show()

    def getVarsToHighlight(self):
        return self.varsToHighlight

    def initializeInterpreter(self, terp):
        startup = JESResources.getPathTo('python/jes/user-startup.py')
        #terp.runFile(startup, False)
        #Henry Rachootin did this. This way, everything will be loaded before we start using it.
        startupThread = terp.runFile(startup, False)
        startupThread.join()

##########################################################################
# Function name: loadFile
# Description: checks for possible errors, then calls the interpreter's load file
#              function
#
#              the errors are:
#              1) the program.filename field can contain no file name (ie, a
#                 null string)
#              2) program.filename is a valid string, but the file no longer
#                 exists
#              3) tabnanny throws a Token Error - some kind of problem parsing
#                 the file.  has something to do with unbalanced parenthesis
#              4) The file contains ambigious indentation
#        If any of these errors are present, a JESExceptionRecord is created
#        and the code is not loaded by the interpreter
#       Otherwise, the code is loaded.
##########################################################################
    def loadFile(self):
        if self.fileManager.filename is None:
            self.setErrorByHand(ERROR_NO_FILE, 0)
        else:  # error 1. didn't occur

            try:
                file = open(self.fileManager.filename, 'r')
                fileText = file.read()
                file.close()
            except:
                self.setErrorByHand(ERROR_LOADING_FILE + self.fileManager.filename + '\n', 0)

            else:  # error 2. didn't occur
                try:
                    lineWithError = checkTabs(self.fileManager.filename)

                except:

                    import sys
                    a, b, c = sys.exc_info()

                    self.setErrorFromUserCode(a, b, c)
                    return

                #this is clugy
                # tabnanny can either throw an exception,
                # or return a line number.
                # both signal an error, and we handle them seperatly
                # error 3. didn't occur
                if not lineWithError is None:
                    # an error has occured in the file
                    self.setErrorByHand(TAB_ERROR_MESSAGE + '%d\n' % lineWithError, lineWithError)
                    return

                # error 4. didn't occur,
                # Cancel the prompt, since .load() will redisplay it
                # anyway
                self.gui.commandWindow.cancelPrompt()
                self.gui.commandWindow.display(
                    "======= Loading Program =======\n", 'system-message')
                self.interpreter.runFile(self.fileManager.filename)
                self.interpreter.debugger.setTargetFilenames([self.fileManager.filename])
                self.gui.commandWindow.requestFocus()
                self.gui.editor.getDocument().removeErrorHighlighting()
                self.gui.loadCurrent()

    def setErrorByHand(self, message, lineNumber):
        excRecord = JESExceptionRecord(self.fileManager.filename)
        if message == ERROR_NO_FILE:
            excRecord.setByHand(message)
        else:
            excRecord.setByHand(TAB_ERROR_MESSAGE + '%d\n' % lineNumber, lineNumber)

        self._sendFakeError(excRecord)

    def setErrorFromUserCode(self, type, value, trace):
        excRecord = JESExceptionRecord(self.fileManager.filename)
        excRecord.setFromUserCode(type, value, trace)

        self._sendFakeError(excRecord)

    def _sendFakeError(self, excRecord):
        terp = self.interpreter
        terp.onException.send(terp, mode='execfile', excRecord=excRecord)


##########################################################################
# Function name: closeProgram
# Description:
#     Exits JES
##########################################################################

    def closeProgram(self):
        JESConfig.getInstance().writeConfig()
        self.pluginInstaller.cleanUp()
        System.exit(0)


##########################################################################
# Function Name: setHelpArray
# Description:
#     This sets the array of help file names in self.gui.  If the folder
#     JESHelp cannot be located, the function will throw an exception which is
#     caught by the function.
##########################################################################
    def setHelpArray(self):
        try:
            myFile = JESResources.getFileFor("help/JESHelp")

            arrayOfFiles = myFile.listFiles()
            arrayOfNames = []

            for x in arrayOfFiles:
                arrayOfNames.append(x.toURL())
            stringNames = []
            for x in arrayOfNames:
                stringNames.append(x.toString())

            # for name in stringNames:
            # if (name.find('.DS_Store') != -1):
            #     if(name.startswith('.')):
            #         stringNames.remove(name)

            stringNames = [
                name for name in stringNames if not helpfile_strip(name).startswith(".")]
            stringNames.sort(helpfile_cmp)

            # l = stringNames[1]
            # stringNames.remove(l)
            # stringNames.insert(10, l)
            self.gui.SetHelpFiles(stringNames)
        except Exception, e:
            print "ERROR opening help files"
            print e

# locally useful util functions.
def getdigits(str):
    out = ""

    for c in str:
        if(c.isdigit()):
            out += c
        else:
            break
    return out

HELP_FILE_EXTENTION = '.html'


def helpfile_strip(str):
    out = os.path.basename(str)
    out = out.replace(HELP_FILE_EXTENTION, '')
    out = out.replace('_', ' ')
    return out


def helpfile_cmp(str1, str2):
    if str1 == str2:
        return 0

    str1 = helpfile_strip(str1)
    str2 = helpfile_strip(str2)

    numstr1 = getdigits(str1)
    numstr2 = getdigits(str2)

    if(numstr1 and numstr2):
        return cmp(int(numstr1), int(numstr2))

    return cmp(str1, str2)

if __name__ == '__main__':
    mainJESProgram = JESProgram()

