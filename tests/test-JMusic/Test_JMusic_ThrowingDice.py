# throwingDice.py
#
# Demonstrates the division of randomness to several choices.
 
from music import *
from random import *
 
numNotes = 14        # how many random notes to play
 
phrase = Phrase()    # create an empty phrase
 
for i in range(numNotes):
 
   dice = randint(1, 6)  # throw dice (1 and 6 inclusive)
 
   # determine which dice face came up
   if dice == 1:
      note = Note(C4, QN)   # C4 note
   elif dice == 2:
      note = Note(D4, QN)   # D4 note
   elif dice == 3:
      note = Note(E4, QN)   # E4 note
   elif dice == 4:
      note = Note(F4, QN)   # F4 note
   elif dice == 5:
      note = Note(G4, QN)   # G4 note
   elif dice == 6:
      note = Note(A4, QN)   # A4 note
   else:
      print "Something unexpected happened... dice =", dice
 
   phrase.addNote(note)  # add this random note to phrase
 
# now, all random notes have been created
 
# so, play them
Play.midi(phrase)