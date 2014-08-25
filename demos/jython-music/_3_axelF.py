# axelF.py
# Generates Harold Faltermeyer's electronic instrumental theme 
# from the film Beverly Hills Cop (1984).

from music import *

# theme (notice how we line up corresponding pitches and rhythms)
pitches1   = [F4, REST, AF4, REST, F4, F4, BF4, F4, EF4]
durations1 = [QN, QN,   QN,  EN,   QN, EN, QN,  QN, QN] 
pitches2   = [F4, REST, C5, REST, F4, F4, DF5, C5, AF4]
durations2 = [QN, QN,   QN, EN,   QN, EN, QN,  QN, QN]
pitches3   = [F4, C5, F5, F4, EF4, EF4, C4, G4, F4]
durations3 = [QN, QN, QN, EN, QN,  EN,  QN, QN, DQN]

# create an empty phrase, and construct theme using pitch/rhythm data
theme = Phrase()   
theme.addNoteList(pitches1, durations1)
theme.addNoteList(pitches2, durations2)
theme.addNoteList(pitches3, durations3)

# set the instrument and tempo for the theme
theme.setInstrument(SYNTH_BASS_2)
theme.setTempo(220)

# play it
Play.midi(theme)