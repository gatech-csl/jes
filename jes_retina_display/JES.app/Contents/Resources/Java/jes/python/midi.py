################################################################################################################
# midi.py       Version 1.4     13-May-2013     David Johnson, Bill Manaris, Kenneth Hanson

###########################################################################
#
# This file is part of Jython Music.
#
# Copyright (C) 2014 David Johnson, Bill Manaris, Kenneth Hanson
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
# This module includes functionality to connect to MIDI devices from input and output.
#
#
# REVISIONS:
#
#   1.4    13-May-2013  (bzm) Function MidiIn.onInput() now has an eventType parameter (i.e., the number
#                       associated with a particular message type.  This makes it even more convenient
#                       for the end-programmer to specify callback functions for specific MIDI event types.
#                       MidiIn.onInput() can be used repeatedly to associate different event types with 
#                       different callback functions (one function per event type).  
#
#                       NOTE:  If called more than once for the same event type, only the latest callback 
#                       function is retained (the idea is that this function can contain all that is needed 
#                       to handle this event type).  If eventType is ALL_EVENTS, the associated callback function
#                       is called for all events not handled already. 
#
#   1.3    12-May-2013  (bzm) Added MidiIn functions onNoteOn(), onNoteOff(), onSetInstrument()
#                       to specify callback functions to call when these MIDI events arrive.
#                       The rationale is that most MIDI applications will include code that
#                       handles these most-common MIDI events, so why require the end-programmer
#                       to always include the necessary "parsing" (if-else) code.  Let's hide this under
#                       the API abstraction.  For less-common MIDI messages, the end-programmer
#                       can still use the onInput() function to specify other callbacks for
#                       for different types of incoming MIDI messages.
#

from javax.sound.midi import *
from gui import *
from time import sleep


#################### MidiIn ##############################
#
# MidiIn is used to receive input from a MIDI device.
#
# This class may be instantiated several times to receive input from different MIDI devices
# by the same program.  Each MidiIn object is associated with a (callback) function to be called
# when a MIDI input event arrives from the corresponding MIDI device.  This function should
# accepts four integer parameters: msgType, msgChannel, msgData1, msgData2.  
#
# When instantiating, the constructor brings up a GUI with all available input MIDI devices.
#
# For example:
#
# midiIn = MidiIn()
#
# def processMidiEvent(msgType, msgChannel, msgData1, msgData2):
#   print "MIDI In - Message Type:", msgType, ", Channel:", msgChannel, ", Data 1:", msgData1, ", Data 2:", msgData2
#
# midiIn.onInput( ALL_EVENTS, processMidiEvent )   # register callback function to handle all input MIDI events
#

# some useful MIDI event constants
ALL_EVENTS = -1
NOTE_ON    = 144   # 0x90
NOTE_OFF   = 128   # 0x80
SET_INSTRUMENT = 192   # 0xC0  (also known as MIDI program/patch change)

