#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information
#Revisions:
# 5/14/03: added removeErrorHighlighting() to be called before any changes take
#	   place in the text - AdamW
# 5/15/03: added call to removeErrorHighlighting before setting error highlighting
#	   to prevent multiple highlightings which can't be undone. -AdamW
# 5/15/03: added comment and string highlighting. - AdamW
# 5/29/08: added support for "redo" - Buck Scharfnorth
# 5/13/09: Changes for redesigning configuration writing from python to java -Buck

import JESConfig
import JESConstants
import JESUndoableEdit
import java.awt as awt
import javax.swing as swing
import HighlightingStyledDocument as HighlightingStyledDocument
import keyword
import string
import java.lang.System as System

WORD_BREAKS = [' ', '\n', '\t', '[', ']', '{', '}', ',', '\'', '-', '+', '=',
               '<', '>',  ':', ';', '_', '(', ')', '.',  '#', '"', '%' ]
KEYWORD_BOLD = 1
INVALID_PAREN_BOLD = 1
INSERT_EVENT = 1
REMOVE_EVENT = 2
MAX_UNDO_EVENTS_TO_RETAIN = 500

ERROR_LINE_FONT_COLOR       = awt.Color.black
ERROR_LINE_BACKGROUND_COLOR = awt.Color.yellow
HIGHLIGHT_LINE_FONT_COLOR       = awt.Color.black
HIGHLIGHT_LINE_BACKGROUND_COLOR = awt.Color.green

class JESEditorDocument(HighlightingStyledDocument):
################################################################################
# Function name: __init__
# Parameters:
#     -editor: JESEditor object that this object is associated with
# Return:
#     An instance of the JESEditorDocument class.
# Description:
#     Creates an instance of the JESEditorDocument class.
################################################################################
    def __init__(self, editor):
        self.editor = editor
        self.textAttrib = swing.text.SimpleAttributeSet()
        self.keywordAttrib = swing.text.SimpleAttributeSet()
        self.jesEnvironmentWordAttrib = swing.text.SimpleAttributeSet()
        self.errorLineAttrib = swing.text.SimpleAttributeSet()
        self.highlightLineAttrib = swing.text.SimpleAttributeSet()
        self.commentAttrib = swing.text.SimpleAttributeSet()
        self.stringAttrib = swing.text.SimpleAttributeSet()
        self.lParenAttrib = swing.text.SimpleAttributeSet()
        self.rParenAttrib = swing.text.SimpleAttributeSet()
        self.needToSetEnvironment = 1
        self.fontSize = JESConfig.getInstance().getIntegerProperty( JESConfig.CONFIG_FONT )

        swing.text.StyleConstants.setForeground(self.stringAttrib, JESConstants.STRING_COLOR)
        swing.text.StyleConstants.setFontFamily(self.stringAttrib, "Monospaced");

        swing.text.StyleConstants.setForeground(self.commentAttrib, JESConstants.COMMENT_COLOR)
        swing.text.StyleConstants.setFontFamily(self.commentAttrib, "Monospaced");

        swing.text.StyleConstants.setForeground(self.jesEnvironmentWordAttrib, JESConstants.ENVIRONMENT_WORD_COLOR)
        swing.text.StyleConstants.setBold(self.jesEnvironmentWordAttrib, KEYWORD_BOLD)
        swing.text.StyleConstants.setFontSize(self.jesEnvironmentWordAttrib, self.fontSize)
        swing.text.StyleConstants.setFontSize(self.textAttrib, self.fontSize)
        swing.text.StyleConstants.setBackground(self.textAttrib, awt.Color.white)
        swing.text.StyleConstants.setFontFamily(self.jesEnvironmentWordAttrib, "Monospaced");
        swing.text.StyleConstants.setFontFamily(self.textAttrib, "Monospaced");

        swing.text.StyleConstants.setForeground(self.keywordAttrib, JESConstants.KEYWORD_COLOR)
        swing.text.StyleConstants.setBold(self.keywordAttrib, KEYWORD_BOLD)
        swing.text.StyleConstants.setFontSize(self.keywordAttrib, self.fontSize)
        swing.text.StyleConstants.setFontFamily(self.keywordAttrib, "Monospaced");

        swing.text.StyleConstants.setForeground(self.lParenAttrib, JESConstants.LPAREN_COLOR)
        swing.text.StyleConstants.setBold(self.lParenAttrib, INVALID_PAREN_BOLD)
        swing.text.StyleConstants.setFontSize(self.lParenAttrib, self.fontSize)
        swing.text.StyleConstants.setFontFamily(self.lParenAttrib, "Monospaced");

        swing.text.StyleConstants.setForeground(self.rParenAttrib, JESConstants.RPAREN_COLOR)
        swing.text.StyleConstants.setBold(self.rParenAttrib, INVALID_PAREN_BOLD)
        swing.text.StyleConstants.setFontSize(self.rParenAttrib, self.fontSize)
        swing.text.StyleConstants.setFontFamily(self.rParenAttrib, "Monospaced");

        swing.text.StyleConstants.setForeground(self.errorLineAttrib, ERROR_LINE_FONT_COLOR)
        swing.text.StyleConstants.setBackground(self.errorLineAttrib, ERROR_LINE_BACKGROUND_COLOR)
        swing.text.StyleConstants.setFontFamily(self.errorLineAttrib, "Monospaced")

        swing.text.StyleConstants.setForeground(self.highlightLineAttrib, HIGHLIGHT_LINE_FONT_COLOR)
        swing.text.StyleConstants.setBackground(self.highlightLineAttrib, HIGHLIGHT_LINE_BACKGROUND_COLOR)
        swing.text.StyleConstants.setFontFamily(self.highlightLineAttrib, "Monospaced")


        #self.undoEvents = []

        #Sets up the UndoManager which handles all undos/redos
        self.undoManager = swing.undo.UndoManager()
        self.undoManager.setLimit(MAX_UNDO_EVENTS_TO_RETAIN)

        HighlightingStyledDocument.setKeywordStyle(self, self.keywordAttrib)
        HighlightingStyledDocument.setEnvironmentWordStyle(self, self.jesEnvironmentWordAttrib)
        HighlightingStyledDocument.setStringStyle(self, self.stringAttrib)
        HighlightingStyledDocument.setLParenStyle(self, self.lParenAttrib)
        HighlightingStyledDocument.setRParenStyle(self, self.rParenAttrib)
        HighlightingStyledDocument.setCommentStyle(self, self.commentAttrib)
        HighlightingStyledDocument.setDefaultStyle(self, self.textAttrib)


        #The following variables are set when showErrorLine is called.  They
        #are then used to unhighlight the line when the next text modification
        #is made.
        self.errorLineStart = -1
        self.errorLineLen   = -1
        self.highlightLineStart = -1
        self.highlightLineLen = -1

