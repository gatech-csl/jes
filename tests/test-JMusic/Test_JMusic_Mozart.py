# Provided by: https://jythonmusic.me/ch-6-randomness-and-choices/
#
# This program generates an excerpt of Mozart's "Musikalisches
# Wurfelspiel" (aka Mozart's Dice Game). It demonstrates how
# randomness may be sieved (harnessed) to produce aesthetic results.
#
# See Schwanauer, S, and D Levitt. 1993. Appendix, in Machine Models
# of Music. Cambridge, MA: MIT Press, pp. 533-538.
#
# The original has 16 measures with 11 choices per measure.
# This excerpt is a simplified form. In this excerpt,
# musical material is selected from this matrix:
#
# I II III IV
# 96 6 141 30
# 32 17 158 5
# 40
#
# Columns represent alternatives for a measure. The composer throws
# dice to select an alternative (choice) from first column.
# Then, connects it with the choice from second column, and so on.
#

from music import *
from random import *
 
# musical data structure
walzerteil = Part() # contains a four-measure motif generated
# randomly from the matrix above
 
# measure 1 - create alternatives
# choice 96
pitches96 = [[C3, E5], C5, G4]
durations96 = [EN, EN, EN]
choice96 = Phrase()
choice96.addNoteList(pitches96, durations96)
 
# choice 32
pitches32 = [[C3, E3, G4], C5, E5]
durations32 = [EN, EN, EN]
choice32 = Phrase()
choice32.addNoteList(pitches32, durations32)
 
# choice 40
pitches40 = [[C3, E3, C5], B4, C5, E5, G4, C5]
durations40 = [SN, SN, SN, SN, SN, SN]
choice40 = Phrase()
choice40.addNoteList(pitches40, durations40)
 
# measure 2 - create alternatives
# choice 6 (same as choice 32)
choice6 = Phrase()
choice6.addNoteList(pitches32, durations32)
 
# choice 17
pitches17 = [[E3, G3, C5], G4, C5, E5, G4, C5]
durations17 = [SN, SN, SN, SN, SN, SN]
choice17 = Phrase()
choice17.addNoteList(pitches17, durations17)
 
# measure 3 - create alternatives
# choice 141
pitches141 = [[B2, G3, D5], E5, F5, D5, [G2, C5], B4]
durations141 = [SN, SN, SN, SN, SN, SN]
choice141 = Phrase()
choice141.addNoteList(pitches141, durations141)
 
# choice 158
pitches158 = [[G2, B4], D5, B4, A4, G4]
durations158 = [EN, SN, SN, SN, SN]
choice158 = Phrase()
choice158.addNoteList(pitches158, durations158)
 
# measure 4 - create alternatives
# choice 30
pitches30 = [[C5, G4, E4, C4, C2]]
durations30 = [DQN]
choice30 = Phrase()
choice30.addNoteList(pitches30, durations30)
 
# choice 5
pitches5 = [[C2, C5, G4, E4, C4], [G2, B4], [C2, E4, C5]]
durations5 = [SN, SN, QN]
choice5 = Phrase()
choice5.addNoteList(pitches5, durations5)
 
# roll the dice!!!
measure1 = choice([choice96, choice32, choice40])
measure2 = choice([choice6, choice17])
measure3 = choice([choice141, choice158])
measure4 = choice([choice30, choice5])
 
# connect the random measures into a waltz excerpt
walzerteil.addPhrase(measure1)
walzerteil.addPhrase(measure2)
walzerteil.addPhrase(measure3)
walzerteil.addPhrase(measure4)
 
# view and play randomly generated waltz excerpt
View.sketch(walzerteil)
Play.midi(walzerteil)