class MidiIn(Receiver):

   def __init__(self):
      
      self.waitingToSetup = True       # used to busy-wait until user has selected a MIDI input device 
      self.midiInput = None            # holds MIDI input device asscociated with this instance

      self.eventHandlers = {}          # holds callback functions to be called upon receipt of any input events
                                       # (events are keys, functions are dictionary values)
      # prompt user to select an existing MIDI input device
      self.selectMidiInput()            
      
      # and, since above GUI is asynchronous, wait until user has selected a MIDI input device
      while(self.waitingToSetup):
         sleep(0.1)    # sleep for 0.1 second

      # if we reach this point, the user has made a selection, so we should be good to go
      
      # define a catch-all event handler for incoming MIDI messages
      # (end-programmer may redfine this, by calling onInput() again)
      self.onInput( ALL_EVENTS, self.__printMessage__ )

   def onInput(self, eventType, callbackFunction):
      """
      Associates an incoming event type with a callback function.  Can be used repeatedly to associate different
      event types with different callback functions (one function per event type).  If called more than once for the
      same event type, only the latest callback function is retained (the idea is that this function can contain all
      that is needed to handle this event type).  If eventType is ALL_EVENTS, the associated callback function is 
      called for all events not handled already.
      """
      self.eventHandlers[eventType] = callbackFunction    # associate eventType with callback function

   def onNoteOn(self, callbackFunction):
      """
      Set up a callback function to handle only noteOn MIDI input events.
      """
      self.eventHandlers[NOTE_ON] = callbackFunction    

   def onNoteOff(self, callbackFunction):
      """
      Set up a callback function to handle only noteOff MIDI input events.
      """
      self.eventHandlers[NOTE_OFF] = callbackFunction    

   def onSetInstrument(self, callbackFunction):
      """
      Set up a callback function to handle only setInstrument MIDI input events.
      """
      self.eventHandlers[SET_INSTRUMENT] = callbackFunction    

   def __printMessage__(self, msgType, msgChannel, msgData1, msgData2):
      """Prints out MIDI event data."""      
      print "\nMidiEvent:"
      print "MIDI In - Message Type:", msgType, ", Channel:", msgChannel, ", Data 1:", msgData1, ", Data 2:", msgData2

   ###### functions required by Receiver interface #######

   def send(self, message, timeStamp):
      """Method required by the Receiver Interface.  It handles incoming MIDI events."""

      # based on code from Andrew Brown's jMusic package

      m = message.getMessage()      # get message bytes to deserialize
      msgStatus = message.getStatus()     # get message status
      
      # a MIDI message can be one of 3 types:
      # ShortMessage, SysexMessage(System Exclusive), or MetaMessage
      
      if isinstance(message, ShortMessage):     # is this a ShortMessage?
      
         # if so then, get message data
         msgType = (m[0] & 0xFF) >> 4     # get message type from byte array
         msgChannel = m[0] & 0xF          # get message channel from byte array
         msgData1 = m[1]                  # get data 1 info from byte array
         msgData2 = -1                    # initialize data 2 to -1 if message doesn't contain data 2 info
         if len(m) > 2:                   # if message has data 2 info
            msgData2 = m[2]                  # get info from byte array
      
         # There are two types of short MIDI messages (at the highest level) - channel and system messages.
         # Let's find out which type this is...
         
         if msgType != 15:  # is it a channel message?

            # get eventType
            eventType = msgStatus-msgChannel
            
            # normalize NOTE-OFF events (sometimes they are presented as NOTE_ON events with 0 velocity)
            if (eventType == NOTE_ON and msgData2 == 0):
               eventType = NOTE_OFF    # this is actually a NOTE_OFF event, so remember it as such

            # get callback function for this event (if any)
            if self.eventHandlers.has_key( eventType ):
               eventHandler = self.eventHandlers[ eventType ]
            else:
               eventHandler = self.eventHandlers[ ALL_EVENTS ]
               
            # call the event handler with the input message
            eventHandler(eventType, msgChannel, msgData1, msgData2)

            
         else:    # it is a system message
         
            if msgStatus == ShortMessage.TIMING_CLOCK:
               print "MIDI Clock message"
            elif msgStatus == ShortMessage.ACTIVE_SENSING:
               print "MIDI Active Sensing message"
            else:
               print "A non-identified MIDI System message", msgStatus

      elif isinstance(message, SysexMessage):      # or is it a System Exclusive Message
         # if it is print the data
         print "Sysex MIDI Message <<",
         for i in range(len(m)):
            print m[i],
         print ">>"

      elif isinstance(message, MetaMessage):       # or is it a Meta Message?
         # if is print the data
         print "Meta MIDI Message <<",
         for i in range(len(m)):
            print m[i],
         print ">>"
      else:                                        # otherwise it is an unknown type
         # print the data
         print "Unknown MIDI Message <<",
         for i in range(len(m)):
            print m[i],
         print ">>"

   def close(self):
      '''Method required by Receiver interface.  Closes MIDI input device
      to free any resources it is using'''
      if self.midiInput:
         self.midiInput.close()


   ############# helper functions #################

   # creates display with available input MIDI devices and allows to select one
   def selectMidiInput(self):

      availDevices = MidiSystem.getMidiDeviceInfo()         # get information about MIDI devices available to the system
      self.inputDevices = {}                                # get name of device for more user friendly display
      for device in availDevices:
         key = device.getVendor() + " " + device.getName()

         # select only input MIDI devices (as opposed to output devices) 
         try:
            midiDevice = MidiSystem.getMidiDevice(device)    # get selected MIDI device from system
            midiDevice.open()                                # try to open it
            t = midiDevice.getTransmitter()                  # check if it has a transmitter (i.e., if it is an input device)
            midiDevice.close()                               # and close it
            
            # if we reach this point without an error, this is a valid input device
            self.inputDevices[key] = device    # so, remember it

         except:
            pass
            
         # now, only available MIDI input devices are stored in self.inputDevices

      # create selection GUI
      self.display = Display("Select MIDI Input", 400, 125) # display info to user

      self.display.drawLabel('Select a MIDI input device from the list', 45, 30)

      # create dropdown list of available MIDI input devices
      items = self.inputDevices.keys()
      items.sort()
      deviceDropdown = DropDownList(items, self.openInputDevice)
      self.display.add(deviceDropdown, 40, 50)
      self.display.setColor( Color(124, 201, 251) )   # set color to shade of blue (for input)
      
   # callback for dropdown list
   def openInputDevice(self, selectedItem):

      # open selected input device
      print "Receiving MIDI Input from", selectedItem
      deviceInfo = self.inputDevices[selectedItem]          # get device info from dictionary
      self.midiInput = MidiSystem.getMidiDevice(deviceInfo) # get selected device from Midi System
      self.midiInput.open()   # open it
      t = self.midiInput.getTransmitter()
      t.setReceiver(self)

      # selection has been made so close display and exit busy loop in constructor
      self.waitingToSetup = False                           # no longer waiting to be setup, set to False so we can move on
      self.display.hide()                                   # close display since it is no longer needed

