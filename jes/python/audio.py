################################################################################################################
# audio.py      Version 2.1         09-Jun-2016       Chris Benson and Bill Manaris
#
###########################################################################
#
# This file is part of Jython Music.
#
# Copyright (C) 2015 Chris Benson and Bill Manaris
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
# Imports jSyn packages into jython.  Also provides additional functionality related to audio manipulation and playback.
#
#
# REVISIONS:
#
#   2.1     09-Jun-2016 (cb) Reverted jSyn imports to global level to fix import problem in some JEM installations.
#
#   2.0     26-Dec-2015 (bm,cb) Updated the jSyn engine startup to fix an error with some Windows boxes (actually,
#                       their audio cards) which do not support little endian.  Now, we poll the available sound cards
#                       and let the user (i.e., programmer - whoever imported audio.py) to select which audio card
#                       they wish to use.  This provides a little more visibility in the inner workings, and allows
#                       the user to try different audio cards, for different tasks (and potentially recover from the
#                       little endian error, if it is present).
#
#   1.0     30-Oct-2014 (bm)    First draft.

from music import *
from math import *
from java.io import *
from gui import *
from time import sleep

from com.jsyn import JSyn
from com.jsyn.data import FloatSample
from com.jsyn.unitgen import LineIn,LineOut, Pan, VariableRateMonoReader, VariableRateStereoReader, LinearRamp, FixedRateMonoWriter, FixedRateStereoWriter
from com.jsyn.util import SampleLoader

##### jSyn synthesizer ######################################
# NOTE:  music.py (imported above) starts its own instance of the jSyn synthesizer.  We chose to simply overwrite
# the variable jSyn (see later below) just in case there was something already playing, so that we don't stop it
# (in case of, say, interactive, live coding).
#
# If the above is not an issue, simply uncomment the following del statement:
#
# del jSyn    # delete music.py jSyn instance


