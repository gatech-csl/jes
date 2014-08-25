################################################################################################################
# music.py      Version 2.7         19-Aug-2014       Bill Manaris, Nora Grossman, and Kenneth Hanson

###########################################################################
#
# This file is part of Jython Music.
#
# Copyright (C) 2014 Bill Manaris, Nora Grossman, and Kenneth Hanson
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
# Imports jMusic and jSyn packages into jython.  Also provides additional functionality.
#
#
# REVISIONS:
#
# 2.7   19-Aug-2014 (bm) INDIAN_SCALE and TURKISH_SCALE were taken out because they were incorrect/misleading,
#                   as per Andrew Brown's recommendation.
#
# 2.6   29-May-2014 (bm) Added JEM's registerStopFunction() to register a callback function to be called,
#                   inside JEM, when the Stop button is pressed.  This is needed to stop Play.midi from
#                   playing music. For now, we register Play.stop(), which stops any music started through
#                   the Play class from sounding.  Also, changed stopMidiSynths() to __stopMidiSynths__()
#                   to hide it, since Play.stop() is now the right way to stop Play generated music from
#                   sounding.
#
# 2.5   27-May-2014 (bm) Added stopMidiSynths() - a function to stop all Play.midi music right away - this 
#                   was needed for JEM. Also,Play.midi() returns the MIDI synthesizer used, so
#                   m = Play.midi(), followed by, m.stop(), will stop that synthesizer.
#
# 2.4   02-May-2014 (bm) Updated fixWorkingDirForJEM() solution to work with new JEM editor by Tobias Kohn.
#
# 2.3   17-Dec-2013 (bm, ng) Added AudioSample panning ranging from 0 (left) to 127 (right).  Also
#                   added Envelope class and updated AudioSample to work with it.
#
# 2.2   21-Nov-2013 Added a Play.note(pitch, start, duration, velocity=100, channel=0) function,
#                   which plays a note with given 'start' time (in milliseconds from now), 
#                   'duration' (in milliseconds from 'start' time), with given 'velocity' on 'channel'.
#                   This allows scheduling of future note events, and thus should facilitate
#                   playing score-based or event-based musical material.
#
# 2.1   14-Mar-2013 Two classes - AudioSample and MidiSequence.  
#
#                   AudioSample is instantiated with a string - the filename of an audio file (.wav or .aiff).  
#                   It supports the following functions: play(), loop(), loop(numOfTimes), stop(), pause(), resume(),
#                   setPitch( e.g., A4 ), getPitch(), getDefaultPitch(), 
#                   setFrequency( e.g., 440.0 ), getFrequency(), 
#                   setVolume( 0-127 ), getVolume().
#
#                   MidiSequence is instantiated with either a string - the filename of a MIDI file (.mid), or 
#                   music library material (Score, Part, Phrase, or Note).
#                   It supports the following functions: play(), loop(), stop(), pause(), resume(), 
#                   setPitch( e.g., A4 ), getPitch(), getDefaultPitch(), 
#                   setTempo( e.g., 80.1 ), getTempo(), getDefaultTempo(), 
#                   setVolume( 0-127 ), getVolume().
#
#                   For more information on function parameters, see the class definition.
#
# 2.0  17-Feb-2012  Added jSyn synthesizer functionality.  We now have an AudioSample class for loading audio
#                   files (WAV or AIF), which can be played, looped, paused, resumed, and stopped.
#                   Also, each sound has a MIDI pitch associated with it (default is A4), so we 
#                   can play different pitches with it (through pitch shifting). 
#                   Finally, we improved code organization overall.
#
# 1.91 13-Feb-2013  Modified mapScale() to add an argument for the key of the scale (default is C).
# 
# 1.9  10-Feb-2013  Removed Read.image() and Write.image() - no content coupling with 
#                   image library anymore.
# 1.81 03-Feb-2013  Now mapScale() returns an int (since it intended to be used as
#                   a pitch value).  If we return a float, it may be confused as
#                   a note frequency (by the Note() constructor) - that would not be good.
#
# 1.8  01-Jan-2013  Redefine Jython input() function to fix problem with jython 2.5.3
#                   (see 
# 1.7  30-Dec-2012  Added missing MIDI instrument constants
# 1.6  26-Nov-2012  Added Play.frequencyOn/Off(), and Play.set/getPitchBend() functions.
# 1.52 04-Nov-2012  Divided complicated mapValue() to simpler mapValue() and mapScale() functions.
# 1.51 20-Oct-2012  Restablished access to jMusic Phrase's toString() via __str__() and __repr__().
#                   Added missing jMusic constants.
#                   Added pitchSet parameter to mapValue()
# 1.5  16-Sep-2012  Added MIDI_INSTRUMENTS to be used in instrument selection menus, etc.
# 1.4  05-Sep-2012  Renamed package to 'music'.
# 1.3  17-Nov-2011  Extended jMusic Phrase, Read, Write by wrapping them in jython classes.
#

from jm.JMC import *     # import jMusic constants and utilities
from jm.util import *

from jm.music.tools import *

from jm.gui.cpn import *
from jm.gui.helper import *
from jm.gui.histogram import *
from jm.gui.show import *
from jm.gui.wave import *

from jm.audio.io import *
from jm.audio.synth import *
from jm.audio.Instrument import *

from jm.constants.Alignments import *
from jm.constants.Articulations import *
from jm.constants.DrumMap import *
from jm.constants.Durations import *
from jm.constants.Dynamics import *
from jm.constants.Frequencies import *
from jm.constants.Instruments import *
from jm.constants.Noises import *
from jm.constants.Panning import *
from jm.constants.Pitches import *
from jm.constants.ProgramChanges import *
from jm.constants.Durations import *
from jm.constants.Scales import *
from jm.constants.Tunings import *
from jm.constants.Volumes import *
from jm.constants.Waveforms import *

######################################################################################
# Jython 2.5.3 fix for input()
# see http://python.6.n6.nabble.com/input-not-working-on-Windows-td4987455.html
# also see fix at http://pydev.org/faq.html#PyDevFAQ-Whyrawinput%28%29%2Finput%28%29doesnotworkcorrectlyinPyDev%3F
def input(prompt):
   return eval( raw_input(prompt) )


######################################################################################
# redefine scales as Jython lists (as opposed to Java arrays - for cosmetic purposes)
AEOLIAN_SCALE        = list(AEOLIAN_SCALE) 
BLUES_SCALE          = list(BLUES_SCALE) 
CHROMATIC_SCALE      = list(CHROMATIC_SCALE) 
DIATONIC_MINOR_SCALE = list(DIATONIC_MINOR_SCALE)
DORIAN_SCALE         = list(DORIAN_SCALE) 
HARMONIC_MINOR_SCALE = list(HARMONIC_MINOR_SCALE) 
LYDIAN_SCALE         = list(LYDIAN_SCALE) 
MAJOR_SCALE          = list(MAJOR_SCALE) 
MELODIC_MINOR_SCALE  = list(MELODIC_MINOR_SCALE) 
MINOR_SCALE          = list(MINOR_SCALE) 
MIXOLYDIAN_SCALE     = list(MIXOLYDIAN_SCALE) 
NATURAL_MINOR_SCALE  = list(NATURAL_MINOR_SCALE) 
PENTATONIC_SCALE     = list(PENTATONIC_SCALE) 


######################################################################################
# define text labels for MIDI instruments (index in list is same as MIDI instrument number)
MIDI_INSTRUMENTS = [ # Piano Family
                     "Acoustic Grand Piano", "Bright Acoustic Piano", "Electric Grand Piano",    
                    "Honky-tonk Piano", "Electric Piano 1 (Rhodes)", "Electric Piano 2 (DX)", 
                    "Harpsichord", "Clavinet", 
                    
                    # Chromatic Percussion Family
                    "Celesta", "Glockenspiel", "Music Box", "Vibraphone", "Marimba",            
                    "Xylophone", "Tubular Bells", "Dulcimer",
                    
                    # Organ Family
                    "Drawbar Organ", "Percussive Organ", "Rock Organ", "Church Organ",          
                    "Reed Organ", "Accordion", "Harmonica", "Tango Accordion", 
                    
                    # Guitar Family
                    "Acoustic Guitar (nylon)", "Acoustic Guitar (steel)", "Electric Guitar (jazz)", 
                    "Electric Guitar (clean)", "Electric Guitar (muted)", "Overdriven Guitar", 
                    "Distortion Guitar", "Guitar harmonics",
                    
                    # Bass Family
                    "Acoustic Bass", "Electric Bass (finger)", "Electric Bass (pick)", "Fretless Bass",
                    "Slap Bass 1", "Slap Bass 2", "Synth Bass 1", "Synth Bass 2", 
                    
                    # Strings and Timpani Family
                    "Violin", "Viola", "Cello", "Contrabass", "Tremolo Strings", "Pizzicato Strings",
                    "Orchestral Harp", "Timpani", 
                    
                    # Ensemble Family
                    "String Ensemble 1", "String Ensemble 2", "Synth Strings 1", "Synth Strings 2", 
                    "Choir Aahs", "Voice Oohs", "Synth Voice", "Orchestra Hit", 
                    
                    # Brass Family
                    "Trumpet", "Trombone", "Tuba", "Muted Trumpet", "French Horn", 
                    "Brass Section", "SynthBrass 1", "SynthBrass 2",
                    
                    # Reed Family
                    "Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax", "Oboe", "English Horn", 
                    "Bassoon", "Clarinet", 
                    
                    # Pipe Family
                    "Piccolo", "Flute", "Recorder", "Pan Flute", "Blown Bottle", "Shakuhachi", 
                    "Whistle", "Ocarina", 
                    
                    # Synth Lead Family
                    "Lead 1 (square)", "Lead 2 (sawtooth)", "Lead 3 (calliope)",  "Lead 4 (chiff)", 
                    "Lead 5 (charang)", "Lead 6 (voice)", "Lead 7 (fifths)", "Lead 8 (bass + lead)", 
                    
                    # Synth Pad Family
                    "Pad 1 (new age)", "Pad 2 (warm)", "Pad 3 (polysynth)", "Pad 4 (choir)", 
                    "Pad 5 (bowed)", "Pad 6 (metallic)", "Pad 7 (halo)", "Pad 8 (sweep)",
                    
                    # Synth Effects Family
                    "FX 1 (rain)", "FX 2 (soundtrack)", "FX 3 (crystal)", "FX 4 (atmosphere)", 
                    "FX 5 (brightness)", "FX 6 (goblins)", "FX 7 (echoes)", "FX 8 (sci-fi)",
                    
                    # Ethnic Family
                    "Sitar",  "Banjo", "Shamisen", "Koto", "Kalimba", "Bag pipe", "Fiddle", "Shanai",
                    
                    # Percussive Family
                    "Tinkle Bell", "Agogo", "Steel Drums", "Woodblock", "Taiko Drum", "Melodic Tom",
                    "Synth Drum", "Reverse Cymbal", 
                    
                    # Sound Effects Family
                    "Guitar Fret Noise", "Breath Noise", "Seashore", "Bird Tweet", "Telephone Ring",
                    "Helicopter", "Applause", "Gunshot" ]

