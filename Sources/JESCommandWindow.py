#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information
#Revisions:
# 5/29/08: Added support for Redo - Buck Scharfnorth
# 5/14/09: Made input and raw_input work through the console

import JESConstants
import JESCommandWindowDocument
import JESCommandHistory

#Dorn: for input and raw_input
from JESInputManager import JESInputManager

import string
import sys
import re
import java.awt as awt
import java.awt.Toolkit as Toolkit
import java.awt.datatransfer.Clipboard as Clipboard
import java.awt.datatransfer.Transferable as Transferable
import java.awt.datatransfer.DataFlavor as DataFlavor
import javax.swing.text.JTextComponent as JTextComponent
import javax.swing as swing
from JESAction import JESAction


from org.python.core import PyString

#from pawt import colors, swing
import java.lang.System as System
if System.getProperty('os.name').find('Mac') <> -1:
    import colors
else:
    from pawt import colors

#from pawt.swing import KeyStroke, text
import javax.swing.KeyStroke as KeyStroke

import string

ELLIPSIS_SPACE = '... '
ELLIPSIS = '...'
FALSE = (-1)
TRUE = 1
class JESCommandWindow(swing.JTextPane,
                       awt.event.FocusListener):

################################################################################
# Function name: __init__
# Parameters:
#     -gui: A reference to the parent JESUI class
# Return:
#     A new instance of the JESCommandWindow class
# Description:
#     Creates a new instance of JESCommandWindow
################################################################################
    def __init__(self, gui):
        self.program = gui.program
        self.gui = gui

	# 5/14/09 Dorn:  added these lines to allow the input manager to 
	# communicated with the command window to read for input and raw_input
	self.inputManager = JESInputManager()
	self.inputManager.setCommandWindow(self)

        self.inMultiLineCommand = None
        self.setDocument(JESCommandWindowDocument.JESCommandWindowDocument(self))
        self.document = self.getDocument()
        self.setCharacterAttributes(self.document.getTextAttrib(), TRUE)
        self.setBackground(colors.black)
        self.setForeground(colors.white)
        self.setCaretColor(colors.white)
        self.setCaretPosition(0)

        parentKeymap = self.getKeymap()
        commandKeymap = self.addKeymap("commandKeymap", parentKeymap)
        commandKeymap.addActionForKeyStroke(KeyStroke.getKeyStroke('\n'),
                                            makeAction(self.enter))

        commandKeymap.addActionForKeyStroke(KeyStroke.getKeyStroke('UP'),makeAction(self.up))
        commandKeymap.addActionForKeyStroke(KeyStroke.getKeyStroke('DOWN'),makeAction(self.down))

        self.setKeymap(commandKeymap)

        #This is a flag for JESCommandWindowDocument's insertString method.  It
        #indicates whether or not JES made the method call.

        self.currentPos = self.document.getLength()
        self.oldPos = self.currentPos
        #Text cleared with undo (used for redo)
        self.oldText = ''

        self.my_keymap = commandKeymap

        #Initialize command.  Command holds the line or lines of commands
        #entered by the user that will be sent to the interpreter
        self.command = ""

        #initialize heldText.  heldText holds the last text to be copied or cut.
        self.heldText = ""

        self.commandHistory = JESCommandHistory.JESCommandHistory()
        self.isSystem = TRUE
        self.setText(">>> ")
        self.isSystem = FALSE
        self.currentPos = self.document.getLength()
        self.oldPos = self.currentPos
        self.addFocusListener(self)

    def focusGained(self, e):
        self.gui.FocusOwner = self

    def focusLost(self, e):
        pass

################################################################################
# Function name: getCommandText
# Return:
#     -commandText: a string containing commands for the interpreter
# Description:
#     This function gets all the text in the command window in between the old
#     cursor position and the new cursor position.
################################################################################
    def getCommandText(self):
        self.currentPos = self.document.getLength()
        command = self.document.getText(self.oldPos,
                                        self.currentPos - self.oldPos)
        self.oldPos = self.currentPos
        return commandText

################################################################################
# Function name: showText
# Parameters:
#     -text: output message to display
# Description:
#     This function displays the text as output from the interpreter.
################################################################################
    def showText(self, text):
        self.isSystem = TRUE
        self.document.insertString(self.document.getLength(),
                                   text,
                                   self.document.getTextAttrib())
        self.isSystem = FALSE
        self.oldPos = self.currentPos
        self.currentPos = self.document.getLength()

