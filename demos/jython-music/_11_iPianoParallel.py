# iPiano.py
#
# Demonstrates how to build a simple piano instrument playable through 
# the computer keyboard.  
#
import os.path
from music import *
from gui import *

demos = os.path.dirname(__file__)

def makeIcon(path):
  return Icon(os.path.join(demos, path))


Play.setInstrument(PIANO)   # set desired MIDI instrument (0-127)

# load piano image and create display with appropriate size
pianoIcon = makeIcon("iPianoOctave.png")     # image for complete piano
d = Display("iPiano", pianoIcon.getWidth(), pianoIcon.getHeight())
d.add(pianoIcon)       # place image at top-left corner

# NOTE: The following loads a partial list of icons for pressed piano keys,
#       and associates them (via parallel lists) with the virtual keys 
#       corresponding to those piano keys and the corresponding pitches.
#       These lists should be expanded to cover the whole octave (or more).

# load icons for pressed piano keys 
# (continue loading icons for additional piano keys)
downKeyIcons = []    # holds all down piano-key icons
downKeyIcons.append( makeIcon("iPianoWhiteLeftDown.png") )   # C 
downKeyIcons.append( makeIcon("iPianoBlackDown.png") )       # C sharp
downKeyIcons.append( makeIcon("iPianoWhiteCenterDown.png") ) # D
downKeyIcons.append( makeIcon("iPianoBlackDown.png") )       # D sharp
downKeyIcons.append( makeIcon("iPianoWhiteRightDown.png") )  # E
downKeyIcons.append( makeIcon("iPianoWhiteLeftDown.png") )   # F

# lists of virtual keys and pitches corresponding to above piano keys
virtualKeys = [VK_Z, VK_S, VK_X, VK_D, VK_C, VK_V]
pitches     = [C4,   CS4,  D4,   DS4,  E4,   F4]

# create list of display positions for downKey icons
iconWidths = [0, 45, 76, 138, 150, 223]   # these are hardcoded!

keysPressed = []   # holds which keys are currently pressed

############################################################################
# define callback functions
def beginNote( key ):
   """Called when a computer key is pressed.  Implements the corresponding 
      piano key press (i.e., adds key-down icon on display, and starts note).
      Also, counteracts the key-repeat function of computer keyboards.
   """
   for i in range( len(virtualKeys) ):   # loop through all known virtual keys
   
      # if this is a known key (and NOT already pressed)
      if key == virtualKeys[i] and key not in keysPressed:  
             
         d.add( downKeyIcons[i], iconWidths[i], 0 )  # "press" this piano key
         Play.noteOn( pitches[i] )    # play corresponding note
         keysPressed.append( key )    # and remember key (to avoid key-repeat)

def endNote( key ):
   """Called when a computer key is released.  Implements the corresponding 
      piano key release (i.e., removes key-down icon, and stops note).
   """
   for i in range( len(virtualKeys) ):   # loop through known virtual keys
   
      # if this is a known key (we can assume it is already pressed)
      if key == virtualKeys[i]:  
             
         d.remove( downKeyIcons[i] )   # "release" this piano key
         Play.noteOff( pitches[i] )    # stop corresponding note
         keysPressed.remove( key )     # and forget key (for key-repeat)

############################################################################
# associate callback functions with GUI events
d.onKeyDown( beginNote )
d.onKeyUp( endNote )