# define text labels for inverse-lookup of MIDI pitches (index in list is same as MIDI pitch number) 
# (for enharmonic notes, e.g., FS4 and GF4, uses the sharp version, e.g. FS4)
MIDI_PITCHES = ["C_1", "CS_1", "D_1", "DS_1", "E_1", "F_1", "FS_1", "G_1", "GS_1", "A_1", "AS_1", "B_1",
                "C0", "CS0", "D0", "DS0", "E0", "F0", "FS0", "G0", "GS0", "A0", "AS0", "B0",
                "C1", "CS1", "D1", "DS1", "E1", "F1", "FS1", "G1", "GS1", "A1", "AS1", "B1",
                "C2", "CS2", "D2", "DS2", "E2", "F2", "FS2", "G2", "GS2", "A2", "AS2", "B2",
                "C3", "CS3", "D3", "DS3", "E3", "F3", "FS3", "G3", "GS3", "A3", "AS3", "B3",
                "C4", "CS4", "D4", "DS4", "E4", "F4", "FS4", "G4", "GS4", "A4", "AS4", "B4",
                "C5", "CS5", "D5", "DS5", "E5", "F5", "FS5", "G5", "GS5", "A5", "AS5", "B5",
                "C6", "CS6", "D6", "DS6", "E6", "F6", "FS6", "G6", "GS6", "A6", "AS6", "B6",
                "C7", "CS7", "D7", "DS7", "E7", "F7", "FS7", "G7", "GS7", "A7", "AS7", "B7",
                "C8", "CS8", "D8", "DS8", "E8", "F8", "FS8", "G8", "GS8", "A8", "AS8", "B8",
                "C9", "CS9", "D9", "DS9", "E9", "F9", "FS9", "G9"]

######################################################################################
# provide additional MIDI rhythm constant

DOTTED_WHOLE_NOTE = 4.5
DWN = 4.5

######################################################################################
# provide additional MIDI pitch constants (for first octave, i.e., minus 1 octave)
BS_1 = 12
bs_1 = 12
B_1 = 11
b_1 = 11
BF_1 = 10
bf_1 = 10
AS_1 = 10
as_1 = 10
A_1 = 9
a_1 = 9
AF_1 = 8
af_1 = 8
GS_1 = 8
gs_1 = 8
G_1 = 7
g_1 = 7
GF_1 = 6
gf_1 = 6
FS_1 = 6
fs_1 = 6
F_1 = 5
f_1 = 5
FF_1 = 4
ff_1 = 4
ES_1 = 5
es_1 = 5
E_1 = 4
e_1 = 4
EF_1 = 3
ef_1 = 3
DS_1 = 3
ds_1 = 3
D_1 = 2
d_1 = 2
DF_1 = 1
df_1 = 1
CS_1 = 1
cs_1 = 1
C_1 = 0
c_1 = 0
                    
######################################################################################
# provide additional MIDI instrument constants (missing from jMusic specification)
EPIANO1 = 4
RHODES_PIANO = 4
DX_PIANO = 5
DX = 5
DULCIMER = 15
DRAWBAR_ORGAN = 16
PERCUSSIVE_ORGAN = 17
ROCK_ORGAN = 18
TANGO_ACCORDION = 23
BANDONEON = 23
OVERDRIVEN_GUITAR = 29
DISTORTION_GUITAR = 30
SLAP_BASS1 = 36
SLAP_BASS2 = 37
SYNTH_BASS1 = 38
SYNTH_BASS2 = 39
ORCHESTRAL_HARP = 46
STRING_ENSEMBLE1 = 48
STRING_ENSEMBLE2 = 49
SYNTH = 50
SYNTH_STRINGS1 = 50
SYNTH_STRINGS2 = 51
CHOIR_AHHS = 52
VOICE_OOHS = 53
SYNTH_VOICE = 54
BRASS_SECTION = 61
SYNTH_BRASS1 = 62
SYNTH_BRASS2 = 63
BLOWN_BOTTLE = 76
LEAD_1_SQUARE = 80
LEAD_2_SAWTOOTH = 81
LEAD_3_CALLIOPE = 82
CALLIOPE = 82
LEAD_4_CHIFF = 83
CHIFF = 83
LEAD_5_CHARANG = 84
LEAD_6_VOICE = 85
LEAD_7_FIFTHS = 86
FIFTHS = 86
LEAD_8_BASS_LEAD = 87
BASS_LEAD = 87
PAD_1_NEW_AGE = 88
NEW_AGE = 88
PAD_2_WARM = 89
PAD_3_POLYSYNTH = 90
POLYSYNTH = 90
PAD_4_CHOIR = 91
SPACE_VOICE = 91
PAD_5_GLASS = 92
PAD_6_METTALIC = 93
METALLIC = 93
PAD_7_HALO = 94
HALO = 94
PAD_8_SWEEP = 95
FX_1_RAIN = 96
FX_2_SOUNDTRACK = 97
FX_3_CRYSTAL = 98
FX_4_ATMOSPHERE = 99
FX_5_BRIGHTNESS = 100
FX_6_GOBLINS = 101
GOBLINS = 101
FX_7_ECHOES = 102
ECHO_DROPS = 102
FX_8_SCI_FI = 103
SCI_FI = 103
TAIKO_DRUM = 116
MELODIC_TOM = 117
TOM_TOM = 117      # this is a fix (jMusic defines this as 119!)
GUITAR_FRET_NOISE = 120
FRET_NOISE = 120
BREATH_NOISE = 121
BIRD_TWEET = 123
TELEPHONE_RING = 124
GUNSHOT = 127

# and MIDI drum and percussion abbreviations
ABD = 35 
BASS_DRUM = 36
BDR = 36
STK = 37
SNARE = 38
SNR = 38
CLP = 39
ESN = 40
LFT = 41
CHH = 42
HFT = 43
PHH = 44
LTM = 45
OHH = 46
LMT = 47
HMT = 48
CC1 = 49
HGT = 50
RC1 = 51
CCM = 52
RBL = 53
TMB = 54
SCM = 55
CBL = 56
CC2 = 57
VSP = 58
RC2 = 59
HBG = 60
LBG = 61
MHC = 62
OHC = 63
LCG = 64
HTI = 65
LTI = 66
HAG = 67
LAG = 68
CBS = 69
MRC = 70
SWH = 71
LWH = 72
SGU = 73
LGU = 74
CLA = 75
HWB = 76
LWB = 77
MCU = 78
OCU = 79
MTR = 80
OTR = 81


######################################################################################
#### Free music library functions ####################################################
######################################################################################

def mapValue(value, minValue, maxValue, minResultValue, maxResultValue):
   """
   Maps value from a given source range, i.e., (minValue, maxValue), 
   to a new destination range, i.e., (minResultValue, maxResultValue).
   The result will be converted to the result data type (int, or float).
   """
   # check if value is within the specified range
   if value < minValue or value > maxValue:
      raise ValueError("value, " + str(value) + ", is outside the specified range, " \
                                 + str(minValue) + " to " + str(maxValue) + ".")
                                    
   # we are OK, so let's map   
   value = float(value)  # ensure we are using float (for accuracy)
   normal = (value - minValue) / (maxValue - minValue)   # normalize source value

   # map to destination range
   result = normal * (maxResultValue - minResultValue) + minResultValue
   
   destinationType = type(minResultValue)  # find expected result data type
   result = destinationType(result)        # and apply it

   return result   

def mapScale(value, minValue, maxValue, minResultValue, maxResultValue, scale=CHROMATIC_SCALE, key=None):
   """
   Maps value from a given source range, i.e., (minValue, maxValue), to a new destination range, i.e., 
   (minResultValue, maxResultValue), using the provided scale (pitch row) and key.  The scale provides
   a sieve (a pattern) to fit the results into.  The key determines how to shift the scale pattern to
   fit a particular key - if key is not provided, we assume it is the same as minResultValue (e.g., C4 
   and C5 both refer to the key of C)).  
     
   The result will be within the destination range rounded to closest pitch in the
   provided pitch row.   It always returns an int (since it is intended to be used
   as a pitch value).
   
   NOTE:  We are working within a 12-step tonal system (MIDI), i.e., octave is 12 steps away,
          so pitchRow must contain offsets (from the root) between 0 and 11.
   """
   # check if value is within the specified range
   if value < minValue or value > maxValue:
      raise ValueError("value, " + str(value) + ", is outside the specified range, " \
                                 + str(minValue) + " to " + str(maxValue) + ".")
     
   # check pitch row - it should contain offsets only from 0 to 11
   badOffsets = [offset for offset in scale if offset < 0 or offset > 11]
   if badOffsets != []:  # any illegal offsets?
      raise TypeError("scale, " + str(scale) + ", should contain values only from 0 to 11.")
   
   # figure out key of scale
   if key == None:             # if they didn't specify a key
      key = minResultValue % 12   # assume that minResultValue the root of the scale
   else:                       # otherwise,
      key = key % 12              # ensure it is between 0 and 11 (i.e., C4 and C5 both mean C, or 0).
   
   # we are OK, so let's map   
   value = float(value)  # ensure we are using float (for accuracy)
   normal = (value - minValue) / (maxValue - minValue)   # normalize source value

   # map to destination range (i.e., chromatic scale)
   # (subtracting 'key' aligns us with indices in the provided scale - we need to add it back later)
   chromaticStep = normal * (maxResultValue - minResultValue) + minResultValue - key
   
   # map to provided pitchRow scale
   pitchRowStep = chromaticStep * len(scale) / 12   # note in pitch row
   scaleDegree  = int(pitchRowStep % len(scale))    # find index into pitchRow list
   register     = int(pitchRowStep / len(scale))    # find pitch register (e.g. 4th, 5th, etc.)
   
   # calculate the octave (register) and add the pitch displacement from the octave.
   result = register * 12 + scale[scaleDegree]
   
   # adjust for key (scale offset)
   result = result + key
         
   # now, result has been sieved through the pitchSet (adjusted to fit the pitchSet)
   
   #result = int(round(result))   # force an int data type
   result = int(result)   # force an int data type

   return result
      
