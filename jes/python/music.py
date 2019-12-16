################################################################################################################
# music.py      Version 4.11         21-Mar-2017       Bill Manaris, Marge Marshall, Chris Benson, and Kenneth Hanson

###########################################################################
#
# This file is part of Jython Music.
#
# Copyright (C) 2011-2016 Bill Manaris, Marge Marshall, Chris Benson, and Kenneth Hanson
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
# Imports jMusic and jSyn packages into jython.  Also provides additional functionality.
#
#
# REVISIONS:
#
# 4.11  21-Mar-2017 (bm)  Fixed Play.setPitchBend() to actually set the pitch bend, as it should.
#
# 4.10  16-Jan-2017 (bm)  Fixed Note.getPitch() to return REST for rest notes, as it should.
#
# 4.9   27-Dec-2016 (bm)  Fixed jMusic Note bug, where, if int pitch is given, both frequency and pitch attributes are populated, but 
#					if float pitch is given (i.e., frequency in Hertz), only the frequency attribute is populated - no pitch).
#					Consequently, in the second case, calling getPitch() crashes the system.  We fix it by also calling setFrequency()
#					or setPitch() in our wrapper of the Note constructor.  Also added getPitch() and getPitchBend() to fully convert
#					a frequency to MIDI pitch information.
#
# 4.8   26-Dec-2016 (mm)  Added Envelope class for using with Play.audio().  An envelope contains a list of attack times (in milliseconds, 
#					relative from the previous time) and values (to reach at those times), how long to wait (delay time, in milliseconds, 
#					relative from the previous time) to get to a sustain value, and then how long to wait to reach a value of zero 
#					(in milliseconds, relative from the end time).  Also modified Play.audio() to accept an Envelope as an optional parameter.
#
# 4.7   11-Nov-2016 (bm)  Small bug fix in Play.midi - now we pay attention to global instrument settings, i.e., Play.setInstrument(),
#					unless instrument has been set explicitely locally (e.g., at Phrase level).
#
# 4.6   07-Nov-2016 (bm)  Fixed inefficiency problem in Play.midi (took forever to play long scores, e.g., > 3000 notes).  Now, things work
#                   in real time again.
#
# 4.5   05-Nov-2016 (bm)  Fixed small but important bug in Play.midi (a missing variable in the part scheduling all notes in the chord list).
#
# 4.4   21-Oct-2016 (bm, mm)  Fixed clicking in Play.audio() by adding a timer to lower volume right before the ending of an audio note.
#
# 4.3   28-Aug-2016 (bm, mm)  Added Play.audio(), Play.audioNote(), Play.audioOn(), Play.audioOff(), Play.allAudioNotesOff() to 
#                   play musical material via AudioSamples.  These functions parallel the corresponding Play.note(), etc. functions.
#                   The only difference is that audio samples are provided to be used in place of MIDI channels to render the music.
#                   Also fixed bug with rendering panning information in notes in Play.midi() and Play.audio().  
#                   Also, if panning information is not provided in Play.noteOn(), Play.audioOn(), etc., the global Play.setPanning()
#                   info is now used.
#
# 4.2   12-Aug-2016 (bm)  Using Timer2() class (based on java.util.Timer) for Play.note(), etc.  More reliable.
#
# 4.1   28-Jul-2016 (bm, mm)  Resolved following issues with Play.midi():
#                   (a) Playback now uses length of a note (vs. its duration) to determine how long it sounds (as it should).
#                   (b) Chord durations were calculated improperly for some chord notes, due to a note sorting error.  This has been fixed by
#                   sorting noteList in Play.midi() by start time, then duration, then pitch then etc.
#                   (c) Fixed race condition which caused some notes from not turning off.  The dictionary used to hold instances of overlapping 
#                   notes was changed to a list.  Now, for every note to play, a tuple of pitch and channel is added to by frequencyOn() and 
#                   removed from the list by frequencyOff(), respectively. (Race condition is still present, but due to rewritten logic, it
#                   does not cause any trouble anymore.  All concurrent notes are turned off when they should.)
#
# 4.0   14-May-2016 (bm, mm)  Added microtonal capabilities.  Now, we can create and play notes using frequencies (float, in Hz), 
#                   instead of pitch (0-127).  Updated new Play.midi() function to handle microtones / frequencies (by using pitchbend).  
#                   Only one frequency per channel can be played accurately (since there is only one pitchbend per channel).  Regular notes
#                   can play concurrently as usual (i.e., for chords).  However, for concurrent microtones on a given channel, 
#				unless they have same pitchbend, only the last microtone will be rendered accurately (all others will be affected by the
#				latest pichbend - the one used to render the last microtone - again, only one pitchbend is available per channel).
#                   To render concurrent microtones, they have to be spread across different channels.  That's the only way to render 
#                   microtonal chords using MIDI (i.e., we are pushing MIDI as far as it goes here).
#                   Also, updated Play.noteOn/Off(), and Play.frequencyOn/Off() accordingly, and added a few more error checks/warnings.
#                   Additionally, now only the last note-off event for a given note-channel is executed, thus allowing overlapping notes with
#                   same pitch (e.g., overlapping A4 notes) to render more accurately.
#				Finally, Play.setPitchBend() changes the global pitch bend, so if a certain frequency is played, it will be 
#				pitchbended if pitch bend is NOT zero. This is similar to playing any note with pitch bend set to anything other
#				than zero.
#
# 3.9   30-Mar-2016 (bm)  Changed to new Play.midi() function.  It issues Play.note() calls, instead of using jMusic's Play.midi() -
#                   the latter usually hesitates at the beginning of playing.  New way is more robust / reliable.
#                   Old function is still available under Play.midi2().
#
# 3.8   04-Mar-2016 (bm)  Reverted back to __Active__ lists removing objects.  Not a good idea, especially when loading large audio files.
#                   We need to remove old objects, when we stop, otherwise we quickly run out of memory...
#
# 3.7   28-Feb-2016 (bm)  Updated Metronome class to improve API and implementation - updated method add() to use absolute beats (with
#                   the exception of 0, which means at the next beat), also soundOn() now takes a MIDI pitch to use and volume, as parameters.
#                   Updated __Active__ lists to not remove objects.  This way, when Stop button is pressed, all objects are stopped,
#                   even if they are not referenced in the program anymore (during Live Coding, variables may be redefined and leave
#                   orphan objects still playing - which before could only be stopped by quiting JEM!).
#
# 3.6   05-Feb-2016 (bm)  Added Metronome class - it provides for synchronization of musical tasks, especially for live coding.
#                   Methods include add(), remove(), start(), stop(), show(), hide(), soundOn(), soundOff().
#
# 3.5   17-Jan-2016 (bm)  Fixed Mod.invert() bug, which modified RESTs - now, we only invert non-REST notes.
#
# 3.4   01-Dec-2015 (bm)  Moved LiveSample to audio.py, where we can do more extensive testing for audio card formats
#                   (e.g., Little Endian), which appeared in some Windows boxes.  Also, fixed problem of Java imports
#                   overridding Python's enumerate() function.
#
# 3.3   06-May-2015 (cb)  Added LiveSample(), which implements live recording of audio, and offers 
#                   an API similar to AudioSample.  Nice!
#
# 3.2   22-Feb-2015 (bm)  Added Mod.elongate() to fix a problem with jMusic's Mod.elongate (it messes up the
#                   the length of elongated notes).  Added Mod.shift() to shift the start time of material
#                   as a whole; and Mod.merge() to merge two Parts (or two Scores) into one.  Also, updated
#                   Mod.retrograde() to work with Parts and Scores, in addition to Phrases.
#
# 3.1   07-Dec-2014 (bm)  Added Note() wrapping to allow specifying length in the Note constructor (in addition
#                   to pitch, duration, dynamic, and panning.  Updated Phrase.addNoteList() and addChord() to
#                   include a length parameter.  This allows for easier specification of legato and staccato notes.
#                   Also updated Note.setDuration() to adjust the note's length proportionally.
#
# 3.0   06-Nov-2014 (bm)  Added functionality to stop AudioSample and MidiSequence objects via JEM's Stop button
#                       - see registerStopFunction().
#
# 2.9   07-Oct-2014 (bm) Resolved the various Play.midi() issues.  Andrew (Brown) fixed jMusic's MidiSynth, so
#                   we now can use it as documented.  We initialize a total of 12 MidiSynth's (which allows up to
#                   12 concurrent Play.midi()'s).  This should be sufficient for all practical purposes.
#
# 2.8   06-Sep-2014 (bm) Fixed a couple of bugs in Mod.invert() and Mod.mutate().  Also added a more meaningful
#                   error message in Phrase.addNoteList() for the common error of providing lists with different lengths.
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

# preserve Jython bindings that get overwritten by the following Java imports - a hack!
# (also see very bottom of this file)
enumerate_preserve = enumerate


