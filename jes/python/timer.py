###############################################################################
# timer.py        Version 1.0   29-May-2013     Bill Manaris

###########################################################################
#
# This file is part of Jython Music.
#
# Copyright (C) 2014 Bill Manaris
#
#    Jython Music is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    Jython Music is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Jython Music.  If not, see <http://www.gnu.org/licenses/>.
#
###########################################################################

#
# Timer class to schedule repeated tasks to be executed, without using sleep().  
# (For instance, the latter causes the Swing GUI event loop to sleep, locking
# up a GUI.)
#

from java.awt.event import *

###############################################################################
# Timer
#
# Class for creating a timer (for use to schedule tasks to be executed after 
# a given time interval, repeatedly or once).
#
# Methods:
#
# Timer( timeInterval, function, parameters, repeat)
#   Creates a new Timer to call 'function' with 'parameters', after 'timeInterval' (if 'repeat'
#   is True this will go on indefinitely (default); False means once.  
#   It uses either Swing's Timer.
#
# start()
#   Starts the timer.
#
# stop()
#   Stops the timer.
#
# isRunning()
#   Returns True if timer is running; False otherwise.
#
# stop()
#   Stops the timer.
#
# setRepeats( flag )
#   Sets the repeat attribute of the timer (True means repeat; False means once).
###############################################################################

# TimerListener
#
# Listener for Timer objects.  eventHandler is called when the timer interval expires.
# Extends Swing's ActionListener class.

class TimerListener(ActionListener):
   """
   Event handler for timer events
   """

   def __init__(self, eventFunction, parameters=[]):
      """
      Points this listener to eventFunction when the timer interval expires.
      """
      self.eventFunction = eventFunction
      self.parameters = parameters

   def actionPerformed(self, event = None):
      """
      Call the eventFunction.
      """
      # call the function with the specified parameters 
      # (see http://docs.python.org/2/tutorial/controlflow.html#unpacking-argument-lists)
      self.eventFunction(*self.parameters)  


from javax.swing import Timer as JTimer

class Timer(JTimer):
   """Timer used to schedule tasks to be run at fixed time intervals."""
   
   def __init__(self, timeInterval, function, parameters=[], repeat=True):
      """Specify time interval (in milliseconds), which function to call when the time interval has passed
         and the parameters to pass this function, and whether to repeat (True) or do it only once."""
         
      self.timeListener = TimerListener(function, parameters)    # define the timer event listener and provide function and parameters to be called 
      
      JTimer.__init__(self, int(timeInterval), self.timeListener)
      self.setRepeats( repeat )      # should we do this once or forever? 

   def setFunction(self, function, parameters=[]):
      """Sets the function to execute.  The optional parameter parameters is a list of parameters to pass to the function (when called)."""
      self.timeListener.eventFunction = eventFunction
      self.timeListener.parameters = parameters

   def getRepeat(self):
      """Returns True if timer is set to repeat, False otherwise."""
      return self.isRepeats()

   def setRepeat(self, flag):
      """Timer is set to repeat if flag is True, and not to repeat if flag is False."""
      self.setRepeats( flag )   # set the repeat flag
      self.start()              # and start it (in case it had stopped)


#####################################################################################
from music import mapValue
from math import cos, pi

class timedOscillator:
   """It calls a provided function giving it an oscillating value at timed intervals.
      It may be used to fluctuate volume, panning, or frequency of sounds, among other things.
   """
   
   def __init__(self, delay, minValue, maxValue, step, function):
      """Specify a time interval ('delay', in milliseconds), the min and max values within which to oscillate,
         the 'step' increment by which to advance the oscillating value at every time interval, and finally
         the function to call when the time interval has passed.  
         This function is passed on argument, namely the current value of the oscillator.
      """
         
      self.minValue = minValue     # the lowest point of the oscillating value
      self.maxValue = maxValue     # the highest point of the oscillating value
         
      self.function = function     # the function to call passing it the oscillating value
        
      # initialize oscillation
      self.oscillatorPhase  = 0.0  # ranges from -0 to 2*pi
      self.oscillatingValue = mapValue( cos(self.oscillatorPhase), -1.0, 1.0, self.minValue, self.maxValue)
         
      # convert the step increment to an angle/phase increment (in radians)         
      self.stepPhase = mapValue(step, self.minValue, self.maxValue, 0.0, 2*pi)
         
      # define timer
      self.timer = Timer(delay, self.__oscillate__, [], True)
         
   def __oscillate__(self):
      """It calls the callback function with the current oscillator value, and calculates the next oscillator value."""
      
      # ***
      print "phase =", self.oscillatorPhase, ", value =", self.oscillatingValue
      
      self.function( self.oscillatingValue )
      
      # advance angle and wrap around
      self.oscillatorPhase  = (self.oscillatorPhase + self.stepPhase) % (2*pi)
      
      # caclulate new oscillation value 
      self.oscillatingValue = mapValue( cos(self.oscillatorPhase), -1.0, 1.0, self.minValue, self.maxValue)

   def start(self):
      """Start the oscillator and the begin calling the function."""
      self.timer.start()
   
   def stop(self):
      """Start the oscillator."""
      self.timer.stop()
   
   def setDelay(self, delay):
      """Set the time interval to wait before advancing the oscillating value."""
      self.timer.setDelay(delay)
   
   def getDelay(self):
      """Get the current time interval to wait before advancing the oscillating value."""
      return self.timer.getDelay()
               
   