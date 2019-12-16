# brownianMelody.py
#
# Demonstrates how to create more correlated music from chaos
# (i.e., randomness). This process simulates the random "walks" of
# particles within water, etc., i.e., unpredictable, but not chaotic.
# It models the flip of a coin - if heads, next note in the melody
# goes up one scale degree; if tails, next note is down one scale
# degree.
 
from music import *
from random import *
 
numberOfNotes = 29
 
##### define the data structure
brownianMelodyScore = Score("Brownian melody", 130)
brownianMelodyPart = Part("Brownian melody", TUBULAR_BELLS, 0)
brownianMelodyPhrase = Phrase()
 
##### create musical data
note = Note(C4, EN) # create first note
brownianMelodyPhrase.addNote(note) # add note to phrase
 
for i in range(numberOfNotes): # create enough notes
 
	# now, let's get next note according to brownian motion
	note = note.copy() # create a new copy
 
	# flip a coin
	heads = random() < 0.5     # a 50-50 chance to be True
	 
	if heads: # if we got heads,
		Mod.transpose(note, 1, MAJOR_SCALE, C4) # up a scale degree
	else: # otherwise
		Mod.transpose(note, -1, MAJOR_SCALE, C4) # down a scale degree
 
	brownianMelodyPhrase.addNote(note) # add note to phrase
	# now, all notes have been generated
 
##### combine musical material
brownianMelodyPart.addPhrase(brownianMelodyPhrase)
brownianMelodyScore.addPart(brownianMelodyPart)
 
##### view score and play it
View.sketch(brownianMelodyScore)
Play.midi(brownianMelodyScore)