# import jMusic constants and utilities
from jm.JMC import *     
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
   
   def invert(phrase, pitchAxis):
      """Invert phrase using pitch as the mirror (pivot) axis."""
      
      # traverse list of notes, and adjust pitches accordingly
      for note in phrase.getNoteList():
         
         if not note.isRest():  # modify regular notes only (i.e., do not modify rests)
                     
            invertedPitch = pitchAxis + (pitchAxis - note.getPitch())  # find mirror pitch around axis (by adding difference)
            note.setPitch( invertedPitch )                             # and update it 
      
      # now, all notes have been updated
                  
   def mutate(phrase):
      """Same as jMod.mutate()."""
      
      # adjust jMod.mutate() to use random durations from phrase notes
      durations = [note.getDuration() for note in phrase.getNoteList()]
      
      jMod.mutate(phrase, 1, 1, CHROMATIC_SCALE, phrase.getLowestPitch(),  
                  phrase.getHighestPitch(), durations)

   def elongate(material, scaleFactor):
      """Same as jMod.elongate(). Fixing a bug."""
      
      # define helper functions
      def elongateNote(note, scaleFactor):
         """Helper function to elongate a single note."""
         note.setDuration( note.getDuration() * scaleFactor)
      
      def elongatePhrase(phrase, scaleFactor):
         """Helper function to elongate a single phrase."""
         for note in phrase.getNoteList():
            elongateNote(note, scaleFactor)
      
      def elongatePart(part, scaleFactor):
         """Helper function to elongate a single part."""
         for phrase in part.getPhraseList():
            elongatePhrase(phrase, scaleFactor)
      
      def elongateScore(score, scaleFactor):
         """Helper function to elongate a score."""
         for part in score.getPartList():
            elongatePart(part, scaleFactor)
      
      # check type of material and call the appropriate function
      if type(material) == Score:
         elongateScore(material, scaleFactor)
      elif type(material) == Part:
         elongatePart(material, scaleFactor)
      elif type(material) == Phrase or type(material) == jPhrase:
         elongatePhrase(material, scaleFactor)
      elif type(material) == Note:
         elongateNote(material, scaleFactor)
      else:   # error check    
         raise TypeError( "Unrecognized time type " + str(type(material)) + " - expected Note, Phrase, Part, or Score." )

   def shift(material, time):
      """It shifts all phrases' start time by 'time' (measured in QN's, i.e., 1.0 equals QN).
         If 'time' is positive, phrases are moved later. 
         If 'time' is negative, phrases are moved earlier (at most, at the piece's start time, i.e., 0.0), 
         as negative start times make no sense.
         'Material' can be Phrase, Part, or Score (since Notes do not have a start time).
      """
      
      # define helper functions
      def shiftPhrase(phrase, time):
         """Helper function to shift a single phrase."""
         newStartTime = phrase.getStartTime() + time
         newStartTime = max(0, newStartTime)          # ensure that the new start time is at most 0 (negative start times make no sense)
         phrase.setStartTime( newStartTime )
      
      def shiftPart(part, time):
         """Helper function to shift a single part."""
         for phrase in part.getPhraseList():
            shiftPhrase(phrase, time)
      
      def shiftScore(score, time):
         """Helper function to shift a score."""
         for part in score.getPartList():
            shiftPart(part, time)
      
      # check type of time
      if not (type(time) == float or type(time) == int):
         raise TypeError( "Unrecognized time type " + str(type(time)) + " - expected int or float." )

      # check type of material and call the appropriate function
      if type(material) == Score:
         shiftScore(material, time)
      elif type(material) == Part:
         shiftPart(material, time)
      elif type(material) == Phrase or type(material) == jPhrase:
         shiftPhrase(material, time)
      else:   # error check   
         raise TypeError( "Unrecognized material type " + str(type(material)) + " - expected Phrase, Part, or Score." )

   def merge(material1, material2):
      """Merges 'material2' into 'material1'.  'Material1' is changed, 'material2' is unmodified.
         Both 'materials' must be of the same type, either Part or Score.
         It does not worry itself about instrument and channel assignments - it is left to the caller
         to ensure that the two 'materials' are compatible this way.
      """

      # define helper functions
      def mergeParts(part1, part2):
         """Helper function to merge two parts into one."""
         for phrase in part2.getPhraseList():
            part1.addPhrase(phrase)
      
      def mergeScores(score1, score2):
         """Helper function to merge two scores into one."""
         for part in score2.getPartList():
            score1.addPart(part)
      
      # check type of material and call the appropriate function
      if type(material1) == Score and type(material2) == Score:
         mergeScores(material1, material2)
      elif type(material1) == Part and type(material2) == Part:
         mergeParts(material1, material2)
      elif (type(material1) == Part and type(material2) == Score) or \
           (type(material1) == Score and type(material2) == Part):
         raise TypeError( "Cannot merge Score and Part - arguments must be of the same type (both Score or both Part)." )
      else:       
         raise TypeError( "Arguments must be both either Score or Part." )

 
   def retrograde(material):
      """It reverses the start times of notes in 'material'.
         'Material' can be Phrase, Part, or Score.
      """
      
      # define helper functions
      def getPartStartTime(part):
         """Helper function to return the start time of a part."""

         minStartTime = 10000000000.0   # holds the earliest start time among all phrases (initialize to a very large value)
         for phrase in part.getPhraseList():
            minStartTime = min(minStartTime, phrase.getStartTime())   # accumulate the earliest start time, so far
         # now, minStartTime holds the earliest start time of a phrase in this part

         return minStartTime   # so return it

      def getPartEndTime(part):
         """Helper function to return the end time of a part."""

         maxEndTime   = 0.0             # holds the latest end time among all phrases
         for phrase in part.getPhraseList():
            maxEndTime   = max(maxEndTime, phrase.getEndTime())       # accumulate the latest end time, so far
         # now, maxEndTime hold the latest end time of a phrase in this part

         return maxEndTime   # so return it

      def retrogradePart(part):
         """Helper function to retrograde a single part."""

         startTime = getPartStartTime(part)  # the earliest start time among all phrases
         endTime   = getPartEndTime(part)    # the latest end time among all phrases
 
         # retrograde each phrase and adjust its start time accordingly
         for phrase in part.getPhraseList():
            distanceFromEnd = endTime - phrase.getEndTime()  # get this phrase's distance from end

            jMod.retrograde(phrase)                          # retrograde it

            # the retrograded phrase needs to start as far from the beginning of the part as its orignal end used to be
            # from the end of the part
            phrase.setStartTime( distanceFromEnd + startTime )

         # now, all phrases in this part have been retrograded and their start times have been aranged
         # to mirror their original end times
       
      def retrogradeScore(score):
         """Helper function to retrograde a score."""

         # calculate the score's start and end times
         startTime = 10000000000.0   # holds the earliest start time among all parts (initialize to a very large value)
         endTime   = 0.0             # holds the latest end time among all parts
         for part in score.getPartList():
            startTime = min(startTime, getPartStartTime(part))   # accumulate the earliest start time, so far
            endTime   = max(endTime, getPartEndTime(part))       # accumulate the latest end time, so far
         # now, startTime and endTime hold the score's start and end time, respectively

         print "score startTime =", startTime, "endTime =", endTime

         # retrograde each part and adjust its start time accordingly
         for part in score.getPartList():
            # get this part's distance from the score end
            distanceFromEnd = endTime - (getPartEndTime(part) + getPartStartTime(part)) 
            
            # retrograde this part
            retrogradePart(part)                              

            # the retrograded part needs to start as far as 
            # the orignal part's distance from the score end
            Mod.shift(part, distanceFromEnd) 
         # now, all parts have been retrograded and their start times have been aranged to mirror their original
         # end times


      # check type of material and call the appropriate function
      if type(material) == Score:
         retrogradeScore(material)
      elif type(material) == Part:
         retrogradePart(material)
      elif type(material) == Phrase or type(material) == jPhrase:
         jMod.retrograde(material)
      else:   # error check   
         raise TypeError( "Unrecognized material type " + str(type(material)) + " - expected Phrase, Part, or Score." )


   # make these function callable without having to instantiate this class
   normalize = Callable(normalize)  
   invert = Callable(invert)  
   mutate = Callable(mutate)  
   elongate = Callable(elongate)  
   shift = Callable(shift)  
   merge = Callable(merge)
   retrograde = Callable(retrograde)
   
   
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
#### jMusic Note extensions ########################################################
######################################################################################

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



from jm.music.data import *
from jm.music.data import Note as jNote  # needed to wrap more functionality below