def frange(start, stop, step):
   """
   A range function for floats, with variable accuracy (controlled by
   number of digits in decimal part of 'step').
   """
   import math
   
   if step == 0:   # make sure we do not get into an infinite loop
     raise ValueError, "frange() step argument must not be zero"
   
   result = []                         # holds resultant list
   # since Python's represetation of real numbers may not be exactly what we expect,
   # let's round to the number of decimals provided in 'step' 
   accuracy = len(str(step-int(step))[1:])-1  # determine number of decimals in 'step'
   
   # determine which termination condition to use
   if step > 0:    
      done = start >= stop
   else:
      done = start <= stop
   
   # generate sequence
   while not done:
      start = round(start, accuracy)  # use same number of decimals as 'step'
      result.append(start)
      start += step
      # again, determine which termination condition to use
      if step > 0:    
         done = start >= stop
      else:
         done = start <= stop

   return result

#
#*** If used within JEM, xfrange() will cause an error, since JEM's Jython 2.2 does not support 'yield'
#    If so, just comment this out.
#
def xfrange(start, stop, step):
   """
   A generator range function for floats, with variable accuracy (controlled by
   number of digits in decimal part of 'step').
   """
   import math
   
   if step == 0:   # make sure we do not get into an infinite loop
     raise ValueError, "frange() step argument must not be zero"

   # since Python's represetation of real numbers may not be exactly what we expect,
   # let's round to the number of decimals provided in 'step' 
   accuracy = len(str(step-int(step))[1:])-1  # determine number of decimals in 'step'

   # determine which termination condition to use
   if step > 0:    
      done = start >= stop
   else:
      done = start <= stop

   # generate sequence
   while not done:
      start = round(start, accuracy)  # use same number of decimals as 'step'
      yield start
      start += step
      # again, determine which termination condition to use
      if step > 0:    
         done = start >= stop
      else:
         done = start <= stop


######################################################################################
#### jMusic library extensions #########################################################
######################################################################################

# A wrapper to turn class functions into "static" functions (e.g., for Mod functions).
#
# See http://code.activestate.com/recipes/52304-static-methods-aka-class-methods-in-python/
#

class Callable:
    def __init__(self, functionName):
        self.__call__ = functionName


######################################################################################
#### jMusic Mod extensions #########################################################
######################################################################################

from jm.music.tools import Mod as jMod  # needed to wrap more functionality below

# Create various Mod functions, in addition to Mod's default functionality.
# This class is not meant to be instantiated, hence no "self" in function definitions.
# Functions are made callable through class Callable, above.

class Mod(jMod):

   def normalize(material):
      """Same as jMod.normalise()."""
      
      jMod.normalise(material)

   # make this function callable without having to instantiate this class
   normalize = Callable(normalize)  
   
   def invert(phrase, pitch):
      """Invert phrase using pitch as the mirror (pivot) axis."""
      
      # use regular jMusic invert(), which mirrors around the first note of the phrase
      temp = Phrase()             # build a dummy phrase, with first note as pivot, for inversion purposes
      temp.addNote( pitch, QN )   # add a dummy first note, to be used as inversion axis
      jMod.append( temp, phrase ) # ...add the original phrase's notes
      jMod.invert( temp )         # do the inversion
      
      # re-build the original phrase (remove first note from temp)
      noteList = list( temp.getNoteList() ) # get the notes as a Python list
      del noteList[0]                       # remove the dummy first note we had added
      phrase.empty()                        # clear the original phrase
      phrase.addNoteList( noteList )        # and add the inverted notes
      
   def mutate(phrase):
      """Same as jMod.mutate()."""
      
      # adjust jMod.mutate() to use random rhythm values from phrase notes
      rhythms = [note.getRhythmValue() for note in phrase.getNoteList()]
      
      jMod.mutate(phrase, 1, 1, CHROMATIC_SCALE, phrase.getLowestPitch(),  
                  phrase.getHighestPitch(), rhythms)

   # make this function callable without having to instantiate this class
   normalize = Callable(normalize)  
   invert = Callable(invert)  
   mutate = Callable(mutate)  
   
   
######################################################################################
# JEM working directory fix
#
# JEM (written partially in Java) does not allow changing current directory.
# So, when we have the user's desired working directory we CANNOT use it to read/write
# jMusic media files, unless we add it as a prefix here to every Read/Write operation.
# We do so only if the filepath passed to Read/Write is just a filename (as opposed
# to a path).
#
# Let's define some useful stuff here, for this fix

import os.path

def fixWorkingDirForJEM( filename ):
   """It prefixes the provided filename with JEM's working directory, if available,
      only if filename is NOT an absolute path (in which case the user truly knows
      where they want to store it).
   """
   
   try:

      JEM_getMainFilePath   # check if function JEM_getMainFilePath() is defined (this happens only inside JEM) 
      
      # get working dir, if JEM is available
      workDir = JEM_getMainFilePath()
      
      # two cases for filename: 
      # 
      # 1. a relative filepath (e.g., just a filename, or "../filename")
      # 2. an absolute filepath
      
      if os.path.isabs( filename ):          # if an absolute path, the user knows what they are doing 
         return filename                     # ...so, do nothing
      else:                                  # else (if a relative pathname),
         return workDir + filename           # ...fix it
   
   except:   
      # if JEM is not available, do nothing (e.g., music.py is being run outside of JEM)
      return filename


######################################################################################
#### jMusic Read extensions ##########################################################
######################################################################################

from jm.util import Read as jRead  # needed to wrap more functionality below
from image import *                # import Image class and related Java libraries

# Create Read.image("test.jpg") to return an image, in addition to Read's default functionality.
# This class is not meant to be instantiated, hence no "self" in function definitions.
# Functions are made callable through class Callable, above.
class Read(jRead):

   def midi(score, filename):
      """Import a standard MIDI file to a jMusic score."""
      
      # JEM working directory fix (see above)
      filename = fixWorkingDirForJEM( filename )   # does nothing if not in JEM
      
      # use fixed filename with jMusic's Read.midi() 
      jRead.midi(score, filename)

   # make this function callable without having to instantiate this class
   midi = Callable(midi)  

######################################################################################
#### jMusic Write extensions #########################################################
######################################################################################

from jm.util import Write as jWrite  # needed to wrap more functionality below

# Create Write.image(image, "test.jpg") to write an image to file, in addition 
# to Write's default functionality.
# This class is not meant to be instantiated, hence no "self" in function definitions.
# Functions are made callable through class Callable, above.

class Write(jWrite):

   def midi(score, filename):
      """Save a standard MIDI file from a jMusic score."""
      
      # JEM working directory fix (see above)
      filename = fixWorkingDirForJEM( filename )   # does nothing if not in JEM
      
      #***
      #print "fixWorkingDirForJEM( filename ) =", filename
      
      # use fixed filename with jMusic's Write.midi() 
      jWrite.midi(score, filename)

   # make this function callable without having to instantiate this class
   midi = Callable(midi)  

######################################################################################
#### jMusic Phrase extensions ########################################################
######################################################################################

from jm.music.data import *
from jm.music.data import Phrase as jPhrase  # needed to wrap more functionality below

# update Phrase's addNoteList to handle chords, i.e., lists of pitches, 
# in addition to single pitches (the default functionality).
class Phrase(jPhrase):

   def __str__(self):    
      # we disrupted access to jMusic's (Java's) Phrase.toString() method,
      # so, let's fix it
      return self.toString()

   def __repr__(self):    
      # we disrupted access to jMusic's (Java's) Phrase.toString() method,
      # so, let's fix it
      return self.toString()

   def addChord(self, pitches, duration, dynamic=85, panoramic=0.5):    
      # add all notes, minus the last one, as having no duration,
      # but normal length (exploiting how Play.midi() and Write.midi() work)
      for i in range( len(pitches)-1 ):
         n = Note(pitches[i], 0.0, dynamic, panoramic)
         n.setLength(duration * Note.DEFAULT_LENGTH_MULTIPLIER)
         self.addNote(n)

      # now, add the last note with the proper rhythm value
      n = Note(pitches[-1], duration, dynamic, panoramic)
      self.addNote(n)

   def addNoteList(self, pitches, durations, dynamics=[], panoramics=[]):    
      # if dynamics was not provided, construct it with max value
      if dynamics == []:
         dynamics = [85] * len(pitches)
      
      # if panoramics was not provided, construct it at CENTER
      if panoramics == []:
         panoramics = [0.5] * len(pitches)
      
      # traverse the pitch list and handle every item appropriately
      for i in range( len(pitches) ):        
         if type(pitches[i]) == list:              # is it a chord?
            self.addChord(pitches[i], durations[i], dynamics[i], panoramics[i])  # yes, so add it
         else:                                     # else, not a chord
            n = Note(pitches[i], durations[i], dynamics[i], panoramics[i])
            self.addNote(n)   # so handle it as usual

# Do NOT make these functions callable - Phrase class is meant to be instantiated,
# i.e., we will always call these from a Phrase object - not the class, e.g., as in Mod.

######################################################################################
#### jMusic Play extensions ##########################################################
######################################################################################

from jm.util import Play as jPlay  # needed to wrap more functionality below

# Create Play.noteOn(pitch, velocity, channel) to start a MIDI note sounding,  
#        Play.noteOff(pitch, channel) to stop the corresponding note from sounding, and
#        Play.setInstrument(instrument, channel) to change instrument for this channel.
#
# This adds to existing Play functionality.
# This class is not meant to be instantiated, hence no "self" in function definitions.
# Functions are made callable through class Callable, above.

from javax.sound.midi import *

# NOTE: Opening the Java synthesizer below generates some low-level noise in the audio output.
# But we need it to be open, in clase the end-user wishes to use functions like Play.noteOn(), below. 
# (*** Is there a way to open it just-in-time, and/or close it when not used? I cannot think of one.)
 
Java_synthesizer = MidiSystem.getSynthesizer()  # get a Java synthesizer
Java_synthesizer.open()                         # and activate it (should we worry about close()???)

