# simpleButtonInstrument.py
#
# Demonstrates how to create a instrument consisting of two buttons,
# one to start a note, and another to end it.  
#

from gui import *
from music import *

# create display
d = Display("Simple Button Instrument", 270, 130)

pitch = A4            # pitch of note to be played

# define callback functions
def startNote():   # function to start the note

   global pitch        # we use this global variable

   Play.noteOn(pitch)  # start the note

def stopNote():    # function to stop the note

   global pitch        # we use this global variable

   Play.noteOff(pitch) # stop the note

# next, create the button widgets and assign their callback functions
b1 = Button("On", startNote)
b2 = Button("Off", stopNote)

# finally, add buttons to the display
d.add(b1, 90, 30)
d.add(b2, 90, 65)