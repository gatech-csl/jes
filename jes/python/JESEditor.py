#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information
#Revisions:
# 5/29/08: added support for "redo" - Buck Scharfnorth
# 5/13/09: Changes for redesigning configuration writing from python to java -Buck

import JESConfig
import JESConstants
import JESEditorDocument
import java.awt as awt
import javax.swing as swing
import java.lang.String as String
import java.lang.Character as Character

class JESEditor(swing.JTextPane,
                swing.event.DocumentListener,
                swing.event.CaretListener,
                awt.event.FocusListener):
################################################################################
# Function name: __init__
# Parameters:
#     -gui: JESUI object that this object is associated with
# Return:
#     An instance of the JESEditor class.
# Description:
#     Creates an instance of the JESEditor class.
################################################################################
    def __init__(self, gui):
        self.gui     = gui
        self.program = gui.program
        self.setContentType("text/plain")
        self.setDocument(JESEditorDocument.JESEditorDocument(self))
        self.addCaretListener(self)
        self.modified = 0
        self.boxX = 0
        self.boxY = 0
        self.boxWidth = 0
        self.boxHeight = 0
        self.addFocusListener(self)


    def focusGained(self, e):
        self.gui.FocusOwner = self

    def focusLost(self, e):
        pass


################################################################################
# Function name: showErrorLine
# Parameters:
#      -lineNumber
# Description:
#     When this function is called, the specified line will be highlighted so
#     that the user can tell which line contains an error.
################################################################################
    def showErrorLine(self, lineNumber):
        self.document.showErrorLine(lineNumber)

################################################################################
# Function name: undo
# Description:
#     This function can be called to undo the last text modification that was
#     performed.
################################################################################
    def undo(self):
        self.document.undo()

################################################################################
# Function name: redo
# Description:
#     This function can be called to redo the last text modification that was
#     performed.
################################################################################
    def redo(self):
        self.document.redo()

################################################################################
# Function name: getScrollableTracksViewportWidth
# Description:
#     Overrides base getScrollableTracksViewportWidth function to disable
#     word-wrapping.
################################################################################
    def getScrollableTracksViewportWidth(self):
        parent = self.getParent()
        ui     = self.getUI()
        return ui.getPreferredSize(self).width <= parent.getSize().width

################################################################################
# Function name: caretUpdate
# Parameters:
#      -e: event object containing infomation about the caret event
# Description:
#     Catches the caretUpdate event for the JESEditorClass.  It then updates
#     the gui status bar with the current row and column.
################################################################################
    def caretUpdate(self, e):
        offset = self.getCaretPosition()
        defaultElement = self.document.getDefaultRootElement()
        elementIndex = defaultElement.getElementIndex(offset)
        row = offset-defaultElement.getElement(elementIndex).getStartOffset()+1
        col = elementIndex + 1
        self.gui.UpdateRowCol(row, col)
        self.checkIfOnKeyword()
        if not JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BLOCK):
            self.updateBox(offset)
            #print str(self.isBlank(offset))
            self.repaint()
        else:
            self.boxX = 0
            self.repaint()


    # see if we can describe the word we are on with the caret
    def checkIfOnKeyword(self):
        offset = self.getCaretPosition()
        currentPosition = offset
        startPosition = 0;
        endPosition = 0;

        if currentPosition > 0 and not Character.isLetter(String(self.getText(currentPosition, 1)).charAt(0)):
            currentPosition -= 1

        while currentPosition > 0 and Character.isLetter(String(self.getText(currentPosition, 1)).charAt(0)):
            currentPosition -= 1

        startPosition = currentPosition
        currentPosition = offset

        while currentPosition < self.document.getLength() and Character.isLetter(String(self.getText(currentPosition, 1)).charAt(0)):
            currentPosition += 1

        endPosition = currentPosition

        keyword = self.getText(startPosition, endPosition-startPosition+1)

        ## the above selects more text than is needed sometimes, so we prune the edges
        if keyword[0] == ' ':
            keyword = keyword[1:]

        if not keyword[len(keyword)-1].isalpha():
            keyword = keyword[:len(keyword)-1]

        self.gui.UpdateToolbarHelp(keyword)




################################################################################
# Function name: removeBox
# Description:
#     Sets the boxX to 0, disabling the box, and repaints the text area
################################################################################
    def removeBox(self):
        self.boxX = 0
        self.repaint()

################################################################################
# Function name: addBox
# Description:
#     Explicitly draws the box without a caretUpdate event.
################################################################################
    def addBox(self):
        offset = self.getCaretPosition()
        defaultElement = self.document.getDefaultRootElement()
        elementIndex = defaultElement.getElementIndex(offset)
        row = offset-defaultElement.getElement(elementIndex).getStartOffset()+1
        col = elementIndex + 1
        self.gui.UpdateRowCol(row, col)
        self.updateBox(offset)
        self.repaint()

