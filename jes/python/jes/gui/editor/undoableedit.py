# -*- coding: utf-8 -*-
"""
jes.editor.document
===================
An implementation of AbstractUndoableEdit for the UndoManager.

:copyright: (C) 2008 Buck Scharfnorth
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import javax.swing as swing

INSERT_EVENT = 1
REMOVE_EVENT = 2
MAX_UNDO_EVENTS_TO_RETAIN = 500

class UndoableEdit(swing.undo.AbstractUndoableEdit):

    ######################################################################
    # Function name: __init__
    # Parameters:
    #     -document: the JESEditorDocument object that is being used
    #     -isSignificant: not yet implemented
    #     -eventType: identifies the type of event that occured (insert or remove)
    #     -offset: offset in the text that the event occured in
    #     -str: text that is being inserted or removed
    # Description:
    #     Creates an instance of the UndoableEdit class.
    #     The last 3 parameters are the same as the classic JES addUndoEvent method
    ######################################################################

    def __init__(self, document, isSignificant, eventType, offset, str):
        self.isSignificant = isSignificant
        self.undoEvent = [eventType, offset, str]
        self.document = document

######################################################################
# Function name: undo
# Description:
#     Undoes the last UndoableEdit from the document
######################################################################
    def undo(self):
        try:
            swing.undo.AbstractUndoableEdit.undo(self)
            lastEvent = self.getUndoEvent()
            if lastEvent[0] == INSERT_EVENT:
                self.document.remove(lastEvent[1], len(lastEvent[2]), 0)
            else:
                self.document.insertString(
                    lastEvent[1], lastEvent[2], self.document.textAttrib, 0)
        except Exception, e:
            print "Exception thrown in undo"

######################################################################
# Function name: undo
# Description:
#     Undoes the last UndoableEdit from the document
######################################################################
    def redo(self):
        try:
            swing.undo.AbstractUndoableEdit.redo(self)
            lastEvent = self.getUndoEvent()
            if lastEvent[0] == REMOVE_EVENT:
                self.document.remove(lastEvent[1], len(lastEvent[2]), 0)
            else:
                self.document.insertString(
                    lastEvent[1], lastEvent[2], self.document.textAttrib, 0)
        except Exception, e:
            print "Exception thrown in redo"

######################################################################
# Function name: __init__
# Returns:
#     An UndoEvent based on this UndoableEdit
# Description:
#     Returns this UndoableEdit in the classic JES UndoEvent format
######################################################################
    def getUndoEvent(self):
        return self.undoEvent