# update Note to accept length which specifies the actual length (performance) of the note,
# (whereas duration specifies the score (or denoted) length of the note).
class Note(jNote):

   def __str__(self):    
      # we disrupted access to jMusic's (Java's) Note.toString() method,
      # so, let's fix it
      return self.toString()

   def __repr__(self):    
      # we disrupted access to jMusic's (Java's) Note.toString() method,
      # so, let's fix it
      return self.toString()

   def __init__(self, value, duration, dynamic=85, pan=0.5, length=None):   

      # NOTE: If value is an int, it signifies pitch; otherwise, if it is a float,
      # it signifies a frequency.

      # set note length (if needed)
      if length == None:   # not provided?
         length = duration * jNote.DEFAULT_LENGTH_MULTIPLIER  # normally, duration * 0.9

      # do some basic error checking
      if type(value) == int and value != REST and (value < 0 or value > 127):
        raise TypeError( "Note pitch should be an integer between 0 and 127 (it was " + str(value) + ")." )
      elif type(value) == float and not value > 0.0:
        raise TypeError( "Note frequency should be a float greater than 0.0 (it was " + str(value) + ")." )
      elif (type(value) != int) and (type(value) != float): 
        raise TypeError( "Note first parameter should be a pitch (int) or a frequency (float) - it was " + str(type(value)) + "." )
      
      # now, construct a jMusic Note with the proper attributes
      jNote.__init__(self, value, duration, dynamic, pan)     # construct note
      self.setLength( length )                                # and set its length

      # NOTE: jMusic Notes if int pitch is given, they populate both frequency and pitch;
      # (if float pitch is given, they treat if as frequency and populate only frequency - no pitch).
      # This is a bug.  Below, we fix it by also using setPitch() or setFrequency(), which may appear
      # redundant, but they fix this problem (as they do the proper cross-updating of pitch and frequency).

      # fix jMusic Note bug (see above)
      if type(value) == int:
      	 self.setPitch(value)
      elif type(value) == float:
      	 self.setFrequency(value)
    

   # fix set duration to also adjust length proportionally
   def setDuration(self, duration):
   
      # calculate length fector from original values
      lengthFactor = self.getLength() / self.getDuration()
      
      # and set new duration and length appropriately
      jNote.setDuration(self, duration )
      self.setLength(duration * lengthFactor )

   # fix error message returned from getPitch() if frequency and pitch are not equivalent
   def getPitch(self):
   
      # get frequency
      frequency = self.getFrequency()

      # convert to corresponding pitch
      if frequency == float(REST):    # is it a rest?
         pitch = REST                    # yes, so update accordingly
      else:   # it's a regular note, so...
         # calculate corresponding pitch and pith bend
         pitch, bend = freqToNote(frequency)

      # return only pitch
      return pitch

   # also, create a way to get the difference between frequency and pitch, in pitch bend units (see Play class)
   def getPitchBend(self):
   
      # get frequency
      frequency = self.getFrequency()
      
      # and calculate corresponding pitch and pith bend
      pitch, bend = freqToNote(frequency)

      # return only pitch bend (from 0 to )
      return bend + PITCHBEND_NORMAL


######################################################################################
#### jMusic Phrase extensions ########################################################
######################################################################################

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

   def addChord(self, pitches, duration, dynamic=85, panoramic=0.5, length=None):    
      # set chord length (if needed)
      if length == None:   # not provided?
         length = duration * jNote.DEFAULT_LENGTH_MULTIPLIER  # normally, duration * 0.9

      # add all notes, minus the last one, as having no duration, yet normal length 
      # (exploiting how Play.midi() and Write.midi() work)
      for i in range( len(pitches)-1 ):
         n = Note(pitches[i], 0.0, dynamic, panoramic, length)
         self.addNote(n)

      # now, add the last note with the proper duration (and length)
      n = Note(pitches[-1], duration, dynamic, panoramic, length)
      self.addNote(n)

   def addNoteList(self, pitches, durations, dynamics=[], panoramics=[], lengths=[]):   
      """Add notes to the phrase using provided lists of pitches, durations, etc. """ 

      # check if provided lists have equal lengths
      if len(pitches) != len(durations) or \
         (len(dynamics) != 0) and (len(pitches) != len(dynamics)) or \
         (len(panoramics) != 0) and (len(pitches) != len(panoramics)) or \
         (len(lengths) != 0) and (len(pitches) != len(lengths)):
         raise ValueError("The provided lists should have the same length.")

      # if dynamics was not provided, construct it with max value
      if dynamics == []:
         dynamics = [85] * len(pitches)
      
      # if panoramics was not provided, construct it at CENTER
      if panoramics == []:
         panoramics = [0.5] * len(pitches)
               
      # if note lengths was not provided, construct it at 90% of note duration
      if lengths == []:
         lengths = [duration * jNote.DEFAULT_LENGTH_MULTIPLIER for duration in durations]
               
      # traverse the pitch list and handle every item appropriately
      for i in range( len(pitches) ):        
         if type(pitches[i]) == list:              # is it a chord?
            self.addChord(pitches[i], durations[i], dynamics[i], panoramics[i], lengths[i])  # yes, so add it
         else:                                     # else, it's a note
            n = Note(pitches[i], durations[i], dynamics[i], panoramics[i], lengths[i])       # create note
            self.addNote(n)                                                                  # and add it

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
# But we need it to be open, in case the end-user wishes to use functions like Play.noteOn(), below. 
# ( *** Is there a way to open it just-in-time, and/or close it when not used? I cannot think of one.)
 
Java_synthesizer = MidiSystem.getSynthesizer()  # get a Java synthesizer
Java_synthesizer.open()                         # and activate it (should we worry about close()???)

# make all instruments available
Java_synthesizer.loadAllInstruments(Java_synthesizer.getDefaultSoundbank())   
 

# The MIDI specification stipulates that pitch bend be a 14-bit value, where zero is 
# maximum downward bend, 16383 is maximum upward bend, and 8192 is the center (no pitch bend).
PITCHBEND_MIN = 0 
PITCHBEND_MAX = 16383 
PITCHBEND_NORMAL = 8192

# calculate constants from the way we handle pitch bend
OUR_PITCHBEND_MAX    = PITCHBEND_MAX - PITCHBEND_NORMAL
OUR_PITCHBEND_MIN    = -PITCHBEND_NORMAL 
OUR_PITCHBEND_NORMAL = 0 

# initialize pitchbend across channels to 0
CURRENT_PITCHBEND = {}    # holds pitchbend to be used when playing a note / frequency (see below)
for i in range(16):
   CURRENT_PITCHBEND[i] = 0   # set this channel's pitchbend to zero

  
#########
# NOTE:  The following code addresses Play.midi() functionality.  In order to be able to stop music
# that is currently playing, we wrap the jMusic Play class inside a Python Play class and rebuild 
# play music functionality from basic elements.

from jm.midi import MidiSynth  # needed to play and loop MIDI
from time import sleep         # needed to implement efficient busy-wait loops (see below)
from timer import *            # needed to schedule future tasks

# allocate enough MidiSynths and reuse them (when available)
__midiSynths__ = []            # holds all available jMusic MidiSynths 
MAX_MIDI_SYNTHS = 12           # max number of concurrent MidiSynths allowed 
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
# An envelope contains a list of attack times (in milliseconds, relative from the previous time) and values (to reach at those times), 
# how long to wait (delay time, in milliseconds, relative from the previous time) to get to a sustain value, and 
# then how long to wait to reach a value of zero (in milliseconds, relative from the end time).

class Envelope():
    def __init__(self, attackTimes = [2], attackValues = [1.0], delayTime = 1, sustainValue = 1.0, releaseTime = 2):

        # make sure attack times and values are parallel
        if len(attackValues) != len(attackTimes):

            raise IndexError("Envelope: attack times and values need to have the same length")

        else:  # all seems well 

            self.attackTimes = attackTimes    # in milliseconds, relative from the previous time...
            self.attackValues = attackValues  # and the corresponding values
            self.delayTime = delayTime        # in milliseconds, relative from the previous time...
            self.sustainValue = sustainValue  # to reach this value
            self.releaseTime = releaseTime    # in milliseconds, relative from the end time

    # get list of attack times
    def getAttackTimes(self):
        return self.attackTimes

    # get list of attack values
    def getAttackValues(self):
        return self.attackValues

    # get list of lists - first element is list of attack times and second element is list attack values
    def getAttackTimesAndValues(self):
        return [self.attackTimes, self.attackValues]

    # update attack times
    def setAttackTimes(self, attackTimes):
        # make sure attack times and values are parallel
        if len(self.attackValues) != len(attackTimes):

            raise IndexError("Envelope.setAttackTimes(): attack times and values need to have the same length")

        else:  # all seems well 
            self.attackTimes = attackTimes

    # 
    def setAttackValues(self, attackValues):
        # make sure attack times and values are parallel
        if len(attackValues) != len(self.attackTimes):

            raise IndexError("Envelope.setAttackValues(): attack times and values need to have the same length")

        else:  # all seems well 
            self.attackValues = attackValues

    def setAttackTimesAndValues(self, attackTimes, attackValues):
        # make sure attack times and values are parallel
        if len(self.attackValues) != len(attackTimes):

            raise IndexError("Envelope.setAttackTimesAndValues(): attack times and values need to have the same length")

        else:  # all seems well 
            self.attackTimes = attackTimes            
            self.attackValues = attackValues

    def getSustain(self):
        return self.sustainValue

    def setSustain(self, sustainValue):
        self.sustainValue = sustainValue

    def getDelay(self):
        return self.delayTime

    def setDelay(self, delayTime):
        self.delayTime = delayTime
       
    def getRelease(self):
        return self.releaseTime

    #update release
    def setRelease(self, releaseTime):
        self.releaseTime = releaseTime

    # get length of envelope
    def getLength(self):
        return self.__getAbsoluteDelay__() + self.releaseTime

    # get list of absolute attack times, attack time distance from start of envelope
    def __getAbsoluteAttackTimes__(self):
        # now convert relative attack times to absolute from the start time
        absoluteAttackTimes = [ self.attackTimes[0] ]   # initialize first list element
        for i in range(1, len(self.attackTimes)):            # process remaining times
            absoluteAttackTimes.append(self.attackTimes[i] + absoluteAttackTimes[i-1])
        return absoluteAttackTimes

    def __getAbsoluteDelay__(self):
        # same for delay
        absoluteAttackTimes = self.__getAbsoluteAttackTimes__()
        absoluteDelayTime =  absoluteAttackTimes[len(absoluteAttackTimes) - 1] + self.delayTime
        return absoluteDelayTime



