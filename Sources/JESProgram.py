#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information
#5/16/03: updated save() and saveAs() to return success booleans. -AdamW
#5/20/03: added loadSuccess to be called when a JESThread has successfully loaded
#         code. - AdamW
#18 Jul 2007: Added option for backup save.
#5/13/09: Changes for redesigning configuration writing from python to java -Buck

import JESConfig
import JESAbout
import JESIntroduction
import JESExceptionRecord
import JESRunnable
import JESConstants
import JESInterpreter
import JESStdOutputBuffer
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

FILE_EXISTS_ERROR=2

class JESProgram:
################################################################################
# Function name: __init__
# Return:
# Description:
#
################################################################################
    def __init__(self):
        #"@sig public JESProgram()"
       #swing.UIManager.setLookAndFeel("javax.swing.plaf.metal.MetalLookAndFeel");
#        self.userExperience = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MODE);
#        self.gutterOn = JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_GUTTER);
#        self.blockBoxOff = JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BLOCK);
#        self.autoSaveOnRun = JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_AUTOSAVEONRUN);
#        self.backupSave = JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BACKUPSAVE);
#        self.wrapPixelValues = JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_WRAPPIXELVALUES);
#        self.userFont = JESConfig.getInstance().getIntegerProperty(JESConfig.CONFIG_FONT);
#        self.showTurnin = JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_SHOWTURNIN);
#        self.skin = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_SKIN);
#        self.webDefinitions = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_WEB_TURNIN);
#        self.mediaFolder = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MEDIAPATH);

        self.logBuffer=JESLogBuffer.JESLogBuffer(self)
#        self.logBuffer.saveBoolean = JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_LOGBUFFER);
	
        # let's just read the config file once, and if
        # it's no there, we'll handle it right now.
        # self.preCheckForConfigFile()
        # self.getSettingsLater = 0
        # self.loadConfigFile()

        self.textForCommandWindow = ''
        self.aboutWindow = None
        self.introWindow = None

        self.gui = JESUI.JESUI(self)
        self.filename = ' '
        self.settingsFileName=''
        self.interpreter = JESInterpreter.JESInterpreter(self)
        # a gross hack?, see JESUI.py on why it's commentted out there
        self.interpreter.debugger.watcher.setMinimumSize(awt.Dimension(500,400))
        self.interpreter.debugger.watcher.setPreferredSize(awt.Dimension(600,400))

        self.gui.windowSetting(None)
        
        self.varsToHighlight = self.interpreter.getVarsToHighlight()

        self.chooser = JESFileChooser.JESFileChooser()
        self.defaultPath = io.File( JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MEDIAPATH) )
        self.setHelpArray()
	#self.loadSuccess(), 5/15/09 Dorn: removed as unnecessary and breaks due to needed code in loadSuccess for input

        self.gui.changeSkin( JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_SKIN) )
        self.gui.show()

        if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BLOCK):
            self.gui.editor.removeBox()
        else:
            self.gui.editor.addBox()

        if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_GUTTER):
            self.gui.turnOnGutter()
        else:
            self.gui.turnOffGutter()

        # self.checkForConfigFile()
            ## do these once we're started...

        # later is now!
        #if self.getSettingsLater:
            #self.openSettingsGUI()
            #self.openIntroductionWindow()

        #Show introduction window if settings could not be loaded (Either new JES user or bad write permissions)
        if not JESConfig.getInstance().isConfigLoaded():
            self.openIntroductionWindow()
            #self.openSettingsGUI()
            
        #self.gui.repaint()

        #JavaMusic.open()
    def getVarsToHighlight(self):
        return self.varsToHighlight

        
#main
    def main(self, args):
        "@sig public static void main(String args[])"
        self.__init__()
        return self

################################################################################
# Function name: newFile
# Description: 
#     Blanks outthe fileName and the text in the editor window. 
################################################################################
    def newFile(self):
        self.gui.editor.setText('')
        self.gui.setFileName('')
        self.logBuffer.resetBuffer()
        self.chooser = swing.JFileChooser() #reset the filechooser to keep

