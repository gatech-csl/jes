import sys

class JESCommandHistory:

######################################################################
# init
#
# defines the following fields:
#
# commandStack - the structure that holds the commands that have been
#                typed
# position     - stores how far "up" or "down" the user is in the stack
#                tells which commands should be returned by the
#                moveUp / moveDown functions
# partialCommand - the commmand partially typed by the user, recorded
#                  so it will still be available if the user dosen't
#                  want to pull something from the history.
#                  returned with the position falls to -1
#
# the moveUp and moveDown functions are called by the command window
# when the user hits up or down on the keyboard.  
######################################################################
    def __init__(self):
        self.commandStack = ['' ]

        self.position = -1
        self.partialCommand = ''

######################################################################
# push
#
# prepends a new command on to the command stack
# resets the position, and the partial command because we assume that
# command are only pushed after a whole command has been typed
######################################################################
    def push(self,command):
        self.commandStack = [command] + self.commandStack
        self.position = -1
        self.setPartialCommand('')


######################################################################
# moveUp
#
# adds one to the position (unless it is already at the end of the
# stack), and returns the command at that point
######################################################################
    def moveUp(self):

        if len(self.commandStack) == 0:
            return None
        if (self.position < len(self.commandStack) - 1):
            self.position += 1

        return self.commandStack[self.position]

    

######################################################################
# moveDown
#
# subtracts one from the position (unless it is at -1).  returns
# the commandd at that position.
# the command at position -1 on the stack is whatever command was
# partially typed when the user first hit up.
######################################################################
    def moveDown(self):
        if not len(self.commandStack) > 0:
            return None
        if self.position > 0:
            self.position -= 1
            return self.commandStack[self.position]
        if self.position == 0:
            self.position -= 1
            return self.partialCommand

######################################################################
# setPartialCommand
#
# accepts a partially typed command from the command window.
# resets the position of the stack
######################################################################
    def setPartialCommand(self,partialCommand):


        self.partialCommand = partialCommand
        self.position = -1



if __name__ == '__main__':
    stack = JESCommandHistory()
    stack.append('one')
    stack.append('two')
    stack.append('onone')
    stack.append('twtwoo')
    stack.append('three')

    print stack.moveUp()
    print stack.moveUp()
    print stack.moveDown()

    stack.setPartialCommand('on')

    print stack.moveUp()
    print stack.moveUp()
    print stack.moveUp()
    print stack.moveDown()

    stack.setPartialCommand('tw')
    print stack.moveUp()
    print stack.moveUp()
    print stack.moveUp()
    print stack.moveDown()
    print stack.moveDown()
    print stack.moveDown()
