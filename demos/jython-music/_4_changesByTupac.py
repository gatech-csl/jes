# changesByTupac.py
# Plays main chord progression from 2Pac's "Changes" (1998).

from music import *

mPhrase = Phrase()
mPhrase.setTempo(105)

# section 1 - chords to be repeated
pitches1   = [[E4,G4,C5], [E4,G4,C5], [D4,G4,B4], A4, G4, [D4, FS4, A4], 
              [D4, G4, B4], [C4, E4, G4], E4, D4, C4, [G3, B4, D4]]
durations1 = [DEN,        DEN,        HN,         SQ, SQ,  DEN,         
              DEN,          DQN,          EN, SN, SN, DQN]

# section 2 - embellishing chords
pitches2   = [A4, B4]
durations2 = [SN, SN] 

mPhrase.addNoteList(pitches1, durations1)  # add section 1 
mPhrase.addNoteList(pitches2, durations2)  # add section 2
mPhrase.addNoteList(pitches1, durations1)  # re-add section 1

Play.midi(mPhrase)