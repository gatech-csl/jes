# drumsComeAlive.py
#
# Demonstrates how to uses randomness to make a drum pattern come
# "alive", i.e., to sound more natural, more human-like.
# In this example, every now and then (randomly, 35% of the time),
# we play an open hi-hat sound (as opposed to a closed one).
#
 
from music import *
from random import *
 
##### musical parameters
# 35% of the time we try something different
comeAlive = 0.35
 
# how many measures to play
measures = 8    
 
##### define the data structure
score = Score("Drums Come Alive", 125.0) # tempo is 125 bpm
 
drumsPart = Part("Drums", 0, 9)  # using MIDI channel 9 (percussion)
 
bassDrumPhrase = Phrase(0.0)     # create phrase for each drum sound
snareDrumPhrase = Phrase(0.0)
hiHatPhrase = Phrase(0.0)
 
##### create musical data
# kick
# bass drum pattern (one bass 1/2 note) x 2 = 1 measure
# (we repeat this x 'measures')
for i in range(2 * measures):
 
   dynamics = randint(80, 110)   # add some variation in dynamics
   n = Note(ACOUSTIC_BASS_DRUM, HN, dynamics)
   bassDrumPhrase.addNote(n)
 
# snare
# snare drum pattern (one rest + one snare 1/4 notes) x 2 = 1 measure
# (we repeat this x 'measures')
for i in range(2 * measures):
 
   r = Note(REST, QN)
   snareDrumPhrase.addNote(r)
 
   dynamics = randint(80, 110)    # add some variation in dynamics
   n = Note(SNARE, QN, dynamics)
   snareDrumPhrase.addNote(n)
 
# hats
# a hi-hat pattern (one hi-hat + one rest 1/16 note) x 8 = 1 measure
# (we repeat this x 'measures')
for i in range(8 * measures):
 
   # if the modulo of i divided by 2 is 1, we are at an odd hit
   # (if it is 0, we are at an even hit)
   oddHit = i%2 == 1
 
   # time to come alive?
   doItNow = random() < comeAlive
 
   # let's give some life to the hi-hats
   if oddHit and doItNow:    # on odd hits, if it's time to do it,
      pitch = OPEN_HI_HAT       # let's open the hit-hat
   else:                     # otherwise,
      pitch = CLOSED_HI_HAT     # keep it closed   
 
   # also add some variation in dynamics
   dynamics = randint(80, 110)
 
   # create hi-hat note
   n = Note(pitch, SN, dynamics)
   hiHatPhrase.addNote(n)
 
   # now, create rest
   r = Note(REST, SN)
   hiHatPhrase.addNote(r)
 
##### combine musical material
drumsPart.addPhrase(bassDrumPhrase)
drumsPart.addPhrase(snareDrumPhrase)
drumsPart.addPhrase(hiHatPhrase)
score.addPart(drumsPart)
 
##### view and play
View.sketch(score)
Play.midi(score)