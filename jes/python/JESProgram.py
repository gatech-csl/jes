# JES- Jython Environment for Students
# Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
# See JESCopyright.txt for full licensing information
# 5/16/03: updated save() and saveAs() to return success booleans. -AdamW
# 18 Jul 2007: Added option for backup save.
# 5/13/09: Changes for redesigning configuration writing from python to
# java -Buck

import JESConfig
import JESExceptionRecord
import JESConstants
import JESResources
import JESFileChooser
import JESLogBuffer
import JESUI
import os
import os.path
import java.io as io
import java.lang as lang
import javax.swing as swing
import java.awt as awt

import string
import sys
import JESTabnanny
import JavaMusic

from code import compile_command
from tokenize import TokenError
from javax.swing import JOptionPane
from jes.bridge.replbuffer import REPLBuffer
from jes.bridge.terpactions import addInterpreterActions
from jes.bridge.terpcontrol import InterpreterControl
from jes.core.interpreter import Interpreter
from jes.core.interpreter.watcher import Watcher
from jes.gui.components.threading import threadsafe
from jes.gui.dialogs.intro import introController
from jes.gui.filemanager import FileManager

FILE_EXISTS_ERROR = 2


class JESProgram:
    ##########################################################################
    # Function name: __init__
    # Return:
    # Description:
    #
    ##########################################################################

    def __init__(self, initialFilename=None):
        JESProgram.activeInstance = self
        self.startupTimeSec = 0

        self.logBuffer = JESLogBuffer.JESLogBuffer(self)

        self.interpreter = terp = Interpreter()
        self.debugger = terp.debugger
        self.watcher = Watcher(self.debugger)

        addInterpreterActions(terp)

        terp.initialize(self.initializeInterpreter)
        self.varsToHighlight = list(terp.initialNames)

        # Install the file manager.
        self.fileManager = FileManager(self.logBuffer)

        self.setupGUI(initialFilename)

        # Open the first Python prompt!
        self.replBuffer.startStatement()

    @threadsafe
    def setupGUI(self, initialFilename):
        self.gui = JESUI.JESUI(self)
        self.gui.windowSetting(None)

        self.chooser = JESFileChooser.JESFileChooser()
        self.defaultPath = io.File(
            JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MEDIAPATH))
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
        startTimeNS = lang.System.getProperty("jes.starttimens")
        if startTimeNS is not None:
            self.startupTimeSec = (
                (lang.System.nanoTime() - long(startTimeNS)) / 1000000000.0
            )

        # Show introduction window if settings could not be loaded (Either new
        # JES user or bad write permissions)
        config = JESConfig.getInstance()
        loadError = config.getLoadError()

        if loadError is not None:
            swing.JOptionPane.showMessageDialog(
                self.gui,
                "Your JESConfig.properties file could not be opened!\n" +
                loadError.toString(),
                "JES Configuration",
                swing.JOptionPane.ERROR_MESSAGE
            )
        elif config.wasMigrated():
            swing.JOptionPane.showMessageDialog(
                self.gui,
                "Your settings were imported from JES 4.3.\n" +
                "JES doesn't use the JESConfig.txt file in " +
                "your home directory anymore, so you can delete it.",
                "JES Configuration",
                swing.JOptionPane.INFORMATION_MESSAGE
            )
        elif not config.wasLoaded():
            introController.show()

        # JavaMusic.open()
    def getVarsToHighlight(self):
        return self.varsToHighlight

    def initializeInterpreter(self, terp):
        preproc = JESResources.getPathTo('python/JESPreprocessing.py')
        terp.runFile(preproc, False)

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
#              3) JESTabnanny throws a Token Error - some kind of problem parsing
#                 the file.  has something to do with unbalanced parenthesis
#              4) The file contains ambigious indentation
#        If any of these errors are present, a JESExceptionRecord is created
#        and the code is not loaded by the interpreter
#       Otherwise, the code is loaded.
##########################################################################
    def loadFile(self):
        if self.fileManager.filename is None:
            self.setErrorByHand(JESConstants.JESPROGRAM_NO_FILE, 0)
        else:  # error 1. didn't occur

            try:
                file = open(self.fileManager.filename, 'r')
                fileText = file.read()
                file.close()
            except:
                self.setErrorByHand(
                    JESConstants.JESPROGRAM_ERROR_LOADING_FILE + self.fileManager.filename + '\n', 0)

            else:  # error 2. didn't occur
                try:
                    lineWithError = JESTabnanny.check(self.fileManager.filename)

                except:

                    import sys
                    a, b, c = sys.exc_info()

                    self.setErrorFromUserCode(a, b, c)
                    return

                #this is clugy
                # JESTabnanny can either throw an exception,
                # or return a line number.
                # both signal an error, and we handle them seperatly
                # error 3. didn't occur
                if not lineWithError is None:
                    # an error has occured in the file
                    self.setErrorByHand(JESConstants.TAB_ERROR_MESSAGE + '%d\n' % lineWithError,
                                        lineWithError)

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
        excRecord = JESExceptionRecord.JESExceptionRecord(self.fileManager.filename)
        if message == JESConstants.JESPROGRAM_NO_FILE:
            excRecord.setByHand(message)
        else:
            excRecord.setByHand(JESConstants.TAB_ERROR_MESSAGE +
                                '%d\n' % lineNumber,
                                lineNumber
                                )

        self._sendFakeError(excRecord)

    def setErrorFromUserCode(self, type, value, trace):
        excRecord = JESExceptionRecord.JESExceptionRecord(self.fileManager.filename)
        excRecord.setFromUserCode(type, value, trace)

        self._sendFakeError(excRecord)

    def _sendFakeError(self, excRecord):
        terp = self.interpreter
        terp.onException.send(terp, mode='execfile', excRecord=excRecord)


##########################################################################
# Function name: debugger_paused
# Parameters:
#     None
# Description:
#     sets the Interpreter and the JES gui into debugger mode, the debugger
#     made a stop
##########################################################################
    def goto_debugger():
        debugger_mode = true

##########################################################################
# Function name: editorLoaded
# Description:
#     returns whether the text editor has been loaded
#
##########################################################################

    def editorLoaded(self):
        return self.gui.loadButton.getForeground() == JESConstants.LOAD_BUTTON_DIFF_COLOR

##########################################################################
# Function name: closeProgram
# Description:
#     Exits JES
##########################################################################

    def closeProgram(self):
        lang.System.exit(0)

##########################################################################
# Function name: stopThread
# Description:
#
##########################################################################
    def stopThread(self):
        self.interpreter.stopThread()

##########################################################################
# Function name: openSettingsGUI
# Description:
#     Opens up a settingd GUI Dialog.
##########################################################################
    def openSettingsGUI(self):
        self.gui.openSettings()

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

##########################################################################
# Function name: runCommand
# Parameters:
#     -text:
# Description:
#
##########################################################################
    def runCommand(self, text):
        # If the document in the editor is not current with the interpreter, warn
        # the user.
        if self.editorLoaded():
            self.gui.commandWindow.display(JESConstants.EDITOR_LOAD_WARNING, 'system-message')

        self.logBuffer.addCommand(text)
        self.interpreter.runCommand(text)

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
