################################################################################################################
# midi.py       Version 2.2     31-Dec-2016     Marge Marshall, David Johnson, Bill Manaris, Kenneth Hanson

###########################################################################
#
# This file is part of Jython Music.
#
# Copyright (C) 2016 Marge Marshall, David Johnson, Bill Manaris, Kenneth Hanson
#
#    Jython Music is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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
#   2.2     31-Dec-2016 (bm) Updated MidiOut so that, when JEM's stop button is pressed, to first stop all actives notes
#						from sounding, and then close down.
#
#   2.1     12-Nov-2016 (bm) Updated MidiOut play() to respect global instrument settings, also updated set/getInstrument(),
#                       set/getVolume(), set/getPanning().  MidiOut() now also accepts a preferred output device as a string.
#                       If available, it is selected directly (without a selection display - faster!).  Same thing for MidiIn()
#
#   2.0     03-Aug-2016 (mm, bm) Updated MidiOut play() to include microtonal capability. Copied the updated music.py functions
#                       frequencyOn(), noteOn(), noteOff(), setPitchBend(), getPitchBend(), freqToNote(), noteToFreq().
#                       Also copied frequencyOff() and noteOnPitchBend(), however these need to be changed here (whenever copied
#                       from music.py, after another update), since they use self.sendMessage() to start and stop notes.
#                       Microtonal frequencies are floats (e.g., 440.0), whereas ordinary MIDI pitches are ints (e.g, 69).
#                       These are utilized in note creation, e.g., Note(440.0, QN) vs. Note(69, QN), which refer to the same
#                       note, A4.
#                       
#   1.9     19-Mar-2016 (bm) Updated code to handle Mac OSX Java MIDI implementation problem, which does not
#                       allow for closing and re-opening an external MIDI device.  Now, we maintain existing 
#                       connection(s) and reuse them.  Close and re-open, on Mac, simply re-initializes 
#                       existing MIDI device object(s), instead of default behavior, which is to create a new object
#                       (the latter still supported on other operating systems).
#                       Also, now, we allow for multiple callbacks to be registered for each event type
#                       (i.e., we accumulate callback registrations in a list) to be consistent with OscIn class.
#
#   1.8     07-Jan-2016 (bm) Fixed pesky bug with closing MidiIn objects (was using the wrong variable,
#                       but error was not being printed because code is running inside Java - ouch!).  
#                       Now, _stopActiveMidiObjects_ corrently closes MidiIn objects by calling 
#                       midiIn.midiDevice.close().  Also, added MidiIn.open() and MidiIn.close()
#
#   1.7     06-Dec-2014 (bm) Added MidiIn showMessages() and hideMessages() to turn on and off printing 
#                       of incoming MIDI messages.  This allows to easily explore what messages are being send 
#                       by a particular device (so that they can be mapped to different functions).
#
#   1.6     19-Nov-2014 (bm) Fixed bug in cleaning up objects after JEM's stop button is pressed -
#                       if list of active objects already exists, we do not redefine it - thus, we 
#                       do not lose older objects, and can still clean them up.
#
#   1.5     06-Nov-2014 (bm)  Added functionality to stop midi objects via JEM's Stop button
#                       - see registerStopFunction().
#
#   1.4    13-May-2013  (bm) Function MidiIn.onInput() now has an eventType parameter (i.e., the number
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
#   1.3    12-May-2013  (bm) Added MidiIn functions onNoteOn(), onNoteOff(), onSetInstrument()
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

# ***
# NOTE: Used to take care of Mac OSX pesky Java MIDI implementation problem 
#       (i.e. MIDI devices cannot be closed and re-opened)...
from platform import platform      


# used to keep track which midi objects are active, so we can stop them when
# JEM's Stop button is pressed

#try:
#
#   _ActiveMidiInObjects_         # if already defined (from an earlier run, do nothing, as it already contains material)
#   
#except:
#
#   _ActiveMidiInObjects_  = []   # first run - let's define it to hold active objects
#   _ActiveMidiOutObjects_ = []   # first run - let's define it to hold active objects

_ActiveMidiInObjects_  = []   # holds active MidiIn objects
_ActiveMidiOutObjects_ = []   # holds active MidiOut objects


# holds notes still on to prevent premature note-off for overlapping notes (only last note-off will be executed)
# - dictionary key is (note, channel) and value is count of notes currently playing on this channel
# (only when count is 1 will Play.frequencyOff() send a NOTE-OFF messsage for this channel-note pair)
#notesCurrentlyPlaying = {}
# notesCurrentlyPlaying should be a list of tuples to prevent the race condition that happened with the dictionary
notesCurrentlyPlaying = [] 


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

# The MIDI specification stipulates that pitch bend be a 14-bit value, where zero is 
# maximum downward bend, 16383 is maximum upward bend, and 8192 is the center (no pitch bend).
PITCHBEND_MIN = 0 
PITCHBEND_MAX = 16383 
PITCHBEND_NORMAL = 8192