# make all instruments available
Java_synthesizer.loadAllInstruments(Java_synthesizer.getDefaultSoundbank())   
 
# The MIDI specification stipulates that pitch bend be a 14-bit value, where zero is 
# maximum downward bend, 16383 is maximum upward bend, and 8192 is the center (no pitch bend).
PITCHBEND_MIN = 0 
PITCHBEND_MAX = 16383 
PITCHBEND_NORMAL = 8192

###############################################################################
# freqToNote   Convert frequency to MIDI note number
#        freqToNote(f) converts frequency to the closest MIDI note
#        number with pitch bend value for finer control.  A4 corresponds to 
#        the note number 69 (concert pitch is set to 440Hz by default).  
#        The default pitch bend range is 2 half tones above and below.
# 
#        2005-10-13 by MARUI Atsushi
#        See http://www.geidai.ac.jp/~marui/octave/node3.html
#
# For example, "sliding" from A4 (MIDI pitch 69, frequency 440 Hz) 
#              to a bit over AS4 (MIDI pitch 70, frequency 466.1637615181 Hz).
#
#>>>for f in range(440, 468):                                       
#...    print freqToNote(f)
#... 
#(69, 0)
#(69, 322)
#(69, 643)
#(69, 964)
#(69, 1283)
#(69, 1603)
#(69, 1921)
#(69, 2239)
#(69, 2555)
#(69, 2872)
#(69, 3187)
#(69, 3502)
#(69, 3816)
#(70, -4062)
#(70, -3750)
#(70, -3438)
#(70, -3126)
#(70, -2816)
#(70, -2506)
#(70, -2196)
#(70, -1888)
#(70, -1580)
#(70, -1272)
#(70, -966)
#(70, -660)
#(70, -354)
#(70, -50)
#(70, 254)
#
# The above overshoots AS4 (MIDI pitch 70, frequency 466.1637615181 Hz).
# So, here is converting the exact frequency:
#
#>>> freqToNote(466.1637615181) 
#(70, 0)
###############################################################################

def freqToNote(f):
   """Converts frequency to the closest MIDI note number with pitch bend value 
      for finer control.  A4 corresponds to the note number 69 (concert pitch
      is set to 440Hz by default).  The default pitch bend range is 4 half tones.
   """
   
   from math import log
   
   concertPitch = 440.0   # 440Hz
   bendRange = 4          # 4 half tones (2 below, 2 above)
    
   x = log(f / concertPitch, 2) * 12 + 69
   note = round(x)
   pitchBend = round((x - note) * 8192 / bendRange * 2)

   return int(note), int(pitchBend)
    
    
#########
# NOTE:  The following code addresses Play.midi() functionality.  There have been some problems
#        with jMusic's Play.midi.  Thi code was introduced to address them.  It wraps the 
# jMusic Play class inside a Python Play class and rebuilding play music functionality from basic elements.  
# This code does not work perfectly.  Every now and then users report some slow downs, or dropped notes, etc.
# It seems that, after a while, MidiSynths get bogged down with data that have not been cleared
# well, or that some threading issues emerge.  Unknown for now.  The following code works well
# enough for most people - the errors cannot be recreated consistently, so it is unclear how
# to fix them.
#
###############################################################################
# Andrew Brown has offered another solution (from inside jMusic), which may be something to try
# in the future - copied here verbatim from his email:
#
#   There is a Play.midi() call with four arguments that might assist.
#
#   Play.midi(score, true, false, 1, 0);
#
#   This takes a score (only). 
#   The first boolean relates to exiting the when done.
#   The second boolean is about initiating ht wait thread , or not.
#   The third argument is the number of synths necessary.
#   The fourth is an addition time (milliseconds) before exiting - sometime useful for not chopping off reverb tails.
#
#   If you use either
#   Play.midi(score, true, false, 1, 0);
#   or
#   Play.midi(score, false, false, 1, 0);
#
#   This might for the basis of a solution and Play.stopMidi() may halt playback mid stream. 
#   This assumes there is a GUI to keep Java active. At the command line these calls can shut down 
#   before the music starts to play.
###############################################################################


# Below is the Python solution - wrapping jMusic's Play inside a Python class, and 
# rebuilding play music functionality from basic elements. 

from jm.midi import MidiSynth  # needed to play and loop MIDI
from time import sleep         # needed to implement efficient busy-wait loops (see below)
from timer import *            # needed to schedule future tasks

# NOTE:  For some reason, jMusic's Play.midi() stops working after 12 invocations.
# We fix this problem below, by allocating several MidiSynths and reusing them (when available).
__midiSynths__ = []            # holds all available jMusic MidiSynths 
MAX_MIDI_SYNTHS = 4            # max number of concurrent MidiSynths allowed 
                               # NOTE: This is an empirical value - not documented - may change.                               
                               
def __getMidiSynth__():
   """Returns the next available MidiSynth (if any), or None."""
         
   # make sure all possible MidiSynths are allocated 
   if __midiSynths__ == []:
      for i in range(MAX_MIDI_SYNTHS):
         __midiSynths__.append( MidiSynth() )   # create a new MIDI synthesizer
   # now, all MidiSynths are allocated
      
   # find an available MidiSynth to play the material (it's possible that all are allocated,
   # since this function may be called repeatedly, while other music is still sounding
   i = 0
   while i < MAX_MIDI_SYNTHS and __midiSynths__[i].isPlaying():
      i = i + 1     # check if the next MidiSynth is available
   # now, i either points to the next available MidiSynth, or MAX_MIDI_SYNTHS if none is available
      
   # did we find an available MidiSynth?
   if i < MAX_MIDI_SYNTHS:
      midiSynth = __midiSynths__[i]
   else:
      midiSynth = None

   return midiSynth    # let them have it (hopefully, they will use it right away)

# Provide a way to stop all MidiSynths from playing.
def __stopMidiSynths__():
   """Stops all MidiSynths from playing."""
   for midiSynth in __midiSynths__:
      if midiSynth.isPlaying():    # if playing, stop it
         midiSynth.stop()
   
      
#########
class Play(jPlay):      

   # redefine Play.midi to fix jMusic bug (see above) - now, we can play as many times as we wish.
   def midi(material):
      """Play jMusic material (Score, Part, Phrase, Note) using next available MidiSynth (if any)."""
      
      from jm.music.data import Phrase as jPhrase   # since we extend Phrase later
      
      midiSynth = __getMidiSynth__()  # get next available MidiSynth (or None if all busy)
      #midiSynth = MidiSynth()    # create a new MIDI synthesizer
            
      # did we find an available midiSynth?
      if midiSynth:
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
         
            midiSynth.play( material )   # play it!
         
         else:   # error check    
            print "Play.midi() - Unrecognized type", type(material), "- expected Note, Phrase, Part, or Score."

      else:   # error check    
         print "Play.midi() - All", MAX_MIDI_SYNTHS, "MIDI synthesizers are busy - (try again later?)"
         
      return midiSynth  # return midiSynth playing
                     
   def noteOn(pitch, velocity=100, channel=0):
      """Send a NOTE_ON message for this pitch to the Java synthesizer object."""
      
      global Java_synthesizer
            
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      channelHandle.noteOn(pitch, velocity)                     # send the message
      
   def noteOff(pitch, channel=0):
      """Send a NOTE_OFF message for this pitch to the Java synthesizer object."""
      
      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      channelHandle.noteOff(pitch)                              # send the message

   def allNotesOff():
      """It turns off all notes on all channels."""
      
      global Java_synthesizer
      
      for channel in range(16):  # cycle through all channels
         channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
         channelHandle.allNotesOff()                               # send the message         

   def stop():
      """It stops all Play music from sounding."""
      
      # NOTE:  This needs to be updated to handle Play.note() notes, which may have been
      #        scheduled to start sometime in the future.  To do so, we will need to maintain
      #        a list of timers, __Play_startNoteTimers__, updated every time Play.note creates
      #        a timer.  Then, we cycle through it and stop all these timers (and delete them).
      #
      #        This may not be a big problem though to require fixing.
      
      # first, stop the internal __getMidiSynth__ synthesizers
      __stopMidiSynths__()
      
      # then, stop all sounding notes
      Play.allNotesOff()
      
      # in the future, we may also want to handle scheduled notes through Play.note() 


   def setInstrument(instrument, channel=0):
      """Send a patch change message for this channel to the Java synthesizer object."""
      
      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      channelHandle.programChange(channel, instrument)          # send the message

   def getInstrument(channel=0):
      """Gets the current instrument for this channel of the Java synthesizer object."""
      
      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      instrument = channelHandle.getProgram()                   # get the instrument
      return instrument

   def setVolume(volume, channel=0):
      """Sets the current coarse volume for this channel to the Java synthesizer object."""
      
      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      channelHandle.controlChange(7, volume)                    # send the message

   def getVolume(channel=0):
      """Gets the current coarse volume for this channel of the Java synthesizer object."""

      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      return channelHandle.getController(7)                     # obtain the current value for volume controller

   def setPanning(position, channel=0):
      """Sets the current panning setting for this channel to the Java synthesizer object."""
      
      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      channelHandle.controlChange(10, position)                 # send the message

   def getPanning(channel=0):
      """Gets the current panning setting for this channel of the Java synthesizer object."""

      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      return channelHandle.getController(10)                    # obtain the current value for panning controller
      
   # No (normal) pitch bend is 0, max downward bend is -8192, and max upward bend is 8191.
   # (Result is undefined if you exceed these values - it may wrap around or it may cap.)
   def setPitchBend(bend = 0, channel=0):
      """Send a pitchbend message for this channel to the Java synthesizer object."""
      
      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel

      # NOTE: The MIDI specification states that pitch is a 14-bit value, where zero is 
      # maximum downward bend, 16383 is maximum upward bend, and 8192 is center - no pitch bend.
      # Here we adjust for no pitch bend (center) to be 0, max downward bend to be -8192, and
      # max upward bend to be 8191.  
      channelHandle.setPitchBend(bend + PITCHBEND_NORMAL)       # send the message

   def getPitchBend(channel=0):
      """Gets the current pitchbend for this channel of the Java synthesizer object."""
      
      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      bend = channelHandle.getPitchBend()                       # get the pitchbend
      return bend
      
   def note(pitch, start, duration, velocity=100, channel=0):
      """Plays a note with given 'start' time (in milliseconds from now), 'duration' (in milliseconds
         from 'start' time), with given 'velocity' on 'channel'.""" 
         
      # TODO: We should probably test for negative start times and durations.
         
      # create a timer for the note-on event
      noteOn = Timer(start, Play.noteOn, [pitch, velocity, channel], False)

      # create a timer for the note-off event
      noteOff = Timer(start+duration, Play.noteOff, [pitch, channel], False)

      # and activate timers (set thinsg in motion)
      noteOn.start()
      noteOff.start()
      
      # NOTE:  Upon completion of this function, the two Timer objects become unreferenced.
      #        When the timers elapse, then the two objects (in theory) should be garbage-collectable,
      #        and should be eventually cleaned up.  So, here, no effort is made in reusing timer objects, etc.

   def score(score):
      """Plays a jMusic Score using above functions."""
      
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
         Play.setInstrument(instrument, channel)
         # schedule a Play.note event
         Play.note(pitch, int(start * FACTOR), int(duration * FACTOR), velocity, channel)
         #print "Play.note(" + str(pitch) + ", " + str(int(start * FACTOR)) + ", " + str(int(duration * FACTOR)) + ", " + str(velocity) + ", " + str(channel) + ")"
       

   ################################
   # Now, a bit more esoteric stuff

   def frequencyOn(frequency, velocity=100, channel=0):
      """Send a NOTE_ON message for this frequency (in Hz) to the Java synthesizer object."""
      
      pitch, bend = freqToNote( frequency )  # convert to MIDI note and pitch bend
      Play.noteOnPitchBend(pitch, bend, velocity, channel)
      
   def frequencyOff(frequency, channel=0):
      """Send a NOTE_OFF message for this frequency (in Hz) to the Java synthesizer object."""
      
      pitch, bend = freqToNote( frequency )  # convert to MIDI note and pitch bend
      Play.noteOff(pitch, channel)

      # NOTE: Just to be good citizens, also rurn pitch bend to normal (i.e., no bend).
      Play.setPitchBend(0, channel)

   def allFrequenciesOff():
      """It turns off all notes on all channels."""

      Play.allNotesOff()   

   # No (normal) pitch bend is 0, max downward bend is -8192, and max upward bend is 8191.
   # (Result is undefined if you exceed these values - it may wrap around or it may cap.)
   def noteOnPitchBend(pitch, bend = 0, velocity=100, channel=0):
      """Send a NOTE_ON message for this pitch and pitch bend to the Java synthesizer object."""
            
      Play.setPitchBend(bend, channel)  # adjust for normal pitchbend setting for Java synthsizer
      Play.noteOn(pitch, velocity, channel)
      