################################################################################
# Function name: openFile
# Description: 
#     This function will open a dialog window allowing the user to select a 
#     file.  If the user selects a file, it is opened, and its contents are  
#     place into the text editor. 
################################################################################
    def openFile(self):
        self.chooser = swing.JFileChooser(self.defaultPath)
        self.chooser.setApproveButtonText("Open File")
        returnVal = self.chooser.showOpenDialog(self.gui)
        if returnVal ==  0: #User has chosen a file, so now it can be opened
            file = open(self.chooser.getSelectedFile().getPath(),'r')
            self.filename = file.name
            self.gui.setFileName(self.chooser.getSelectedFile().getName())
            self.gui.editor.setText(file.read())
            self.gui.editor.modified = 0
            self.gui.loadDifferent()
            file.close()
            self.defaultPath = self.chooser.getCurrentDirectory()
            self.logBuffer.openLogFile(file.name)
      
################################################################################
# Function name: saveFile
# Description:  
#     This function is called when the user selects the save file option from 
#     the user menu.  If there is no file opened yet, the function will do          
#     nothing.  If the file has no name, the function will call saveAs.  Else, 
#     it will write the contents of the text editor to the file of the current 
#     name.
################################################################################
    def saveFile(self):
        try:
            if self.filename != '' :
                text=self.gui.editor.getText()
                #self.chooser.setCurrentDirectory(self.defaultPath)
                #file = open(self.chooser.getSelectedFile().getPath(),'w+')
                #David - testing something out
                #text = text.splitlines(1)
                #file.writelines(text)
                #self.filename = file.name
                #file.close()
                #Commented out by AW: Trying to see if using java instead of jython
                #gets rid of the newline errors
                
                filePath = self.chooser.getSelectedFile().getPath()
                self.filename =  os.path.normpath(filePath)

                fileWriter = io.FileWriter(filePath, 0)
                fileWriter.write(text)
                fileWriter.close()
                
                self.defaultPath = self.chooser.getCurrentDirectory()
                self.logBuffer.saveLogFile(self.filename)
                self.gui.editor.modified = 0
                self.gui.setFileName(os.path.basename(self.filename))
                
                #Now write the backup
                if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BACKUPSAVE):
                    backupPath = filePath+"bak"
                    fileWriter = io.FileWriter(backupPath, 0)
                    fileWriter.write(text)
                    fileWriter.close()
                return 1
            else:
                return self.saveAs()
        except:
            #Error handling for saveFile
            return self.saveAs()

################################################################################
# Function name: saveAs
# Description: 
#     Opens a dialog and allows users to select or either type in a filename to
#     save the file as.  If the user selects cancel, nothing happens.
################################################################################
    def saveAs(self):
        try:
            self.chooser.setCurrentDirectory(self.defaultPath)
            text = self.gui.editor.getText()
            self.chooser.setApproveButtonText("Save File")
            
            returnVal = self.chooser.showSaveDialog(self.gui)
            if returnVal ==  0: #User has chosen a file, so now it can be saved
                #DNR
                #file = open(self.chooser.getSelectedFile().getPath(),'w+')
                #self.gui.setFileName(self.chooser.getSelectedFile().getName())
                #text = text.splitlines(1)
                #file.writelines(text)
                #self.filename = file.name
                #file.close()
                #Commented out by AW: Trying to see if using java instead of jython
                #gets rid of the newline errors

                filePath = self.chooser.getSelectedFile().getPath()
                self.filename = os.path.normpath(filePath)

                fileWriter = io.FileWriter(filePath, 0)
                fileWriter.write(text)
                fileWriter.close()

                self.defaultPath = self.chooser.getCurrentDirectory()
                self.gui.editor.modified = 0
                self.gui.setFileName(os.path.basename(self.filename))
                self.logBuffer.saveLogFile(self.filename)

                #Now write the backup
                if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BACKUPSAVE):
                    backupPath = filePath+"bak"
                    fileWriter = io.FileWriter(backupPath, 0)
                    fileWriter.write(text)
                    fileWriter.close()

            return 1
        
        except lang.Exception, e:
        #TODO - fix
            #Error handling for saveAs
            e.printStackTrace()
            return 0