class jSyn_AudioEngine():
   """Encasulates a jSyn synthesizer.  Only one may exist (no need for more).
      We modularize the synth and its operations in a class for convenience.
   """
   instance = None      # only one instance allowed (no need for more)


   def __init__(self):

      if jSyn_AudioEngine.instance == None:  # first time?

         self.synth = JSyn.createSynthesizer()   # create synthesizer
         jSyn_AudioEngine.instance = self        # remember the only allowable instance
         # create device manager for sound card to poll for audio device information (name, device id, number of channels)
         self.audioDeviceManager = self.synth.getAudioDeviceManager()
         self.deviceCount = self.audioDeviceManager.getDeviceCount()    # get number of audio devices (both input and output) on computer

         self.chosenInputDevice = -1                  # set audio input device to default
         self.chosenOutputDevice = -1                 # set audio output device to default
         self.inputDevices = []                  # contains list of input device dictionaries available
         self.outputDevices = []                 # contains list of output device dictionaries available

         # Sets self.chosenInputDevice to the input device chosen by the user as a dictionary.
         # Sets self.chosenOutputDevice to the output device chosen by the user as a dictionary.
         self.setAudioDevices()


         print "Here is the chosen Input! ", self.chosenInputDevice
         print "Here is the chosen Output! ", self.chosenOutputDevice
         self.FRAMERATE = 44100                 # default frame rate
         self.inputPortID = self.chosenInputDevice['DeviceID']   # use chosen audio input
         self.numberInputs = self.chosenInputDevice['NumInputs']          # use chosen amount of audio input channels
         self.outputPortID = self.chosenOutputDevice['DeviceID']          # use default audio output
         self.numberOutputs = self.chosenOutputDevice['NumOutputs']       # stereo (use 1 for mono)

         self.samples = []                         # holds audio samples connected to synthesizer

      else:                                  # an instance already exists
         print "Only one jSyn audio engine may exist (use existing one)."

   def setAudioDevices(self):

      self.waitingToSetupInput = True       # used to busy-wait until user has selected an audio input device
      self.waitingToSetupOutput = True      # used to busy-wait until user has selected an audio output device
      # prompt user to select an input and output device
      self.selectOutputLine()
      self.selectInputLine()

      # and, since above GUI is asynchronous, wait until user has selected an audio input and output device
      while(self.waitingToSetupInput or self.waitingToSetupOutput):
         sleep(0.1)    # sleep for 0.1 second

      # if we reach this point, the user has made a selection, so we should be good to go
      #print "You Got Out!!"



   # creates display with available audio input devices and allows user to select one
   def selectInputLine(self):

      self.liveSampleActive = True # a check to see if user can use the LiveSample class

      # find all audio devices
      for deviceID in range(self.deviceCount):

         # get num input channels for this device
         numInputs = self.audioDeviceManager.getMaxInputChannels(deviceID)

         # is this an input device?
         if  numInputs > 0:

            # menu item for drop-down menu consists of the device name (as returned by the system) and
            # the number of channels
            menuItem = str(self.audioDeviceManager.getDeviceName(deviceID)) + "  (" + str(numInputs) + " input channels)"
            deviceDict = {'Name':menuItem, 'NumInputs':numInputs, 'DeviceID':deviceID}  # create a dictionary
            self.inputDevices.append(deviceDict)                    # and store it

      # now, only available input devices are stored in self.inputDevices list as dictionaries

      # is there no available audio input devices
      if self.inputDevices == []:
         self.liveSampleActive = False # user cannot use LiveSample since no available audio input device exists
         menuItem = "You Have No Devices That Are Capable Of Recording Audio"
         deviceDict = {'Name':menuItem, 'NumInputs':0, 'DeviceID':-1}
         self.inputDevices.append(deviceDict)

      # create selection GUI
      self.displayInput = Display("Select Input Device", 500, 125) # display info to user

      self.displayInput.drawLabel('Select an Input device from the list', 45, 30)

      # create dropdown list of available audio input devices
      deviceDropdown = DropDownList([x['Name'] for x in self.inputDevices], self.getInputDevice)
      self.displayInput.add(deviceDropdown, 40, 50)
      self.displayInput.setColor( Color(124, 201, 251) )   # set color to shade of blue (for input)


   # callback for dropdown list - called when user selects an audio input device
   def getInputDevice(self, selectedItem):

      # gets selected input devices key
      inputDevice = (item for item in self.inputDevices if item['Name'] == selectedItem).next()
      self.chosenInputDevice = inputDevice

      # selection has been made so close display and exit busy loop in constructor
      self.waitingToSetupInput = False                           # no longer waiting to be setup, set to False so we can move on
      self.displayInput.hide()                                   # close display since it is no longer needed

   # creates display with available audio output devices and allows the user to select one
   def selectOutputLine(self):
       
      # find all audio devices
      for deviceID in range(self.deviceCount):

         # get num output channels for this device
         numOutputs = self.audioDeviceManager.getMaxOutputChannels(deviceID)

         # is this an output device?
         if  numOutputs > 0:

            # menu item for drop-down menu consists of the device name (as returned by the system) and
            # the number of channels
            menuItem = str(self.audioDeviceManager.getDeviceName(deviceID)) + "  (" + str(numOutputs) + " output channels)"
            deviceDict = {'Name':menuItem, 'NumOutputs':numOutputs, 'DeviceID':deviceID}  # create a dictionary
            self.outputDevices.append(deviceDict)                    # and store it

      # now, only available output devices are stored in self.outputDevices list as dictionaries
      if self.outputDevices == []:
         menuItem = "You Have No Devices That Are Capable Of Playing Audio"
         deviceDict = {'Name':menuItem, 'NumOutputs':0, 'DeviceID':-1}
         self.inputDevices.append(deviceDict)

      # create selection GUI
      self.displayOutput = Display("Select Output Device", 500, 125) # display info to user

      self.displayOutput.drawLabel('Select an Output device from the list', 45, 30)

      # create dropdown list of available audio output devices
      deviceDropdown = DropDownList([x['Name'] for x in self.outputDevices], self.getOutputDevice)
      self.displayOutput.add(deviceDropdown, 40, 50)
      self.displayOutput.setColor( Color(255, 153, 153) )   # set color to shade of red (for output)

    # callback for dropdown list - called when user selects an audio output device
   def getOutputDevice(self, selectedItem):

      # gets selected output dictionary from outputDevices dictionary key
      outputDevice = (item for item in self.outputDevices if item['Name'] == selectedItem).next()
      self.chosenOutputDevice = outputDevice

      # selection has been made so close display and exit busy loop in constructor
      self.waitingToSetupOutput = False                           # no longer waiting to be setup, set to False so we can move on
      self.displayOutput.hide()                                   # close display since it is no longer needed

   def start(self):
      """Starts the synthesizer."""
      # start the synth  (will need parameters if the sample is a live sample for number of inputs and their ID's)
      self.synth.start(self.FRAMERATE, self.inputPortID, self.numberInputs, self.outputPortID, self.numberOutputs)
      for sample in self.samples:   # and all the sample lineOut units
         sample.lineOut.start()

   def stop(self):
      """Stops the synthesizer."""

      self.synth.stop()             # stop the synth
      for sample in self.samples:   # and all the sample lineOut units
         sample.lineOut.stop()

   # *** This should probably be happening inside AudioSample() - much cleaner.
   def add(self, sample):
      """Connects an audio sample to the jSyn lineOut unit."""

      self.synth.add( sample.player )   # add the sample's player to the synth
      self.synth.add( sample.amplitudeSmoother )  # add the sample's amplitude linearRamp to the synth
      self.synth.add( sample.panLeft )  # add the sample's left pan control to the synth
      self.synth.add( sample.panRight ) # add the sample's right pan control to the synth
      self.synth.add( sample.lineOut )  # add the sample's output mixer to the synth
      self.samples.append( sample )     # remember this sample

   def addLive(self, sample):
      """Connects an live sample to the jSyn lineOut unit."""

      self.synth.add( sample.player )   # add the sample's player to the synth
      self.synth.add( sample.amplitudeSmoother ) # add the sample's amplitude linearRamp to the synth
      self.synth.add( sample.panLeft )  # add the sample's left pan control to the synth
      self.synth.add( sample.panRight ) # add the samples's right pan control to the synth
      self.synth.add( sample.lineOut )  # add the sample's lineOut to the synth
      self.synth.add( sample.lineIn  )
      self.synth.add( sample.writer )
      self.samples.append( sample )     # remember this sample


