#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information
# 5/13/09: Changes for redesigning configuration writing from python to java -Buck

import JESConfig
import JESCommandWindow
import JESConstants
import java.awt as awt
import javax.swing as swing
import javax.swing.text.DefaultStyledDocument as DefaultStyledDocument
import string
import java.lang.System as System
if System.getProperty('os.name').find('Mac') <> -1:
    import colors
else:
    from pawt import colors

FALSE = (-1)

class JESCommandWindowDocument(DefaultStyledDocument):
################################################################################
# Function name: __init__
# Parameters:
#     -command: JESCommandWindow object that this object is associated with
# Return:
#     An instance of the JESCommandWindowDocument class.
# Description:
#     Creates an instance of the JESEditorDocument class.
################################################################################
    def __init__(self, command):
        self.command = command
        self.textAttrib = swing.text.SimpleAttributeSet()
        swing.text.StyleConstants.setFontSize(self.textAttrib, JESConfig.getInstance().getIntegerProperty(JESConfig.CONFIG_FONT))
        swing.text.StyleConstants.setForeground(self.textAttrib, colors.yellow)

################################################################################
# Function name: changeFontSize
#     -fontSize: the font size we want our document to use
# Description:
#
#     This function changes the text in the current command document to reflect
#     the user's font selection. In theory.
################################################################################
    def changeFontSize(self, fontSize):
        newFontSize = int(fontSize)
        swing.text.StyleConstants.setFontSize(self.textAttrib, newFontSize)
        text = DefaultStyledDocument.getText(self, 0, DefaultStyledDocument.getLength(self))
        DefaultStyledDocument.remove(self, 0, DefaultStyledDocument.getLength(self))
        DefaultStyledDocument.insertString(self, 0, text, self.textAttrib)


# some other undocumented functions.

    def addString(self,offset,str):


        if str == '\t':
            str = JESConstants.TAB
            
        if self.command.getIsSystem() != FALSE:
            DefaultStyledDocument.insertString(self,
                                               offset,
                                               str,
                                               self.textAttrib)
            
        else:
            #When insertString is called by Jython, check to make sure the
            #string is to be inserted after the most recent prompt

            
            if self.command.getCaretPosition() >= self.command.getOldPos():

                DefaultStyledDocument.insertString(self,
                                                   offset,
                                                   str,
                                                   self.textAttrib)
            else:
                # if an absent minded user has put the cursor
                # behind the current ">>>" command start point,
                # and he starts typing, we move the cursor to the right
                # place, and insert the text at the end of the text.
                self.command.setCaretPosition( self.getLength() )
                DefaultStyledDocument.insertString(self,
                                                   #offset,
                                                   self.getLength(),
                                                   str,
                                                   self.textAttrib)
            # sort of a hack
            # if a backspace is pressed from the initial cursor position,
            # getCaretPosition becomes less than old position, and the system
            # locks up
            if self.command.getCaretPosition() + 1 == self.command.getOldPos():
                DefaultStyledDocument.insertString(self,
                                                   offset,
                                                   ' ',
                                                   self.textAttrib)
                
                DefaultStyledDocument.insertString(self,
                                                   offset + 1,
                                                   str,
                                                   self.textAttrib)
################################################################################
# Function name: insertString
# Parameters:
#     -offset: offset where the text will be inserted
#     -str: string that is being inserted
#     -a: attribute for the text that is being inserted.
# Description:
#     This function overrides the inherited insertString function.
################################################################################
    def insertString(self, offset, str, a):
        #When insertString is called by methods in JES, there is no need to
        #check the position

    

        
        self.addString(offset,str)
        self.command.commandHistory.setPartialCommand( self.command.getCurrentCommandLine() )
################################################################################
# Function name: remove
# Parameters:
#     -offset: offset of the text that is being removed
#     -len: length of the text that is being removed
# Description:
#     This function overrides the inherited remove function.  
################################################################################
    def remove(self, offset, len):
        #When remove is called by methods in JES, there is no need to check the
        #position
        if self.command.getIsSystem() != FALSE:
            DefaultStyledDocument.remove(self, offset, len)
        else:
            #When remove is called by Jython, check to make sure the string is
            #to be inserted after the most recent prompt
            if self.command.getCaretPosition() >= self.command.getOldPos() + 1:
                DefaultStyledDocument.remove(self, offset, len)

################################################################################
# Function name: getTextAttrib
# Return:
#     -textAttrib: the text attribute set.
# Description:
#     This method returns the document's text attrib variable.
################################################################################
    def getTextAttrib(self):
        return self.textAttrib
       