################################################################################
# Function name: checkForSave
# Description:
#
################################################################################
    def checkForSave(self):
        pass

################################################################################
# Function name: loadFile
# Description: checks for possible errors, then calls JESInterpreter's load file
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
#        If any of these errors are present, a JESExceptionRecord is created,
#        and a JESRunnable is called and the code is not loaded by the interpreter
#       Otherwise, the code is loaded.
################################################################################
    def loadFile(self):
        if self.filename == ' ':
            self.setErrorByHand(JESConstants.JESPROGRAM_NO_FILE, 0)
        else: # error 1. didn't occur
          
            try:
                file = open(self.filename, 'r')
                fileText = file.read()
                file.close()
            except:
                self.setErrorByHand(JESConstants.JESPROGRAM_ERROR_LOADING_FILE +   self.filename + '\n',0)

            else: # error 2. didn't occur
                self.gui.commandWindow.setKeymap(None)
                try:
                    lineWithError = JESTabnanny.check(self.filename)

      
                except:

                    import sys
                    a,b,c = sys.exc_info()

                    self.setErrorFromUserCode( a,b,c )
                    return

                #this is clugy
                #JESTabnanny can either throw an exception,
                # or return a line number.
                # both signal an error, and we handle them seperatly
                # error 3. didn't occur
                if not lineWithError is None:
                    # an error has occured in the file
                    self.setErrorByHand(JESConstants.TAB_ERROR_MESSAGE +'%d\n' % lineWithError,
                                         lineWithError)

                    return

                # error 4. didn't occur,
                # give the command area the focus
		self.gui.commandWindow.showText("\n======= Loading Progam =======\n")
                self.interpreter.load( self.filename)   
                self.gui.commandWindow.requestFocus()
                self.gui.editor.getDocument().removeErrorHighlighting()

    def setErrorByHand(self,message,lineNumber):
        excRecord = JESExceptionRecord.JESExceptionRecord(self.filename,self)
        if message == JESConstants.JESPROGRAM_NO_FILE:
                excRecord.setByHand(message)
        else:
                excRecord.setByHand(JESConstants.TAB_ERROR_MESSAGE + \
                                   '%d\n' % lineNumber,
                                    lineNumber
                                   )    
        runnable = JESRunnable.JESRunnable(self.interpreter,'',excRecord,'run')
        runnable.run()

    def setErrorFromUserCode(self,type,value,trace):
        excRecord = JESExceptionRecord.JESExceptionRecord(self.filename,self)
        excRecord.setFromUserCode(type,value,trace)
        runnable = JESRunnable.JESRunnable(self.interpreter,
                                           '',
                                           excRecord,
                                           'run')
        runnable.run()

        
        
################################################################################
# Function name: debugger_paused
# Parameters:
#     None
# Description: 
#     sets the Interpreter and the JES gui into debugger mode, the debugger
#     made a stop
################################################################################
    def goto_debugger():
        debugger_mode = true

################################################################################
# Function name: editorLoaded
# Description:
#     returns whether the text editor has been loaded
#     
################################################################################

    def editorLoaded(self):
        return self.gui.loadButton.getForeground() == JESConstants.LOAD_BUTTON_DIFF_COLOR

################################################################################
# Function name: loadSuccess
# Description:
#     Called whenever the interpreter successfully loads a Editor Document.
#     5/20/03 AdamW: Used for recoloring the Load Button on load success
################################################################################
    def loadSuccess(self):
        #self.gui.refreshDebugMenu()
        self.gui.loadCurrent()
        

################################################################################
# Function name: checkTabs
# Description:
#
################################################################################
    def checkTabs(self):

        if self.filename != '':
            #tabnanny sends the response to stdout, this redirects that output

            badLine = JESTabnanny.check(self.filename)
            # tabnanny calls tokenizer.tokenize, which can
            # throw a TokenError exception
            # we catch it when we call checkTabs

            return badLine
        return ''
