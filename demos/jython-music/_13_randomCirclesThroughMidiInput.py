# randomCirclesThroughMidiInput.py
#
# Demonstrates how to generate a musical animation by drawing random 
# circles on a GUI display using input from a MIDI instrument.  
# Each input note generates a circle - the lower the note, the lower 
# the red+blue components of the circle color.  The louder the note, 
# the larger the circle. The position of the circle on the display 
# is random.  Note pitches come directly from the input instrument.
#

from gui import *
from random import *    
from music import *
from midi import *

##### create main display #####
d = Display("Random Circles with Sound")     

# define callback function for MidiIn object
def drawCircle(eventType, channel, data1, data2):
   """Draws a circle based on incoming MIDI event, and plays 
      corresponding note.
   """
   
   global d                         # we will access the display

   # circle position is random
   x = randint(0, d.getWidth())     # x may be anywhere on display
   y = randint(0, d.getHeight())    # y may be anywhere on display

   # circle radius depends on incoming note volume (data2)
   radius = mapValue(data2, 0, 127, 5, 40)  # ranges 5-40 pixels
   
   # color depends on on incoming note pitch (data1)
   red = mapValue(data1, 0, 127, 100, 255)  # R component (100-255)
   blue = mapValue(data1, 0, 127, 0, 100)   # B component (0-100)
   color = Color(red, 0, blue)      # create color (green is 0)
   
   # create filled circle from parameters
   c = Circle(x, y, radius, color, True)  
   
   # and add it to the display
   d.add(c)                         
   
   # now, let's play the note (data1 is pitch, data2 is volume)
   Play.noteOn(data1, data2)

# establish a connection to an input MIDI device
midiIn = MidiIn()     

# register a callback function to process incoming MIDI events
midiIn.onNoteOn( drawCircle ) 
