# pentatonicMelody.py
# Generate a random pentatonic melody. It begins and ends
# with the root note.
 
from music import *    # import music library
from random import *   # import random library
 
pentatonicScale = [C4, D4, E4, G4, A4]   # which notes to use
durations       = [QN, DEN, EN, SN]      # which durations to use
 
# pick a random number of notes to create (between 12 and 18)
numNotes = randint(12, 18)   # number of notes to create
 
phrase = Phrase()   # create an empty phrase
 
# first note should be root
note = Note(C4, QN)    # create root note
phrase.addNote(note)   # add note to phrase
 
# generate enough random notes (minus starting and ending note)
for i in range(numNotes - 2):
   pitch = choice(pentatonicScale)   # select next pitch
   duration = choice(durations)      # select next duration
   dynamic = randint(80, 120)        # randomly vary the volume
   panning = random()                # and place in stereo field
   note = Note(pitch, duration, dynamic, panning) # create  note
   phrase.addNote(note)              # add it to phrase
 
# last note should be root also (a half note, to signify end)
note = Note(C4, HN)    # create root note
phrase.addNote(note)   # add note to phrase
 
Play.midi(phrase)      # play the melody