################################################################################
# Function name: showError
# Parameters:
#     -text: error message to display
# Description:
#     This method displays the text as an error thrown from the interpreter.
################################################################################
    def showError(self, text):
        self.isSystem = TRUE
        self.document.insertString(self.currentPos,
                                   text,
                                   self.document.getTextAttrib())
        self.isSystem = FALSE
        self.oldPos = self.currentPos
        self.currentPos = self.document.getLength()

################################################################################
# Function name: enter
# Description:
#     checks to make sure that the enter key was pressed after the last command prompt.  If so, calls
#     enterHelper().  If not, nothing happens.
#
################################################################################
    def enter(self):
        self.setCaretPosition(self.document.getLength() )
        enteredTextPos = self.getCaretPosition()
        #enteredTextPos = self.document.getLength()

        line = self.document.getText(self.oldPos,
                                     self.document.getLength() - self.oldPos)

        line = string.join(string.split(line,'\n'),'')
        line += '\n'
        self.document.remove(self.oldPos,
                             self.document.getLength() - self.oldPos)
        self.document.addString(self.oldPos,line)

        if enteredTextPos >= self.oldPos:
            self.enterHelper()



    def up(self):

        line = self.commandHistory.moveUp()
        if not line is None:
            self.changeCurrentCommand(line)

    def down(self):

        line = self.commandHistory.moveDown()
        if not line is None:
            self.changeCurrentCommand(line)

    def changeCurrentCommand(self,line):

        lineLength = len(line)
        if lineLength != 0:
            if ( line[lineLength - 1] == '\n') or (line[lineLength -1] == '\r'):
                line = line[:lineLength -1]

        # DNR - TODO - 10.22.02
        # need to figure out how to add text
        length = self.document.getLength()





        self.document.remove(self.oldPos, (length - self.oldPos))

        if self.inMultiLineCommand:
            line = ELLIPSIS_SPACE + line

        self.document.addString(self.oldPos,line)

##     def stripOutEllipsis(self,line):
##         list = string.
##         str = [None]*len(line):
##             for i in line:
##                 str[i] = i
##             str = "".join(str)
##         return str


################################################################################
# Name: getCurrentCommandLine
#
# returns the line of text that the user has typed since last hitting enter
#
###############################################################################
    def getCurrentCommandLine(self):


        currentCommandLine = ''
        currentPos = self.document.getLength()
        line = self.document.getText(self.oldPos,
                                     currentPos - self.oldPos)

        offset = 0
        count = 0
        for char in ELLIPSIS_SPACE:

            if (not offset > len(line) - 1) and (char == line[offset]):
                count += 1
            offset += 1
        if count == 4:
            line = line[3:]

        return line


################################################################################
# Function name: enterHelper
# Description:
#     This method listens for the enter key to be pressed, and compiles a string
#     to send to the interpreter that is either single line or multiline.
#
#
# 10.23.02 - DNR - last line of enterHelper puts commands into a command history
# 10.24.02 - DNR - The test to see if the line has an ellipsis is not correct
#                  Assumes that ANY ellipsis has been inserted by the command
#                  window.  But the user could easily insert the '...' as a
#                  string literal.  ie:
#                  >>> print 'hello ... world'
#                  Now we say that the ellipsis HAS to appear at the beginning
#                  of a line
# 10.24.02 - DNR - a similar problem with the colon.  the old version
#                  assumed that every colon was the same as having
#                  a colon at the end of a line
# 10.25.02 - DNR - TODO - JES still dosen't properly handle lines that end in
#                  "\".  In python, these signal single line commands that are
#                  very long and wrap across multiple lines
###############################################################################

    def enterHelper(self):
        self.currentPos = self.document.getLength()
        self.oldText = ''
        line = self.document.getText(self.oldPos,
                                     self.currentPos - self.oldPos)

        #line = string.join(string.split(line,'\n'),'')

	#5/14/09 Dorn: Before doing anything check to see if this is input
	#needed for raw_input or input.  If so, we'll send the value to the
	#inputManager and return early.  This must also be threadsafe
	if self.inputManager.isWaiting():
		#remove the \n from the end of the string
		line = string.join(string.split(line,'\n'),'')

		#disable keyboard again and send the value back
		self.setKeymap(None);
		self.inputManager.setReturnValue(line)
		self.inputManager.setWaiting(False)
		return


        # DNR - boolean, does the line end in a colon
        #colon = string.rfind(line, ':')
        endsWithColon = self.doesLineEndWithColon(line)

        # DNR - boolean, does line begin with
        #ellipsis = string.find(line, ELLIPSIS)#  - removed DNR 10.24.02
        beginsWithEllipsis = self.doesLineBeginWithEllipsis(line) # added DNR 10.24.02

        #first check to see if the line ends with a colon
        if endsWithColon:
            self.inMultiLineCommand = not None
            #then check for an ellipsis at the  beginning of the line
            if beginsWithEllipsis:

                self.showText(ELLIPSIS_SPACE)

                # DNR remove ellipsis from beginning
                textToAdd = self.removeEllipsisFromBeginning(line)
                self.command += textToAdd

                self.commandHistory.push( textToAdd)
            else:


                self.showText(ELLIPSIS_SPACE)

                # DNR remove '>>>" from the end
                # DNR 10.24.02 - Is this necessary, the line dosen't
                # seem to have a prompt

                self.command = self.removePromptFromEnd(line)
                self.commandHistory.push( self.command )

        #if there is no colon:
        else:

            #check to see if the line begins with an ellipsis
            if beginsWithEllipsis:

                # DNR remove beginning ellipsis
                newLineCheck = self.removeEllipsisFromBeginning(line)
                #Check to see if it's just a newline, signifying the end of a
                #multiline sequence
                if newLineCheck == '\n':
                    self.runCommand()
                    self.inMultiLineCommand = None

                else:

                    self.showText(ELLIPSIS_SPACE)

                    # DNR -adds a single space to the end of the line
                    textToAdd = '' + newLineCheck

                    self.command += textToAdd
                    self.commandHistory.push(textToAdd)
            #if there's no colon or ellipsis, it's a single line command
            else:
