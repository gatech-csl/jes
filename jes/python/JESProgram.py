# JES- Jython Environment for Students
# Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
# See JESCopyright.txt for full licensing information
# 5/16/03: updated save() and saveAs() to return success booleans. -AdamW
# 18 Jul 2007: Added option for backup save.
# 5/13/09: Changes for redesigning configuration writing from python to
# java -Buck

import JESConfig
import JESIntroduction
import JESExceptionRecord
import JESConstants
import JESResources
import JESFileChooser
import JESLogBuffer
import JESUI
import os
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
from jes.bridge.replbuffer import REPLBuffer
from jes.bridge.terpactions import addInterpreterActions
from jes.bridge.terpcontrol import InterpreterControl
from jes.core.interpreter import Interpreter
from jes.core.interpreter.watcher import Watcher
from jes.gui.components.threading import threadsafe

FILE_EXISTS_ERROR = 2


class JESProgram:
    ##########################################################################
    # Function name: __init__
    # Return:
    # Description:
    #
    ##########################################################################

    def __init__(self):
        JESProgram.activeInstance = self
        self.logBuffer = JESLogBuffer.JESLogBuffer(self)

        self.interpreter = terp = Interpreter()
        self.debugger = terp.debugger
        self.watcher = Watcher(self.debugger)

        addInterpreterActions(terp)

        terp.initialize(self.initializeInterpreter)
        self.varsToHighlight = list(terp.initialNames)

        self.introWindow = None

        self.setupGUI()

        # Open the first Python prompt!
        self.replBuffer.startStatement()

    @threadsafe
    def setupGUI(self):
        self.gui = JESUI.JESUI(self)
        self.gui.windowSetting(None)

        self.filename = ' '
        self.settingsFileName = ''

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
            self.openIntroductionWindow()

        # JavaMusic.open()
    def getVarsToHighlight(self):
        return self.varsToHighlight

    def initializeInterpreter(self, terp):
        preproc = JESResources.getPathTo('python/JESPreprocessing.py')
        terp.runFile(preproc, False)

##########################################################################
# Function name: newFile
# Description:
#     Blanks outthe fileName and the text in the editor window.
##########################################################################
    def newFile(self):
        self.gui.editor.setText('')
        self.gui.setFileName('')
        self.logBuffer.resetBuffer()
        self.chooser = swing.JFileChooser()  # reset the filechooser to keep

##########################################################################
# Function name: openFile
# Description:
#     This function will open a dialog window allowing the user to select a
#     file.  If the user selects a file, it is opened, and its contents are
#     place into the text editor.
##########################################################################
    def openFile(self):
        self.chooser = swing.JFileChooser(self.defaultPath)
        self.chooser.setApproveButtonText("Open File")
        returnVal = self.chooser.showOpenDialog(self.gui)
        if returnVal == 0:  # User has chosen a file, so now it can be opened
            file = open(self.chooser.getSelectedFile().getPath(), 'r')
            self.filename = file.name
            self.gui.setFileName(self.chooser.getSelectedFile().getName())
            self.gui.editor.setText(file.read())
            self.gui.editor.modified = 0
            self.gui.loadDifferent()
            file.close()
            self.defaultPath = self.chooser.getCurrentDirectory()
            self.logBuffer.openLogFile(file.name)

##########################################################################
# Function name: saveFile
# Description:
#     This function is called when the user selects the save file option from
#     the user menu.  If there is no file opened yet, the function will do
#     nothing.  If the file has no name, the function will call saveAs.  Else,
#     it will write the contents of the text editor to the file of the current
#     name.
##########################################################################
    def saveFile(self):
        try:
            if self.filename != '':
                text = self.gui.editor.getText()
                # self.chooser.setCurrentDirectory(self.defaultPath)
                #file = open(self.chooser.getSelectedFile().getPath(),'w+')
                # David - testing something out
                #text = text.splitlines(1)
                # file.writelines(text)
                #self.filename = file.name
                # file.close()
                # Commented out by AW: Trying to see if using java instead of jython
                # gets rid of the newline errors

                filePath = self.chooser.getSelectedFile().getPath()
                self.filename = os.path.normpath(filePath)

                fileWriter = io.FileWriter(filePath, 0)
                fileWriter.write(text)
                fileWriter.close()

                self.defaultPath = self.chooser.getCurrentDirectory()
                self.logBuffer.saveLogFile(self.filename)
                self.gui.editor.modified = 0
                self.gui.setFileName(os.path.basename(self.filename))

                # Now write the backup
                if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BACKUPSAVE):
                    backupPath = filePath + "bak"
                    fileWriter = io.FileWriter(backupPath, 0)
                    fileWriter.write(text)
                    fileWriter.close()
                return 1
            else:
                return self.saveAs()
        except:
            # Error handling for saveFile
            return self.saveAs()