# Handle Mac OS X Java MIDI problem, i.e., once a MIDI device is opened, we cannot close it and reopen it,
# without closing down JEM (which we do not want)...
# Solution:  Keep a list of all opened input MIDI devices.  When MidiIn constructor is called again, we check
# against this list, and if a defice is in it, we simply reuse it without letting the end-user know (from their
# perspective it looks like we reopen it).  Also, when closing a MidiIn device, if on a Mac we simply clean up
# things, but do NOT actually close it (as this leads to an unstable state manytimes).  In essence, on a Mac,
# we are faking closing and subsequent openings of a MidiIn device.

from platform import platform   # to find out what OS we are using (looking for Mac OS X)

# are we on a Mac?
if "Mac_OS_X" in platform():

   if "Mac_OS_X_MidiIn_Devices" not in globals():   # initialize ONLY if first time!
      Mac_OS_X_MidiIn_Devices = {}   # holds resources of opened MidiIn devices (so we can reuse them, as needed)


def freqToNote(frequency):
   """Converts frequency to the closest MIDI note number with pitch bend value 
      for finer control.  A4 corresponds to the note number 69 (concert pitch
      is set to 440Hz by default).  The default pitch bend range is 4 half tones.
   """
   
   from math import log
   
   concertPitch = 440.0   # 440Hz
   bendRange = 4          # 4 half tones (2 below, 2 above)
    
   x = log(frequency / concertPitch, 2) * 12 + 69
   note = round(x)
   pitchBend = round((x - note) * 8192 / bendRange * 2)

   return int(note), int(pitchBend)


def noteToFreq(note):
   """Converts a MIDI note to the corresponding frequency.  A4 corresponds to the note number 69 (concert pitch
      is set to 440Hz by default).
   """
   
   concertPitch = 440.0   # 440Hz

   frequency = concertPitch * 2 ** ( (note - 69) / 12.0 )
    
   return frequency