#################### MidiOut ##############################
#
# MidiOut is used to send output a MIDI device.
#
# This class may be instantiated several times to send output to different MIDI devices
# by the same program.  
#
# When instantiating, the constructor brings up a GUI with all available output MIDI devices.
# You may create several instances, one for every MIDI device you wish to send output to.
# Then, to output a MIDI message, call sendMidiMessage() with 4 parameters: msgType, msgChannel
# msgData1, msgData2.
#
# For example:
#
# midiOut = MidiOut()
#
# noteOn = 144   # msgType for starting a note
# noteOff = 128  # msgType for ending a note
# channel = 0    # channel to send message
# data1 = 64     # for NOTE_ON this is pitch
# data2 = 120    # for NOYE_ON this is velocity (volume)
#
# midiOut.sendMidiMessage(noteOn, channel, data1, data2)  # start note
# 
# midiOut.sendMidiMessage(noteOff, channel, data1, data2) # end note
# midiOut.sendMidiMessage(noteOn, channel, data1, 0)      # another way to end note (noteOn with 0 velocity)

# NOTE: The default synthesizer in Java 6 stops playing after a while, and then starts again.
#       One solution is to use Gervill with Java 6 - see http://stackoverflow.com/questions/7749172/why-java-midi-synth-on-mac-stop-playing-notes
#       Another solution is to use another software synthesizer, e.g., SimpleSynth - http://notahat.com/simplesynth/
#