# Holds notes currently sounding, in order to prevent premature NOTE-OFF for overlapping notes on the same channel 
# For every frequencyOn() we add the tuple (pitch, channel), and for every frequencyOff() we rmove the tuple.  
# If it is the last one, we execute a NOTE-OFF (otherwise, we don't). 
notesCurrentlyPlaying = [] 

class Play(jPlay):

   # redefine Play.midi to fix jMusic bug (see above) - now, we can play as many times as we wish.
   def midi(material):
      """Play jMusic material (Score, Part, Phrase, Note) using our own Play.note() function."""
      
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
            instrument = Play.getInstrument(channel)  # get global instrument for this channel
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
            Play.setInstrument(instrument, channel)

            # handle chord (if any)
            # Chords are denoted by a sequence of notes having the same start time and 0 duration (except the last note
            # of the chord).
            if duration == 0:   # does this note belong in a chord?
               chordNotes.append([start, duration, pitch, velocity, channel, panning])  # add it to the list of chord notes
               
            elif chordNotes == []:   # is this a regular, solo note (not part of a chord)?
               
               # yes, so schedule it to play via a Play.note event
               Play.note(pitch, start, duration, velocity, channel, panning)
               #print "Play.note(" + str(pitch) + ", " + str(int(start * FACTOR)) + ", " + str(int(duration * FACTOR)) + ", " + str(velocity) + ", " + str(channel) + ")"

            else:   # note has a normal duration and it is part of a chord

               # first, add this note together with this other chord notes
               chordNotes.append([start, duration, pitch, velocity, channel, panning])
               
               # now, schedule all notes in the chord list using last note's duration
               for start, ignoreThisDuration, pitch, velocity, channel, panning in chordNotes:
                  # schedule this note using chord's duration (provided by the last note in the chord)
                  Play.note(pitch, start, duration, velocity, channel, panning)
                  #print "Chord: Play.note(" + str(pitch) + ", " + str(int(start * FACTOR)) + ", " + str(int(duration * FACTOR)) + ", " + str(velocity) + ", " + str(channel) + ")"
               # now, all chord notes have been scheduled

               # so, clear chord notes to continue handling new notes (if any)
               chordNotes = []
   
         # now, all notes have been scheduled for future playing - scheduled notes can always be stopped using
         # JEM's stop button - this will stop all running timers (used by Play.note() to schedule playing of notes)
         #print "Play.note(" + str(pitch) + ", " + str(int(start * FACTOR)) + ", " + str(int(duration * FACTOR)) + ", " + str(velocity) + ", " + str(channel) + ")"

      else:   # error check    
         print "Play.midi(): Unrecognized type " + str(type(material)) + ", expected Note, Phrase, Part, or Score."


   # old way - should be removed in future release (together will *all* references of __midiSynths__'s)
   def midi2(material):
      """This is the original Play.midi() - retained for backup and testing purposes.  
         Play jMusic material (Score, Part, Phrase, Note) using next available MidiSynth (if any)."""
      
      from jm.music.data import Phrase as jPhrase   # since we extend Phrase later
      
      midiSynth = __getMidiSynth__()  # get next available MidiSynth (or None if all busy)
      #midiSynth = MidiSynth()    # create a new MIDI synthesizer
            
      # did we find an available midiSynth?
      if midiSynth:
         # play the music        
         # do necessary datatype wrapping (MidiSynth() expects a Score)
         if type(material) == Note:
            material = Phrase(material)
         if type(material) == jNote:    # (also wrap jMusic default Notes, in addition to our own)
            material = Phrase(material)
         if type(material) == Phrase:   # no elif - we need to successively wrap from Note to Score
            material = Part(material)
         if type(material) == jPhrase:  # (also wrap jMusic default Phrases, in addition to our own)
            material = Part(material)
         if type(material) == Part:     # no elif - we need to successively wrap from Note to Score
            material = Score(material)
         if type(material) == Score:
         
            midiSynth.play( material )   # play it!
         
         else:   # error check    
            print "Play.midi(): Unrecognized type" + str(type(material)) + ", expected Note, Phrase, Part, or Score."

      else:   # error check    
         print "Play.midi(): All", MAX_MIDI_SYNTHS, "MIDI synthesizers are busy - (try again later?)"
         
      return midiSynth  # return midiSynth playing
   

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
   def noteOn(pitch, velocity=100, channel=0, panning = -1):
      """Send a NOTE_ON message for this pitch to the Java synthesizer object.  Default panning of -1 means to
         use the default (global) panning setting of the Java synthesizer."""

      if (type(pitch) == int) and (0 <= pitch <= 127):   # a MIDI pitch?
         # yes, so convert pitch from MIDI number (int) to Hertz (float)
         pitch = noteToFreq(pitch)       

      if type(pitch) == float:        # a pitch in Hertz?
         Play.frequencyOn(pitch, velocity, channel, panning)  # start it
                  
      else:         

         print "Play.noteOn(): Unrecognized pitch " + str(pitch) + ", expected MIDI pitch from 0 to 127 (int), or frequency in Hz from 8.17 to 12600.0 (float)."


   def frequencyOn(frequency, velocity=100, channel=0, panning = -1):
      """Send a NOTE_ON message for this frequency (in Hz) to the Java synthesizer object.  Default panning of -1 means to
         use the default (global) panning setting of the Java synthesizer."""
      
      if (type(frequency) == float) and (8.17 <= frequency <= 12600.0): # a pitch in Hertz (within MIDI pitch range 0 to 127)?

         pitch, bend = freqToNote( frequency )                     # convert to MIDI note and pitch bend

         # also, keep track of how many overlapping instances of this pitch are currently sounding on this channel
         # so that we turn off only the last one - also see frequencyOff()
         noteID = (pitch, channel)              # create an ID using pitch-channel pair
         notesCurrentlyPlaying.append(noteID)   # add this note instance to list

         Play.noteOnPitchBend(pitch, bend, velocity, channel, panning)      # and start it 

      else:         

         print "Play.frequencyOn(): Invalid frequency " + str(frequency) + ", expected frequency in Hz from 8.17 to 12600.0 (float)."
      
   def noteOff(pitch, channel=0):
      """Send a NOTE_OFF message for this pitch to the Java synthesizer object."""

      if (type(pitch) == int) and (0 <= pitch <= 127):   # a MIDI pitch?
         # yes, so convert pitch from MIDI number (int) to Hertz (float)
         pitch = noteToFreq(pitch)       

      if type(pitch) == float:        # a pitch in Hertz?
         Play.frequencyOff(pitch, channel)  # stop it
                  
      else:         

         print "Play.noteOff(): Unrecognized pitch " + str(pitch) + ", expected MIDI pitch from 0 to 127 (int), or frequency in Hz from 8.17 to 12600.0 (float)."

   def frequencyOff(frequency, channel=0):
      """Send a NOTE_OFF message for this frequency (in Hz) to the Java synthesizer object."""
      
      global Java_synthesizer

      if (type(frequency) == float) and (8.17 <= frequency <= 12600.0): # a frequency in Hertz (within MIDI pitch range 0 to 127)?

         pitch, bend = freqToNote( frequency )                     # convert to MIDI note and pitch bend

         # also, keep track of how many overlapping instances of this frequency are currently playing on this channel
         # so that we turn off only the last one - also see frequencyOn()
         noteID = (pitch, channel)                   # create an ID using pitch-channel pair

         # next, remove this noteID from the list, so that we may check for remaining instances
         notesCurrentlyPlaying.remove(noteID)        # remove noteID
         if noteID not in notesCurrentlyPlaying:     # is this last instance of note?

            # yes, so turn it off!
            channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
            channelHandle.noteOff(pitch)                              # and turn it off

      else:     # frequency was outside expected range    

         print "Play.frequencyOff(): Invalid frequency " + str(frequency) + ", expected frequency in Hz from 8.17 to 12600.0 (float)."

      # NOTE: Just to be good citizens, also turn pitch bend to normal (i.e., no bend).
      # Play.setPitchBend(0, channel)