##                 removePrompt = string.split(line, '>>>')
##                 self.command = removePrompt[0]

                self.command = self.removePromptFromEnd(line)
                self.commandHistory.push(self.command)
                self.runCommand()


##         print >> sys.stderr, "JESCommandWindow:enterHelper:commandLine: |%s|" % \
##               self.getCurrentCommandLine()

##         self.commandHistory.push(self.removeEllipsisFromEnd( self.getCurrentCommandLine()) )

        # DNR - TODO - add commandHistory.append(self.command) here 10.22.02




    def doesLineEndWithColon(self,line):
        return re.search('[.]*[\s]*:[\s]*\n$',line)
    def doesLineBeginWithEllipsis(self,line):
        return  re.search('^[\.][\.][\.][.]*',line)

    def removeEllipsisFromEnd(self,line):
        match = re.search('[.][.][.][ ]$',line)

        if match is None:
            return line

        if match.start() == -1:
            return line
        return line[ :match.start()]
    def removeEllipsisFromBeginning(self,line):
        match = re.search('^[.][.][.][ ]',line)
        if match is None:
            return line

        if match.end() == -1:
            return line
        return line[ match.end():]

    def removePromptFromEnd(self,line):
        match = re.search('>>>$',line)
        if match is None:
            return line

        if match.start() == -1:
            return line
        return line[ :match.start()]

    def doesLineEndWithNewLine(self,line):
        match = re.search('\n$',line)
        return match
################################################################################
# Function name: runCommand
# Description:
#     calls JESProgram.runCommand with the code entered by the user
#
################################################################################
    def runCommand(self):


        self.program.runCommand(self.command)

################################################################################
# Function name: restoreConsole
# Description:
#	Gathers the output of the interpreter and redraws the command window.
#
################################################################################
    def restoreConsole(self,mode):
        self.command = ""
        responseText = self.program.getTextForCommandWindow()

        #if responseText == '':
        #    self.showText( responseText)
        #    self.showText(">>> ")
        #    self.currentPos = self.document.getLength()
        #    self.setCaretPosition( self.currentPos )
        #    self.oldPos = self.currentPos
        if mode == "run":
            if responseText == '':
                self.showText(">>> ")
            else:
                self.showText( responseText)
                self.showText(">>> ")

            self.oldPos = self.document.getLength()
	#5/14/09 Dorn: added in a condition for LOAD since we added a notice of load on the console
	elif mode == "load":     
	    self.showText(">>> ")
	    self.oldPos = self.document.getLength()
        else:
            pass
        self.currentPos = self.document.getLength()
        self.setCaretPosition( self.currentPos )
        self.setKeymap(self.my_keymap)
        self.commandHistory.setPartialCommand('')




    def printNowUpdate(self,text):
        if not text == '':
            self.showText( text )


