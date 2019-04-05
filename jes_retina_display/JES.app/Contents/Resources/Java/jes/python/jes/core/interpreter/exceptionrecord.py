# -*- coding: utf-8 -*-
"""
jes.core.interpreter.exceptionrecord
====================================
This class holds information about exceptions.

(It's kinda twisty. It's been this way since '09, and I'm scared to change
it because it could subtly break the screenshots in the textbook.)

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial;
            (C) 2009 William Scharfnorth, Brian Dorn, and Barbara Ericson;
            (C) 2002 Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import JESConfig
import os.path
from java.lang import ThreadDeath
from .messages import (GENERIC_EXCEPTION_MESSAGE, EXCEPTION_MESSAGES,
                       STOP_MESSAGE)

COMMAND_FROM_CONSOLE = '<input>'
STACK_MSG = ' in file %s, on line %d, in function %s\n'
LINE_NUM_MSG = 'Please check line %d of %s\n'


class JESExceptionRecord:
    def __init__(self, programFileName):
        self.programFileName = programFileName

    def getExceptionMsg(self):
        return self.exc_msg

    def getLineNumber(self):
        return self.line_number


##########################################################################
# Function name: getExceptionDescription
# Parameters:
#     -exception: Exception object containing information about the exception
#                 that occured. (This is the exception value, not the type!)
# Return:
#     Returns a message as a string describing the error that occured.
# Description:
#     This function takes in an exception object and returns a user friendly
#     message describing the error that occured.
##########################################################################
    def getExceptionDescription(self, exception):
        import org.python.core.PyString as PyString
        if exception.__class__ == PyString:
            return exception + '\n'

        cls = type(exception)
        className = cls.__name__
        doc = getattr(cls, '__doc__')

        # At least some exceptions don't have a __dict__ under Jython 2.5.
        # We build our own __dict__ here.
        attributes = {}
        for name in dir(exception):
            attributes[name] = getattr(exception, name)

        if EXCEPTION_MESSAGES.has_key(className):
            template = EXCEPTION_MESSAGES[className]
            msg = template % attributes
            if doc:
                msg = doc + '\n' + msg
        else:
            msg = GENERIC_EXCEPTION_MESSAGE % className
            if doc:
                msg = doc + '\n' + msg

            args = getattr(exception, 'args', ())
            for arg in args:
                msg += '\n' + arg

        msg += '\n'
        return msg


##########################################################################
# Function name: setByHand
#
# Allows the message and line number of the exception record to be set by hand
#
# Parameters:
#    - errMsgTxt: The message to be printed to the screen
#    - errLineNum: The number of the line that threw the exception
#
# returns : nothing
##########################################################################
    def setByHand(self, errMsgTxt, errLineNum=None):

        self.exc_msg = errMsgTxt
        self.line_number = errLineNum

    ###########################################################################
    # setFromUserCode
    #
    # sets the values of the exception record from the return values of
    # sys.exc_info()
    #
    # Whereas setByHand accepts error text an an optional error line,
    # this file determines all of that automatically
    #
    # Syntax errors are handled differently than exceptions generated while
    # running, so setFromUserCode calls seetFromUserCodeSyntaxError or
    # setFromUserCodeException
    #
    # param= exc_type, exc_value, exc_traceback -
    #        the return values of sys.exc_info()
    #        NOTE - sys.exc_info() only returns interestering values when called
    #               *inside* the "except" block
    # return: None
    #         BUT
    # sets self.exc_msg, and self.line_number
    ###########################################################################

    def setFromUserCode(self, exc_type, exc_value, exc_traceback):

        if hasattr(exc_type, '__name__') and \
            ((exc_type.__name__ == 'SyntaxError') or
             (exc_type.__name__ == 'TokenError')):

            self.setFromUserCodeSyntaxError(exc_type, exc_value, exc_traceback)

        else:
            self.setFromUserCodeException(exc_type, exc_value, exc_traceback)

    ##########################################################################
    # setFromUserCodeSyntaxError
    #
    # handles the user's code if a SyntaxError has occured
    # param - type,value,traceback - the return values of sys.exc_info()
    # return: None
    #
    # The exc_msg is set entirely from getExceptionDescription
    # The line_number is set from a value of exc_value, which here
    # is an array
    ##########################################################################

    def setFromUserCodeSyntaxError(self, exc_type, exc_value, exc_traceback):
        import traceback

        try:
            msg, (filename, lineno, offset, line) = exc_value

        except:
            pass

        self.exc_msg = self.getExceptionDescription(exc_value)
        txtStack = self.getExceptionInfo(exc_traceback)

        if (self.showLineNumber(txtStack)):
            self.line_number = self.getLineNum(txtStack)
        else:
            self.line_number = None
        (lastFileName, lastNum) = self.getLastFileOnTxtStack(txtStack)

        list = []
        try:
            msg, (filename, lineno, offset, line) = exc_value

        except:
            pass

        else:
            # if filename equals '<input>', then the message was typed from the command
            # line

            if filename == self.programFileName:

                self.line_number = lineno

            if (not self.line_number is None) and (self.line_number != 0):
                if (filename == self.programFileName):
                    self.exc_msg += "The error is on line %d.\n" % self.line_number
                else:
                    (filename, lineno) = (lastFileName, lastNum)
                    self.exc_msg += "Look at line %d of the current file.\n" % self.line_number
                    self.exc_msg += "That line refers to the file '%s'.\n" % filename
                    self.exc_msg += "The file '%s' has a syntax error on line %d.\n" %\
                                    (os.path.basename(filename), lineno)

            else:

                self.line_number == None

    ###########################################################################
    # setFromUserCodeException
    #
    # uses the (type,value,traceback) set in a bit tricker way than the other
    # functions
    #
    # the following variables are filled in the function,  and appended to
    # set the value of self.exc_msg:
    #
    # exceptionDesc: the return value of self.getExceptionDescription
    # stackMsg: the (possibly empty (ie, '') ) text stack trace
    #           not shown if the error occured in a single line in the
    #           command window
    # nameOfExcMsg : a line of text that includes the name of the actual exception
    #                the exceptionDesc can be vague
    #
    # lineNumMsg :  Mentions the line number in the *currently open* file
    #               where the error occured.
    #               not shown  if the error did not occur in a file that is
    #               currently opened
    ###########################################################################
    def setFromUserCodeException(self, exc_type, exc_value, exc_traceback):
        import traceback

        # a representation of the stack trace of the exception
        txtStack = self.getExceptionInfo(exc_traceback)

        # if true, the error occured in one line, and no
        # stack trace needs to be printed
        showLineNum = self.showLineNumber(txtStack)

        # if true, the error occured in a file that was read in from the
        # filesystem
        # if false, the error occured in code defined in the command window
        showStk = self.showStack(txtStack)

        isThreadDeath = exc_type is ThreadDeath
        asString = str(exc_value)

        if isThreadDeath:
            valueMsg = ''
        elif ': ' in asString:
            valueMsg = 'The error was: ' + asString[asString.find(': ') + 2:] + '\n'
        else:
            valueMsg = 'The error value is: ' + asString + '\n'

        stackMsg = ''
        nameOfExcMsg = ''
        lineNumMsg = ''
        self.line_number = None

        if isThreadDeath:
            exceptionDesc = STOP_MESSAGE + '\n'
        else:
            exceptionDesc = self.getExceptionDescription(exc_value)
            try:
                nameOfExcMsg = self.getNameOfExcMsg(exc_type, exc_value)
            except:
                # some exceptions don't have names
                pass

        if showLineNum and not isThreadDeath:
            lineNumMsg = self.getLineNumMsgForFile(txtStack)
            self.line_number = self.getLineNum(txtStack)

        if showStk:
            stackMsg = self.getStackMsg(txtStack)

        self.exc_msg = valueMsg + exceptionDesc + stackMsg +\
            nameOfExcMsg + lineNumMsg


######################################################################
# showLineNumber
#
# returns true if a line number should be shown by the command window
# returns false otherwise
#
# a line number should be shown if it would correspond to the currently
# opened file- if the name of the opened file appears on the stack,
######################################################################
    def showLineNumber(self, txtStack):

        # error is from a single line if stack is one long
        for frame in txtStack:
            if frame[0] == self.programFileName:
                return not None

        return None


######################################################################
# showStack
#
# returns true if the stack should be printed with the exception
# message, false if not
#
# the stack should be shown unless the error comes from a
# simple command typed in the command window that has only a
# one level stack
# ie, >>> f = 5 / 0
# and not a function call.
######################################################################
    def showStack(self, txtStack):

        if ( len(txtStack) == 1) and \
           (txtStack[0][0] == COMMAND_FROM_CONSOLE):
            return None

        return not None

######################################################################
# getNameOfExcMsg
#
# returns a string containing the name and value of the exception
# message.
######################################################################
    def getNameOfExcMsg(self, exc_type, exc_value):
        if JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MODE) == JESConfig.MODE_EXPERT:
            return "%s: %s\n" % (exc_type.__name__, exc_value)
        elif exc_type.__name__ == 'SoundException':
            return "%s\n" % (exc_value)
        else:
            return ''

    def getLineNum(self, txtStack):
        goodFrame = ('', 0, '')
        for frame in txtStack:
            if frame[0] == self.programFileName:

                goodFrame = frame

        return goodFrame[1]

######################################################################
# getLineNumMsgForFile
#
# called if we are supposed to show the line number for this exception
# returns a string that is the line number message
#
# param: txtStack - the version of the stack trace returned by
#                   self.getExceptionInfo()
# return: msg - the line number message for the stack
######################################################################
    def getLineNumMsgForFile(self, txtStack):

        goodFrame = ('', 0, '')
        for frame in txtStack:
            if frame[0] == self.programFileName:

                goodFrame = frame

        msg = LINE_NUM_MSG % (goodFrame[1], goodFrame[0])
        return msg

    def getStackMsg(self, txtStack):

        if JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MODE) == JESConfig.MODE_EXPERT:
            stackMsg = ''

            count = 1
            for frame in txtStack:
                if (count == 1)and (frame[0] == COMMAND_FROM_CONSOLE):
                    pass
                else:

                    stackMsg = stackMsg + \
                        STACK_MSG % frame
                count += 1
            return stackMsg
        else:
            stackMsg = ''
            return stackMsg

######################################################################
# getExceptionInfo
#
# accepts a copy of the traceback returned by sys.exc_info().
# reads through that, and returns a text version of the stack trace,
# where each level corresponds to a stack frame, and is composed of the
# elements [ filename, lineNumber, functionName ]
#
# param: tb, the third parameter returned by sys.exc_info()
# return: txtStack - the data structure described above
######################################################################
    def getExceptionInfo(self, tb):
        import traceback

        txtStack = []
        lineno = 0
        while (tb is not None):

            f = tb.tb_frame

            lineno = traceback.tb_lineno(tb)
            co = f.f_code
            filename = co.co_filename
            name = co.co_name
            tb = tb.tb_next

            txtStack.append((filename, lineno, name))

        return txtStack

    def getLastFileOnTxtStack(self, txtStack):
        goodFrame = (None, None)
        for frame in txtStack:

            if frame[0] != '<string>' and \
               frame[0] != '<input>':

                goodFrame = frame[:2]

        return goodFrame