class MidiOut():

   def __init__(self):

      self.waitingToSetup = True          # used to busy-wait until user has selected a MIDI input device 
      self.midiOutput = None              # holds the selected output MIDI device (we may want to close it?)
      self.midiReceiver = None            # holds the selected device's MIDI receiver (to send MIDI messages to)

      # prompt user to select an existing output MIDI device
      self.selectMidiOutput()

      # and, since above GUI is asynchronous, wait until user has selected a MIDI output device
      while(self.waitingToSetup):
         sleep(0.1)    # sleep for 0.1 second

      # if we reach this point, the user has made a selection, so we should be good to go

   def setInstrument(self, instrument, channel=0):
      """Sets 'channel' to 'instrument' through the selected output MIDI device.""" 

      self.sendMidiMessage(192, channel, instrument, 0)

   def noteOn(self, pitch, velocity=100, channel=0):
      """Send a NOTE_ON message for this pitch to the selected output MIDI device."""
            
      self.sendMidiMessage(144, channel, pitch, velocity)
      
   def noteOff(self, pitch, channel=0):
      """Send a NOTE_OFF message for this pitch to the selected output MIDI device."""
      
      #self.sendMidiMessage(144, channel, pitch, 0)
      self.sendMidiMessage(128, channel, pitch, 0)

   def playNote(self, pitch, start, duration, velocity=100, channel=0):
      """Plays a note with given 'start' time (in milliseconds from now), 'duration' (in milliseconds
         from 'start' time), with given 'velocity' on 'channel' via MIDI Out.""" 
         
      # TODO: We should probably test for negative start times and durations.
               
      # create a timer for the note-on event
      #noteOn = Timer(start, self.sendMidiOutput, [144, channel, pitch, velocity], False)
      noteOn = Timer(start, self.noteOn, [pitch, velocity, channel], False)
            
      # create a timer for the note-off event (note-off is done using note-on with 0 velocity)
      #noteOff = Timer(start+duration, self.sendMidiOutput, [144, channel, pitch, 0], False)
      noteOff = Timer(start+duration, self.noteOff, [pitch, channel], False)

      # and activate timers (set thinsg in motion)
      noteOn.start()
      noteOff.start()
      
      # NOTE:  Upon completion of this function, the two Timer objects become unreferenced.
      #        When the timers elapse, then the two objects (in theory) should be garbage-collectable,
      #        and should be eventually cleaned up.  So, here, no effort is made in reusing timer objects, etc.


   def play(self, material):
      """Play jMusic material (Score, Part, Phrase, Note) via MIDI Out."""
      
      from jm.music.data import Phrase as jPhrase   # since we redefine Phrase
      
      # play the music        
      # do necessary datatype wrapping (MidiSynth() expects a Score)
      if type(material) == type(Note()):
         material = Phrase(material)
      if type(material) == type(Phrase()):   # no elif - we need to successively wrap from Note to Score
         material = Part(material)
      if type(material) == type(jPhrase()):  # (also wrap jMusic default Phrases, in addition to our own)
         material = Part(material)
      if type(material) == type(Part()):     # no elif - we need to successively wrap from Note to Score
         material = Score(material)
      if type(material) == type(Score()):
         
         self.__playScore__( material )   # play it!
         
      else:   # error check    
         print "Play.midi() - Unrecognized type", type(material), "- expected Note, Phrase, Part, or Score."


   def __playScore__(self, score):
      """Plays a jMusic Score via MIDI Out."""
      
      # loop through all parts and phrases to get all notes
      noteList = []     # holds all notes
      for part in score.getPartArray():   # traverse all parts
         channel = part.getChannel()        # get part channel
         instrument = part.getInstrument()  # get part instrument
         for phrase in part.getPhraseArray():   # traverse all phrases in part
            if phrase.getInstrument() > -1:        # is this phrase's instrument set?
               instrument = phrase.getInstrument()    # yes, so it takes precedence
            for index in range(phrase.length()):      # traverse all notes in this phrase
               note = phrase.getNote(index)              # and extract needed note data
               pitch = note.getPitch()
               start = phrase.getNoteStartTime(index)
               duration = note.getDuration()
               velocity = note.getDynamic()
                
               # accumulate non-REST notes
               if (pitch != REST):
                  noteList.append((start, pitch, duration, velocity, channel, instrument))   # put start time first, so we can sort easily by start time (below)
                
      # sort notes by start time
      noteList.sort()
    
      # time factor (approx.) to convert time from jMusic Score units to milliseconds
      FACTOR = 1000 * 60 / score.getTempo()

      # Schedule playing all notes in noteList
      for start, pitch, duration, velocity, channel, instrument in noteList:

         # set appropriate instrument for this channel
         self.setInstrument(instrument, channel)

         # schedule note-on and note-off events for this note
         self.playNote(pitch, int(start * FACTOR), int(duration * FACTOR), velocity, channel)
         #print "Play.note(" + str(pitch) + ", " + str(int(start * FACTOR)) + ", " + str(int(duration * FACTOR)) + ", " + str(velocity) + ", " + str(channel) + ")"

   ####### function to output MIDI message through selected output MIDI device ########
   
   def sendMidiMessage(self, msgType, msgChannel, msgData1, msgData2):
      #print "Sending Message...", msgType, msgChannel, msgData1, msgData2
      try:
         msg = ShortMessage()
         msg.setMessage(msgType, msgChannel, msgData1, msgData2)
         self.midiReceiver.send(msg, -1L)
      except InvalidMidiDataException, e:
         print e


   ####### helper functions ########
   
   # creates display with available output MIDI devices and allows to select one
   def selectMidiOutput(self):

      availDevices = MidiSystem.getMidiDeviceInfo()         # get information about MIDI devices available to the system
      self.outputDevices = {}                               # get name of device for more user friendly display
      for device in availDevices:
         key = device.getVendor() + " " + device.getName()

         # select only output MIDI devices (as opposed to input devices) 
         # select only input MIDI devices (as opposed to output devices) 
         try:
            midiDevice = MidiSystem.getMidiDevice(device)    # get selected MIDI device from system
            midiDevice.open()                                # try to open it
            r = midiDevice.getReceiver()                     # check if it has a receiver (i.e., if it is an output device)
            midiDevice.close()                               # and close it
            
            ## if we reach this point without an error, this is a valid output device
            self.outputDevices[key] = device    # so, remember it

         except:
            pass
            
         # now, only available MIDI output devices are stored in self.outputDevices

      # create selection GUI
      self.display = Display("Select MIDI Output", 400, 125) # display info to user

      self.display.drawLabel('Select a MIDI output device from the list', 45, 30)

      # create dropdown list of available MIDI input devices
      items = self.outputDevices.keys()
      items.sort()
      deviceDropdown = DropDownList(items, self.openOutputDevice)
      self.display.add(deviceDropdown, 40, 50)
      self.display.setColor( Color(255, 153, 153) )   # set color to shade of red (for output)

   # callback for dropdown list
   def openOutputDevice(self, selectedItem):

      # open selected input device
      print "Sending MIDI Output to", selectedItem
      deviceInfo = self.outputDevices[selectedItem]             # get device info from dictionary
      self.midiOutput = MidiSystem.getMidiDevice(deviceInfo) # get selected device from Midi System
      self.midiOutput.open()   # open it
      self.midiReceiver = self.midiOutput.getReceiver()      # get receiver to send messages to

      # selection has been made so close display and exit busy loop in constructor
      self.waitingToSetup = False                           # no longer waiting to be setup, set to False so we can move on
      self.display.hide()                                   # close display since it is no longer needed


#################### Unit Testing ##############################

if __name__ == '__main__':

   #from music import *
   
   # establish a connection to an input MIDI device
   midiIn = MidiIn()     

   # establish a connection to an output MIDI device
   midiOut = MidiOut()   
   
   # create a function to send (echo) incoming MIDI messages to the selected output MIDI device
   def patchIn2Out(eventType, channel, data1, data2):
      """Echo MIDI event to the selected MIDI output."""
      
      global midiOut
      
      print "\nMIDI In - Message Type:", eventType, ", Channel:", channel, ", Data 1:", data1, ", Data 2:", data2

      # play through MIDI out
      midiOut.sendMidiMessage(eventType, channel, data1, data2)
   
   # register a callback function to process incoming MIDI events
   midiIn.onInput( ALL_EVENTS, patchIn2Out ) 
   