################################################################################
# Function name: changeFontSize
# 		-fontSize: the font size we want our document to use
# Description:
#
#			This function changes the text in the current editor document to reflect
#			the user's font selection. In theory.
################################################################################
    def changeFontSize(self, fontSize):
        newFontSize = int(fontSize)
        swing.text.StyleConstants.setFontSize(self.errorLineAttrib, newFontSize)
        swing.text.StyleConstants.setFontSize(self.commentAttrib, newFontSize)
        swing.text.StyleConstants.setFontSize(self.stringAttrib, newFontSize)
        swing.text.StyleConstants.setFontSize(self.textAttrib, newFontSize)
        swing.text.StyleConstants.setFontSize(self.jesEnvironmentWordAttrib, newFontSize)
        swing.text.StyleConstants.setFontSize(self.rParenAttrib, newFontSize)
        swing.text.StyleConstants.setFontSize(self.lParenAttrib, newFontSize);
        swing.text.StyleConstants.setFontSize(self.keywordAttrib, newFontSize)
        HighlightingStyledDocument.updateHighlightingInRange(self, 0, HighlightingStyledDocument.getLength(self))
        self.editor.gui.gutter.repaint()

################################################################################
# Function name: insertString
# Parameters:
#     -offset: offset where the text will be inserted
#     -str: string that is being inserted
#     -a: attribute for the text that is being innserted.
# Description:
#     This function overrides the inherited insertString function.  It inserts
#     the target text and then calls the keywordHighlightEvent function to
#     highlight keywords.
################################################################################
    def insertString(self, offset, str, a, addUndoEvent=1):
        if self.needToSetEnvironment:
            #Give the environment and key words to the Highlighting Document
            HighlightingStyledDocument.setEnvironmentWords(self, self.editor.program.getVarsToHighlight().keys())
            HighlightingStyledDocument.setKeywords(self, keyword.kwlist)
            self.needToSetEnvironment = 0
        if self.errorLineStart >= 0:
	    self.removeErrorHighlighting()
        if self.highlightLineStart >= 0:
            self.removeLineHighlighting()
        if str == '\t':
            str = JESConstants.TAB
	#Added to make auto indent work
	if str == '\n':
	    defaultElement = self.getDefaultRootElement()
	    rowIndex = defaultElement.getElementIndex(offset)
	    rowStart = defaultElement.getElement(rowIndex).getStartOffset()
	    rowEnd = defaultElement.getElement(rowIndex).getEndOffset() - 1
	    rowText = self.getText(rowStart, rowEnd - rowStart)#.expandtabs()
	    newRowText = rowText.lstrip()
	    numSpaces = (len(rowText) - len(newRowText))
	    str = "\n" + (" " * numSpaces)
        self.editor.modified = 1
        self.editor.gui.loadButton.enabled = 1
        if addUndoEvent:
            self.addUndoEvent(INSERT_EVENT,
                              offset,
                              str)
        HighlightingStyledDocument.insertString(self, offset, str, self.textAttrib)


