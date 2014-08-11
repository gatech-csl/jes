# hotCrossBuns.py
# This is the only song I can play on the piano.
# - Matthew Frazier

from jm import JMC
from jm.music.data import Note, Phrase
from jm.util import Play

full = 0.8
half = 0.4

hotCrossBuns = [Note(n, full) for n in [JMC.B4, JMC.A4, JMC.G4]]
hotCrossBuns.append(Note(JMC.REST, half))

oneAPenny = [Note(JMC.G4, half) for n in range(4)]
twoAPenny = [Note(JMC.A4, half) for n in range(4)]

songNotes = hotCrossBuns + hotCrossBuns + oneAPenny + twoAPenny + hotCrossBuns

phrase = Phrase()
for note in songNotes:
  phrase.addNote(note)

def playHotCrossBuns():
  Play.midi(phrase)