jSyn = jSyn_AudioEngine()
jSyn.start()


# used to keep track which AudioSample and LiveSample objects are active, so we can stop them when
# JEM's Stop button is pressed
__ActiveAudioSamples__ = []     # holds active LiveSample objects

##### AudioSample class ######################################

import os   # to check if provided filename exists

class AudioSample():
   """
   Encapsulates a sound object created from an external audio file, which can be played once,
   looped, paused, resumed, and stopped.  Also, each sound has a MIDI pitch associated with it
   (default is A4), so we can play different pitches with it (through pitch shifting).
   Finally, we can set/get its volume (0-127), panning (0-127), pitch (0-127), and frequency (in Hz).
   Ideally, an audio object will be created with a specific pitch in mind.
   Supported data formats are WAV or AIF files (16, 24 and 32 bit PCM, and 32-bit float).
   """

   def __init__(self, filename, pitch=A4, volume=127):

      # ensure the file exists (jSyn will NOT complain on its own)
      if not os.path.isfile(filename):
         raise ValueError("File '" + str(filename) + "' does not exist.")

      # file exists, so continue
      self.filename = filename

      # remember is sample is paused or not - needed for function isPaused()
      self.hasPaused = False

      # load and create the audio sample
      SampleLoader.setJavaSoundPreferred( False )  # use internal jSyn sound processes
      datafile = File(self.filename)               # get sound file
      self.sample = SampleLoader.loadFloatSample( datafile )  # load it as a a jSyn sample
      self.channels = self.sample.getChannelsPerFrame()       # get number of channels in sample

      # create lineOut unit (it mixes output to computer's audio (DAC) card)
      self.lineOut = LineOut()

      # create panning control (we simulate this using two pan controls, one for the left channel and
      # another for the right channel) - to pan we adjust their respective pan
      self.panLeft  = Pan()
      self.panRight = Pan()

      # NOTE: The two pan controls have only one of their outputs (as their names indicate)
      # connected to LineOut.  This way, we can set their pan value as we would normally, and not worry
      # about clipping (i.e., doubling the output amplitude).  Also, this works for both mono and
      # stereo samples.

      # create sample player (mono or stereo, as needed) and connect to lineOut mixer
      if self.channels == 1:    # mono audio?
         self.player = VariableRateMonoReader()                  # create mono sample player

         self.player.output.connect( 0, self.panLeft.input, 0)   # connect single channel to pan control
         self.player.output.connect( 0, self.panRight.input, 0)

      elif self.channels == 2:  # stereo audio?
         self.player = VariableRateStereoReader()                # create stereo sample player

         self.player.output.connect( 0, self.panLeft.input, 0)   # connect both channels to pan control
         self.player.output.connect( 1, self.panRight.input, 0)

      else:
         raise TypeError( "Can only play mono or stereo samples." )

      # now that we have a player, set the default and current pitches
      self.defaultPitch = pitch                                 # the default pitch of the audio sample
      self.pitch = pitch                                        # remember playback pitch (may be different from default pitch)
      self.frequency = self.__convertPitchToFrequency__(pitch)  # and corresponding frequency

      # now, connect pan control to mixer
      self.panLeft.output.connect( 0, self.lineOut.input, 0 )
      self.panRight.output.connect( 1, self.lineOut.input, 1 )

      # now, that panning is set up, initialize it to center
      self.panning = 63                # ranges from 0 (left) to 127 (right) - 63 is center
      self.setPanning( self.panning )  # and initialize

      # smooth out (linearly ramp) changes in player amplitude (without this, we get clicks)
      self.amplitudeSmoother = LinearRamp()
      self.amplitudeSmoother.output.connect( self.player.amplitude )   # connect to player's amplitude
      self.amplitudeSmoother.input.setup( 0.0, 0.5, 1.0 )              # set minimum, current, and maximum settings for control
      self.amplitudeSmoother.time.set( 0.0002 )                        # and how many seconds to take for smoothing amplitude changes

      # play at original pitch
      self.player.rate.set( self.sample.getFrameRate() )

      self.volume = volume           # holds current volume (0 - 127)
      self.setVolume( self.volume )  # set the desired volume

      # NOTE:  Adding to global jSyn synthesizer
      jSyn.add(self)   # connect sample unit to the jSyn synthesizer

      # remember that this AudioSample has been created and is active (so that it can be stopped by JEM, if desired)
      __ActiveAudioSamples__.append(self)


   ### functions to control playback and looping ######################
   def play(self, start=0, size=-1):
      """
      Play the sample once from the millisecond 'start' until the millisecond 'start'+'size'
      (size == -1 means to the end). If 'start' and 'size' are omitted, play the complete sample.
      """
      # for faster response, we restart playing (as opposed to queue at the end)
      if self.isPlaying():      # is another play is on?
         self.stop()            # yes, so stop it

      self.loop(1, start, size)


   def loop(self, times = -1, start=0, size=-1):
      """
      Repeat the sample indefinitely (times = -1), or the specified number of times
      from millisecond 'start' until millisecond 'start'+'size' (size == -1 means to the end).
      If 'start' and 'size' are omitted, repeat the complete sample.
      """

      startFrames = self.__msToFrames__(start)
      sizeFrames = self.__msToFrames__(size)

      self.lineOut.start()   # should this be here?

      if size == -1:   # to the end?
         sizeFrames = self.sample.getNumFrames() - startFrames  # calculate number of frames to the end

      if times == -1:   # loop forever?
         self.player.dataQueue.queueLoop( self.sample, startFrames, sizeFrames )

      else:             # loop specified number of times
         self.player.dataQueue.queueLoop( self.sample, startFrames, sizeFrames, times-1 )

   def stop(self):
      """
      Stop the sample play.
      """
      self.player.dataQueue.clear()
      self.hasPaused = False          # reset

   def isPlaying(self):
      """
      Returns True if the sample is still playing.
      """
      return self.player.dataQueue.hasMore()

   def isPaused(self):
      """
      Returns True if the sample is paused.
      """
      return self.hasPaused

   def pause(self):
      """
      Pause playing recorded sample.
      """

      if self.hasPaused:
         print "Sample is already paused!"
      else:
         self.lineOut.stop()    # pause playing
         self.hasPaused = True  # remember sample is paused

   def resume(self):
      """
      Resume Playing the sample from the paused position
      """

      if not self.hasPaused:
         print "Sample is already playing!"

      else:
         self.lineOut.start()    # resume playing
         self.hasPaused = False  # remember the sample is not paused

   def setFrequency(self, freq):
      """
      Set sample's playback frequency.
      """
      rateChangeFactor = float(freq) / self.frequency      # calculate change on playback rate

      self.frequency = freq                                # remember new frequency
      self.pitch = self.__convertFrequencyToPitch__(freq)  # and corresponding pitch

      self.__setPlaybackRate__(self.__getPlaybackRate__() * rateChangeFactor)   # and set new playback rate

   def getFrequency(self):
      """
      Return sample's playback frequency.
      """
      return self.frequency

   def setPitch(self, pitch):
      """
      Set sample playback pitch.
      """

      self.pitch = pitch                                         # remember new playback pitch
      self.setFrequency(self.__convertPitchToFrequency__(pitch)) # update playback frequency (this changes the playback rate)

   def getPitch(self):
      """
      Return sample's current pitch (it may be different from the default pitch).
      """
      return self.pitch

   def getDefaultPitch(self):
      """
      Return sample's default pitch.
      """
      return self.defaultPitch

   def setPanning(self, panning):
      """
      Set panning of sample (panning ranges from 0 - 127).
      """
      if panning < 0 or panning > 127:
         print "Panning (" + str(panning) + ") should range from 0 to 127."
      else:
         self.panning = panning                               # remember it
         panValue = mapValue(self.panning, 0, 127, -1.0, 1.0) # map panning from 0,127 to -1.0,1.0

         self.panLeft.pan.set(panValue)                       # and set it
         self.panRight.pan.set(panValue)

   def getPanning(self):
      """
      Return sample's current panning (panning ranges from 0 - 127).
      """
      return self.panning

   def setVolume(self, volume):
      """
      Set sample's volume (volume ranges from 0 - 127).
      """
      if volume < 0 or volume > 127:
         print "Volume (" + str(volume) + ") should range from 0 to 127."
      else:
         self.volume = volume                            # remember new volume
         amplitude = mapValue(self.volume,0,127,0.0,1.0) # map volume to amplitude
         self.amplitudeSmoother.input.set( amplitude )   # and set it

   def getVolume(self):
      """
      Return sample's current volume (volume ranges from 0 - 127).
      """
      return self.volume


   ### low-level functions related to FrameRate and PlaybackRate  ######################
   def getFrameRate(self):
      """
      Return the sample's default recording rate (e.g., 44100.0 Hz).
      """
      return self.sample.getFrameRate()

   def __setPlaybackRate__(self, newRate):
      """
      Set the sample's playback rate (e.g., 44100.0 Hz).
      """
      self.player.rate.set( newRate )

   def __getPlaybackRate__(self):
      """
      Return the sample's playback rate (e.g., 44100.0 Hz).
      """
      return self.player.rate.get()

   def __msToFrames__(self, milliseconds):
      """
      Converts milliseconds to frames based on the frame rate of the sample
      """
      return int(self.getFrameRate() * (milliseconds / 1000.0))


   ### helper functions for various conversions  ######################

   # Calculate frequency in Hertz based on MIDI pitch. Middle C is 60.0. You
   # can use fractional pitches so 60.5 would give you a pitch half way
   # between C and C#.  (by Phil Burk (C) 2009 Mobileer Inc)
   def __convertPitchToFrequency__(self, pitch):
      """
      Convert MIDI pitch to frequency in Hertz.
      """
      concertA = 440.0
      return concertA * 2.0 ** ((pitch - 69) / 12.0)

   def __convertFrequencyToPitch__(self, freq):
      """
      Converts pitch frequency (in Hertz) to MIDI pitch.
      """
      concertA = 440.0
      return log(freq / concertA, 2.0) * 12.0 + 69

   # following conversions between frequencies and semitones based on code
   # by J.R. de Pijper, IPO, Eindhoven
   # see http://users.utu.fi/jyrtuoma/speech/semitone.html
   def __getSemitonesBetweenFrequencies__(self, freq1, freq2):
      """
      Calculate number of semitones between two frequencies.
      """
      semitones = (12.0 / log(2)) * log(freq2 / freq1)
      return int(semitones)

   def __getFrequencyChangeBySemitones__(self, freq, semitones):
      """
      Calculates frequency change, given change in semitones, from a frequency.
      """
      freqChange = (exp(semitones * log(2) / 12) * freq) - freq
      return freqChange