# (BZM) Commented out below, because it might give the impression that different pitch bends
# signify different notes to be turned off - not so.  NOTE_OFF messages are based solely on pitch.

#   def noteOffPitchBend(pitch, bend = 0, channel=0):
#      """Send a NOTE_OFF message for this pitch to the Java synthesizer object."""
#      # NOTE_OFF messages are based on pitch (i.e., pitch bend is irrelevant / ignored)
#      Play.noteOff(pitch, channel)

   # make these functions callable without having to instantiate this class
   midi = Callable(midi)  
   noteOn = Callable(noteOn)  
   noteOnPitchBend = Callable(noteOnPitchBend)  
   noteOff = Callable(noteOff)  
   note = Callable(note)  
   #noteOffPitchBend = Callable(noteOffPitchBend)  
   allNotesOff = Callable(allNotesOff)  
   frequencyOn = Callable(frequencyOn)  
   frequencyOff = Callable(frequencyOff)  
   allFrequenciesOff = Callable(allFrequenciesOff)  
   stop = Callable(stop)  
   setInstrument = Callable(setInstrument)  
   getInstrument = Callable(getInstrument)
   setVolume = Callable(setVolume)
   getVolume = Callable(getVolume)
   setPanning = Callable(setPanning)
   getPanning = Callable(getPanning)
   setPitchBend = Callable(setPitchBend)  
   getPitchBend = Callable(getPitchBend)  


######################################################################################
# If running inside JEM, register function that stops music from playing, when the 
# Stop button is pressed inside JEM.
######################################################################################

try:

    # if we are inside JEM, registerStopFunction() will be available
    registerStopFunction(Play.stop)   # tell JEM which function to call when the Stop button is pressed

except:  # otherwise (if we get an error), we are NOT inside JEM 

    pass    # so, do nothing.


######################################################################################
#### jSyn extensions #################################################################
######################################################################################


##### jSyn synthesizer ######################################
# create the jSyn synthesizer (one synthesizer for everything)

from java.io import *  # for File

from com.jsyn import *
from com.jsyn.data import *
from com.jsyn.unitgen import *
from com.jsyn.util import *

from math import *

class jSyn_AudioEngine():
   """Encasulates a jSyn synthesizer.  Only one may exist (no need for more).
      We modularize the synth and its operations in a class for convenience.
   """
   
   instance = None      # only one instance allowed (no need for more)
   
   def __init__(self):
   
      if jSyn_AudioEngine.instance == None:  # first time?
      
         self.synth = JSyn.createSynthesizer()   # create synthesizer         
         jSyn_AudioEngine.instance = self        # remember the only allowable instance         
         
         self.samples = []                       # holds audio samples connected to synthesizer

      else:                                  # an instance already exists
         print "Only one jSyn audio engine may exist (use existing one)."

   def start(self):
      """Starts the synthesizer."""
      self.synth.start()            # start the synth
      for sample in self.samples:   # and all the sample lineOut units
         sample.lineOut.start()
   
   def stop(self):
      """Stops the synthesizer."""
      
      self.synth.stop()             # stop the synth      
      for sample in self.samples:   # and all the sample lineOut units
         sample.lineOut.stop()

   def add(self, sample):
      """Connects an audio sample to the jSyn lineOut unit."""
      
      self.synth.add( sample.player )   # add the sample's player to the synth
      self.synth.add( sample.lineOut )  # add the sample's lineOut to the synth

      self.samples.append( sample )     # remmeber this sample
   
# *** NOTE:  This synthesizer should be started only when an audio file (AudioSample) is created.
#            Perhaps do the same with the Java synthesizer above?  Is that synthesizer needed?

# create the jSyn synthesizer (again, only one for everything)
jSyn = jSyn_AudioEngine()
jSyn.start()                 # should this be happening here? (or inside the Audio class, when needed?) ***

##### AudioSample class ######################################

import os   # to check if provided filename exists

class AudioSample():
   """
   Encapsulates a sound object created from an external audio file, which can be played once,
   looped, paused, resumed, and stopped.  Also, each sound has a MIDI pitch associated with it
   (default is A4), so we can play different pitches with it (through pitch shifting).
   Finally, we can set/get its volume (0-127).
      
   Ideally, an audio object will be created with a specific pitch in mind.
      
   Supported data formats are WAV or AIF files (16, 24 and 32 bit PCM, and 32-bit float).
   """
   
   def __init__(self, filename, pitch=A4, volume=127, envelope=None):
   
      # ensure the file exists (jSyn will NOT complain on its own)
      if not os.path.isfile(filename):
         raise ValueError("File '" + str(filename) + "' does not exist.")
         
      # file exists, so continue   
      self.filename = filename
      
      self.defaultPitch = pitch  # the default pitch of the audio file (sample)
      self.pitch = pitch         # holds playback MIDI pitch (may be different from default pitch)
      self.frequency = self.__convertPitchToFrequency__(pitch)  # holds the frequency equivalent of the current MIDI pitch

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

      # now, connect pan control to mixer
      self.panLeft.output.connect( 0, self.lineOut.input, 0 ) 
      self.panRight.output.connect( 1, self.lineOut.input, 1 ) 

      # now, that panning is set up, initialize it to center
      self.panning = 63                # ranges from 0 (left) to 127 (right) - 63 is center
      self.setPanning( self.panning )  # and initialize
      

      # create sample player (mono or stereo, as needed) and connect to lineOut mixer
