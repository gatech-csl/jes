# -*- coding: utf-8 -*-
"""
jes.core.interpreter.debugger
=============================
This provides a running debugger for JES's use.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import time
from blinker import NamedSignal
from pdb import Pdb

class Debugger(Pdb, object):
    #: When the debugger's speed is set to this, execution proceeds
    #: at 1 statement per second. Double this is 2 statements per second,
    #: half this is a statement every 2 seconds.
    UNIT_SPEED = 20.0

    #: The lowest speed you (should) be able to set the debugger to.
    #: You can technically set it to any nonnegative integral speed,
    #: but sticking above this is preferred.
    #: (A speed setting of 2 is a statement every 10 seconds.)
    MIN_SPEED = 2

    #: When the debugger's speed is set to this, the speed is ignored.
    #: Statements are simply run as fast as possible.
    MAX_SPEED = int(3 * UNIT_SPEED)

    #: The default speed setting for the debugger.
    #: (Twice unit speed is 2 statements per second.)
    DEFAULT_SPEED = int(2 * UNIT_SPEED)

    def __init__(self, interpreter):
        """
        Connects the debugger to the interpreter.
        """
        super(Debugger, self).__init__()
        self.interpreter = interpreter
        self.speed = self.DEFAULT_SPEED
        self.targetFilenames = set()
        self.running = False

        self.onSpeedSet = NamedSignal('onSpeedSet')

        self.onStart = NamedSignal('onStart')
        self.onStop = NamedSignal('onStop')
        self.onFrame = NamedSignal('onFrame')

    def starting(self):
        """
        Fires the debugger's start signal.
        """
        self.running = True
        self.onStart.send(self)

    def stopping(self):
        """
        Fires the debugger's stop signal.
        """
        self.running = False
        self.onStop.send(self)

    def setSpeed(self, speed):
        """
        Sets a new speed for the debugger. This fires onSpeedSet.
        """
        speed = int(speed)
        if speed > self.MAX_SPEED:
            speed = self.MAX_SPEED
        elif speed <= 0:
            raise ValueError("Speed must be a positive integer")

        self.speed = speed
        self.onSpeedSet.send(self, newSpeed=speed)

    def setTargetFilenames(self, filenames):
        """
        Sets the set of filenames which will make the debugger stop.
        """
        self.targetFilenames = set(filenames)


    ###
    ### PDB INTERCEPTION METHODS
    ###

    # Overrides Pdb.interaction
    # This is used whever the debugger would step
    def interaction(self, frame, traceback):
        currentFilename = frame.f_code.co_filename

        if currentFilename in self.targetFilenames:
            lineno = frame.f_lineno

            self.onFrame.send(self,
                filename=currentFilename, lineno=lineno,
                frame=frame, traceback=traceback
            )

            if self.interpreter.runningThread.stopSignal:
                raise ThreadDeath

            if self.speed < self.MAX_SPEED:
                period = self.UNIT_SPEED / self.speed
                time.sleep(period)

            if self.interpreter.runningThread.stopSignal:
                raise ThreadDeath

    # Overrides pdb.user_line
    def user_line(self, frame):
        """This function is called when we stop or break at this line."""
        self.interaction(frame, None)

    # Overrides pdb.user_return
    def user_return(self, frame, return_value):
        pass

    # Overrides pdb.user_return
    def user_exception(self, frame, (exc_type, exc_value, exc_traceback)):
        pass

    # Overrides pdb.user_call
    def user_call(self, frame, argument_list):
        """This method is called when there is the remote possibility
        that we ever need to stop in this function."""
        if self._wait_for_mainpyfile:
            return
        if self.stop_here(frame):
            # Only overridden just to remove this line:
            #print >>self.stdout, '--Call--'
            self.interaction(frame, None)

