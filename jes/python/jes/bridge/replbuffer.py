# -*- coding: utf-8 -*-
"""
jes.bridge.replbuffer
=====================
Accepts input from the command window, and feeds it into the interpreter
when appropriate.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import re
from codeop import compile_command

class REPLBuffer(object):
    def __init__(self, interpreter, commandWindow):
        self.interpreter = interpreter
        self.commandWindow = commandWindow

        self.bufferedStatements = []

        # JES 4.3 uses a similar regex to determine whether to continue.
        # We use compile_command for robustness's sake, but in order to
        # preserve the JES 4.3 behavior of processing syntax errors when
        # we try to exec the line, we use this to decide whether to ignore
        # errors for now and keep reading.
        self.incompleteRegex = re.compile(r'[^#]+:\s*(?:#.*)?$')

        interpreter.afterRun.connect(self.onInterpreterReady)

    def onInterpreterReady(self, terp, **_):
        if self.commandWindow.isInPrompt():
            self.commandWindow.cancelPrompt()
        self.startStatement()

    def startStatement(self):
        self.bufferedStatements = []
        self.commandWindow.prompt(
            ">>> ", 'python-prompt', self.submitFirstLine, 'python-code', 'python'
        )

    def submitFirstLine(self, line):
        if line is None:
            # We just got cancelled. Do nothing, and wait for someone else
            # to start us up again.
            return

        # Right now, we need to decide whether to continue the command
        # across multiple lines.
        try:
            code = compile_command(line)
            complete = code is not None
        # (Don't) Handle exceptions from compile_command.
        # Why? According to a comment in JES 4.3, Jython's compile_command
        # doesn't detect all syntax errors. (This may not be true any longer.)
        except SyntaxError:
            complete = self.incompleteRegex.match(line) is None
        except ValueError:
            complete = self.incompleteRegex.match(line) is None
        except OverflowError:
            complete = self.incompleteRegex.match(line) is None

        if not complete:
            self.continueStatement(line)
        else:
            self.finishStatement(line)

    def submitNextLine(self, line):
        if line is None:
            # Cancelled.
            return

        # Here, we buffer input regardless of content,
        # and push it all to the system once a blank line is entered.
        if not line:
            self.finishStatement(line)
        else:
            self.continueStatement(line)

    def continueStatement(self, line):
        self.bufferedStatements.append(line)
        self.commandWindow.prompt(
            "... ", 'python-prompt', self.submitNextLine, 'python-code', 'python'
        )

    def finishStatement(self, line):
        self.bufferedStatements.append(line)
        fragment = '\n'.join(self.bufferedStatements)
        self.interpreter.runCodeFragment(fragment)