##### LiveSample class ######################################

# If an audio input device is detected allow use of LiveSample class
if jSyn.liveSampleActive:

   class LiveSample():
      """
      Encapsulates a sound object created from live sound via the computer microphone (or line-in),
      which can be played once, looped, paused, resumed, stopped, copied and erased.
      The first parameter, maxSizeInSeconds, is the recording capacity (default is 30 secs).
      The larger this value, the more memory the object occupies, so this needs to be handled carefully.
      Also, each sound has a MIDI pitch associated with it (default is A4), so we can play different
      pitches with it (through pitch shifting).
      Finally, we can set/get its volume (0-127), panning (0-127), pitch (0-127), and frequency (in Hz).
      """

      def __init__(self, maxSizeInSeconds = 30, pitch = A4, volume = 127, channels = 2): # SampleLength in milliseconds

         print "Max recording time:", maxSizeInSeconds, "secs"

         self.SampleSize = maxSizeInSeconds * 1000   # convert seconds into milliseconds
         self.MAX_LOOP_TIME  = self.__msToFrames__(self.SampleSize)
         self.LOOP_CHANNELS = channels

         # holds recorded audio
         self.sample = FloatSample(self.MAX_LOOP_TIME, self.LOOP_CHANNELS)

         # create units
         self.lineIn = LineIn()                  # create input line (stereo)
         self.lineOut = LineOut()                # create output line (stereo)(mixes output to computer's audio (DAC) card)

         self.panning = 63                       # ranges from 0 (left) to 127 (right) - 63 is center
         self.panLeft = Pan()                    # Pan control for the left channel
         self.panRight = Pan()                   # Pan control for the right channel
         self.setPanning(self.panning)           # initialize panning to center (63)

         # create sample player (mono or stereo, as needed) and connect to lineOut mixer
         if self.LOOP_CHANNELS == 1:    # mono audio?

            # handle input
            self.writer = FixedRateMonoWriter()                     # captures incoming audio (mono)
            self.lineIn.output.connect(0, self.writer.input, 0)     # connect line input to the sample writer (recorder)

            # handle output
            self.player = VariableRateMonoReader()                  # create mono sample player
            self.player.output.connect( 0, self.panLeft.input, 0)   # connect single channel to pan control
            self.player.output.connect( 0, self.panRight.input, 0)

         elif self.LOOP_CHANNELS == 2:  # stereo audio?

            # handle input
            self.writer = FixedRateStereoWriter()                   # captures incoming audio
            self.lineIn.output.connect(0, self.writer.input, 0)     # connect line input to the sample writer (recorder)
            self.lineIn.output.connect(0, self.writer.input, 1)

            # handle output
            self.player = VariableRateStereoReader()                # create stereo sample player
            self.player.output.connect( 0, self.panLeft.input, 0)   # connect both channels to pan control
            self.player.output.connect( 1, self.panRight.input, 0)

         else:
            raise TypeError( "Can only record mono (1) or stereo (2 channels)." )

         # now that we have a player, set the default and current pitches
         self.defaultPitch = pitch                                 # default pitch of the live sample
         self.pitch = pitch                                        # playback pitch (may be different from default pitch)
         self.frequency = self.__convertPitchToFrequency__(pitch)  # and corresponding frequency

         # smooth out (linearly ramp) changes in player amplitude (without this, we get clicks)
         self.amplitudeSmoother = LinearRamp()
         self.amplitudeSmoother.output.connect( self.player.amplitude )   # connect to player's amplitude
         self.amplitudeSmoother.input.setup( 0.0, 0.5, 1.0 )              # set minimum, current, and maximum settings for control
         self.amplitudeSmoother.time.set( 0.0002 )                        # and how many seconds to take for smoothing amplitude changes

         self.player.rate.set(jSyn.FRAMERATE)

         self.volume = volume        # holds current volume (0-127)
         self.setVolume(self.volume) # sets the desired volume

         # connect panned sample to line output
         self.panLeft.output.connect (0, self.lineOut.input, 0)
         self.panRight.output.connect (1, self.lineOut.input, 1)

         # remember is sample is paused or not - needed for function isPaused()
         self.hasPaused = False

         # create time stamp variables
         self.beginRecordingTimeStamp = None    # holds timestamp of when we start recording into the sample
         self.endRecordingTimeStamp   = None    # holds timestamp of when we stop recording into the sample

         self.recordedSampleSize = None         # holds overall length of time of the sample rounded to nearest int

         self.recordingFlag = False             # boolean flag that is only true when the sample is being written to
         self.monitoringFlag = False            # boolean flag that is only true when monitor is turned on

         jSyn.addLive(self) # connect sample unit to the jSyn synthesizer

         # remember that this LiveSample has been created and is active (so that it can be stopped by JEM, if desired)
         __ActiveAudioSamples__.append(self)


      def startRecording(self):
         """
         Writes lineIn data to the sample data structure.
         Gets a time stamp so that, when we stop, we may calculate the duration of the recording.
         """

         # make sure sample is empty
         if self.recordedSampleSize != None:
            print "Warning: cannot record over an existing sample.  Use erase() first, to clear it."

         else:   # sample is empty, so it's OK to record
            print "Recording..."

            # make sure we are not already recording
            if not self.recordingFlag:

               # get timestamp of when we started recording,
               # so, later, we can calculate duration of recording
               self.beginRecordingTimeStamp = jSyn.synth.createTimeStamp()

               # start recording into the sample
               # (self.writer will update self.sample - the latter is passive, just a data holder)
               self.writer.dataQueue.queueOn( self.sample )    # connect the writer to the sample
               self.writer.start()                             # and write into it

               self.recordingFlag = True  # remember that recording has started

            else:   # otherwise, we are already recording, so let them know
               print "But, you are already recording..."

      def stopRecording(self):
         """
         Stops the writer from recording into the sample data structure.
         Also, gets another time stamp so that, now, we may calculate the duration of the recording.
         """

         # make sure we are currently recording
         if not self.recordingFlag:
            print "But, you are not recording!"

         else:
            print "Stopped recording."

            # stop writer from recording into the sample
            self.writer.dataQueue.queueOff( self.sample )
            self.writer.stop()

            self.recordingFlag = False  # remember that recording has stopped

            # now, let's calculate duration of recording

            # get a new time stamp
            self.endRecordingTimeStamp =  jSyn.synth.createTimeStamp()

            # calculate number of frames in the recorded sample
            # (i.e., total duration in seconds x framerate)
            startTime = self.beginRecordingTimeStamp.getTime()  # get start time
            endTime = self.endRecordingTimeStamp.getTime()      # get end time
            recordingTime = endTime - startTime                 # recording duration (in seconds)

            # if we have recorded more than we can store, then we will truncate
            # (that's the least painful solution...)
            recordingCapacity = self.SampleSize / 1000   # convert to seconds
            if recordingTime > recordingCapacity:

               # let them know
               exceededSeconds = recordingTime-recordingCapacity  # calculate overun
               print "Warning: Recording too long (by", round(exceededSeconds, 2), " secs)... truncating!"

               # truncate extra recording (by setting sample duration to max recording capacity)
               sampleDuration = self.SampleSize / 1000
            else:
               # sample duration is within the recording capacity
               sampleDuration = recordingTime

            # let's remember duration of recording (convert to frames - an integer)
            self.recordedSampleSize = int(jSyn.FRAMERATE * sampleDuration)


      def startMonitoring(self):
         """
         Starts monitoring audio being recorded (through the speakers).
         """

         self.monitoringFlag = True # remember that monitoring is now on

         # make audio being recorded sound through the speakers.
         self.lineIn.output.connect(0, self.lineOut.input, 0)
         self.lineIn.output.connect(0, self.lineOut.input, 1)
         self.lineOut.start()

         print "Monitoring..."

      def stopMonitoring(self):
         """
         Stops monitoring audio being recorded (through the speakers).
         """

         self.monitoringFlag = False  # remember that monitoring is now off.

         # make audio being recorded stop sounding through the speakers.
         self.lineIn.output.disconnect(0, self.lineOut.input, 0)
         self.lineIn.output.disconnect(0, self.lineOut.input, 1)

         print "Stopped monitoring."

      def isRecording(self):
         """
         Returns True if LiveSample is recording; False otherwise.
         """
         return self.recordingFlag

      def isMonitoring(self):
         """
         Returns True if monitoring is on; ; False otherwise.
         """
         return self.monitoringFlag


      def play(self, start = 0, size = -1):
         """
         Play the sample once from the millisecond 'start' until the millisecond 'start' + 'size'
         (size == -1 means to the end).
         If 'start' and 'size' are omitted, play complete sample.
         """
         # start playing back from the sample (loop it)
         # (sample frames get retrieved by the reader)
         if self.recordedSampleSize == None:
            print "Sample is empty!  You need to record before you can play."

         else:
            # for faster response, we restart playing (as opposed to queue at the end)
            if self.isPlaying():      # is the sample already playing?
               self.stop()            # yes, so stop it

            self.loop(1, start, size)

      def loop(self, times = -1 , start = 0, size = -1):
         """
         Repeat the sample indefinitely (times = -1), or the specified piece of the sample
         from millisecond 'start' until millisecond 'start'+'size' (size == -1 means to the end).
         If 'start and 'size' are omitted, repeat the complete sample.
         """

         if self.recordedSampleSize == None: # is the sample currently empty?
            print "Sample is empty!  You need to record before you can loop."
            return -1

         sampleTotalDuration = (self.recordedSampleSize / jSyn.FRAMERATE) * 1000 # total time of sample in milliseconds

         # is specified start time within the total duration of sample?
         if start < 0 or start > sampleTotalDuration:
            print "Start time provided (" + str(start) + ") should be between 0 and sample duration (" + str(sampleTotalDuration) + ")."
            return -1

         # does the size specified exceed the total duration of the sample or is size an invalid value?
         if size == 0 or start + size > sampleTotalDuration:
            print "Size (" + str(size) + ") exceeds total sample duration (" + str(sampleTotalDuration) + "), given start ("+ str(start) + ")."
            return -1

         # was the size specified less than the lowest value allowed?
         if size <= -1:
            size = self.recordedSampleSize # play to the end of the sample
         else:
            size = (size/1000) * jSyn.FRAMERATE # convert milliseconds into frames
            start = (start/1000) * jSyn.FRAMERATE

         # loop the sample continuously?
         if times == -1:
            self.player.dataQueue.queueLoop(self.sample, start, size)

         if times == 0:
            print "But, don't you want to play the sample at least once?"
            return -1

         else:
            # Subtract 1 from number of times a sample should be looped.
            # 'times' is the number of loops of the sample after the initial playing.
            self.player.dataQueue.queueLoop(self.sample, start, size, times - 1)

         self.lineOut.start()   # starts playing

      def stop(self):
         """
         Stops sample from playing any further and restarts the sample from the beginning
         """

         self.player.dataQueue.clear()
         self.hasPaused = False  # remember sample is not paused

      def isPlaying(self):
         """
         Returns True if the recorded sample is still playing; False otherwise.
         """
         return self.player.dataQueue.hasMore()

      def isPaused(self):
         """
         Returns True if the sample is paused; False otherwise.
         """
         return self.hasPaused

      def pause(self):
         """
         Pause playing recorded sample.
         """

         if self.hasPaused:
            print "Sample is already paused!"
         else:
            self.lineOut.stop()    # pause playing
            self.hasPaused = True  # remember sample is paused

      def resume(self):
         """
         Resume Playing the sample from the paused position
         """

         if not self.hasPaused:
            print "Sample is already playing!"

         else:
            self.lineOut.start()    # resume playing
            self.hasPaused = False  # remember the sample is not paused

      def copy(self):
         """
         Creates a copy of the sample.
         """

         # verify we can make a copy
         if self.isRecording():
            print "Cannot make a copy while recording!"

         else:

            # create copy with same duration (in seconds), default pitch, and volume (as original sample)
            copySample = LiveSample(self.SampleSize / 1000, self.defaultPitch, self.volume)

            copySample.recordedSampleSize = self.recordedSampleSize  # also copy the recorded size (not part of the constructor)


            # copy original audio frames in new sample
            for i in range(self.sample.getNumFrames()):
               copySample.sample.writeDouble(i, self.sample.readDouble(i))

            # also, copy all other attributes (so the two copies are identical)
            copySample.setFrequency( self.getFrequency() )     # yes, so make them sound alike
            copySample.setVolume( self.getVolume() )
            copySample.setPanning( self.getPanning() )

         # done, so return the copy
         return copySample


      def erase(self):
         """
         Erases all contents of the sample.
         """

         # is sample currently recording?
         if self.isRecording():
            print "Cannot erase while recording!"

         # is sample currently playing, stop it
         if self.isPlaying():
            self.stop()

         # clear the dataQueue, so recording of the sample will start at the beginning
         self.writer.dataQueue.clear()

         # rewrite audio data within sample frame by frame (0.0 means empty frame - no sound)
         for i in range(self.sample.getNumFrames()):
            self.sample.writeDouble(i, 0.0)

         # try to reset defaults
         self.setPitch( self.defaultPitch )
         self.setPanning( 63 )
         self.setVolume( 127 )

         # set sample size to empty
         self.recordedSampleSize = None

      def setFrequency(self, freq):
         """
         Set sample's playback frequency.
         """
         rateChangeFactor = float(freq) / self.frequency      # calculate change on playback rate

         self.frequency = freq                                # remember new frequency
         self.pitch = self.__convertFrequencyToPitch__(freq)  # and corresponding pitch

         self.__setPlaybackRate__(self.__getPlaybackRate__() * rateChangeFactor)   # and set new playback rate

      def getFrequency(self):
         """
         Return sample's playback frequency.
         """
         return self.frequency

      def setPitch(self, pitch):
         """
         Set sample playback pitch.
         """

         self.pitch = pitch                                         # remember new playback pitch
         self.setFrequency(self.__convertPitchToFrequency__(pitch)) # update playback frequency (this changes the playback rate)

      def getPitch(self):
         """
         Return sample's current pitch (it may be different from the default pitch).
         """
         return self.pitch

      def getDefaultPitch(self):
         """
         Return sample's default pitch.
         """
         return self.defaultPitch

      def setPanning(self, panning):
         """
         Set panning of sample (panning ranges from 0 - 127).
         """
         if panning < 0 or panning > 127:
            print "Panning (" + str(panning) + ") should range from 0 to 127."
         else:
            self.panning = panning                               # remember it
            panValue = mapValue(self.panning, 0, 127, -1.0, 1.0) # map panning from 0,127 to -1.0,1.0

            self.panLeft.pan.set(panValue)                       # and set it
            self.panRight.pan.set(panValue)

      def getPanning(self):
         """
         Return sample's current panning (panning ranges from 0 - 127).
         """
         return self.panning

      def setVolume(self, volume):
         """
         Set sample's volume (volume ranges from 0 - 127).
         """
         if volume < 0 or volume > 127:
            print "Volume (" + str(volume) + ") should range from 0 to 127."
         else:
            self.volume = volume                            # remember new volume
            amplitude = mapValue(self.volume,0,127,0.0,1.0) # map volume to amplitude
            self.amplitudeSmoother.input.set( amplitude )   # and set it

      def getVolume(self):
         """
         Return sample's current volume (volume ranges from 0 - 127).
         """
         return self.volume

   ######## low-level functions related to FrameRate and PlaybackRate ############################

      def getFrameRate(self):
         """
         Return sample's default recording rate (e.g., 44100.0 Hz).
         """
         return jSyn.FRAMERATE

      def __setPlaybackRate__(self, newRate):
         """
         Set sample's playback rate (e.g., 44100.0 Hz).
         """
         self.player.rate.set(newRate)

      def __getPlaybackRate__(self):
         """
         Return sample's playback rate (e.g., 44100.0 Hz).
         """
         return self.player.rate.get()

      def __msToFrames__(self, milliseconds):
         """
         Convert milliseconds to frames based on the frame rate of the sample.
         """
         return int(self.getFrameRate() * (milliseconds / 1000.0) )


   ######### Helper Functions for Various Conversions ##################################################################

      #Calculate the frequency in Hertz based on MIDI pitch (Middle C is 60.0)
      #Can use fractional pitches such as 60.5 which would give you a pitch half way between Middle C and C#
      def __convertPitchToFrequency__(self, pitch):
         """
         Convert MIDI pitch to frequency in Hertz.
         """
         concertA = 440.0
         return concertA * 2.0 ** ((pitch - 69) / 12.0)

      def __convertFrequencyToPitch__(self, freq):
         """
         Converts pitch frequency (in Hertz) to MIDI pitch.
         """
         concertA = 440.0
         return log(freq / concertA, 2.0) * 12.0 + 69

      def __getSemitonesBetweenFrequencies__(self, freq1, freq2):
         """
         Calculate number of semitones between two frequencies.
         """
         semitones = (12.0 / log(2)) * log(freq2 / freq1)
         return int(semitones)

      def __getFrequencyChangeBySemitones__(self, freq, semitones):
         """
         Calculates frequency change, given change in semitones, from a frequency.
         """
         freqChange = (exp(semitones * log(2) / 12) * freq) - freq
         return freqChange

# No audio input device detected
else:
   print "You cannot use LiveSample"