################################################################################
# Function name: remove
# Parameters:
#     -offset: offset of the text that is being removed
#     -len: length of the text that is being removed
# Description:
#     This function overrides the inherited remove function.  It removes the
#     target text and then calls the keywordHighlightEvent function to highlight
#     keywords.
################################################################################
    def remove(self, offset, len, addUndoEvent=1):
	if self.errorLineStart >= 0:
	    self.removeErrorHighlighting()
        if self.highlightLineStart >= 0:
	    self.removeLineHighlighting()
        self.editor.modified = 1
        self.editor.gui.loadButton.enabled = 1
        if addUndoEvent:
            self.addUndoEvent(REMOVE_EVENT,
                              offset,
                              self.getText(offset, len))
        HighlightingStyledDocument.remove(self, offset, len)


################################################################################
# Function name: removeErrorHighlighting
# Description:
#     This funciton will remove any error highlighting set between
#     errorLineStart and errorLineLen.
################################################################################
    def removeErrorHighlighting(self):
	#Unhighlight a line if showErrorLine was called earlier
        if self.errorLineStart >= 0:
            HighlightingStyledDocument.updateHighlightingInRange(self, self.errorLineStart,
                                               self.errorLineLen)
            self.errorLineStart = -1
            self.errorLineLen   = -1

    def removeLineHighlighting(self):
	#Unhighlight a line if showHighlightLine was called earlier
        self.editor.gui.gutter.removeLineMark()
        self.editor.gui.gutter.repaint()
        #if self.highlightLineStart >= 0:
            #self.
            #HighlightingStyledDocument.updateHighlightingInRange(self, self.highlightLineStart,
                                                    #self.highlightLineLen)

            #self.highlightLineStart = -1
            #self.highlightLineLen   = -1



    def isJESEnvironmentWord(self,text):

        varsToHighlight = self.editor.program.getVarsToHighlight()

        if varsToHighlight.has_key(text):

            return not None

        return None

################################################################################
# Function name: addUndoEvent
# Parameters:
#     -eventType: identifies the type of event that occured (insert or remove)
#     -offset: offset in the text that the event occured in
#     -str: text that is being inserted or removed
# Description:
#     Adds an undo event to the event array.  This is needed so that text
#     modification events can be undone.  If the array reaches it's maximum
#     capacity, then the oldest event is removed from the array before adding
#     the new one.  Also triggers tells the JES gui that its contents have
#     changed
# Revisions:
#     Modified to use an UpdateManager instead of event array,
#     making "redo" possible. - 29 May 2008 Buck Scharfnorth
################################################################################
    def addUndoEvent(self, eventType, offset, str):
	self.editor.gui.editorChanged()
	self.undoManager.addEdit( JESUndoableEdit.JESUndoableEdit(self, 1, eventType, offset, str) )
        #if len(self.undoEvents) > MAX_UNDO_EVENTS_TO_RETAIN:
        #    del self.undoEvents[0]

        #self.undoEvents.append([eventType,
        #                        offset,
        #                        str])

################################################################################
# Function name: undo
# Description:
#     Undoes the last text modification that is in the undo events array and
#     removes it from the array.
################################################################################
    def undo(self):
        self.editor.gui.editorChanged()
        #if len(self.undoEvents) > 0:
            #lastEvent = self.undoEvents.pop()
            #if lastEvent[0] == INSERT_EVENT:
            #    self.remove(lastEvent[1],
            #                len(lastEvent[2]),
            #                0)
            #else:
            #    self.insertString(lastEvent[1],
            #                      lastEvent[2],
            #                      self.textAttrib,
            #                      0)
        if self.undoManager.canUndo():
            self.undoManager.undo()

################################################################################
# Function name: redo
# Description:
#     Redoes the last text modification that is in the UndoManager
################################################################################
    def redo(self):
        self.editor.gui.editorChanged()
        if self.undoManager.canRedo():
            self.undoManager.redo()