################################################################################
# Function name: closeProgram
# Description:
#     Exits JES
################################################################################
    def closeProgram(self):
        lang.System.exit(0)

################################################################################
# Function name: stopThread
# Description:
#
################################################################################
    def stopThread(self):
        self.interpreter.stopThread()

################################################################################
# Function name: openAboutWindow
# Description: 
#     Opens up a JESAboutWindow.
################################################################################
    def openAboutWindow(self):
        if self.aboutWindow == None:
            aboutWindow = JESAbout.JESAbout()
        aboutWindow.show()

################################################################################
# Function name: openIntroductionWindow
# Description: 
#     Opens up a JESIntroductionWindow.
################################################################################
    def openIntroductionWindow(self):
        if self.introWindow == None:
            introWindow = JESIntroduction.JESIntroduction()
        introWindow.show()
   
################################################################################
# Function name: openSettingsGUI
# Description: 
#     Opens up a settingd GUI Dialog.
################################################################################
    def openSettingsGUI(self):
        self.gui.openSettings()

################################################################################
# Function Name: setHelpArray
# Description: 
#     This sets the array of help file names in self.gui.  If the folder 
#     JESHelp cannot be located, the function will throw an exception which is 
#     caught by the function.
################################################################################
    def setHelpArray(self):
        try:
            myFile= io.File(JESConstants.JESHELP)

            arrayOfFiles = myFile.listFiles()
            arrayOfNames = []

            for x in arrayOfFiles:
                arrayOfNames.append(x.toURL())
            stringNames = []
            for x in arrayOfNames:
                stringNames.append(x.toString())

            # for name in stringNames:
            #     # if (name.find('.DS_Store') != -1):
            #     if(name.startswith('.')):
            #         stringNames.remove(name)

            stringNames = [name for name in stringNames if not helpfile_strip(name).startswith(".") ]
            stringNames.sort(helpfile_cmp)

            # l = stringNames[1]
            # stringNames.remove(l)
            # stringNames.insert(10, l)
            self.gui.SetHelpFiles(stringNames)
        except Exception, e:
            print "ERROR opening help files"
            print e

################################################################################
# Function name: runCommand
# Parameters:
#     -text:
# Description:
#
################################################################################
    def runCommand(self, text):
        #If the document in the editor is not current with the interpreter, warn
        #the user.
        if self.editorLoaded():
            self.gui.commandWindow.showText(JESConstants.EDITOR_LOAD_WARNING)

        self.gui.commandWindow.setKeymap(None)
        self.logBuffer.addCommand(text)
        self.interpreter.runCommand(text)
 

################################################################################
# Function name: sendTextToCommandWindow
# Parameters: 
#     -text:
# Description:
#     As the interpreter runs, it will generate text for the command window to 
#     display.  That text is buffered in JESProgram until the command window 
#     asks for it with the getTextForCommandWindow function
################################################################################
    def sendTextToCommandWindow(self, text):
        self.textForCommandWindow = self.textForCommandWindow + text

################################################################################
# Function name: getTextForCommandWindow
# Description: 
#     Returns the buffered text that was generated by JESInterpreter
################################################################################
    def getTextForCommandWindow(self):
        returnText = self.textForCommandWindow
        self.textForCommandWindow = ''
        return returnText

################################################################################
# Function name: sendErrorToCommandWindow
# Parameters:
#     -text:
# Description:
#
################################################################################
    def sendErrorToCommandWindow(self, text):
        self.textForCommandWindow = self.textForCommandWindow + text

################################################################################
# Function name: sendError
# Parameters: self
# Description: sends an error tp the command window
#
################################################################################
    def sendError(self):
        errFp = StringIO.StringIO()
        traceback.print_exc( file=errFp )
        errMsg = errFp.getvalue()
        self.sendErrorToCommandWindow( errMsg)