# Commented out below, because it might give the impression that different pitch bends
# signify different notes to be turned off - not so.  NOTE_OFF messages are based solely on pitch.
#
#   def noteOffPitchBend(pitch, bend = 0, channel=0):
#      """Send a NOTE_OFF message for this pitch to the Java synthesizer object."""
#      # NOTE_OFF messages are based on pitch (i.e., pitch bend is irrelevant / ignored)
#      Play.noteOff(pitch, channel)

   def note(pitch, start, duration, velocity=100, channel=0, panning = -1):
      """Plays a note with given 'start' time (in milliseconds from now), 'duration' (in milliseconds
         from 'start' time), with given 'velocity' on 'channel'.  Default panning of -1 means to
         use the default (global) panning setting of the Java synthesizer. """ 
         
      # TODO: We should probably test for negative start times and durations.
         
      # create a timer for the note-on event
      noteOn = Timer2(start, Play.noteOn, [pitch, velocity, channel, panning], False)

      # create a timer for the note-off event
      noteOff = Timer2(start+duration, Play.noteOff, [pitch, channel], False)

      # and activate timers (set things in motion)
      noteOn.start()
      noteOff.start()
      
      # NOTE:  Upon completion of this function, the two Timer objects become unreferenced.
      #        When the timers elapse, then the two objects (in theory) should be garbage-collectable,
      #        and should be eventually cleaned up.  So, here, no effort is made in reusing timer objects, etc.
 
   def frequency(frequency, start, duration, velocity=100, channel=0, panning = -1):
      """Plays a frequency with given 'start' time (in milliseconds from now), 'duration' (in milliseconds
         from 'start' time), with given 'velocity' on 'channel'.  Default panning of -1 means to
         use the default (global) panning setting of the Java synthesizer.""" 
         
      # NOTE:  We assume that the end-user will ensure that concurrent microtones end up on
      # different channels.  This is needed since MIDI has only one pitch band per channel,
      # and most microtones require their unique pitch bending.

      # TODO: We should probably test for negative start times and durations.
         
      # create a timer for the frequency-on event
      frequencyOn = Timer2(start, Play.frequencyOn, [frequency, velocity, channel, panning], False)

      # create a timer for the frequency-off event
      frequencyOff = Timer2(start+duration, Play.frequencyOff, [frequency, channel], False)

      # call pitchBendNormal to turn off the timer, if it is on
      #setPitchBendNormal(channel)
      # and activate timers (set things in motion)
      frequencyOn.start()
      frequencyOff.start()
 
      #setPitchBendNormal(channel, start+duration, True)


# (Repeated here for convenience...)
# The MIDI specification stipulates that pitch bend be a 14-bit value, where zero is 
# maximum downward bend, 16383 is maximum upward bend, and 8192 is the center (no pitch bend).
#PITCHBEND_MIN = 0 
#PITCHBEND_MAX = 16383 
#PITCHBEND_NORMAL = 8192

# calculate constants from the way we handle pitch bend
#OUR_PITCHBEND_MAX    = PITCHBEND_MAX - PITCHBEND_NORMAL
#OUR_PITCHBEND_MIN    = -PITCHBEND_NORMAL 
#OUR_PITCHBEND_NORMAL = 0 


   # No (normal) pitch bend in JythonMusic (as opposed to MIDI) is 0, max downward bend is -8192, and max upward bend is 8191.
   # (Result is undefined if you exceed these values - it may wrap around or it may cap.)
   def setPitchBend(bend = 0, channel=0):
      """Set global pitchbend variable to be used when a note / frequency is played."""

      if (bend <= OUR_PITCHBEND_MAX) and (bend >= OUR_PITCHBEND_MIN):   # is pitchbend within appropriate range?

         CURRENT_PITCHBEND[channel] = bend        # remember the pitch bend (e.g., for Play.noteOn() )
         
         # and set the pitchbend on the Java synthesizer (this is the only place this is done!)   
         MIDI_pitchbend = bend + PITCHBEND_NORMAL                  # convert to MIDI pitchbend to set  
         channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
         channelHandle.setPitchBend( MIDI_pitchbend )              # and set it (send message)!

      else:     # frequency was outside expected range    

         print "Play.setPitchBend(): Invalid pitchbend " + str(bend) + ", expected pitchbend in range " + \
               str(OUR_PITCHBEND_MIN) + " to " + str(OUR_PITCHBEND_MAX) + "."

      
   def getPitchBend(channel=0):
      """returns the current pitchbend for this channel."""
      
      return CURRENT_PITCHBEND[channel]


   # No (normal) pitch bend is 0, max downward bend is -8192, and max upward bend is 8191.
   # (Result is undefined if you exceed these values - it may wrap around or it may cap.)

   def noteOnPitchBend(pitch, bend = 0, velocity=100, channel=0, panning = -1):
      """Send a NOTE_ON message for this pitch and pitch bend to the Java synthesizer object.  
         Default panning of -1 means to use the default (global) panning setting of the Java synthesizer."""
            
      global Java_synthesizer

      #Play.setPitchBend(bend, channel)  # remember current pitchbend for this channel


      # NOTE: Our normal (or no) pitch bend is 0, max downward bend is -8192, and max upward bend is 8191.
      # However, internally, the MIDI specification wants normal pitch bend to be 8192, max downward 
      # bend to be 0, and max upward bend to be 16383).  
      # So, convert it and add the current global pitchbend, as set previously.
      MIDI_pitchbend = bend + PITCHBEND_NORMAL + CURRENT_PITCHBEND[channel]    

      # Since it is possible that, together with the global pitchbend, we may be out of range,
      # let's check to make sure.
      if (MIDI_pitchbend <= PITCHBEND_MAX) and (MIDI_pitchbend >= PITCHBEND_MIN):   # is pitchbend within appropriate range?

         # we are OK, so set pitchbend on the Java synthesizer!
         channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
         channelHandle.setPitchBend( MIDI_pitchbend )              # send message

         # then, also send message to start the note on this channel
         if panning != -1:                              # if we have a specific panning...
            channelHandle.controlChange(10, panning)       # ... use it (otherwise, we use the default global panning)

         channelHandle.noteOn(pitch, velocity)          # and start the note on Java synthesizer

      else:     # frequency was outside expected range    

         print "Play.noteOnPitchBend(): Invalid pitchbend " + str(pitchbend - PITCHBEND_NORMAL) + \
               ", expected pitchbend in range " + str(PITCHBEND_MIN-PITCHBEND_NORMAL) + " to " + str(PITCHBEND_MAX-PITCHBEND_NORMAL) + \
               ".  Perhaps reset global pitch bend via Play.setPitchBend(0)... ?"


   def allNotesOff():
      """It turns off all notes on all channels."""

      Play.allFrequenciesOff()   
      

   def allFrequenciesOff():
      """It turns off all notes on all channels."""

      global Java_synthesizer
      
      for channel in range(16):  # cycle through all channels
         channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
         channelHandle.allNotesOff()                               # send the message   

         # also reset pitch bend
         Play.setPitchBend(0, channel)      


   def stop():
      """It stops all Play music from sounding."""
      
      # NOTE:  This could also handle Play.note() notes, which may have been
      #        scheduled to start sometime in the future.  For now, we assume that timer.py
      #        (which provides Timer objects) handles stopping of timers on its own.  If so,
      #        this takes care of our problem, for all practical purposes.  It is possible
      #        to have a race condition (i.e., a note that starts playing right when stop()
      #        is called, but a second call of stop() (e.g., double pressing of a stop button)
      #        will handle this, so we do not concern ourselves with it.
      
      # first, stop the internal __getMidiSynth__ synthesizers
      __stopMidiSynths__()
      
      # then, stop all sounding notes
      Play.allNotesOff()
      Play.allAudioNotesOff()

      # NOTE: In the future, we may also want to handle scheduled notes through Play.note().  This could be done
      # by creating a list of Timers created via note() and looping through them to stop them here.


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

   def setPanning(panning, channel=0):
      """Sets the current panning setting for this channel to the Java synthesizer object."""
      
      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      channelHandle.controlChange(10, panning)                  # send the message

   def getPanning(channel=0):
      """Gets the current panning setting for this channel of the Java synthesizer object."""

      global Java_synthesizer
      
      channelHandle = Java_synthesizer.getChannels()[channel]   # get a handle to channel
      return channelHandle.getController(10)                # obtain the current value for panning controller


   def audio(material, listOfAudioSamples, listOfEnvelopes = []):
      """Play jMusic material using a list of audio samples as voices"""
      
      # do necessary datatype wrapping (MidiSynth() expects a Score)
      if type(material) == Note:
         material = Phrase(material)
      if type(material) == jNote:    # (also wrap jMusic default Notes, in addition to our own)
         material = Phrase(material)
      if type(material) == Phrase:   # no elif - we need to successively wrap from Note to Score
         material = Part(material)
      if type(material) == jPhrase:  # (also wrap jMusic default Phrases, in addition to our own)
         material = Part(material)
      if type(material) == Part:     # no elif - we need to successively wrap from Note to Score
         material = Score(material)
      if type(material) == Score:

         # we are good - let's play it then!

         score = material   # by now, material is a score, so create an alias (for readability)

        # loop through all parts and phrases to get all notes
         noteList = []               # holds all notes
         tempo = score.getTempo()    # get global tempo (can be overidden by part and phrase tempos)
         for part in score.getPartArray():   # traverse all parts
            #NOTE: channel is used as an index for the audio voice
            channel = part.getChannel()        # get part channel
            instrument = part.getInstrument()  # get part instrument
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

               for index in range(phrase.length()):      # traverse all notes in this phrase
                  note = phrase.getNote(index)              # and extract needed note data
                  frequency = note.getFrequency()
                  panning = note.getPan()
                  panning = mapValue(panning, 0.0, 1.0, 0, 127)    # map from range 0.0..1.0 (Note panning) to range 0..127 (as expected by Java synthesizer)
                  start = int(phrase.getNoteStartTime(index) * FACTOR)  # get time and convert to milliseconds

                  # NOTE:  Below we use note length as opposed to duration (getLength() vs. getDuration())
                  # since note length gives us a more natural sounding note (with proper decay), whereas 
                  # note duration captures the more formal (printed score) duration (which sounds unnatural).
                  duration = int(note.getLength() * FACTOR)             # get note length (as oppposed to duration!) and convert to milliseconds
                  velocity = note.getDynamic()
                   
                  # accumulate non-REST notes
                  if (frequency != REST):
                     noteList.append((start, duration, frequency, velocity, channel, instrument, panning))   # put start time first and duration second, so we can sort easily by start time (below),
                     # and so that notes that are members of a chord as denoted by having a duration of 0 come before the note that gives the specified chord duration
                   
         # sort notes by start time
         noteList.sort()
       
         for start, duration, pitch, velocity, channel, instrument, panning in noteList:


            # this function only supprts a regular, solo note (not part of a chord)
               if len(listOfEnvelopes) != 0:
                  Play.audioNote(pitch, start, duration, listOfAudioSamples[channel], velocity, panning, listOfEnvelopes[channel])
               else:
                  Play.audioNote(pitch, start, duration, listOfAudioSamples[channel], velocity, panning)

         # now, all notes have been scheduled for future playing - scheduled notes can always be stopped using
         # JEM's stop button - this will stop all running timers (used by Play.note() to schedule playing of notes)
         #print "Play.note(" + str(pitch) + ", " + str(int(start * FACTOR)) + ", " + str(int(duration * FACTOR)) + ", " + str(velocity) + ", " + str(channel) + ")"

      else:   # error check    
         print "Play.audio(): Unrecognized type " + str(type(material)) + ", expected Note, Phrase, Part, or Score."

   def audioNote(pitch, start, duration, audioSample, velocity = 127, panning = -1, envelope = Envelope()):
      """Play a note using an AudioSample for generating the sound."""

      if (type(pitch) == int) and (0 <= pitch <= 127):   # a MIDI pitch?
         # yes, so convert pitch from MIDI number (int) to Hertz (float)
         pitch = noteToFreq(pitch)


      # apply envelope to note
      if envelope.getLength() > duration:
         print("Play.audioNote(): Envelope is too large for this note,\n midi: " + str(pitch) + "\nnote length: " + str(duration) + "\nenvelope length: " + str(envelope.getLength()))
      else:
         envelopeLength = envelope.getLength()
         #now create the list of delays that will be passed to the setVolume method
         # convert delays to seconds for the amplitude smoother
         attackDelays = []
         attackTimes = envelope.getAttackTimes()
         for i in range(len(attackTimes)):
            attackDelays.append(float(attackTimes[i]) / 1000.0)
         # now we have a list of how long each attack lasts in seconds

         delayDelay = float(envelope.getDelay() / 1000.0)
         releaseDelay = float(envelope.getRelease() / 1000.0)
         # and how long the delay and release lasts in seconds

         # adjust attackValues relative to note velocity
         relativeAttackValues = []
         for i in range( len(envelope.getAttackValues() ) ):
            relativeValue = mapValue( envelope.getAttackValues()[i], 0.0, 1.0, 0, velocity )   # adjust
            relativeAttackValues.append( relativeValue )                                       # and remember

         # adjust sustainValue relative to note velocity
         relativeSustainValue = mapValue( envelope.sustainValue, 0.0, 1.0, 0, velocity )

         # get absolute release time
         absoluteReleaseTime = duration - envelope.getRelease()

         # create list of timers to perform volume changes
         attackTimers = []

         # first, create timers for envelope attack 
         for i in range( len(relativeAttackValues) ):
             timerOffset = envelope.__getAbsoluteAttackTimes__()[i]
             volume = relativeAttackValues[i]
             delay = attackDelays[i]
             timer = Timer2(start+timerOffset, audioSample.setVolume, [volume, delay], False)
             attackTimers.append( timer )
 
         # now, create timers for envelope sustain and release
         sustainTimer = Timer2(start + envelope.__getAbsoluteDelay__(), audioSample.setVolume, [relativeSustainValue, delayDelay], False)
         releaseTimer = Timer2(start + absoluteReleaseTime, audioSample.setVolume, [0, releaseDelay], False)
  
         # finally, create timers for note-on and note-off events
         audioOn  = Timer2(start, Play.audioOn, [pitch, audioSample, velocity, panning], False)
         audioOff = Timer2(start+duration, Play.audioOff, [pitch, audioSample], False)
         
         # everything is ready, so start timers to schedule playng of note
         audioOn.start()
         for i in range(len(attackTimers)):
           attackTimers[i].start()
         sustainTimer.start()
         releaseTimer.start()
         audioOff.start()
         

   def audioOn(pitch, audioSample, velocity = 127, panning = -1):
      """Start playing a specific pitch at a given volume using provided audio sample."""

      if panning != -1:                              # if we have a specific panning...
         audioSample.setPanning(panning)                # then, use it (otherwise let default / global panning stand
      else:                                          # otherwise...
         audioSample.setPanning( Play.getPanning() )    # use the global / default panning

      audioSample.setFrequency(pitch)                # set the sample to the specified frequency
      audioSample.setVolume(velocity)                # and specified volume
      
      audioSample.play()                             # and play the pitch!

   def audioOff(pitch, audioSample):
      """Stop playing the specified pitch on the provided audio sample."""

      # NOTE: For now we ignore pitch...
      audioSample.stop()

   def allAudioNotesOff():
      """It turns off all notes on all audio samples."""

      # NOTE:  We are probably overreaching here... as this will stop *all* AudioSamples from playing.
      # This is a quick way to stop music played via Play.audio().
      __stopActiveAudioSamples__()
      
      # NOTE: In the future, we may also want to handle scheduled notes through Play.audio().  This could be done
      # by creating a list of AudioSamples and Timers created via audioNote() and looping through them to stop them here.
      

   ########################################################################
   # make these functions callable without having to instantiate this class
   midi = Callable(midi)  
   midi2 = Callable(midi2)  
   noteOn = Callable(noteOn)  
   noteOnPitchBend = Callable(noteOnPitchBend)  
   noteOff = Callable(noteOff)  
   note = Callable(note)   
   frequency = Callable(frequency)
   #microtonal = Callable(microtonal)  
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
   #setPitchBendNormal = Callable(setPitchBendNormal)
   audioNote = Callable(audioNote)
   audio = Callable(audio)
   audioOn = Callable(audioOn)
   audioOff = Callable(audioOff)
   allAudioNotesOff = Callable(allAudioNotesOff)


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

