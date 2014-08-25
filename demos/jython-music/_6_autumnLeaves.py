# autumnLeaves.py
# It plays the theme from "Autumn Leaves", in a Jazz trio arrangement
# (using trumpet, vibraphone, and acoustic bass instruments).

from music import *

##### define the data structure (score, parts, and phrases)
autumnLeavesScore = Score("Autumn Leaves (Jazz Trio)", 140) # 140 bpm

trumpetPart = Part(TRUMPET, 0)       # trumpet to MIDI channel 0
vibesPart  = Part(VIBES, 1)          # vibraphone to MIDI channel 1
bassPart    = Part(ACOUSTIC_BASS, 2) # bass to MIDI channel 2

melodyPhrase = Phrase()   # holds the melody
chordPhrase  = Phrase()   # holds the chords
bassPhrase   = Phrase()   # holds the bass line

##### create musical data
# melody
melodyPitch1 = [REST, E4, FS4, G4, C5, REST, D4, E4, FS4, B4,  B4] 
melodyDur1   = [QN,   QN, QN,  QN, WN, EN,   DQN,QN, QN,  DQN, HN+EN]
melodyPitch2 = [REST, C4, D4, E4, A4, REST, B3, A4, G4, E4]
melodyDur2   = [QN,   QN, QN, QN, WN, EN,   DQN,QN, QN, 6.0]

melodyPhrase.addNoteList(melodyPitch1, melodyDur1) # add to phrase
melodyPhrase.addNoteList(melodyPitch2, melodyDur2)

# chords
chordPitches1   = [REST, [E3, G3, A3, C4], [E3, G3, A3, C4], REST, 
                    [FS3, A3, C4]]
chordDurations1 = [WN,    HN,               QN,              QN,    
                    QN]           
chordPitches2   = [REST, [D3, FS3, G3, B3], [D3, FS3, G3, B3]]
chordDurations2 = [DHN,  HN,                QN]               
chordPitches3   = [REST, [C3, E3, G3, B3], REST, [E3, FS3, A3, C4], 
                    [E3, FS3, A3, C4]]
chordDurations3 = [QN,   QN,               DHN,  HN,                
                    QN]
chordPitches4   = [REST, [DS3, FS3, A3, B3], REST, [E3, G3, B3], 
                   [DS3, FS3, A3, B3]]
chordDurations4 = [QN,   QN,                 DHN,  HN,           
                   QN]
chordPitches5   = [REST, [E3, G3, B3], REST]
chordDurations5 = [QN,   HN,           HN]

chordPhrase.addNoteList(chordPitches1, chordDurations1)  # add them
chordPhrase.addNoteList(chordPitches2, chordDurations2)
chordPhrase.addNoteList(chordPitches3, chordDurations3)
chordPhrase.addNoteList(chordPitches4, chordDurations4)
chordPhrase.addNoteList(chordPitches5, chordDurations5)

# bass line
bassPitches1   = [REST, A2, REST, A2, E2, D2, REST, D2, A2, G2, REST, 
                   G2, D2, C2] 
bassDurations1 = [WN,   QN, EN,   EN, HN, QN, EN,   EN, HN, QN, EN,   
                   EN, HN, QN] 
bassDurations2 = [EN,   EN, HN, QN,  EN,   EN,  HN, QN, EN,   EN, HN,  
                   QN]
bassPitches2   = [REST, C2, G2, FS2, REST, FS2, C2, B1, REST, B1, FS2, 
                   E2] 
bassPitches3   = [REST, E2, E2, B1, E2, REST]
bassDurations3 = [EN,   EN, QN, QN, HN, HN]

bassPhrase.addNoteList(bassPitches1, bassDurations1)  # add them
bassPhrase.addNoteList(bassPitches2, bassDurations2)
bassPhrase.addNoteList(bassPitches3, bassDurations3)

##### combine musical material
trumpetPart.addPhrase(melodyPhrase) # add phrases to parts
vibesPart.addPhrase(chordPhrase)
bassPart.addPhrase(bassPhrase)

autumnLeavesScore.addPart(trumpetPart) # add parts to score
autumnLeavesScore.addPart(vibesPart)
autumnLeavesScore.addPart(bassPart)

Play.midi(autumnLeavesScore)  # play music