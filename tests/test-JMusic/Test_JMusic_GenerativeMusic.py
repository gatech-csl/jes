# generativeMusic.py
#
# Demonstrates how to create music with weighted probabilities.
#
 
from music import *
from random import *
 
numNotes = 32        # how many random notes to play
 
# pitches and their chances to appear in output (the higher the
# chance, the more likely the pitch is to appear)
pitches   = [C4, D4, E4, F4, G4, A4, B4, C5]
durations = [QN, EN, QN, EN, QN, EN, SN, QN]
chances   = [5,  1,  3,  2,  4,  3,  1,  5]
 
####
# Create weighted lists of pitches and durations, where the number of
# times a pitch appears depends on the corresponding chance value.
# For example, if pitches[0] is C4, and chances[0] is 5, the weighted
# pitches list will get 5 instances of C4 added.
weightedPitches = []
weightedDurs    = []
for i in range( len(chances) ):
   weightedPitches = weightedPitches + [ pitches[i] ] * chances[i]
   weightedDurs    = weightedDurs + [ durations[i] ] * chances[i]
# now, len(weightedPitches) equals sum(chances)
# same applies to weightedDurs
 
# debug lines:
print "weightedPitches = ", weightedPitches
print "weightedDurations = ", weightedDurs
 
phrase = Phrase()    # create an empty phrase
 
# now create all the notes
for i in range(numNotes):
 
   event = randint(0, len(weightedPitches)-1)
   note  = Note(weightedPitches[event], weightedDurs[event])
 
   # the note has been found; now add this note
   phrase.addNote(note)
# now, all notes have been generated
 
# so, play them
Play.midi(phrase)