#      if self.channels == 1:    # mono audio?
#         self.player = VariableRateMonoReader()                  # create mono sample player
#         self.player.output.connect( 0, self.lineOut.input, 0 )  # connect single channel to mixer 
#
#      elif self.channels == 2:  # stereo audio?
#         self.player = VariableRateStereoReader()                # create stereo sample player
#         self.player.output.connect( 0, self.lineOut.input, 0 )  # connect both channels to mixer 
#         self.player.output.connect( 1, self.lineOut.input, 1 ) 
#
#      else:
#         raise TypeError( "Can only play mono or stereo samples." )
   
      self.player.rate.set( self.sample.getFrameRate() )  # play at original pitch

      self.volume = volume           # holds current volume (0 - 127)
      self.setVolume( self.volume )  # set the desired volume      
      
      self.envelope = envelope       # remember the envelope (if any)
      
      # if they provided an envelope
      if self.envelope:
         
         # create a synth envelope and set its sustain points
         self.envelopeData = SegmentedEnvelope(self.envelope.getDurationValuePairs())
         
         self.envelopeData.setSustainBegin(self.envelope.getLoopStart())
         self.envelopeData.setSustainEnd(self.envelope.getLoopEnd())
         
      # create an envelope player and connect to the synthesizer
         self.envelopePlayer = VariableRateMonoReader()
 
         self.envelopePlayer.output.connect(self.player.amplitude) 
         jSyn.synth.add(self.envelopePlayer)


      # NOTE:  Adding to global jSyn synthesizer
      jSyn.add(self)   # connect sample unit to the jSyn synthesizer
     
      
   ### functions to control playback and looping ######################
   def play(self, start=0, size=-1):
      """
      Play the sample once from the millisecond 'start' until the millisecond 'start'+'size' 
      (size == -1 means to the end). If 'start' and 'size' are omitted, play the complete sample.
      """
      # for faster response, restart playing (as opposed to queue at the end)
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
         

   def queueOn(self):
      """
      If no envelope is specified for the sample, functions exactly like play(). 
      If an envelope is specified, plays the sample with the envelope, looping the
      sustain loop of the envelope, if there is one.
      """
      if self.envelope:   # if they provided an envelope
     
         self.envelopePlayer.dataQueue.clear()          # clear old data from the queue
         self.envelopePlayer.dataQueue.queueOn(self.envelopeData)   # enqueue the user data
         self.envelopePlayer.start()                    # start the volume envelope
         
      self.play()
      
      
   def queueOff(self):
      """
      If no envelope is specified for the sample, calls stop().
      If an envelope is specified, ends the sustain loop for the envelope and finishes
      executing the release portion of the envelope.
      """
      if self.envelope:   # if they provided an envelope
      
         self.envelopePlayer.dataQueue.queueOff(self.envelopeData)      # end sustain loop and continue
         
         # calculate how much sound is remaining
         releaseList = self.envelope.getTimes()[self.envelope.getLoopEnd() + 1:]
         totalTime = 0
         for time in releaseList:
            totalTime += time
    
         jSyn.synth.sleepFor(totalTime / 1000)   # sleep until the end of the envelope

      # stop the sound
      self.stop()
      
      
   def stop(self):
      """
      Stop the sample play.
      """
      self.player.dataQueue.clear()   
      
   def isPlaying(self):
      """
      Returns True if the sample is still playing.
      """
      return self.player.dataQueue.hasMore()   
      
   def pause(self):
      """
      Pause the sample play (remembers current position for resume).
      """
      self.lineOut.stop() 
   
   def resume(self):
      """
      Resume playing the sample (from the paused position).
      """
      self.lineOut.start() 

   ### functions to control playback parameters (pitch, frequency, and volume) ##########
   def setPitch(self, pitch):
      """
      Set the sample pitch (through pitch shifting from sample's base pitch).
      """
      self.pitch = pitch    # remember new playback pitch      
      self.frequency = self.__convertPitchToFrequency__(pitch)  # and corresponding pitch frequency
            
      semitones = pitch - self.defaultPitch  # get the pitch change in semitones                    
   
      # calculate the change in playback rate, and adjust the playback rate
      rateChange = self.__getFrequencyChangeBySemitones__( self.getFrameRate(), semitones )   
      self.__setPlaybackRate__( self.getFrameRate() + rateChange )        

   def getPitch(self):
      """
      Return the sample's current pitch (it may be different from the default pitch).
      """
      return self.pitch
         
   def getDefaultPitch(self):
      """
      Return the sample's default pitch.
      """
      return self.defaultPitch
         
   def setFrequency(self, freq):
      """
      Set the sample pitch frequency.
      """      
      self.setPitch( self.__convertFrequencyToPitch__(freq) )
            
   def getFrequency(self):
      """
      Return the playback frequency.
      """      
      return self.frequency
         
   def setPanning(self, panning):
      """
      Set the panning of the sample (panning ranges from 0 - 127).
      """
      self.panning = panning                                     # remember new panning
      panValue     = mapValue(self.panning, 0, 127, -1.0, 1.0)   # map panning from 0, 127 to -1.0, 1.0

      # NOTE: The two pan controls have only one of their outputs (as their names indicate)
      # connected to LineOut.  This way, we can set their pan value as we would normally, and not worry
      # about clipping (i.e., doubling the output amplitude).  Also, this works for both mono and
      # stereo samples.

      self.panLeft.pan.set( panValue )                           # and set it
      self.panRight.pan.set( panValue )                    
  
   def getPanning(self):
      """
      Return the current panning of the sample (panning ranges from 0 - 127).
      """
      return self.panning

   def setVolume(self, volume):
      """
      Set the volume (amplitude) of the sample (volume ranges from 0 - 127).
      """
      self.volume = volume                                 # remember new volume
      amplitude = mapValue(self.volume, 0, 127, 0.0, 1.0)  # map volume to amplitude
      self.player.amplitude.set( amplitude )               # and set it
   
   def getVolume(self):
      """
      Return the current volume (amplitude) of the sample (volume ranges from 0 - 127).
      """
      return self.volume
      
      
   def getVolumeEnvelope(self):
      """Returns the volume envelope (if any)."""
      return self.envelope
      

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
   
   
   
##### Envelope class ######################################

class Envelope():
   """
   Creates an envelope of volume mappings which can be added to an AudioSample to modify its
   amplitude. Note that the envelope does NOT change the sample's volume property directly,
   but rather serves as a filter through which it is played, leaving the original sample
   unchanged. The Envelope consists of a list of duration-value tuples specifying 
   the volume changes.  It also has two optional indices into that list demarcating a section of the
   envelope to be looped continually until the end of the sample, at which point the 
   remainder of the envelope beyond the sustainLoopEndIndex will be played.
   """
 
   def __init__(self, times, values, sustainLoopStartIndex, sustainLoopEndIndex):
      self.times = times       # in milliseconds
      self.values = values     # in MIDI volume values (0-127)
      self.loopStart = sustainLoopStartIndex
      self.loopEnd = sustainLoopEndIndex
      self.durationValuePairs = self.__createDurationValuePairs__(times, values)


   def getTimes(self):
      return self.times

   def getValues(self):
      return self.values

   def getLoopStart(self):
      return self.loopStart

   def getLoopEnd(self):
      return self.loopEnd

   def getDurationValuePairs(self):
      return self.durationValuePairs

   def __createDurationValuePairs__(self, times, values):
      """ 
      Integrates the times and value lists into a single list.  Also converts the values in 'times'
      from milliseconds to seconds and then the values in 'values' from MIDI volumes (0 - 127) to JSyn 
      amplitude values (0.0 - 1.0)
      """
      result = []

      if (len(times) == len(values)):  # are the lists parallel
         for i in range(len(times)):
            result.append(times[i] / 1000.0)
            result.append(mapValue(values[i], 0, 127, 0.0, 1.0))  

      else:
         raise IndexError("The two lists should have the same length.")

      return result

   

##### MidiSequence class ######################################

# *** How about re-doing this from scratch, using Java's Sequencer and Seuqnce classes, bypassing jMusic MidiSynth?
#     We will still need to use MidiSynth.scoreToSeq() - but that's all.
#     Perhaps this will take care of the tempo problems described below, and allow us to define more functionality,
#     and be more consistent to AudioSample above...

class MidiSequence():
   """Encapsulates a midi sequence object created from the provided material, which is either a string
      - the filename of a MIDI file (.mid), or music library object (Score, Part, Phrase, or Note).
      The midi sequence has a default MIDI pitch (e.g., A4) and volume.  The sequence can be played once, looped,
      and stopped.  Also, we may change its pitch, tempo, and volume.  These changes happen immediately.  
   """
   
   def __init__(self, material, pitch=A4, volume=127):
   
      # determine what type of material we have
      if type(material) == type(""):   # a string?

         self.filename = material                # assume it's an external MIDI filename

         # load and create the MIDI sample
         self.score = Score()                    # create an empty score
         Read.midi(self.score, self.filename)    # load the external MIDI file
         
      else:  # determine what type of material we have 

         # and do necessary datatype wrapping (MidiSynth() expects a Score)
         if type(material) == type(Note()):
            material = Phrase(material)
         if type(material) == type(Phrase()):   # no elif - we need to successively wrap from Note to Score
            material = Part(material)
         if type(material) == type(jPhrase()):  # (also wrap jMusic default Phrases, in addition to our own)
            material = Part(material)
         if type(material) == type(Part()):     # no elif - we need to successively wrap from Note to Score
            material = Score(material)
         
         if type(material) == type(Score()):
         
            self.score = material     # and remember it
            
         else:   # error check    
            raise TypeError("Midi() - Unrecognized type", type(material), "- expected filename (string), Note, Phrase, Part, or Score.")

      # now, self.score contains a Score object
      
      # create Midi sequencer to playback this sample
      self.midiSynth = self.__initMidiSynth__()
      
      # get access to the MidiSynth's internal components (neededd for some of our operations)
      self.sequencer = self.midiSynth.getSequencer()
      self.synthesizer = self.midiSynth.getSynthesizer()
      
      # set tempo factor
      self.tempoFactor = 1.0   # scales whatever tempo is set for the sequence (1.0 means no change) 

      self.defaultTempo = self.score.getTempo()   # remember default tempo
      self.playbackTempo = self.defaultTempo      # set playback tempo to default tempo

      # set volume 
      self.volume = volume           # holds volume (0-127)
      self.setVolume( self.volume )  # set desired volume     
      
      # set MIDI score's default pitch
      self.pitch = pitch                         # remember provided pitch

   def __initMidiSynth__(self):
      """Ceates and initializes a MidiSynth object."""
      
      # NOTE: Since we need access to the "guts" of the MidiSynth object, it is important to initialize it.
      #       This happens automatically the first time we play something through it, so let's play an empty score.
      midiSynth = MidiSynth()   # create it
      midiSynth.play( Score() ) # and initialize it      
      return midiSynth
   

   def play(self):
      """Play the MIDI score."""

      # make sure only one play is active at a time
      if self.midiSynth.isPlaying():     # is another play is on?
         self.stop()                        # yes, so stop it
         
      #self.sequencer.setLoopCount(0)     # set to no repetition (needed, in case we are called after loop())
      self.midiSynth.setCycle(False)     # turn off looping (just in case)
      self.midiSynth.play( self.score )  # play it!     
      
   def loop(self):
      """Repeat the score indefinitely."""
      
      # make sure only one play is active at a time
      if self.midiSynth.isPlaying():     # is another play is on?
         self.stop()                        # yes, so stop it
         
      # Due to an apparent Java Sequencer bug in setting tempo, we can only loop indefinitely (not a specified 
      # number of times).  Looping a specified number of times causes the second iteration to playback at 120 BPM.
      #self.sequencer.setLoopCount(times)  # set the number of times to repeat the sequence
      self.midiSynth.setCycle(True)
      self.midiSynth.play( self.score )   # play it!

   def isPlaying(self):
      """
      Returns True if the sequence is still playing.
      """
      return self.midiSynth.isPlaying()   
      
   def stop(self):
      """Stop the MIDI score play."""

      self.midiSynth.stop()   

   def pause(self):
      """Pause the MIDI sequence play."""
      self.__setTempoFactor__(0.00000000000000000000000000000000000000000001) # slow play down to (almost) a standstill

   def resume(self):
      """
      Resume playing the sample (from the paused position).
      """
      self.__setTempoFactor__(1.0) # reset playback to original tempo (i.e., resume)

   # low-level helper function
   def __setTempoFactor__(self, factor = 1.0):   
      """
      Set MIDI sequence's tempo factor (1.0 means default, i.e., no change).
      """
      self.sequencer.setTempoFactor( factor )
      

   def setPitch(self, pitch):
      """Set the MidiSequence's playback pitch (by transposing the MIDI material)."""
      
      semitones = pitch - self.pitch          # get the pitch change in semitones       
      Mod.transpose( self.score, semitones )  # update score pitch appropriately
      
      # do some low-level work inside MidiSynth
      updatedSequence = self.midiSynth.scoreToSeq( self.score )  # get new Midi sequence from updated score            
      self.positionInMicroseconds = self.sequencer.getMicrosecondPosition()  # remember where to resume
      self.sequencer.setSequence(updatedSequence)                # update the sequence - this restarts playing...
      self.sequencer.setMicrosecondPosition( self.positionInMicroseconds )   # ...so reset playing to where we left off
      self.sequencer.setTempoInBPM( self.playbackTempo )         # set tempo (needed for the first (partial) iteration)

      # finally, remember new pitch
      self.pitch = pitch

   def getPitch(self):
      """Returns the MIDI score's pitch."""
      
      return self.pitch

   def getDefaultPitch(self):
      """Return the MidiSequence's default pitch."""

      return self.defaultPitch
     

   def setTempo(self, beatsPerMinute):
      """
      Set MIDI sequence's playback tempo.
      """
      # Due to an apparent Java Sequencer bug in setting tempo, when looping a specified number of times causes 
      # all but the first iteration to playback at 120 BPM, regardless of what the current tempo may be.
      # Unable to solve the problem in the general case, below is an attempt to fix it for some cases (e.g.,
      # for looping continuously, but not for looping a specified number of times).
      self.playbackTempo = beatsPerMinute               # keep track of new playback tempo
      self.sequencer.setTempoInBPM( beatsPerMinute )    # and set it
      self.midiSynth.setTempo( beatsPerMinute )         # and set it again (this seems redundant, but see above)
      self.score.setTempo( beatsPerMinute )             # and set it again (this seems redundant, but see above)

   def getTempo(self):   
      """
      Return MIDI sequence's playback tempo.
      """
      return self.playbackTempo

   def getDefaultTempo(self):
      """
      Return MIDI sequence's default tempo (in beats per minute).
      """
      return self.defaultTempo
   

   def setVolume(self, volume):
      """Sets the volume for the MidiSequence (volume ranges from 0 - 127)."""
      
      self.volume = volume    # remember new volume

      # NOTE:  Setting volume through a MidiSynth is problematic.  
      #        Here we use a solution by Howard Amos (posted 8/16/2012) in
      #        http://www.coderanch.com/t/272584/java/java/MIDI-volume-control-difficulties
      volumeMessage = ShortMessage()    # create a MIDI message
      #receiver = self.sequencer.getTransmitters().iterator().next().getReceiver()  # get the MidiSynth receiver
      receiver = self.sequencer.getTransmitters()[0].getReceiver()  # get the MidiSynth receiver

      for channel in range(16):   # change volume of all the MIDI channels
         volumeMessage.setMessage(0xB0 + channel, 7, volume)   # set coarse volume control for this channel
         receiver.send (volumeMessage, -1)                     # and communicate it to the receiver

   def getVolume(self):
      """Returns the volume for the MidiSequence (volume ranges from 0 - 127)."""

      return self.volume


