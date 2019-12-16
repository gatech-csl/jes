# ConcretPH_Xenakis.py
#
# A short example which generates a random cloud texture
# inspired by Iannis Xenakis's 'Concret PH' composition
#
# see http://en.wikipedia.org/wiki/Concret_PH
 
from music import *
from random import *
 
# constants for controlling musical parameters
cloudWidth = 64          # length of piece (in quarter notes)
cloudDensity = 23.44     # how dense the cloud may be
particleDuration = 0.2   # how long each sound particle may be
numParticles = int(cloudDensity * cloudWidth)   # how many particles
 
part = Part(BREATHNOISE)
 
# make particles (notes) and add them to cloud (part)
for i in range(numParticles):
 
   # create note with random attributes
   pitch = randint(0, 127)     # pick from 0 to 127
   duration = random() * particleDuration # 0 to particleDuration
   dynamic = randint(0, 127)   # pick from silent to loud
   panning = random()          # pick from left to right
   note = Note(pitch, duration, dynamic, panning)   # create note
 
   # now, place it somewhere in the cloud (time continuum)
   startTime = random() * cloudWidth    # pick from 0 to end of piece
   phrase = Phrase(startTime)           # create phrase with this start time
   phrase.addNote(note)                 # add the above note
   part.addPhrase(phrase)               # and add both to the part
# now, all notes have been created
 
# add some elegance to the end
Mod.fadeOut(part, 20)
 
View.show(part)
Play.midi(part)
Write.midi(part, "ConcretPh.mid")