################################################################################
# Function name: pasteHelper
# Description:
#	Extracts the first line of a multiline command from the string of text
#       on the clipboard.
#
################################################################################
    def pasteHelper(self):
        #import string
        #ugly work to get the text from the clipboard
        toolkit = Toolkit.getDefaultToolkit()
        clipboardContents = toolkit.getSystemClipboard().getContents(self)
        flavor = clipboardContents.getTransferDataFlavors()



        #flavor is an array of types of representations of data
        #we must find a string representation
        i = 0
        j = None
        for a in flavor:
            if clipboardContents.getTransferData(flavor[i]).__class__ == PyString:
                j = i
            i += 1

        if not j is None:
            clipboardText = clipboardContents.getTransferData(flavor[j])
            #split to remove anything after the newline, if it's multiline

            removeNewline = string.split(clipboardText, '\n')
            self.textToPaste = removeNewline[0]
        else:
            self.textToPaste = ''
            print '\a'

################################################################################
# Function name: paste
# Description:
#     This function overrides JESUI's paste function and performs the paste
#     operation.  If the cursor (or selection) is located after the prompt (and
#     the line of text has not yet been sent to the interpreter), paste.  If
#     the cursor (or selection) is located before the prompt, the paste function
#     does nothing (because anything before the most recent prompt is
#     uneditable).
################################################################################
    def paste(self):
        selection = self.getSelectedText()

        if selection == None:

           insertPoint = self.getCaretPosition()

           #check if cursor is after the last prompt
           if insertPoint >= self.oldPos:
               self.pasteHelper()
               #paste
               self.document.insertString(insertPoint,
                                          self.textToPaste,
                                          self.document.getTextAttrib())

           #if not, append text to the end of the text pane
           else:
               self.setCaretPosition(self.document.getLength())
               self.pasteHelper()
               #paste
               self.document.insertString(self.document.getLength(),
                                          self.textToPaste,
                                          self.document.getTextAttrib())

        else:
            start = self.getSelectionStart()

            #check to see if selection is after the last prompt
            if start >= self.oldPos:
                self.pasteHelper()
                #paste
                self.replaceSelection(self.textToPaste)

            #if not, append text to the end of the text pane
            else:
                self.setCaretPosition(self.document.getLength())
                self.pasteHelper()
                #paste
                self.document.insertString(self.document.getLength(),
                                           self.textToPaste,
                                           self.document.getTextAttrib())


################################################################################
# Function name: cut
# Description:
#     This function overrides JESUI's cut function and performs the cut
#     operation.  If the text is located after the prompt (and has not yet been
#     sent to the interpreter), it can be cut.  Otherwise, the cut function
#     does nothing (because anything before the most recent prompt is
#     uneditable).
################################################################################
    def cut(self):
        start = self.getSelectionStart()
        if start >= self.oldPos:
            JTextComponent.cut(self)
        else:
            JTextComponent.copy(self)

################################################################################
# Function name: undo
# Description:
#     This function overrides JESUI's undo function and performs the undo
#     operation.  This function removes all text entered since that most recent
#     prompt and has not been sent to the interpreter.
################################################################################
    def undo(self):
        length = self.document.getLength()
        #only undo if there is something to remove
        if length - self.oldPos > 0:
            self.oldText = self.document.getText(self.oldPos, (length-self.oldPos))
            self.document.remove(self.oldPos, (length-self.oldPos))

################################################################################
# Function name: redo
# Description:
#     This function overrides JESUI's redo function and performs the redo
#     operation.  This function reinserts all text entered since that most recent
#     prompt after it has been undone.
################################################################################
    def redo(self):
        length = self.document.getLength()
        if length - self.oldPos == 0:
            self.document.insertString(self.currentPos, self.oldText, self.document.textAttrib)
            self.oldText = ''

################################################################################
# Function name: getOldPos
# Return:
#     -oldPos: Returns JESCommandWindow's oldPos variable (which is the
#              location of the most recent prompt)
# Description:
#     This function returns the oldPos variable
################################################################################
    def getOldPos(self):
        return self.oldPos

################################################################################
# Function name: getCurrentPos
# Return:
#     -currentPos: Returns JESCommandWindow's currentPos variable
# Description:
#     This function returns the currentPos variable
################################################################################
    def getCurrentPos(self):
        return self.currentPos

################################################################################
# Function name: getIsSystem
# Return:
#     -isSystem: Returns JESCommandWindow's isSystem variable
# Description:
#     This function returns the isSystem variable
################################################################################
    def getIsSystem(self):
        return self.isSystem

################################################################################
# Function name: makeAction
# Parameters:
#     -obj: an Object to turn into anJESAction
# Return:
#     -obj: either as it entered the function or cast as anJESAction
# Description:
#     This function determines whether or not the object is anJESAction, and
#     casts it as anJESAction if necessary.
################################################################################
def makeAction(obj):
        if isinstance(obj,JESAction): return obj
        if callable(obj): return JESAction(obj)