##### MidiSequence class ######################################

# *** How about re-doing this from scratch, using Java's Sequencer and Seuqnce classes, bypassing jMusic MidiSynth?
#     We will still need to use MidiSynth.scoreToSeq() - but that's all.
#     Perhaps this will take care of the tempo problems described below, and allow us to define more functionality,
#     and be more consistent to AudioSample above...

class MidiSequenceNew():
   """Encapsulates a midi sequence object created from the provided material, which is either a string
      - the filename of a MIDI file (.mid), or music library object (Score, Part, Phrase, or Note).
      The midi sequence has a default MIDI pitch (e.g., A4) and volume.  The sequence can be played once, looped,
      and stopped.  Also, we may change its pitch, tempo, and volume.  These changes happen immediately.  
   """
   
   def __init__(self, material, pitch=A4, volume=127):
   
      # determine what type of material we have
      if type(material) == type(""):   # a string?

         self.filename = material                # assume it's an external MIDI filename

         # load and create the MIDI sample
         self.score = Score()                    # create an empty score
         Read.midi(self.score, self.filename)    # load the external MIDI file
         
      else:  # determine what type of material we have 

         # and do necessary datatype wrapping (MidiSynth() expects a Score)
         if type(material) == type(Note()):
            material = Phrase(material)
         if type(material) == type(Phrase()):   # no elif - we need to successively wrap from Note to Score
            material = Part(material)
         if type(material) == type(jPhrase()):  # (also wrap jMusic default Phrases, in addition to our own)
            material = Part(material)
         if type(material) == type(Part()):     # no elif - we need to successively wrap from Note to Score
            material = Score(material)
         
         if type(material) == type(Score()):
         
            self.score = material     # and remember it
            
         else:   # error check    
            raise TypeError("Midi() - Unrecognized type", type(material), "- expected filename (string), Note, Phrase, Part, or Score.")

      # now, self.score contains a Score object
      
      # create Midi sequencer to playback this sample
      self.midiSynth = self.__initMidiSynth__()
      
      # get access to the MidiSynth's internal components (neededd for some of our operations)
      self.sequencer = self.midiSynth.getSequencer()
      self.synthesizer = self.midiSynth.getSynthesizer()
      
      # set tempo factor
      self.tempoFactor = 1.0   # scales whatever tempo is set for the sequence (1.0 means no change) 

      self.defaultTempo = self.score.getTempo()   # remember default tempo
      self.playbackTempo = self.defaultTempo      # set playback tempo to default tempo

      # set volume 
      self.volume = volume           # holds volume (0-127)
      self.setVolume( self.volume )  # set desired volume     
      
      # set MIDI score's default pitch
      self.pitch = pitch                         # remember provided pitch

   def __initMidiSynth__(self):
      """Ceates and initializes a MidiSynth object."""
      
      # NOTE: Since we need access to the "guts" of the MidiSynth object, it is important to initialize it.
      #       This happens automatically the first time we play something through it, so let's play an empty score.
      midiSynth = MidiSynth()   # create it
      midiSynth.play( Score() ) # and initialize it      
      return midiSynth
   

   def play(self):
      """Play the MIDI score."""

      # make sure only one play is active at a time
      if self.midiSynth.isPlaying():     # is another play is on?
         self.stop()                        # yes, so stop it
         
      #self.sequencer.setLoopCount(0)     # set to no repetition (needed, in case we are called after loop())
      self.midiSynth.setCycle(False)     # turn off looping (just in case)
      self.midiSynth.play( self.score )  # play it!     
      
   def loop(self):
      """Repeat the score indefinitely."""
      
      # make sure only one play is active at a time
      if self.midiSynth.isPlaying():     # is another play is on?
         self.stop()                        # yes, so stop it
         
      # Due to an apparent Java Sequencer bug in setting tempo, we can only loop indefinitely (not a specified 
      # number of times).  Looping a specified number of times causes the second iteration to playback at 120 BPM.
      #self.sequencer.setLoopCount(times)  # set the number of times to repeat the sequence
      self.midiSynth.setCycle(True)
      self.midiSynth.play( self.score )   # play it!

   def isPlaying(self):
      """
      Returns True if the sequence is still playing.
      """
      return self.midiSynth.isPlaying()   
      
   def stop(self):
      """Stop the MIDI score play."""

      self.midiSynth.stop()   

   def pause(self):
      """Pause the MIDI sequence play."""
      self.__setTempoFactor__(0.00000000000000000000000000000000000000000001) # slow play down to (almost) a standstill

   def resume(self):
      """
      Resume playing the sample (from the paused position).
      """
      self.__setTempoFactor__(1.0) # reset playback to original tempo (i.e., resume)

   # low-level helper function
   def __setTempoFactor__(self, factor = 1.0):   
      """
      Set MIDI sequence's tempo factor (1.0 means default, i.e., no change).
      """
      self.sequencer.setTempoFactor( factor )
      

   def setPitch(self, pitch):
      """Set the MidiSequence's playback pitch (by transposing the MIDI material)."""
      
      semitones = pitch - self.pitch          # get the pitch change in semitones       
      Mod.transpose( self.score, semitones )  # update score pitch appropriately
      
      # do some low-level work inside MidiSynth
      updatedSequence = self.midiSynth.scoreToSeq( self.score )  # get new Midi sequence from updated score            
      self.positionInMicroseconds = self.sequencer.getMicrosecondPosition()  # remember where to resume
      self.sequencer.setSequence(updatedSequence)                # update the sequence - this restarts playing...
      self.sequencer.setMicrosecondPosition( self.positionInMicroseconds )   # ...so reset playing to where we left off
      self.sequencer.setTempoInBPM( self.playbackTempo )         # set tempo (needed for the first (partial) iteration)

      # finally, remember new pitch
      self.pitch = pitch

   def getPitch(self):
      """Returns the MIDI score's pitch."""
      
      return self.pitch

   def getDefaultPitch(self):
      """Return the MidiSequence's default pitch."""

      return self.defaultPitch
     

   def setTempo(self, beatsPerMinute):
      """
      Set MIDI sequence's playback tempo.
      """
      # Due to an apparent Java Sequencer bug in setting tempo, when looping a specified number of times causes 
      # all but the first iteration to playback at 120 BPM, regardless of what the current tempo may be.
      # Unable to solve the problem in the general case, below is an attempt to fix it for some cases (e.g.,
      # for looping continuously, but not for looping a specified number of times).
      self.playbackTempo = beatsPerMinute               # keep track of new playback tempo
      self.sequencer.setTempoInBPM( beatsPerMinute )    # and set it
      self.midiSynth.setTempo( beatsPerMinute )         # and set it again (this seems redundant, but see above)
      self.score.setTempo( beatsPerMinute )             # and set it again (this seems redundant, but see above)

   def getTempo(self):   
      """
      Return MIDI sequence's playback tempo.
      """
      return self.playbackTempo

   def getDefaultTempo(self):
      """
      Return MIDI sequence's default tempo (in beats per minute).
      """
      return self.defaultTempo
   

   def setVolume(self, volume):
      """Sets the volume for the MidiSequence (volume ranges from 0 - 127)."""
      
      self.volume = volume    # remember new volume

      # NOTE:  Setting volume through a MidiSynth is problematic.  
      #        Here we use a solution by Howard Amos (posted 8/16/2012) in
      #        http://www.coderanch.com/t/272584/java/java/MIDI-volume-control-difficulties
      volumeMessage = ShortMessage()    # create a MIDI message
      #receiver = self.sequencer.getTransmitters().iterator().next().getReceiver()  # get the MidiSynth receiver
      receiver = self.sequencer.getTransmitters()[0].getReceiver()  # get the MidiSynth receiver

      for channel in range(16):   # change volume of all the MIDI channels
         volumeMessage.setMessage(0xB0 + channel, 7, volume)   # set coarse volume control for this channel
         receiver.send (volumeMessage, -1)                     # and communicate it to the receiver

   def getVolume(self):
      """Returns the volume for the MidiSequence (volume ranges from 0 - 127)."""

      return self.volume