from math import *

class jSyn_AudioEngine():
   """Encasulates a jSyn synthesizer.  Only one may exist (no need for more).
      We modularize the synth and its operations in a class for convenience.
   """
   instance = None      # only one instance allowed (no need for more)
   

   def __init__(self):
   
      # import jSyn stuff here, so as to not polute the global namespace
      from com.jsyn import JSyn
      from com.jsyn.data import FloatSample
      from com.jsyn.unitgen import LineOut, Pan, VariableRateMonoReader, VariableRateStereoReader, LinearRamp, FixedRateMonoWriter, FixedRateStereoWriter
      from com.jsyn.util import SampleLoader

      if jSyn_AudioEngine.instance == None:  # first time?
      
         self.synth = JSyn.createSynthesizer()   # create synthesizer         
         jSyn_AudioEngine.instance = self        # remember the only allowable instance         
         
         self.samples = []                       # holds audio samples connected to synthesizer

      else:                                  # an instance already exists
         print "Only one jSyn audio engine may exist (use existing one)."

   def start(self):
      """Starts the synthesizer."""

      self.synth.start()
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
   
# *** NOTE:  This synthesizer should be started only when an audio file (AudioSample) is created.
#            Perhaps do the same with the Java synthesizer above?  Is that synthesizer needed?

# create the jSyn synthesizer (again, only one for everything)
jSyn = jSyn_AudioEngine()
jSyn.start()                 # should this be happening here? (or inside the Audio class, when needed?) ***


# used to keep track which AudioSample and LiveSample objects are active, so we can stop them when
# JEM's Stop button is pressed
__ActiveAudioSamples__ = []     # holds active AudioSample and LiveSample objects

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
   
   def __init__(self, filename, referencePitch=A4, volume=127):
   
      # import jSyn stuff here, so as to not polute the global namespace
      from com.jsyn import JSyn
      from com.jsyn.data import FloatSample
      from com.jsyn.unitgen import LineOut, Pan, VariableRateMonoReader, VariableRateStereoReader, LinearRamp, FixedRateMonoWriter, FixedRateStereoWriter
      from com.jsyn.util import SampleLoader

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

      # check if the reference is a midi pitch (int) or a frequency (float)
      if (type(referencePitch) == int) and (0 <= referencePitch <= 127):    # is reference pitch in MIDI (an int)?
         self.referencePitch     = referencePitch                               # remember reference pitch
         self.referenceFrequency = self.__convertPitchToFrequency__(referencePitch) # and corresponding reference frequency
         self.pitch              = self.referencePitch                          # initialize playback pitch (may be different from reference pitch) 
         self.frequency          = self.referenceFrequency                      # and corresponding playback frequency    
      elif type(referencePitch) == float:                                   # if reference pitch a frequency (a float, in Hz)?
         self.referenceFrequency = referencePitch                               # remember reference frequency
         self.referencePitch     = self.__convertFrequencyToPitch__(referencePitch) # convert reference frequency to corresponding MIDI pitch
         self.pitch = self.referencePitch                                       # initialize playback pitch (may be different from reference pitch)
         self.frequency = referencePitch                                        # and corresponding playback frequency
      else:                                                                 # otherwise this is an error, so let them know
         raise TypeError("Reference pitch (" + str(referencePitch) + ") should be an int (range 0 and 127) or float (such as 440.0).")

         print "Panning (" + str(panning) + ") should range from 0 to 127."

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
   
   def getReferencePitch(self):
      """
      Return sample's reference pitch.
      """
      return self.referencePitch
   
   def getReferenceFrequency(self):
      """
      Return sample's reference pitch.
      """
      return self.referenceFrequency
   
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
   
   def setVolume(self, volume, delay = 0.0002):
      """
      Set sample's volume (volume ranges from 0 - 127).
      """
      if volume < 0 or volume > 127:
         print "Volume (" + str(volume) + ") should range from 0 to 127."
      elif delay < 0.0:
         print "Delay (" + str(delay) + ") should be at least 0.0"
      else:
         self.volume = volume                            # remember new volume
         amplitude = mapValue(self.volume,0,127,0.0,1.0) # map volume to amplitude
         self.amplitudeSmoother.input.set( amplitude )   # and set it
         self.amplitudeSmoother.time.set(delay)          # set delay time
     
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



