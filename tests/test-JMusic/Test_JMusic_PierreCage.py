# PierreCage.StructuresPourDeuxChances.py
#
# This program (re)creates pieces similar to:
#
# Pierre Boulez, "Structures I for two pianos", and
# John Cage, "Music of Changes, Book I".
#
# The piece generated consists of two parallel phrases containing
# notes with random pitch and duration.
#
 
from music import *
from random import *   # import random number generator
 
numberOfNotes = 100    # how many notes in each parallel phrase
 
##### define the data structure
part = Part()          # create an empty part
melody1 = Phrase(0.0)  # create phrase (at beginning of piece)
melody2 = Phrase(0.0)  # create phrase (at beginning of piece)
 
##### create musical data
# create random notes for first melody
for i in range(numberOfNotes):
   pitch = randint(C1, C7)      # get random pitch between C1 and C6
   duration = random() * 1.0    # get random duration (0.0 to 2.0)
   dynamic = randint(PP, FFF)   # get random dynamic between P and FF
   note = Note(pitch, duration, dynamic) # create note
   melody1.addNote(note)        # and add it to the phrase
# now, melody1 has been created
 
# create random notes for second melody
for i in range(numberOfNotes):
   pitch = randint(C1, C7)      # get random pitch between C1 and C6
   duration = random() * 1.0    # get random duration (0.0 to 2.0)
   dynamic = randint(PP, FFF)   # get random dynamic between P and FF
   note = Note(pitch, duration, dynamic) # create note
   melody2.addNote(note)        # and add it to the phrase
# now, melody2 has been created
 
##### combine musical material
part.addPhrase(melody1)
part.addPhrase(melody2)
 
##### play and write part to a MIDI file
Play.midi(part)
Write.midi(part, "Pierre Cage.Structures pour deux chances.mid")