################################################################################
# Function name: showErrorLine
# Parameters:
#      -lineNumber: number of the line that should be highlighted
# Description:
#     When this function is called, the specified line will be highlighted so
#     that the user can tell which line contains an error.
################################################################################
    def showErrorLine(self, lineNumber):

	#remove any old error highlighting, because we only want to show one error
	# at a time.  Plus, the system only keeps track of one error, so we need to
	# unhighlight the old error before setting the new one (AW 5/15/03)
	if self.errorLineStart >= 0:
	    self.removeErrorHighlighting()

        #Search for the start offset of the error line
        docText = self.getText(0, self.getLength())

        line   = 1
        offset = 0

        while line < lineNumber:
            offset = docText.find('\n', offset) + 1
            line += 1

        #Search for the end offset of the error line
        #offset += 1
        endOffset = docText.find('\n', offset)

        if endOffset == -1:
            endOffset = len(docText)

        #Set error line position and length object variables
        self.errorLineStart = offset
        self.errorLineLen   = endOffset - offset

        #Set the correct text attribute for the error line
        HighlightingStyledDocument.setCharacterAttributes(self, self.errorLineStart,
                                    self.errorLineLen,
                                    self.errorLineAttrib,
                                    1)

        #Set cusor to error line to ensure that the error line will be visible
        self.editor.setCaretPosition(self.errorLineStart)

################################################################################
# Function name: highlightLine
# Parameters:
#      -lineNumber: number of the line that should be highlighted
# Description:
#     When this function is called, the specified line will be highlighted so
#     that the user can tell which line is currently running
################################################################################
    def highlightLine(self, lineNumber):
	#self.removeLineHighlighting()
        defaultElement = self.getDefaultRootElement()
        element = defaultElement.getElement(lineNumber)

        self.highlightLineStart = element.getStartOffset()
        #self.highlightLineLen   = element.getEndOffset() - self.highlightLineStart

        self.editor.gui.gutter.setLineMark(lineNumber)
        #HighlightingStyledDocument.setCharacterAttributes(self, self.highlightLineStart,
        #                            self.highlightLineLen,
        #                            self.highlightLineAttrib,
        #                            1)
        #Set cusor to error line to ensure that the error line will be visible
        try:
            self.editor.setCaretPosition(self.highlightLineStart)
        except:
            pass #Sometime, Java can't keep up.
        self.editor.gui.gutter.repaint()
################################################################################
# Function name: gotoLine
# Parameters:
#      -lineNumber: number of the line that should be highlighted
# Description:
#     When this function is called, the specified line will be highlighted so
#     that the user can tell which line contains an error.
################################################################################
    def gotoLine(self, lineNumber):
        #Search for the start offset of the error line
        docText = self.getText(0, self.getLength())

        line   = 1
        offset = 0

        while line < lineNumber:
            offset = docText.find('\n', offset) + 1
            line += 1

        #Search for the end offset of the target line
        #offset += 1
        endOffset = docText.find('\n', offset)

        if endOffset == -1:
            endOffset = len(docText)

        #Set target line position and length object variables
        self.targetLineStart = offset
        self.targetLineLen   = endOffset - offset

        #Set cusor to target line to ensure that the error line will be visible
        self.editor.setCaretPosition(self.targetLineStart)

    def searchForward(self,toFind):
        try:
            offset = self.editor.getCaretPosition()
            text=self.getText(offset,self.getLength()-offset)
            location=text.find(toFind)
            if location != -1:
                #Highlight Text
                self.setCharacterAttributes(0,
                                        self.getLength(),
                                        self.textAttrib,
                                        0)
                self.setCharacterAttributes(location+offset,
                                        len(toFind),
                                        self.errorLineAttrib,
                                        0)
                self.editor.setCaretPosition(location+offset+len(toFind))
            else:
                if self.editor.getCaretPosition()>1:
                    self.editor.setCaretPosition(1)
                    self.searchForward(toFind)
        except:
            print "Exception thrown in searchForward"
            import sys
            a,b,c=sys.exc_info()
            print a,b,c

    def searchBackward(self,toFind):
        try:
            offset = self.editor.getCaretPosition()
            text=self.getText(0,offset)
            location=text.rfind(toFind)
            if location != -1:
                #Unhighlight Text
                self.setCharacterAttributes(0,
                                        self.getLength(),
                                        self.textAttrib,
                                        0)
                #Highlight Text
                self.setCharacterAttributes(location,
                                        len(toFind),
                                        self.errorLineAttrib,
                                        0)
                self.editor.setCaretPosition(location)
            else:
                if self.editor.getCaretPosition()<self.getLength():
                    self.editor.setCaretPosition(self.getLength())
                    self.searchBackward(toFind)
        except:
            import sys
            a,b,c=sys.exc_info()
            print a,b,c
            print "Exception thrown in searchBackward"
