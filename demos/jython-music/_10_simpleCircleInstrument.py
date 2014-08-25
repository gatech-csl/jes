# simpleCircleInstrument.py
#
# Demonstrates how to use mouse and keyboard events to build a simple 
# drawing musical instrument.
#
# The user plays notes by drawing circles.  The diameter of the 
# circle determines the pitch of the note (using the major scale).  
# To draw a circle, the user presses the mouse on the display and 
# starts moving the mouse.  The point where the mouse is released 
# determines the size of the circle (also the pitch of the note).  
#
# NOTE: The mathematics used to map the diameter of the circle is 
# relatively simple, but generate a musical effect that is 
# interesting.  Although the user might expect that doubling of the 
# diameter will double the pitch of the note, that's not the case.  
# It takes a little while to figure out how mouse distance 
# corresponds to pitch, and it is precisely this challenge that makes
# this "game" interesting - not unlike regular video games.
# 

from gui import *
from music import *
from math import sqrt

### initialize variables ######################
minPitch = C1  # instrument pitch range
maxPitch = C8

# create display
d = Display("Circle Instrument")    # default dimensions (600 x 400)
d.setColor( Color(51, 204, 255) )   # set background to turquoise

beginX = 0   # holds starting x coordinate for next circle
beginY = 0   # holds starting y coordinate

# maximum circle diameter - same as diagonal of display
maxDiameter = sqrt(d.getWidth()**2 + d.getHeight()**2) # calculate it

### define callback functions ######################
def beginCircle(x, y):   # for when mouse is pressed

   global beginX, beginY
   
   beginX = x   # remember new circle's coordinates
   beginY = y

def endCircleAndPlayNote(endX, endY):  # for when mouse is released

   global beginX, beginY, d, maxDiameter, minPitch, maxPitch
   
   # calculate circle parameters 
   # first, calculate distance between begin and end points
   diameter = sqrt( (beginX-endX)**2 + (beginY-endY)**2 )
   diameter = int(diameter)     # in pixels - make it an integer
   radius = diameter/2          # get radius 
   centerX = (beginX + endX)/2  # circle center is halfway between...
   centerY = (beginY + endY)/2  # ...begin and end points

   # draw circle with yellow color, unfilled, 3 pixels thick
   d.drawCircle(centerX, centerY, radius, Color.YELLOW, False, 3)
   
   # create note
   pitch = mapScale(diameter, 0, maxDiameter, minPitch, maxPitch, 
                    MAJOR_SCALE)

   # invert pitch (larger diameter, lower pitch)                    
   pitch = maxPitch - pitch    
   
   # and play note
   Play.note(pitch, 0, 5000)   # start immediately, hold for 5 secs

def clearOnSpacebar(key):  # for when a key is pressed
  
  global d
  
  # if they pressed space, clear display and stop the music
  if key == VK_SPACE:  
     d.removeAll()        # remove all shapes
     Play.allNotesOff()   # stop all notes
    
### assign callback functions to display event handlers #############
d.onMouseDown( beginCircle )
d.onMouseUp( endCircleAndPlayNote )
d.onKeyDown( clearOnSpacebar )