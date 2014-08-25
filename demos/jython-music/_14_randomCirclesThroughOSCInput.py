# randomCirclesThroughOSCInput.py
#
# Demonstrates how to create a musical instrument using an OSC device.
# It receives OSC messages from device accelerometer and gyroscope.
#
# This instrument generates individual notes in succession based on
# its orientation in 3D space.  Each note is visually accompanied by
# a color circle drawn on a display.
#
# NOTE: For this example we used an iPhone running the free OSC app 
# "Control OSC". (There are many other possibilities.)
#
# SETUP:  The device is set up to be handled like an airplane in 
# flight.  Hold your device (e.g., smartphone) flat/horizontal with
# the screen up.  Think of an airplane resting on top of your device's
# screen - its nose pointing away from you - and its wings flat across
# the screen (left wing superimposed on the left side of your screen,
# and right wing on the right side of your screen).
#
# * The pitch of the airplane (the angle of its nose - pointing up or
#   down) corresponds to musical pitch.  The higher the nose, the 
#   higher the pitch. 
#
# * The roll of the airplane (the banking of its wings to the left or 
#   to the right) triggers note generation.  You could visualize 
#   notes dripping off the device's screen, so when you roll/bank the
#   device, notes escape (roll off).
#
# * Finally, device shake corresponds with loudness of notes.  
#   The more intensely you shake or vibrate the device as notes are 
#   generated, the louder the notes are.
#
# Visually, you get one circle per note.  The circle size (radius)
# corresponds to note volume (the louder the note, the larger the 
# circle).  Circle color corresponds to note pitch (the lower the
# pitch, the darker/browner the color, the higher the pitch the
# brighter/redder/bluer the color).
#

from gui import *
from random import *    
from music import *
from osc import *

# parameters
scale = MAJOR_SCALE   # scale used by instrument
normalShake  = 63     # shake value at rest (using xAccel for now)
shakeTrigger = 7      # deviation from rest value to trigger notes
                      # (higher, less sensitive)
shakeAmount  = 0      # amount of shake                       
devicePitch  = 0      # device pitch (set via incoming OSC messages)

##### create main display #####
d = Display("Smartphone Circles", 1000, 800) 

# define function for generating a circle/note
def drawCircle():
   """Draws one circle and plays the corresponding note."""
   
   global devicePitch, shakeAmount, shakeTrigger, d, scale

   # map device pitch to note pitch, and shake amount to volume
   pitch = mapScale(devicePitch, 0, 127, 0, 127, scale)  # use scale
   volume = mapValue(shakeAmount, shakeTrigger, 60, 50, 127)
   x = randint(0, d.getWidth())     # random circle x position
   y = randint(0, d.getHeight())    # random circle y position
   radius = mapValue(volume, 50, 127, 5, 80)  # map volume to radius
   
   # create a red-to-brown gradient
   red = mapValue(pitch, 0, 127, 100, 255)  # map pitch to red
   blue = mapValue(pitch, 0, 127, 0, 100)   # map pitch to blue
   color = Color(red, 0, blue)              # make color (green is 0)
   c = Circle(x, y, radius, color, True)    # create filled circle
   d.add(c)                                 # add it to display
   
   # now, let's play note (lasting 3 secs)
   Play.note(pitch, 0, 3000, volume)

##### define OSC callback functions #####
# callback function for incoming OSC gyroscope data
def gyro(message):
   """Sets global variable 'devicePitch' from gyro OSC message."""
   
   global devicePitch     # holds pitch of device

   args = message.getArguments()  # get OSC message's arguments

   # output message info (for exploration/fine-tuning)
   #print message.getAddress(),    # output OSC address
   #print list(args)               # and the arguments 
   
   # the 4th argument (i.e., index 3) is device pitch
   devicePitch = args[3]
   
# callback function for OSC accelerometer data
def accel(message):
   """
   Sets global variable 'shakeAmount'.  If 'shakeAmount' is higher
   than 'shakeTrigger', we call function drawCircle().
   """
   
   global normalShake, shakeTrigger, shakeAmount

   args = message.getArguments()  # get the message's arguments
   
   # output message info (for exploration/fine-tuning)
   #print message.getAddress(),    # output the OSC address
   #print list(args)               # and the arguments   

   # get sideways shake from the accelerometer
   shake = args[0]    # using xAccel value (for now)
   
   # is shake strong enough to generate a note?
   shakeAmount = abs(shake - normalShake)  # get deviation from rest
   if shakeAmount > shakeTrigger:
      drawCircle()    # yes, so create a circle/note   

##### establish connection to input OSC device (an OSC client) #####
oscIn = OscIn( 57110 )    # get input from OSC devices on port 57110    

# associate callback functions with OSC message addresses
oscIn.onInput("/gyro", gyro) 
oscIn.onInput("/accelerometer", accel)