##########################################################################
# Function name: saveAs
# Description:
#     Opens a dialog and allows users to select or either type in a filename to
#     save the file as.  If the user selects cancel, nothing happens.
##########################################################################
    def saveAs(self):
        try:
            self.chooser.setCurrentDirectory(self.defaultPath)
            text = self.gui.editor.getText()
            self.chooser.setApproveButtonText("Save File")

            returnVal = self.chooser.showSaveDialog(self.gui)
            # User has chosen a file, so now it can be saved
            if returnVal == 0:
                # DNR
                #file = open(self.chooser.getSelectedFile().getPath(),'w+')
                # self.gui.setFileName(self.chooser.getSelectedFile().getName())
                #text = text.splitlines(1)
                # file.writelines(text)
                #self.filename = file.name
                # file.close()
                # Commented out by AW: Trying to see if using java instead of jython
                # gets rid of the newline errors

                filePath = self.chooser.getSelectedFile().getPath()
                self.filename = os.path.normpath(filePath)

                fileWriter = io.FileWriter(filePath, 0)
                fileWriter.write(text)
                fileWriter.close()

                self.defaultPath = self.chooser.getCurrentDirectory()
                self.gui.editor.modified = 0
                self.gui.setFileName(os.path.basename(self.filename))
                self.logBuffer.saveLogFile(self.filename)

                # Now write the backup
                if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BACKUPSAVE):
                    backupPath = filePath + "bak"
                    fileWriter = io.FileWriter(backupPath, 0)
                    fileWriter.write(text)
                    fileWriter.close()

            return 1

        except lang.Exception, e:
            #TODO - fix
            # Error handling for saveAs
            e.printStackTrace()
            return 0

##########################################################################
# Function name: checkForSave
# Description:
#
##########################################################################
    def checkForSave(self):
        pass

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
        if self.filename == ' ':
            self.setErrorByHand(JESConstants.JESPROGRAM_NO_FILE, 0)
        else:  # error 1. didn't occur

            try:
                file = open(self.filename, 'r')
                fileText = file.read()
                file.close()
            except:
                self.setErrorByHand(
                    JESConstants.JESPROGRAM_ERROR_LOADING_FILE + self.filename + '\n', 0)

            else:  # error 2. didn't occur
                try:
                    lineWithError = JESTabnanny.check(self.filename)

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
                    "======= Loading Program =======", 'system-message')
                self.interpreter.runFile(self.filename)
                self.interpreter.debugger.setTargetFilenames([self.filename])
                self.gui.commandWindow.requestFocus()
                self.gui.editor.getDocument().removeErrorHighlighting()
                self.gui.loadCurrent()

    def setErrorByHand(self, message, lineNumber):
        excRecord = JESExceptionRecord.JESExceptionRecord(self.filename)
        if message == JESConstants.JESPROGRAM_NO_FILE:
            excRecord.setByHand(message)
        else:
            excRecord.setByHand(JESConstants.TAB_ERROR_MESSAGE +
                                '%d\n' % lineNumber,
                                lineNumber
                                )

        self._sendFakeError(excRecord)

    def setErrorFromUserCode(self, type, value, trace):
        excRecord = JESExceptionRecord.JESExceptionRecord(self.filename)
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
# Function name: checkTabs
# Description:
#
##########################################################################
    def checkTabs(self):

        if self.filename != '':
            # tabnanny sends the response to stdout, this redirects that output

            badLine = JESTabnanny.check(self.filename)
            # tabnanny calls tokenizer.tokenize, which can
            # throw a TokenError exception
            # we catch it when we call checkTabs

            return badLine
        return ''
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
# Function name: openIntroductionWindow
# Description:
#     Opens up a JESIntroductionWindow.
##########################################################################
    def openIntroductionWindow(self):
        if self.introWindow == None:
            introWindow = JESIntroduction.JESIntroduction()
        introWindow.show()

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
