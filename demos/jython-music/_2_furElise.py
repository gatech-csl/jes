# furElise.py
# Generates the theme from Beethoven's Fur Elise.

from music import *

# theme has some repetition, so break it up to maximize economy
# (also notice how we line up corresponding pitches and rhythms)
pitches1 = [E5, DS5, E5, DS5, E5, B4, D5, C5, A4, REST, C4, E4, A4, B4, REST, E4]
rhythms1 = [SN, SN,  SN, SN,  SN, SN, SN, SN, EN, SN,   SN, SN, SN, EN, SN,   SN]
pitches2 = [GS4, B4, C5, REST, E4]
rhythms2 = [SN,  SN, EN, SN,   SN]
pitches3 = [C5, B4, A4]
rhythms3 = [SN, SN, EN]

# create an empty phrase, and construct theme from the above motifs
theme = Phrase()   
theme.addNoteList(pitches1, rhythms1)
theme.addNoteList(pitches2, rhythms2)
theme.addNoteList(pitches1, rhythms1)  # again
theme.addNoteList(pitches3, rhythms3)

# play it
Play.midi(theme)