class MidiIn(Receiver):

   def __init__(self, preferredDevice=""):
      
      # NOTE: Note that some devices, once closed, cannot be reopened.
   
      self.preferredDevice = preferredDevice    # remember default choice (if any)

      self.display        = None       # holds selection display for available MIDI devices

      self.waitingToSetup = True       # used to busy-wait until user has selected a MIDI input device 
      self.midiDevice = None           # holds MIDI input device asscociated with this instance
      self.midiDeviceName = None       # holds MIDI input device name (text to be displayed)
      self.midiTransmitter = None      # holds the selected device's MIDI transmitter (to receive MIDI messages from)

      self.eventHandlers = {}          # holds callback functions to be called upon receipt of any input events
                                       # (events are keys, functions are dictionary values)

      # prompt the user to connect a MIDI device to this object
      self.selectMidiInput( self.preferredDevice )            
      
      # and, since above GUI is asynchronous, wait until user has selected a MIDI input device
      while(self.waitingToSetup):
         sleep(0.1)    # sleep for 0.1 second

      # if we reach this point, the user has made a selection, so we should be good to go
      
      self.showIncomingMessages = True   # print all incoming MIDI messages by default
      
      # remember that this MidiIn has been created and is active (so that it can be stopped/terminated by JEM, if desired)
      _ActiveMidiInObjects_.append(self)


   # *** required by Receiver interface
   def close(self):
      '''Callback used by Receiver interface to close MIDI input device to free any resources it is using'''

     # NOTE: Some MIDI devices on some systems, once closed, cannot be reopened.

      if self.midiDevice:

         # if on a Mac, keep this device open, as we cannot close it and open it again
         if "Mac_OS_X" in platform():

         	# just clean up this instance (e.g., as if it does not exist)
         	self.hideMessages()       # show no incoming events through this instance
         	self.eventHandlers = {}   # clear all event handlers (i.e., reset all functionality assigned to incoming events)

         else:  # not an a Mac, so proceed as normal

            self.midiTransmitter.close()
            self.midiDevice.close()


   def selectMidiInput(self, preferredDevice=""):
      """ Opens preferred MIDI device for input. If this device does not exist,
          creates display with available input MIDI devices and allows to select one.
      """

      self.preferredDevice = preferredDevice                # remember default choice (if any)

      availDevices = MidiSystem.getMidiDeviceInfo()         # get information about MIDI devices available to the system
      self.inputDevices = {}                                # get name of device for more user friendly display

      # find all input MIDI devices
      for device in availDevices:

         midiDevice = MidiSystem.getMidiDevice(device)      # get selected MIDI device from system

         # this is an input device?
         if midiDevice.getMaxTransmitters() != 0:

            # yes, so remember it
            key = device.getVendor() + " " + device.getName()  # create a nice dictionary key
            self.inputDevices[key] = device                    # and store it
            
      # now, only available MIDI input devices are stored in self.inputDevices

      # check if preferredDevice is available
      if self.preferredDevice in self.inputDevices.keys():

         # yes it is, so select it and open it
         self.openInputDevice( self.preferredDevice )

      else:  # otherwise, create menu with available devices to select

         # create selection GUI
         self.display = Display("Select MIDI Input", 400, 125) # display info to user

         self.display.drawLabel('Select a MIDI input device from the list', 45, 30)

         # create dropdown list of available MIDI input devices
         items = self.inputDevices.keys()
         items.sort()
         deviceDropdown = DropDownList(items, self.openInputDevice)
         self.display.add(deviceDropdown, 40, 50)
         self.display.setColor( Color(124, 201, 251) )   # set color to shade of blue (for input)
      
   # callback for dropdown list - called when user selects a MIDI device
   def openInputDevice(self, selectedItem):

      # open selected input device
      print 'MIDI input device set to "' + selectedItem + '".'   # let them know
      deviceInfo = self.inputDevices[selectedItem]               # get device info from dictionary

      # are we on a Mac, and if so, have we opened this input device before?
      if "Mac_OS_X" in platform() and Mac_OS_X_MidiIn_Devices.has_key(deviceInfo):

      	 # reuse input device resources
      	 midiDevice, transmitter = Mac_OS_X_MidiIn_Devices[deviceInfo]  # get resources

      	 # update class attributes using existing resources
         self.midiDevice = midiDevice
         self.midiDeviceName = selectedItem                     # remember device name (in text)
         self.midiTransmitter = transmitter
         self.midiTransmitter.setReceiver(self)
         #self.midiDevice.open()   # already open

      else:    # not on a Mac (or on a Mac but we have not opened this input device before), so proceed as normal

         self.midiDevice = MidiSystem.getMidiDevice(deviceInfo) # get selected device from Midi System
         self.midiDeviceName = selectedItem                     # remember device name (in text)
         self.midiTransmitter = self.midiDevice.getTransmitter()
         self.midiTransmitter.setReceiver(self)
         self.midiDevice.open()   # open it

         # if on a Mac, remember this opened device, so we do not have to open it again
         if "Mac_OS_X" in platform():

            # remember input device resources
            Mac_OS_X_MidiIn_Devices[deviceInfo] = [self.midiDevice, self.midiTransmitter]


      # selection has been made so close display and exit busy loop in constructor
      self.waitingToSetup = False                           # no longer waiting to be setup, set to False so we can move on

      # is a display showing?
      if self.display:
         self.display.close()     # yes, so close it -- no longer needed


   def onNoteOn(self, function):
      """
      Set up a callback function to handle only noteOn MIDI input events.
      """
      if self.eventHandlers.has_key( NOTE_ON ):
      	 self.eventHandlers[NOTE_ON].append( function )  # add to existing list of callback functions for this event
      else:   # thjis is the first time we register a callback function for this event, so 
         self.eventHandlers[NOTE_ON] = [function]        # create new list of callback functions

   def onNoteOff(self, function):
      """
      Set up a callback function to handle only noteOff MIDI input events.
      """
      if self.eventHandlers.has_key( NOTE_OFF ):
      	 self.eventHandlers[NOTE_OFF].append( function )  # add to existing list of callback functions for this event
      else:   # thjis is the first time we register a callback function for this event, so 
         self.eventHandlers[NOTE_OFF] = [function]        # create new list of callback functions

   def onSetInstrument(self, function):
      """
      Set up a callback function to handle only setInstrument MIDI input events.
      """
      if self.eventHandlers.has_key( SET_INSTRUMENT ):
      	 self.eventHandlers[SET_INSTRUMENT].append( function )  # add to existing list of callback functions for this event
      else:   # thjis is the first time we register a callback function for this event, so 
         self.eventHandlers[SET_INSTRUMENT] = [function]        # create new list of callback functions

   def onInput(self, eventType, function):
      """
      Associates an incoming event type with a callback function.  Can be used repeatedly to associate different
      event types with different callback functions (one function per event type).  If called more than once for the
      same event type, only the latest callback function is retained (the idea is that this function can contain all
      that is needed to handle this event type).  If eventType is ALL_EVENTS, the associated callback function is 
      called for all events not handled already.
      """
      if self.eventHandlers.has_key( eventType ):
      	 self.eventHandlers[eventType].append( function )  # add to existing list of callback functions for this event
      else:   # thjis is the first time we register a callback function for this event, so 
         self.eventHandlers[eventType] = [function]        # create new list of callback functions

   def showMessages(self):
      """
      Turns on printing of incoming MIDI messages (useful for exploring what MIDI messages 
      are generated by a particular device).
      """
      self.showIncomingMessages = True

   def hideMessages(self):
      """
      Turns off printing of incoming MIDI messages.
      """
      self.showIncomingMessages = False


   # *** required by Receiver interface
   def send(self, message, timeStamp):
      """Callback used by Receiver interface to handle incoming MIDI messages."""

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
            functions = []     # initialize
            if self.eventHandlers.has_key( eventType ):
                functions.extend( self.eventHandlers[ eventType ] )
            elif self.eventHandlers.has_key( ALL_EVENTS ):
                functions.extend( self.eventHandlers[ ALL_EVENTS ] )
                
            # call all functions (if any) with the input message
            for function in functions:
               try:	
                  function(eventType, msgChannel, msgData1, msgData2)
               except Exception, e:
                  # print error to console (since, otherwise, error is hidden, due to this happening inside Java)
                  print repr(e)

            # determine if we need to print out the message
            if self.showIncomingMessages:   # echo print incoming MIDI messages?
               print self.midiDeviceName + " (MidiIn) - Event Type:", eventType, ", Channel:", msgChannel, ", Data 1:", msgData1, ", Data 2:", msgData2

            
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


   # initialize pitchbend across channels to 0
   global CURRENT_PITCHBEND
   CURRENT_PITCHBEND = {}    # holds pitchbend to be used when playing a note / frequency (see below)
   for i in range(16):
      CURRENT_PITCHBEND[i] = 0   # set this channel's pitchbend to zero

   from jm.music.data import *

   def __init__(self, preferredDevice=""):

      self.preferredDevice = preferredDevice    # remember default choice (if any)

      self.display        = None       # holds selection display for available MIDI devices

      self.waitingToSetup = True       # used to busy-wait until user has selected a MIDI input device 
      self.midiDevice     = None       # holds the selected output MIDI device (we may want to close it)
      self.midiDeviceName = None       # holds MIDI output device name (text to be displayed)
      self.midiReceiver   = None       # holds the selected device's MIDI receiver (to send MIDI messages to)

      self.instrument = {}        # holds current instrument for each channel
      for channel in range(16):   # initialize all to PIANO (default)
         self.instrument[channel] = 0  

      self.volume = {}            # holds current global volume
      for channel in range(16):   # initialize all to max volume
         self.volume[channel] = 127                

      self.panning = {}           # holds current global panning
      for channel in range(16):   # initialize all to center panning
         self.panning[channel] = 63                

      # prompt user to select an existing output MIDI device
      self.selectMidiOutput( self.preferredDevice )

      # and, since above GUI is asynchronous, wait until user has selected a MIDI output device
      while(self.waitingToSetup):
         sleep(0.1)    # sleep for 0.1 second

      # if we reach this point, the user has made a selection, so we should be good to go

      # remember that this MidiIn has been created and is active (so that it can be stopped/terminated by JEM, if desired)
      _ActiveMidiOutObjects_.append(self)
      

   def close(self):
      '''Close MIDI output device'''

      # NOTE: Some MIDI devices on some systems, once closed, cannot be reopened.

      if self.midiDevice:

      	 self.midiDevice.close()

         # NOTE: maybe we shoud also send a global noteOff message to all channels?


   def play(self, material):
      """Play jMusic material (Score, Part, Phrase, Note) using the MIDI output device."""
      
      from music import Note, Phrase, Part, Score, REST
      from jm.music.data import Phrase as jPhrase   # since we redefine Phrase
      from jm.music.data import Note as jNote  # needed to wrap more functionality below

      # do necessary datatype wrapping (MidiSynth() expects a Score)
      if type(material) == Note:
         material = Phrase(material)
      if type(material) == jNote:    # (also wrap jMusic default Notes, in addition to our own)
         material = Phrase(material)
      if type(material) == Phrase:   # no elif - we need to successively wrap from Note to Score
         material = Part(material)
         material.setInstrument(-1)     # indicate no default instrument (needed to access global instrument)
      if type(material) == jPhrase:  # (also wrap jMusic default Phrases, in addition to our own)
         material = Part(material)
         material.setInstrument(-1)     # indicate no default instrument (needed to access global instrument)
      if type(material) == Part:     # no elif - we need to successively wrap from Note to Score
         material = Score(material)
      if type(material) == Score:

         # we are good - let's play it then!

         score = material   # by now, material is a score, so create an alias (for readability)


         # loop through all parts and phrases to get all notes
         noteList = []               # holds all notes
         tempo = score.getTempo()    # get global tempo (can be overidden by part and phrase tempos)
         for part in score.getPartArray():   # traverse all parts
            channel = part.getChannel()        # get part channel
            instrument = self.getInstrument(channel)  # get global instrument for this channel
            if part.getInstrument() > -1:      # has the part instrument been set?
               instrument = part.getInstrument()  # yes, so it takes precedence
            if part.getTempo() > -1:           # has the part tempo been set?
               tempo = part.getTempo()            # yes, so update tempo
            for phrase in part.getPhraseArray():   # traverse all phrases in part
               if phrase.getInstrument() > -1:        # is this phrase's instrument set?
                  instrument = phrase.getInstrument()    # yes, so it takes precedence
               if phrase.getTempo() > -1:          # has the phrase tempo been set?
                  tempo = phrase.getTempo()           # yes, so update tempo
     
               # time factor to convert time from jMusic Score units to milliseconds
               # (this needs to happen here every time, as we may be using the tempo from score, part, or phrase)
               FACTOR = 1000 * 60.0 / tempo   

               # process notes in this phrase
               startTime = phrase.getStartTime() * FACTOR   # in milliseconds
               for note in phrase.getNoteArray():
                  frequency = note.getFrequency()
                  panning = note.getPan()
                  panning = mapValue(panning, 0.0, 1.0, 0, 127)    # map from range 0.0..1.0 (Note panning) to range 0..127 (as expected by Java synthesizer)
                  start = int(startTime)                           # remember this note's start time (in milliseconds)

                  # NOTE:  Below we use note length as opposed to duration (getLength() vs. getDuration())
                  # since note length gives us a more natural sounding note (with proper decay), whereas 
                  # note duration captures the more formal (printed score) duration (which sounds unnatural).
                  duration = int(note.getLength() * FACTOR)             # get note length (as oppposed to duration!) and convert to milliseconds
                  startTime = startTime + note.getDuration() * FACTOR   # update start time (in milliseconds)
                  velocity = note.getDynamic()
                   
                  # accumulate non-REST notes
                  if (frequency != REST):
                     noteList.append((start, duration, frequency, velocity, channel, instrument, panning))   # put start time first and duration second, so we can sort easily by start time (below),
                     # and so that notes that are members of a chord as denoted by having a duration of 0 come before the note that gives the specified chord duration
                   
         # sort notes by start time
         noteList.sort()

         # Schedule playing all notes in noteList
         chordNotes = []      # used to process notes belonging in a chord
         for start, duration, pitch, velocity, channel, instrument, panning in noteList:
            # set appropriate instrument for this channel
            self.setInstrument(instrument, channel)

            # handle chord (if any)
            # Chords are denoted by a sequence of notes having the same start time and 0 duration (except the last note
            # of the chord).
            if duration == 0:   # does this note belong in a chord?
               chordNotes.append([start, duration, pitch, velocity, channel, panning])  # add it to the list of chord notes
               
            elif chordNotes == []:   # is this a regular, solo note (not part of a chord)?
               
               # yes, so schedule it to play via a Play.note event
               self.note(pitch, start, duration, velocity, channel, panning)
               #print "MidiOut.note(" + str(pitch) + ", " + str(start) + ", " + str(duration) + ", " + str(velocity) + ", " + str(channel) + ", " + str(panning) + ")"

            else:   # note has a normal duration and it is part of a chord

               # first, add this note together with this other chord notes
               chordNotes.append([start, duration, pitch, velocity, channel, panning])
               
               # now, schedule all notes in the chord list using last note's duration
               for start, ignoreThisDuration, pitch, velocity, channel, panning in chordNotes:
                  # schedule this note using chord's duration (provided by the last note in the chord)
                  self.note(pitch, start, duration, velocity, channel, panning)
                  #print "Chord: MidiOut.note(" + str(pitch) + ", " + str(start) + ", " + str(duration) + ", " + str(velocity) + ", " + str(channel) + ", " + str(panning) + ")"
               # now, all chord notes have been scheduled

               # so, clear chord notes to continue handling new notes (if any)
               chordNotes = []
   
         # now, all notes have been scheduled for future playing - scheduled notes can always be stopped using
         # JEM's stop button - this will stop all running timers (used by Play.note() to schedule playing of notes)
         #print "Play.note(" + str(pitch) + ", " + str(int(start * FACTOR)) + ", " + str(int(duration * FACTOR)) + ", " + str(velocity) + ", " + str(channel) + ")"

      else:   # error check    
         print "Play.midi(): Unrecognized type " + str(type(material)) + ", expected Note, Phrase, Part, or Score."


   # NOTE:  Here we connect noteOn() and frequencyOn() with noteOnPitchBend() to allow for 
   # playing microtonal music.  Although this may seem as cyclical (i.e., that in noteOn() we 
   # convert pitch to frequency, and then call frequencyOn() which convert the frequency back to pitch,
   # so that it can call noteOnPitchBend() ), this is the only way we can make everything work.
   # We are constrained by the fact that jMusic Note objects are limited in how they handle pitch and
   # frequency (i.e., that creating a Note with pitch will set the Note's corresponding frequency,
   # but not the other way around), and the fact that we can call Note.getFrequency() above in Play.midi()
   # without problem, but NOT Note.getPitch(), which will crash if the Note was instantiated with a frequency
   # (i.e., pitch is not available / set).
   # Therefore, we need to make the run about here, so that we keep everything else easier to code / maintain,
   # and also keep the API (creating and play notes) simpler.  So, do NOT try to simplify the following code,
   # as it is the only way (I think) that can make everything else work simply - also see Play.midi().
   def noteOn(self, pitch, velocity=100, channel=0, panning = -1):
      """Send a NOTE_ON message for this pitch to the selected output MIDI device.  Default panning of -1 means to
         use the default (global) panning setting of the selected MIDI device."""

      if (type(pitch) == int) and (0 <= pitch <= 127):   # a MIDI pitch?
         # yes, so convert pitch from MIDI number (int) to Hertz (float)
         pitch = noteToFreq(pitch)       

      if type(pitch) == float:        # a pitch in Hertz?
         self.frequencyOn(pitch, velocity, channel, panning)  # start it
                  
      else:         

         print "MidiOut.noteOn(): Unrecognized pitch " + str(pitch) + ", expected MIDI pitch from 0 to 127 (int), or frequency in Hz from 8.17 to 12600.0 (float)."


   def frequencyOn(self, frequency, velocity=100, channel=0, panning = -1):
      """Send a NOTE_ON message for this frequency (in Hz) to the selected output MIDI device.  Default panning of -1 means to
         use the default (global) panning setting of the MIDI device."""
      
      if (type(frequency) == float) and (8.17 <= frequency <= 12600.0): # a pitch in Hertz (within MIDI pitch range 0 to 127)?

         pitch, bend = freqToNote( frequency )                     # convert to MIDI note and pitch bend

         # also, keep track of how many overlapping instances of this pitch are currently sounding on this channel
         # so that we turn off only the last one - also see frequencyOff()
         noteID = (pitch, channel)              # create an ID using pitch-channel pair
         notesCurrentlyPlaying.append(noteID)   # add this note instance to list

         self.noteOnPitchBend(pitch, bend, velocity, channel, panning)      # and start it 

      else:         

         print "MidiOut.frequencyOn(): Invalid frequency " + str(frequency) + ", expected frequency in Hz from 8.17 to 12600.0 (float)."
 

   def noteOff(self, pitch, channel=0):
      """Send a NOTE_OFF message for this pitch to the selected output MIDI device."""

      if (type(pitch) == int) and (0 <= pitch <= 127):   # a MIDI pitch?
         # yes, so convert pitch from MIDI number (int) to Hertz (float)
         pitch = noteToFreq(pitch)       

      if type(pitch) == float:        # a pitch in Hertz?
         self.frequencyOff(pitch, channel)  # stop it
                  
      else:         

         print "MidiOut.noteOff(): Unrecognized pitch " + str(pitch) + ", expected MIDI pitch from 0 to 127 (int), or frequency in Hz from 8.17 to 12600.0 (float)."

   def frequencyOff(self, frequency, channel=0):
      """Send a NOTE_OFF message for this frequency (in Hz) to the selected output MIDI device."""
      
      if (type(frequency) == float) and (8.17 <= frequency <= 12600.0): # a frequency in Hertz (within MIDI pitch range 0 to 127)?

         pitch, bend = freqToNote( frequency )                     # convert to MIDI note and pitch bend

         # also, keep track of how many overlapping instances of this frequency are currently playing on this channel
         # so that we turn off only the last one - also see frequencyOn()
         noteID = (pitch, channel)                   # create an ID using pitch-channel pair

         # next, remove this noteID from the list, so that we may check for remaining instances
         notesCurrentlyPlaying.remove(noteID)        # remove noteID
         if noteID not in notesCurrentlyPlaying:     # is this last instance of note?

            # yes, so turn it off!
            self.sendMidiMessage(128, channel, pitch, 0) 

      else:     # frequency was outside expected range    

         print "MidiOut.frequencyOff(): Invalid frequency " + str(frequency) + ", expected frequency in Hz from 8.17 to 12600.0 (float)."

      # NOTE: Just to be good citizens, also turn pitch bend to normal (i.e., no bend).
      # Play.setPitchBend(0, channel)


   def note(self, pitch, start, duration, velocity=100, channel=0, panning = -1):
      """Plays a note with given 'start' time (in milliseconds from now), 'duration' (in milliseconds
         from 'start' time), with given 'velocity' on 'channel'.  Default panning of -1 means to
         use the default (global) panning setting of the MIDI output device. """ 
         
      # TODO: We should probably test for negative start times and durations.
         
      # create a timer for the note-on event
      noteOn = Timer2(start, self.noteOn, [pitch, velocity, channel, panning], False)

      # create a timer for the note-off event
      noteOff = Timer2(start+duration, self.noteOff, [pitch, channel], False)

      # and activate timers (set things in motion)
      noteOn.start()
      noteOff.start()
      
      # NOTE:  Upon completion of this function, the two Timer objects become unreferenced.
      #        When the timers elapse, then the two objects (in theory) should be garbage-collectable,
      #        and should be eventually cleaned up.  So, here, no effort is made in reusing timer objects, etc.

   def frequency(self, frequency, start, duration, velocity=100, channel=0, panning = -1):
      """Plays a frequency with given 'start' time (in milliseconds from now), 'duration' (in milliseconds
         from 'start' time), with given 'velocity' on 'channel'.  Default panning of -1 means to
         use the default (global) panning setting of the MIDI output device.""" 
         
      # NOTE:  We assume that the end-user will ensure that concurrent microtones end up on
      # different channels.  This is needed since MIDI has only one pitch band per channel,
      # and most microtones require their unique pitch bending.

      # TODO: We should probably test for negative start times and durations.
         
      # create a timer for the frequency-on event
      frequencyOn = Timer2(start, self.frequencyOn, [frequency, velocity, channel, panning], False)

      # create a timer for the frequency-off event
      frequencyOff = Timer2(start+duration, self.frequencyOff, [frequency, channel], False)

      # call pitchBendNormal to turn off the timer, if it is on
      #setPitchBendNormal(channel)
      # and activate timers (set things in motion)
      frequencyOn.start()
      frequencyOff.start()
 
      #setPitchBendNormal(channel, start+duration, True)


   def setPitchBend(self, bend = 0, channel=0):
      """Set global pitchbend variable to be used when a note / frequency is played."""

      CURRENT_PITCHBEND[channel] = bend #this pitchbend will now be calculated into the total pitchbend by noteOnPitchBend()
      
   def getPitchBend(self, channel=0):
      """returns the current pitchbend for this channel."""
      
      return CURRENT_PITCHBEND[channel] 


   def noteOnPitchBend(self, pitch, bend = 0, velocity=100, channel=0, panning = -1):
      """Send a NOTE_ON message for this pitch and pitch bend to the selected output MIDI device.  
         Default panning of -1 means to use the default (global) panning setting of the MIDI device."""
            
      self.setPitchBend(bend, channel)  # remember current pitchbend for this channel

      # now, really set the pitchbend on the MIDI output device (this is the only place this is done!)      

      # NOTE: The MIDI specification states that pitch is a 14-bit value, where zero is 
      # maximum downward bend, 16383 is maximum upward bend, and 8192 is center - no pitch bend.
      # Here we adjust for no pitch bend (center) to be 0, max downward bend to be -8192, and
      # max upward bend to be 8191.  Also, we add the current pitchbend as set previously.
      pitchbend = bend + PITCHBEND_NORMAL + CURRENT_PITCHBEND[channel]   # calculate pitchbend to set
      if (pitchbend <= PITCHBEND_MAX) and (pitchbend >= PITCHBEND_MIN):  # is pitchbend within appropriate range?

         msb = int(pitchbend) / 128 # find the msb values for the first byte of pitchbend data
         lsb = int(pitchbend) % 128 # find the lsb values for the finer tuning byte of pitchbend data

         # send pitch bend MIDI message
         # *** see http://computermusicresource.com/MIDI.Commands.html
         self.sendMidiMessage(224, channel, lsb, msb)

      else:     # frequency was outside expected range    

         print "MidiOut.noteOnPitchBend(): Invalid pitchbend " + str(pitchbend - PITCHBEND_NORMAL) + ", expected pitchbend in range -8192 to 8192."

      # and send the message to start the note on this channel
      if panning != -1:                              # if we have a specific panning,
         
         self.sendMidiMessage(176, channel, 10, panning)   # then, use it (otherwise let default / global panning stand)
         # (see controller numbers - http://www.indiana.edu/~emusic/cntrlnumb.html)

      self.sendMidiMessage(144, channel, pitch, velocity)  # send the message


   def allNotesOff(self):
      """It turns off all notes on all channels."""

      self.allFrequenciesOff()   
      

   def allFrequenciesOff(self):
      """It turns off all notes on all channels."""

      for channel in range(16):  # cycle through all channels

         self.sendMidiMessage(176, channel, 123, 0)        # send message for "All Notes Off" (123)
         # (see controller numbers - http://www.indiana.edu/~emusic/cntrlnumb.html)

         # also reset pitch bend
         self.setPitchBend(0, channel)      


   def stop(self):
      """It stops all MIDI music from sounding."""
      
      # NOTE:  This could also handle self.note() notes, which may have been
      #        scheduled to start sometime in the future.  For now, we assume that timer.py
      #        (which provides Timer objects) handles stopping of timers on its own.  If so,
      #        this takes care of our problem, for all practical purposes.  It is possible
      #        to have a race condition (i.e., a note that starts playing right when stop()
      #        is called, but a second call of stop() (e.g., double pressing of a stop button)
      #        will handle this, so we do not concern ourselves with it.
            
      # then, stop all sounding notes
      self.allNotesOff()

      # NOTE: In the future, we may also want to handle scheduled notes through self.note().  This could be done
      # by creating a list of Timers created via note() and looping through them to stop them here.


   def setInstrument(self, instrument, channel=0):
      """Sets 'channel' to 'instrument' for this channel of  the  output MIDI device.""" 

      self.instrument[channel] = instrument                # remember it
      self.sendMidiMessage(192, channel, instrument, 0)    # and set it
      # (see controller numbers - http://www.indiana.edu/~emusic/cntrlnumb.html)

   def getInstrument(self, channel=0):
      """Gets the current instrument for this channel of the output MIDI device."""
      
      return self.instrument[channel]


   def setVolume(self, volume, channel=0):
      """Sets the current coarse volume for this channel of the output MIDI device."""
      
      self.volume[channel] = volume                    # remember it
      self.sendMidiMessage(176, channel, 7, volume)    # and set it (7 is controller number for global / main volume)
      # (see controller numbers - http://www.indiana.edu/~emusic/cntrlnumb.html)

   def getVolume(self, channel=0):
      """Gets the current coarse volume for this channel of the output MIDI device."""

      return self.volume[channel]


   def setPanning(self, panning, channel=0):
      """Sets the current panning setting for this channel of the output MIDI device."""
      
      self.panning[channel] = panning                   # remember it
      self.sendMidiMessage(176, channel, 10, panning)   # then, use it (otherwise let default / global panning stand)
      # (see controller numbers - http://www.indiana.edu/~emusic/cntrlnumb.html)

   def getPanning(self, channel=0):
      """Gets the current panning setting for this channel of the output MIDI device."""

      return self.panning[channel]

      
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
   
   def selectMidiOutput(self, preferredDevice=""):
      """ Opens preferred MIDI device for output. If this device does not exist,
          creates display with available output MIDI devices and allows to select one.
      """

      self.preferredDevice = preferredDevice                # remember default choice (if any)

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

      # check if preferredDevice is available
      if self.preferredDevice in self.outputDevices.keys():

         # yes it is, so select it and open it
         self.openOutputDevice( self.preferredDevice )

      else:  # otherwise, create menu with available devices to select

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
      print 'MIDI output device set to "' + selectedItem + '".'   # let them know
      deviceInfo = self.outputDevices[selectedItem]               # get device info from dictionary
      self.midiDevice = MidiSystem.getMidiDevice(deviceInfo)      # get selected device from Midi System
      self.midiDeviceName = selectedItem                          # remember device text name
      self.midiDevice.open()                                      # open it
      self.midiReceiver = self.midiDevice.getReceiver()           # get receiver to send messages to

      # selection has been made so close display and exit busy loop in constructor
      self.waitingToSetup = False                            # no longer waiting to be setup, set to False so we can move on

      # is a display showing?
      if self.display:
         self.display.close()     # yes, so close it -- no longer needed


