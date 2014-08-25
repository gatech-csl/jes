# randomCirclesTimed.py
#
# Demonstrates how to generate a musical animation by drawing random 
# circles on a GUI display using a timer.  Each circle generates 
# a note - the redder the color, the lower the pitch; also, 
# the larger the radius, the louder the note.  Note pitches come 
# from the major scale.
#

from gui import *
from random import *    
from music import *

delay = 500   # initial delay between successive circle/notes

##### create display on which to draw circles #####
d = Display("Random Timed Circles with Sound")   

# define callback function for timer
def drawCircle():
   """Draws one random circle and plays the corresponding note."""
   
   global d                         # we will access the display
   
   x = randint(0, d.getWidth())     # x may be anywhere on display
   y = randint(0, d.getHeight())    # y may be anywhere on display
   radius = randint(5, 40)          # random radius (5-40 pixels)
   
   # create a red-to-brown-to-blue gradient (RGB)
   red = randint(100, 255)          # random R component (100-255)
   blue = randint(0, 100)           # random B component (0-100)
   color = Color(red, 0, blue)      # create color (green is 0)
   c = Circle(x, y, radius, color, True)  # create filled circle
   d.add(c)                         # add it to the display
   
   # now, let's create note based on this circle

   # the redder the color, the lower the pitch (using major scale)
   pitch = mapScale(255-red+blue, 0, 255, C4, C6, MAJOR_SCALE)  

   # the larger the circle, the louder the note
   dynamic = mapValue(radius, 5, 40, 20, 127) 
    
   # and play note (start immediately, hold for 5 secs)
   Play.note(pitch, 0, 5000, dynamic)

# create timer for animation
t = Timer(delay, drawCircle)    # one circle per 'delay' milliseconds

##### create display with slider for user input #####
title = "Delay"
xPosition = d.getWidth() / 3    # set initial position of display
yPosition = d.getHeight() + 45
d1 = Display(title, 250, 50, xPosition, yPosition)

# define callback function for slider
def timerSet(value):
   global t, d1, title   # we will access these variables
   t.setDelay(value) 
   d1.setTitle(title + " (" + str(value) + " msec)")

# create slider
s1 = Slider(HORIZONTAL, 10, delay*2, delay, timerSet)
d1.add(s1, 25, 10)

# everything is ready, so start animation (i.e., start timer)
t.start()