################################################################################
# Function name: updateBox
# Parameters:
#     -caretPos: the position of the caret in the document
# Description:
#     Calculates the bounds for the box around the block where the caret is.
#     Iterates up the elements until it finds a line with fewer spaces at the
#     begining and set that as the first line.  Then, it searches down until it
#     finds a line with fewer spaces at the beginning, and sets that as the last
#     line.  Also, as it looks through the lines, it finds the longes one and
#     sets the width to that.
################################################################################
    def updateBox(self, offset):
      try:
        defaultElement = self.document.getDefaultRootElement()
        rowIndex = defaultElement.getElementIndex(offset)
        rowStart = defaultElement.getElement(rowIndex).getStartOffset()
        rowEnd = defaultElement.getElement(rowIndex).getEndOffset() - 1
        indentLevel = self.getNumSpaces(rowStart)
        width = self.modelToView(rowEnd).x
        if ( indentLevel == 0):
            self.boxX = 0
            self.boxY = 0
            self.boxWidth = 0
            self.boxHeight = 0
        else:
            #Get the top row in the same block
            topIndex = rowIndex
            while topIndex > 1:
                if self.getNumSpaces(defaultElement.getElement(topIndex - 1).getStartOffset()) >= indentLevel \
                                     or self.isBlank(defaultElement.getElement(topIndex - 1).getStartOffset()):
                    topIndex = topIndex - 1
                    end = self.modelToView(defaultElement.getElement(topIndex).getEndOffset() - 1).x
                    if end > width:
                        width = end
                else:
                    break
            topStart = defaultElement.getElement(topIndex).getStartOffset()
            rowStart = defaultElement.getElement(rowIndex).getStartOffset()
            topStartWidth = self.modelToView(rowStart + indentLevel)
            topStartCoord = self.modelToView(topStart + indentLevel)

            #Get the bottom row in the same block
            bottomSpaced = 0
            bottomIndex = rowIndex
            bottomLast = bottomIndex
            while bottomIndex < defaultElement.getElementCount() - 1:
                bottomSpaced = self.isBlank(defaultElement.getElement(bottomIndex + 1).getStartOffset())
                if self.getNumSpaces(defaultElement.getElement(bottomIndex + 1).getStartOffset()) >= indentLevel or bottomSpaced:
                    bottomIndex = bottomIndex + 1
                    end = self.modelToView(defaultElement.getElement(bottomIndex).getEndOffset() - 1).x
                    if bottomSpaced == 0:
                        bottomLast = bottomIndex
                    if end > width:
                        width = end
                else:
                    break
            bottomStart = defaultElement.getElement(bottomLast).getStartOffset()
            bottomStartCoord = self.modelToView(bottomStart + indentLevel)

            #Set Coordinates
            self.boxX = topStartWidth.x - 1
            self.boxY = topStartCoord.y
            self.boxHeight = bottomStartCoord.y + bottomStartCoord.height - topStartCoord.y
            self.boxWidth = width - topStartCoord.x + 15

      except Exception, e:
          pass

################################################################################
# Function name: getNumSpaces
# Parameters:
#     -offset: an index on the line to get the number of spaces on
# Description:
#     Returns the number of spaces on the beginning of a line.
################################################################################
    def getNumSpaces(self, offset):
        defaultElement = self.document.getDefaultRootElement()
        rowIndex = defaultElement.getElementIndex(offset)
        rowStart = defaultElement.getElement(rowIndex).getStartOffset()
        rowEnd = defaultElement.getElement(rowIndex).getEndOffset() - 1
        rowText = self.getText(rowStart, rowEnd - rowStart)#.expandtabs()
        newRowText = rowText.lstrip()
        return (len(rowText) - len(newRowText))

################################################################################
# Function name: isBlank
# Parameters:
#     -offset: an index on the line to determine "blankness" or "blankitude"
# Description:
#     Determines if a line is blank, or just has spaces on it.  Returns 1 if
#     the line is blank, and 0 if it has text on it.
################################################################################
    def isBlank(self, offset):
        try:
            defaultElement = self.document.getDefaultRootElement()
            rowIndex = defaultElement.getElementIndex(offset)
            rowStart = defaultElement.getElement(rowIndex).getStartOffset()
            rowEnd = defaultElement.getElement(rowIndex).getEndOffset()
            #print "Start: " + str(rowStart) + "   End: " + str(rowEnd)
            text = self.document.getText(rowStart, rowEnd - rowStart)
            for char in text:
                if char != " " and char != "\n":
                    return 0
            return 1
        except Exception, e:
            return 0

################################################################################
# Function name: setText
# Parameters:
#      -text: text that is being put into the editor
# Description:
#     Overrides the default setText function of the JTextPane.  It resets the
#     modified flag to false, so that the user is not prompted to save on load
#     (unless they make a modification to the file).
################################################################################
    def setText(self, text):
        self.modified = 0
        self.gui.loadButton.enabled = 0
        self.document.undoEvents = []
        swing.JTextPane.setText(self, text)
        self.setCaretPosition(0)

################################################################################
# Function name: paint
# Parameters:
#      -g: the graphics object that will be drawn
# Description:
#     Overrides the Java paint() method to support drawing boxes around the
#     block of code.
################################################################################
    def paint(self, g):
        self.super__paint(g)
        if self.boxX != 0:
            g.setColor(awt.Color(200, 200, 250))
            g.drawRect(self.boxX, self.boxY, self.boxWidth, self.boxHeight)



