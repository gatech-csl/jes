# playNote.py
# Demonstrates how to play a single note.
 
from music import *    # import music library
 
note = Note(C4, HN)    # create a middle C half note
Play.midi(note)        # and play it!