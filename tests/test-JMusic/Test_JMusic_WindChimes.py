# windChimes.py
#
# Simulates a 4-tube wind chime.
#
# Demonstrates how we may sieve (harness) randomness to generate
# aesthetically pleasing musical outcomes.
 
from music import *
from random import *
 
# program parameters
cycles = 24       # how many times striker hits all four tubes
duration = 8.0    # tubes sounds last from 0 to this time units
minVol = 80       # low and high limit for random volume
maxVol = 100
 
# tube tuning (D7 chord)
tube1 = C5
tube2 = F5
tube3 = G4
tube4 = D6
 
# wind chime part
windChimePart = Part(BELLS)
 
# wind chime consists of four tubes
tube1Phrase = Phrase(0.0) # first tube starts at 0.0 time
tube2Phrase = Phrase(1.0) # second tube starts at 1.0 time, ...
tube3Phrase = Phrase(3.0) # ... and so on.
tube4Phrase = Phrase(5.0)
 
# generate wind chime notes and add them to these phrases
for i in range(cycles):
 
   # create random tube strikes (notes)
   note1 = Note(tube1, random() * duration, randint(minVol, maxVol) )
   note2 = Note(tube2, random() * duration, randint(minVol, maxVol) )
   note3 = Note(tube3, random() * duration, randint(minVol, maxVol) )
   note4 = Note(tube4, random() * duration, randint(minVol, maxVol) )
 
   # accumulate notes in parallel sequences
   tube1Phrase.addNote( note1 )
   tube2Phrase.addNote( note2 )
   tube3Phrase.addNote( note3 )
   tube4Phrase.addNote( note4 )
# now, all notes have been created
 
# add note sequences to wind chime part
windChimePart.addPhrase( tube1Phrase )
windChimePart.addPhrase( tube2Phrase )
windChimePart.addPhrase( tube3Phrase )
windChimePart.addPhrase( tube4Phrase )
 
# view and play wind chimes
View.sketch(windChimePart)
Play.midi(windChimePart)