################################################################################
# Function name:  loadConfigFile
# Parameters: self
# Description: Checks to see if the config file already exists.  If it does exist,
#      the function closes the file and exits so that JES can run normally.  If the 
#      file does not exist, an introduction to JES is brought up explaining to the 
#      user about the settings file for JES.  The settings menu option is also 
#      brought up so that the user can create the settings file.
#
################################################################################
#    def loadConfigFile(self):
#        array = self.readFromConfigFile()
#
#        if(None == array):
#            print "No config file found, making a new one!"
#            #Config File doesn't exist, need to create, also need to introduce
#            #the user to JES.
#
#            self.makeNewConfigFile('','','',JESConstants.BEGINNER_MODE, JESConstants.MID_FONT, '')
#            self.getSettingsLater = 1
#        else:
#            self.userExperience=array[JESConstants.CONFIG_MODE]
#            self.userFont=int(array[JESConstants.CONFIG_FONT])
#            self.gutterOn = int(array[JESConstants.CONFIG_GUTTER])
#            self.blockBoxOff = int(array[JESConstants.CONFIG_BLOCK])
#            self.webDefinitions = array[JESConstants.CONFIG_WEB_TURNIN]
#            self.autoSaveOnRun = int(array[JESConstants.CONFIG_AUTOSAVEONRUN])
#            self.backupSave = int(array[JESConstants.CONFIG_BACKUPSAVE])
#            self.mediaFolder = array[JESConstants.CONFIG_MEDIAPATH]
#            self.wrapPixelValues = int(array[JESConstants.CONFIG_WRAPPIXELVALUES])
#            self.logBuffer.saveBoolean = int(array[JESConstants.CONFIG_LOGBUFFER])
#            self.skin = array[JESConstants.CONFIG_SKIN] ## string value
#            self.showTurnin = int(array[JESConstants.CONFIG_SHOWTURNIN])
#            # print "check, program.skin:", self.skin
#
################################################################################
# Function name: makeNewConfigFile
# Parameters: self, name, gt, mail
# Description: Writes the passed in information to the config file.  If the file 
#        exists, it will be over written.  If it does not exist, it will be created.
#        If an IO Error occurs, an error message is printed to the transcript.
#
################################################################################
#    def makeNewConfigFile(self,name,gt,mail,usermode,font,email):
#        try:
#            self.saveOptions()
#
#            self.writeConfigListToFile( [[JESConstants.CONFIG_NAME, name],
#                                         [JESConstants.CONFIG_GT, gt],
#                                         [JESConstants.CONFIG_MAIL, mail],
#                                         [JESConstants.CONFIG_MODE, usermode],
#                                         [JESConstants.CONFIG_FONT, font],
#                                         [JESConstants.CONFIG_EMAIL_ADDR, email]])
#        except Exception, inst:
#            print type(inst)     # the exception instance
#            print inst.args      # arguments stored in .args
#            print 'Warning.  An unexpected IO Error has occurred in writeToConfigFile in JESProgram' 
#
################################################################################
# Function name: writeConfigListToFile
# Parameters:
#     -array: an array of preperties to be written to the file
# Description:
#     Takes an array of an arbitrary amount of properties and writes them out to
#     the config file, filling in any missing properties from the old version of
#     the configuration file.  The property list is in the format:
#     [[JESConstants.CONFIG_GT, gtXXXXX], [JESConstants.CONFIG_GUTTER, 0], ...]
################################################################################
#    def writeConfigListToFile(self, array):
#        try:
#            oldarray = self.readFromConfigFile()
#            if(None == oldarray):
#                oldarray = [''] * JESConstants.CONFIG_NLINES
#
#            # handle the "not there" case in the read function.
#            ## if len(oldarray) < JESConfig.CONFIG_NLINES:
#            ##     oldarray += [''] * (JESCONFIG.CONFIG_NLINES - len(oldarray))
#
#            for i in range(0, len(oldarray)):
#                for element in array:
#                    if element[0] == i:
#                        oldarray[i] = element[1]
#
#            homedir=os.path.expanduser("~")
#            f=open(homedir+io.File.separator+JESConstants.JES_CONFIG_FILE_NAME,'w')
#            #print oldarray
#            for element in oldarray:
#                f.write(str(element))
#                f.write("\n")
#            f.close()
#        except Exception, e:
#            print type(e)     # the exception instance
#            print e.args      # arguments stored in .args
#            print 'Warning: An unexpecter IO Error has occurred in writeConfigListToFile in JESProgram' 
################################################################################