##### Sound Synthesizer class ######################################

class SoundSynth():
   """Encapsulates a hybrid synthesizer which can be instantiated with a combination of 
      MIDI/MidiSequence/AudioSample instruments.  For now, we limit this to 16 instruments,
      to agree with the number of different channels that can be specified in music library Part
      objects.  We provide the following operations: noteOn(), noteOff(), allNotesOff(), and
      midi() - the latter as in Play.midi().  
      Note pitches can be specified by float numbers (so, for MIDI instruments, we utilize pitch bend).  
      Although we can play multiple MIDI notes per channel, if non-integer (i.e., 69.3) MIDI pitches are used, 
      the associated pitch bend applies to all other notes sounding on this channel at the time - hence 
      the suggested limitation of one note per channel.
      If MIDI pitches are all integers (e.g., 69.0), several notes on the same channel can be
      rendered (correctly).
      
      The provided instruments list may consist of integers (i.e., MIDI instruments), music library
      objects (Note, Phrase, Part, or Score), and strings (assumed to be WAV or AIF files).
   """
   
   def __init__(self, sounds, volume=127):
   
      self.sounds = sounds
      self.masterVolume = volume              # holds current volume (0 - 127)
      
      self.instruments = []                   # holds the instruments associated with each sound 

      # create all the instruments by creating Midi sequences, and audio samples
      for sound in self.sounds:

         # detrmine what type of sound we are dealing with, and instantiate appropriate classes (if needed)
         if isinstance(sound, int) and (0 <= sound <= 127):  # a MIDI instrument constant (0-127)?
         
            self.instruments.append( sound )                    # store the MIDI constant verbatim
         
         elif isinstance(sound, Note) or isinstance(sound, Phrase) or isinstance(sound, jPhrase) or isinstance(sound, Part) or isinstance(sound, Score):
         
            self.instruments.append( MidiSequence(sound) )      # build and store a MidiSequence
            
         elif isinstance(sound, str):    # an audio sample?
         
            self.instruments.append( AudioSample(sound) )       # build and store and AudioSample
            
         else:
            raise TypeError("SoundSynth() - Unrecognized sound type", type(sound), "- expected integer (0-127), filename (string), Note, Phrase, Part, or Score.")

      # now, self.instruments contains the various sound instruments (MIDI instrument numbers (0-127), MIDI sequences, or audio samples)
      
      # **** here
                  
      self.freeMidiChannels = range(16)    # holds all MIDI channels (banks) available to play a note
      self.busyMidiChannels = {}           # holds all MIDI channels (banks) playing a note (indexed by the note itself)

      
   def noteOn(self, pitch, instrument=0, volume=127):
      """Start playing this pitch on the corresponding instrument (if pitch is float we use pitch bend)."""
      
      #if 
      
      if len( self.freeBanks ) > 0:   # are there any available banks to play this note?

         # get next available AudioSample
         audioSample = self.freeBanks.pop()    # remove one from the list of available ones
         
         # add it to the collection of busy banks - indexed by pitch being played
         # (since there may be more than one concurrent note with the same pitch, we 
         # store a list of audioSamples per pitch)
         self.busyBanks[pitch] = self.busyBanks.get(pitch, []) + [audioSample]  # and append it 
      
         # NOTE:  We could have indexed self.busyBanks with (pitch, volume) to be able to
         # find the exact audio sample playing this pitch at a given volume, in case of more 
         # than one audio samples playing the same note - but the chances of this ever happening
         # are so small, that, for simplicity, we ignore this possibility (for now).
      
         # start note
         audioSample.setPitch( pitch )   # set the pitch for this audio sample, 
         audioSample.setVolume( volume ) # also set its volume, and
         audioSample.loop()              # start playing this note
      
      else:                             # all banks are busy, so let them know

         print "AudioInstrument.noteOn(" + str(pitch) + "): too many notes sounding."

            
   def noteOff(self, pitch):
      """Stop playing this pitch.  If pitch is not sounding, a warning is output."""
      
      try:     # see if this note is sounding
      
         audioSample = self.busyBanks[pitch].pop()  # get AudioSample playing this pitch (if any)
         audioSample.stop()                         # stop the note
         self.freeBanks.append( audioSample )       # put it back in the available banks
      
      except:  # this note was not sounding

         print "AudioInstrument.noteOff(" + str(pitch) + "): this pitch is not sounding."

   def allNotesOff(self):
      """It turns off all notes on all banks."""
      
      # turn off all sounding banks and return them to the free list
      for bankList in self.busyBanks.values():  # iterate through list of lists
         for audioSample in bankList:              # iterate through this list
            audioSample.stop()                        # stop this note
            self.freeBanks.append( audioSample )      # put it back in the available banks

     
         

##### AudioInstrument class ######################################

class AudioInstrument():
   """Encapsulates an instrument based on an audio sample, which may be used to play up to 16 
      overlapping, continuous notes, via operations noteOn(), noteOff(), allNotesOff(), 
      frequencyOn(), frequencyOff(), and allFrequenciesOff().  
      
      The instrument has a default MIDI pitch associated with it (if not specified, it is A4), 
      so we can play different pitches with it (through pitch shifting).
      
      The maxBanks parameter determines how many parallel (overlapping) notes this instrument
      can play.
      
      Supported data formats are WAV or AIF files (16, 24 and 32 bit PCM, and 32-bit float).
   """
   
   def __init__(self, filename, pitch=A4, volume=127, maxBanks=16):
   
      self.filename = filename
      self.defaultPitch = pitch  # the default pitch of the audio file (sample)
      self.pitch = pitch         # holds playback pitch (may be different from default pitch)
      self.volume = volume       # holds current volume (0 - 127)
      
      self.maxBanks = maxBanks   # number of concurrrent notes supported

      # create all the banks by loading the audio samples
      self.freeBanks = []    # holds all AudioSamples (banks) available to play a note
      for i in range( self.maxBanks ): 
         self.freeBanks.append( AudioSample(filename, pitch, volume) ) 
      # now, all AudioSamples (banks) have been created

      self.busyBanks = {}    # holds all AudioSamples (banks) playing a note (indexed by the note itself)

      
   def noteOn(self, pitch, volume=50):
      """Start playing this pitch on the next available AudioInstrument bank."""
      
      if len( self.freeBanks ) > 0:   # are there any available banks to play this note?

         # get next available AudioSample
         audioSample = self.freeBanks.pop()    # remove one from the list of available ones
         
         # add it to the collection of busy banks - indexed by pitch being played
         # (since there may be more than one concurrent note with the same pitch, we 
         # store a list of audioSamples per pitch)
         self.busyBanks[pitch] = self.busyBanks.get(pitch, []) + [audioSample]  # and append it 
      
         # NOTE:  We could have indexed self.busyBanks with (pitch, volume) to be able to
         # find the exact audio sample playing this pitch at a given volume, in case of more 
         # than one audio samples playing the same note - but the chances of this ever happening
         # are so small, that, for simplicity, we ignore this possibility (for now).
      
         # start note
         audioSample.setPitch( pitch )   # set the pitch for this audio sample, 
         audioSample.setVolume( volume ) # also set its volume, and
         audioSample.loop()              # start playing this note
      
      else:                             # all banks are busy, so let them know

         print "AudioInstrument.noteOn(" + str(pitch) + "): too many notes sounding."

            
   def noteOff(self, pitch):
      """Stop playing this pitch.  If pitch is not sounding, a warning is output."""
      
      try:     # see if this note is sounding
      
         audioSample = self.busyBanks[pitch].pop()  # get AudioSample playing this pitch (if any)
         audioSample.stop()                         # stop the note
         self.freeBanks.append( audioSample )       # put it back in the available banks
      
      except:  # this note was not sounding

         print "AudioInstrument.noteOff(" + str(pitch) + "): this pitch is not sounding."

   def allNotesOff(self):
      """It turns off all notes on all banks."""
      
      # turn off all sounding banks and return them to the free list
      for bankList in self.busyBanks.values():  # iterate through list of lists
         for audioSample in bankList:              # iterate through this list
            audioSample.stop()                        # stop this note
            self.freeBanks.append( audioSample )      # put it back in the available banks

   ################################
   # Now, a bit more esoteric stuff

   def frequencyOn(self, frequency, volume=50):
      """Start playing this frequency on the next available AudioInstrument bank."""
      
      if len( self.freeBanks ) > 0:   # are there any available banks to play this note?

         # get next available AudioSample
         audioSample = self.freeBanks.pop()    # remove one from the list of available ones
         
         # add it to the collection of busy banks - indexed by frequency being played
         # (since there may be more than one concurrent note with the same frequency, we 
         # store a list of audioSamples per pitch)
         self.busyBanks[frequency] = self.busyBanks.get(frequency, []) + [audioSample]  # and append it 
      
         # NOTE:  We could have indexed self.busyBanks with (frequency, volume) to be able to
         # find the exact audio sample playing this frequency at a given volume, in case of more 
         # than one audio samples playing the same note - but the chances of this ever happening
         # are so small, that, for simplicity, we ignore this possibility (for now).
      
         # start note
         audioSample.setFrequency( frequency )   # set the frequency for this audio sample, 
         audioSample.setVolume( volume )         # also set its volume, and
         audioSample.loop()                      # start playing this note
      
      else:                             # all banks are busy, so let them know

         print "AudioInstrument.frequencyOn(" + str(frequency) + "): too many notes sounding."
      
   def frequencyOff(self, frequency):
      """Stop playing this frequency.  If frequency is not sounding, a warning is output."""
      
      try:     # see if this note is sounding
      
         audioSample = self.busyBanks[frequency].pop()  # get AudioSample playing this frequency (if any)
         audioSample.stop()                             # stop the note
         self.freeBanks.append( audioSample )          # put it back in the available banks
      
      except:  # this note was not sounding

         print "AudioInstrument.frequencyOff(" + str(frequency) + "): this pitch is not sounding."

   def allFrequenciesOff(self):
      """It turns off all notes on all channels."""

      self.allNotesOff()   

