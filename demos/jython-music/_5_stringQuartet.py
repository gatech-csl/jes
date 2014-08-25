# stringQuartet.py
# Demonstrates how to create concurrent musical parts.
# Haydn, Opus 64 no 5

from music import *

stringsPart = Part(STRINGS, 0)   # create empty strings part
stringsPart.setTempo(104)

pitches1 =   [A5, REST, A5, REST, A5, REST, A5, A6, E6,  D6, D6, 
               CS6, D6, D6, CS6, D6, E6]
durations1 = [EN, EN,   EN, EN,   EN, EN,   WN, DHN, EN, EN, HN, 
               DEN, SN, DEN, TN, TN, QN]
violin1 = Phrase(0.0)                       # create a phrase
violin1.addNoteList(pitches1, durations1)   # addnotes to the phrase
stringsPart.addPhrase(violin1)              # now, add phrase to part

pitches2 =   [FS4, G4, FS4, E4, D4, REST, G4, A4, G4, FS4, E4]
durations2 = [QN,  QN, QN, QN, QN, DHN,  QN, QN, QN, QN,  QN]
violin2 = Phrase(3.0)                       # create a phrase
violin2.addNoteList(pitches2, durations2)   # addnotes to the phrase
stringsPart.addPhrase(violin2)              # now, add phrase to part

pitches3 =   [D4, E4, D4, A3, FS3, REST, E4, FS4, E4, D4, CS4]
durations3 = [QN, QN, QN, QN, QN,  DHN,  QN, QN,  QN, QN,  QN]
violin3 = Phrase(3.0)                       # create a phrase
violin3.addNoteList(pitches3, durations3)   # addnotes to the phrase
stringsPart.addPhrase(violin3)              # now, add phrase to part

pitches4 =   [D2, FS2, A2, D3, A2, REST, A2]
durations4 = [QN, QN,  QN, QN, QN, DHN,  QN]
violin4 = Phrase(7.0)                       # create a phrase
violin4.addNoteList(pitches4, durations4)   # addnotes to the phrase
stringsPart.addPhrase(violin4)              # now, add phrase to part

Play.midi(stringsPart)