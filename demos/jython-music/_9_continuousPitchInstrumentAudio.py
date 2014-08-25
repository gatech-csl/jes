# continuousPitchInstrumentAudio.py
#
# Demonstrates how to use sliders and labels to create an instrument
# for changing volume and frequency of an audio loop in real time.
#
import os.path
from gui import *
from music import *

# load audio sample
a = AudioSample(os.path.join(os.path.dirname(__file__), "moondog.Bird_sLament.wav"))

# create display
d = Display("Continuous Pitch Instrument", 270, 200)

# set slider ranges (must be integers)
minFreq = 440   # frequency slider range 
maxFreq = 880   # (440 Hz is A4, 880 Hz is A5)

minVol = 0      # volume slider range
maxVol = 127

# create labels
label1 = Label( "Freq: " + str(minFreq) + " Hz" )  # set initial text
label2 = Label( "Vol: " + str(maxVol) )

# define callback functions (called every time the slider changes)
def setFrequency(freq):   # function to change frequency

   #global label1, a           # label to update, and audio to adjust
   
   a.setFrequency(freq)
   label1.setText("Freq: " + str(freq) + " Hz")  # update label

def setVolume(volume):    # function to change volume

   global label2, a           # label to update, and audio to adjust
   
   a.setVolume(volume)
   label2.setText("Vol: " + str(volume))  # update label

# next, create two slider widgets and assign their callback functions
#Slider(orientation, lower, upper, start, eventHandler)
slider1 = Slider(HORIZONTAL, minFreq, maxFreq, minFreq, setFrequency)
slider2 = Slider(HORIZONTAL, minVol, maxVol, maxVol, setVolume)

# add labels and sliders to display
d.add(label1, 40, 30)
d.add(slider1, 40, 60)
d.add(label2, 40, 120)
d.add(slider2, 40, 150)

# start the sound
a.loop()