#    def saveOptions(self):
#        "Write out the current options to the config file"
#        self.writeConfigListToFile([[JESConstants.CONFIG_MODE, self.userExperience],
#                                   [JESConstants.CONFIG_FONT, self.userFont],
#                                   [JESConstants.CONFIG_GUTTER, self.gutterOn],
#                                   [JESConstants.CONFIG_BLOCK, self.blockBoxOff],
#                                   [JESConstants.CONFIG_WRAPPIXELVALUES, self.wrapPixelValues],
#                                   [JESConstants.CONFIG_AUTOSAVEONRUN, self.autoSaveOnRun],
#                                   [JESConstants.CONFIG_BACKUPSAVE, self.backupSave],
#                                   [JESConstants.CONFIG_SHOWTURNIN, self.showTurnin],
#                                   [JESConstants.CONFIG_SKIN, self.skin],
#                                   [JESConstants.CONFIG_LOGBUFFER, self.logBuffer.saveBoolean],
#                                   [JESConstants.CONFIG_MEDIAPATH, self.mediaFolder] ])


################################################################################
# Function name: readFromConfigFile
# Parameters: self
# Description: Attempts to open the Configfile.  If it exists, it is opened and
#       read into an array.  Each line of the file will get its spot in the array
#       and newline characters will be removed.  The array is returned.
#       In the case where it doesn't exist, return an array of the right
#       length, with zeroes.
################################################################################
#    def readFromConfigFile(self):
#        try:
#            homedir=os.path.expanduser("~")
#            f=open(homedir+io.File.separator+JESConstants.JES_CONFIG_FILE_NAME,'r')
#            text=f.read()
#            f.close()
#            array=text.splitlines()
#
#            if(len(array) < JESConstants.CONFIG_NLINES):
#                print "you must be upgrading; adding blanks..."
#
#            while (len(array) < JESConstants.CONFIG_NLINES):
#                array += ["0"]
#
#            return array
#        except Exception, e:
#            print type(e)     # the exception instance
#            # print e.args      # arguments stored in .args
#            # print "not failing silently!!"
#            # return ['0'] * JESConstants.CONFIG_NLINES
#            return None
################################################################################

#    def grabSubmissionAddress():
#        return JESConstants.TO_ADDR

#    def grabFontSize(self):
#        try:
#            homedir=os.path.expanduser("~")
#            f=open(homedir+io.File.separator+JESConstants.JES_CONFIG_FILE_NAME,'r')
#            text=f.read()
#            f.close()
#            array=text.splitlines()
#            return string.atoi(array[JESConstants.CONFIG_FONT])
#        except:
#            return JESConstants.FONT_SIZE       

## locally useful util functions.
def getdigits(str):
    out = ""

    for c in str:
        if(c.isdigit()):
            out += c
        else: break
    return out

HELP_FILE_EXTENTION = '.html'
def helpfile_strip(str):
    out = os.path.basename(str)
    out = out.replace(HELP_FILE_EXTENTION, '')
    out = out.replace('_', ' ')
    return out

def helpfile_cmp(str1, str2):
    if str1 == str2: return 0

    str1 = helpfile_strip(str1)
    str2 = helpfile_strip(str2)

    numstr1 = getdigits(str1)
    numstr2 = getdigits(str2)

    if(numstr1 and numstr2):
        return cmp( int(numstr1), int(numstr2) )

    return cmp(str1, str2)
            
if __name__ == '__main__':   
    mainJESProgram = JESProgram()