######################################################################################
# If running inside JEM, register function that stops everything, when the Stop button
# is pressed inside JEM.
######################################################################################

# function to stop and clean-up all active Midi objects
def _stopActiveMidiObjects_():

   global _ActiveMidiInObjects_, _ActiveMidiOutObjects_

   # stop MidiIn objects
   for midiIn in _ActiveMidiInObjects_:
      midiIn.close()     # this handles special case of being on a Mac 

   # stop MidiOut objects
   for midiOut in _ActiveMidiOutObjects_:
   	  midiOut.stop()     # first, stop all notes playing
   	  midiOut.close()

   # ***
   # NOTE:  Here we take care of Mac OSX pesky Java MIDI implementation problem 
   # (i.e. MIDI devices cannot be closed and re-opened)...
   if "Mac_OS_X" in platform():
      # ***
      #print "MIDI: We are on a Mac!"
      pass    # do nothing (we keep MIDI objects around, and reinitialize them elsewhere)

   else:  # we are not on a Mac, so proceed as usual
          
      # then, delete all of them
      for midiObject in (_ActiveMidiInObjects_ + _ActiveMidiOutObjects_):
         del midiObject

      # also empty list, so things can be garbage collected
      _ActiveMidiInObjects_ = []   # remove access to deleted items   
      _ActiveMidiOutObjects_ = []   # remove access to deleted items   

# now, register function with JEM (if possible)
try:

    # if we are inside JEM, registerStopFunction() will be available
    registerStopFunction(_stopActiveMidiObjects_)   # tell JEM which function to call when the Stop button is pressed

except:  # otherwise (if we get an error), we are NOT inside JEM 

    pass    # so, do nothing.



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
   