######################################################################################
# If running inside JEM, register function that stops everything, when the Stop button
# is pressed inside JEM.
######################################################################################

# function to stop and clean-up all active AudioSamples
def __stopActiveAudioSamples__():

   global __ActiveAudioSamples__

   # first, stop them
   for a in __ActiveAudioSamples__:
      a.stop()    # no need to check if they are playing - just do it (it's fine)

   # then, delete them
   for a in __ActiveAudioSamples__:
      del a

   # also empty list, so things can be garbage collected
   __ActiveAudioSamples__ = []   # remove access to deleted items   

# now, register function with JEM (if possible)
try:

    # if we are inside JEM, registerStopFunction() will be available
    registerStopFunction(__stopActiveAudioSamples__)   # tell JEM which function to call when the Stop button is pressed

except:  # otherwise (if we get an error), we are NOT inside JEM 

    pass    # so, do nothing.


   

# used to keep track which MidiSequence objects are active, so we can stop them when
# JEM's Stop button is pressed
__ActiveMidiSequences__ = []     # holds active MidiSequence objects

##### MidiSequence class ######################################

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
         if type(material) == Note:
            material = Phrase(material)
         if type(material) == Phrase:   # no elif - we need to successively wrap from Note to Score
            material = Part(material)
         if type(material) == jPhrase:  # (also wrap jMusic default Phrases, in addition to our own)
            material = Part(material)
         if type(material) == Part:     # no elif - we need to successively wrap from Note to Score
            material = Score(material)
         
         if type(material) == Score:
         
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
      #self.setVolume( self.volume )  # set desired volume     
      
      # set MIDI score's default pitch
      self.pitch = pitch                         # remember provided pitch

      # remember that this MidiSequence has been created and is active (so that it can be stopped by JEM, if desired)
      __ActiveMidiSequences__.append(self)
      

   def __initMidiSynth__(self):
      """Creates and initializes a MidiSynth object."""
      
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


######################################################################################
# If running inside JEM, register function that stops everything, when the Stop button
# is pressed inside JEM.
######################################################################################

# function to stop and clean-up all active MidiSequences
def __stopActiveMidiSequences__():

   global __ActiveMidiSequences__

   # first, stop them
   for m in __ActiveMidiSequences__:
      m.stop()    # no need to check if they are playing - just do it (it's fine)

   # then, delete them 
   for m in __ActiveMidiSequences__:
      del m

   # also empty list, so things can be garbage collected
   __ActiveMidiSequences__ = []   # remove access to deleted items   

# now, register function with JEM (if possible)
try:

    # if we are inside JEM, registerStopFunction() will be available
    registerStopFunction(__stopActiveMidiSequences__)   # tell JEM which function to call when the Stop button is pressed

except:  # otherwise (if we get an error), we are NOT inside JEM 

    pass    # so, do nothing.



# used to keep track which Metronome objects are active, so we can stop them when
# JEM's Stop button is pressed
__ActiveMetronomes__ = []     # holds active MidiSequence objects

##### Metronome class ######################################

from timer import Timer
#from gui import Display     # for Metronome tick visualization
      
class Metronome():
   """Creates a metronome object used in scheduling and synchronizing function call (intended for starting blocks of musical
      material together, but could be really used for anything (e.g., GUI animzation).  This is based on the Timer class,
      but is higher-level, based on tempo (e.g., 60 BPM), and time signatures (e.g., 4/4).  
   """

   #def __init__(self, tempo=60, timeSignature=[4, 4], displaySize=50, displayTickColor=Color.RED):
   def __init__(self, tempo=60, timeSignature=[4, 4]):
      
      # remember title, tempo and time signature
      self.tempo = tempo
      self.timeSignature = timeSignature  # a list (first item is numerator, second is denominator)

      # list of functions (we are asked to synchronize) and their information (parallel lists)
      self.functions        = []    # functions to call
      self.parameters       = []    # their corresponding parameters
      self.desiredBeats     = []    # on which beat to call them (0 means now)
      self.repeatFlags      = []    # if they are meant to be called repeatedly
      self.beatCountdowns   = []    # holds beat countdown until call

      # create timer, upon which to base our operation
      delay = int((60.0 / self.tempo) * 1000)   # in milliseconds
      self.timer = Timer2(delay, self.__callFunctions__, [], True)

      # set up metronome visualization
#      self.display = Display("Metronome", displaySize, displaySize+20, 0, 0)
#      self.display.hide()      # initially hidden
#
#      # set up display ticking
#      self.displayTickColor = displayTickColor               # color used for ticking
#      self.displayOriginalColor = self.display.getColor()    # color to reset ticking
#      self.flickerTimer = Timer2(100, self.display.setColor, [self.displayOriginalColor])   # create timer to reset display color (it ends fliker)
#      self.add( self.__updateDisplay__, [], 0, True, 1)      # schedule display flickering on every beat (starts flicker)      

      # set up metronome visualization / sonification
      self.currentBeat   = 1       # holds current beat relative to provided time signature (1 means first beat)
      self.visualize     = False   # True means print out current beat on console; False do not print
      self.sonify        = False   # True means sound each tick; False do not
      self.sonifyPitch   = HI_MID_TOM   # which pitch to play whe ticking 
      self.sonifyChannel = 9       # which channel to use (9 is for percussion)
      self.sonifyVolume  = 127     # how loud is strong beat (secondary beats will at 70%)

      # remember that this MidiSequence has been created and is active (so that it can be stopped by JEM, if desired)
      __ActiveMetronomes__.append(self)
      

   def add(self, function, parameters=[], desiredBeat=0, repeatFlag=False):
      """It schedules the provided function to be called by the metronome (passing the provided parameters to it) on the
         desired beat (0 means right away, 1 means first (strong) beat, 2 means second beat, etc.), and whether to keep
         calling in it every time the desired beat comes around.
      """
      self.functions.append( function )
      self.parameters.append( parameters )
      self.desiredBeats.append( desiredBeat )
      self.repeatFlags.append( repeatFlag )
      
      # calculate beat countdown
      beatCountdown = self.__calculateBeatCountdown__( desiredBeat )              
         
      # store beat countdown for this function
      self.beatCountdowns.append( beatCountdown )

   def remove(self, function):
      """It removes the provided function from the list of functions scheduled (via add) to be called by the metronome.
         If several instances of this function have been scheduled, it removes the earliest one (i.e., several calls of this
         will be needed to remove all scheduled instances - a design choice).  If the function is not scheduled, it throws
         an error.
      """
      index = self.functions.index( function )   # find index of leftmost occurrence
      self.functions.pop( index )                # and remove it and all info 
      self.parameters.pop( index ) 
      self.desiredBeats.pop( index ) 
      self.repeatFlags.pop( index ) 
      self.beatCountdowns.pop( index )

   def removeAll(self):
      """It removes all provided functions to be called by the metronome."""

      # reinitialize all function related information
      self.functions        = []    
      self.parameters       = []  
      self.desiredBeats     = []   
      self.repeatFlags      = []  
      self.beatCountdowns   = []   

   def setTempo(self, tempo):
      """It sets the metronome's tempo."""
      
      self.tempo = tempo        # remember new tempo

      # and set it
      delay = int((60.0 / self.tempo) * 1000)   # in milliseconds
      self.timer.setDelay(delay)

   def getTempo(self):
      """It returns the metronome's tempo."""
      return self.tempo

   def setTimeSignature(self, timeSignature):
      """It sets the metronome's time signature."""      
      self.timeSignature = timeSignature        # remember new time signature
      self.currentBeat = 0                      # reinitialize current beat relative to provided time signature (1 means first beat)

   def getTimeSignature(self):
      """It returns the metronome's time signature."""      
      return self.timeSignature

   def start(self):
      """It starts the metronome."""
      self.timer.start()
      print "Metronome started..."

   def stop(self):
      """It starts the metronome."""
      self.timer.stop()
      print "Metronome stopped."

#   def __updateDisplay__(self):
#      """It temporarily flickers the metronome's visualization display to indicate a 'tick'."""
#      
#      # change color to indicate a tick
#      self.display.setColor( self.displayTickColor )  
#
#      # reset display back to original color after a small delay
#      #flikcerTimer = Timer2(250, self.display.setColor, [self.displayOriginalColor]) 
#      #flikcerTimer.start()    # after completion, this timer will eventually be garbage collected (no need to reuse)
#      self.flickerTimer.start() 

#   def __advanceCurrentBeat__(self):
#      """It advances the current metronome beat."""
#
#      if self.visualize:   # do we need to print out current beat?
#         print self.currentBeat
#
#      if self.sonify:   # do we need to sound out current beat?
#         if self.currentBeat == 1:    # strong (first) beat?
#            Play.note(self.sonifyPitch, 0, 200, self.sonifyVolume, self.sonifyChannel)   # louder
#         else:
#            Play.note(self.sonifyPitch, 0, 200, int(self.sonifyVolume * 0.7), self.sonifyChannel)   # softer
#
#      self.currentBeat = (self.currentBeat % self.timeSignature[0]) + 1  # wrap around as needed


   def __callFunctions__(self):
      """Calls all functions we are asked to synchronize."""
      
      # do visualization / sonification tasks (if any)
      if self.visualize:   # do we need to print out current beat?
         print self.currentBeat

      if self.sonify:   # do we need to sound out current beat?
         if self.currentBeat == 1:    # strong (first) beat?
            Play.note(self.sonifyPitch, 0, 200, self.sonifyVolume, self.sonifyChannel)   # louder
         else:
            Play.note(self.sonifyPitch, 0, 200, int(self.sonifyVolume * 0.7), self.sonifyChannel)   # softer

      #***
      #print "self.desiredBeats, self.beatCountdowns = ", 
      #print self.desiredBeats, self.beatCountdowns  

      # NOTE:  The following uses several for loops so that all functions are given quick service.
      #        Once they've been called, we can loop again to do necessary book-keeping...
      
      # first, iterate to call all functions with their (provided) parameters
      nonRepeatedFunctions = []   # holds indices of functions to be called only once (so we can remove them later)
      for i in range( len(self.functions) ):
      
        # see if current function needs to be called right away
        if self.beatCountdowns[i] == 0:
           
           # yes, so call this function!!!
           self.functions[i]( *(self.parameters[i]) )   # strange syntax, but does the trick...

           # check if function was meant to be called only once, and if so remove from future consideration
           if not self.repeatFlags[i]:  # call only once?

              nonRepeatedFunctions.append( i )   # mark it for deletion (so it is not called again)

      # now, all functions who needed to be called have been called
      
      # next, iterate to remove any functions that were meant to be called once
      for i in nonRepeatedFunctions:
         self.functions.pop( i )   
         self.parameters.pop( i ) 
         self.desiredBeats.pop( i ) 
         self.repeatFlags.pop( i ) 
         self.beatCountdowns.pop( i )
      

      ###########################################################################################
      # NOTE:  This belongs exactly here (before updating countdown timers below)      

      # advance to next beat (in anticipation...)
      self.currentBeat = (self.currentBeat % self.timeSignature[0]) + 1  # wrap around as needed

      ###########################################################################################

      # finally, iterate to update countdown timers for all remaining functions
      for i in range( len(self.functions) ):
           
        # if this function was just called
        if self.beatCountdowns[i] == 0:
        
           # reinitialize its beat countdown counter, i.e., reschedule it for its next call
              
           # calculate beat countdown
           self.beatCountdowns[i] = self.__calculateBeatCountdown__( self.desiredBeats[i] )              

        else:   # it's not time to call this function, so update its information

           # reduce ticks remaining to call it
           self.beatCountdowns[i] = self.beatCountdowns[i] - 1     # we are now one tick closer to calling it

      # now, all functions who needed to be called have been called, and all beat countdowns
      # have been updated. 


   def __calculateBeatCountdown__(self, desiredBeat):
      """Calculates the beat countdown given the desired beat."""         
   
#      if desiredBeat == 0:  # do they want now (regardess of current beat)?
#         beatCountdown = 0     # give them now               
#      elif desiredBeat >= self.currentBeat:  # otherwise, is desired beat now or in the future?
#         beatCountdown = desiredBeat - self.currentBeat  # calculate remaining beats until then
#      else:  # desired beat has passed in the time signature, so we need to pick it up in the next measure
#         beatCountdown = (desiredBeat + self.timeSignature[0]) - self.currentBeat
   
      if desiredBeat == 0:  # do they want now (regardess of current beat)?
         beatCountdown = 0     # give them now               
      elif self.currentBeat <= desiredBeat <= self.timeSignature[0]:  # otherwise, is desired beat the remaining measure?
         beatCountdown = desiredBeat - self.currentBeat                            # calculate remaining beats until then
      elif 1 <= desiredBeat < self.currentBeat:                       # otherwise, is desired beat passed in this measure?
         beatCountdown = (desiredBeat + self.timeSignature[0]) - self.currentBeat  # pick it up in the next measure
      elif self.timeSignature[0] < desiredBeat:                       # otherwise, is desired beat beyond this measure?
         beatCountdown = desiredBeat - self.currentBeat + self.timeSignature[0]    # calculate remaining beats until then
      else:  # we cannot handle negative beats
         raise ValueError("Cannot handle negative beats, " + str(desiredBeat) + ".")
    
      # ***
      #print "beatCountdown =", beatCountdown
      return beatCountdown


   def show(self):
      """It shows the metronome visualization display."""
      #self.display.show()
      self.visualize = True

   def hide(self):
      """It shows the metronome visualization display."""
      #self.display.hide()
      self.visualize = False

   def soundOn(self, pitch=ACOUSTIC_BASS_DRUM, volume=127, channel=9):
      """It turns the metronome sound on."""
      self.sonify = True
      self.sonifyPitch   = pitch   # which pitch to play whe ticking 
      self.sonifyChannel = channel # which channel to use (9 is for percussion)
      self.sonifyVolume  = volume  # how loud is strong beat (secondary beats will at 70%)

   def soundOff(self):
      """It turns the metronome sound off."""
      self.sonify = False


   

#
#####################################################################################
# If running inside JEM, register function that stops everything, when the Stop button
# is pressed inside JEM.
######################################################################################

# function to stop and clean-up all active MidiSequences
def __stopActiveMetronomes__():

   global __ActiveMetronomes__

   # first, stop them
   for m in __ActiveMetronomes__:
      m.stop()    # no need to check if they are playing - just do it (it's fine)

   # then, delete them 
   for m in __ActiveMetronomes__:
      del m

   # also empty list, so things can be garbage collected
   __ActiveMetronomes__ = []   # remove access to deleted items   

# now, register function with JEM (if possible)
try:

    # if we are inside JEM, registerStopFunction() will be available
    registerStopFunction(__stopActiveMetronomes__)   # tell JEM which function to call when the Stop button is pressed

except:  # otherwise (if we get an error), we are NOT inside JEM 

    pass    # so, do nothing.
 

   
######################################################################################
# synthesized jMusic instruments (also see http://jmusic.ci.qut.edu.au/Instruments.html)

#import AMInst
#import AMNoiseInst
#import AddInst
#import AddMorphInst
#import AddSynthInst
#import BandPassFilterInst
#import BowedPluckInst
#import BreathyFluteInst
#import ChiffInst
#import ControlledHPFInst
#import DynamicFilterInst
#import FGTRInst
#import FMNoiseInst
#import FractalInst
#import GranularInst
#import GranularInstRT
#import HarmonicsInst
#import LFOFilteredSquareInst
#import LPFilterEnvInst
#import NoiseCombInst
#import NoiseInst
#import OddEvenInst
#import OvertoneInst
#import PluckInst
#import PluckSampleInst
#import PrintSineInst
#import PulseFifthsInst
#import PulsewaveInst
#import RTPluckInst
#import RTSimpleFMInst
#import ResSawInst
#import ReverseResampledInst
#import RingModulationInst
#import SabersawInst
#import SawCombInst
#import SawHPFInst
#import SawLPFInst
#import SawLPFInstB
#import SawLPFInstE
#import SawLPFInstF
#import SawLPFInstG
#import SawLPFInstRT
#import SawtoothInst
#import Sawtooth_LPF_Env_Inst
#import SimpleAMInst
#import SimpleAllPassInst
#import SimpleFMInst
#import SimpleFMInstRT
#import SimplePluckInst
#import SimpleReverbInst
#import SimpleSampleInst
#import SimpleSineInst
#import SimpleTremoloInst
#import SimplestInst
#import SineInst
#import SlowSineInst
#import SquareBackwardsInst
#import SquareCombInst
#import SquareInst
#import SquareLPFInst
#import SubtractiveSampleInst
#import SubtractiveSynthInst
#import SuperSawInst
#import TextInst
#import TimpaniInst
#import TremoloInst
#import TriangleInst
#import TriangleRepeatInst
#import VaryDecaySineInst
#import VibesInst
#import VibratoInst
#import VibratoInstRT

# preserve Jython bindings that get ovwerwritten by the following Java imports - a hack!
# (also see very top of this file)
enumerate = enumerate_preserve


print
print