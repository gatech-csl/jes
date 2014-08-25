# oscClient.py
#
# Demonstrates how to create an OSC client program.
#

from osc import *

###### create an OSC output object ######
oscOut = OscOut( "localhost", 57110 )    # send output to "localhost" at port 57110 
   
# send a couple of messages (first without arguments, and then with arguments)
oscOut.sendMessage("/helloWorld")                              # first message 
oscOut.sendMessage("/itsFullOfStars", 1, 2.35, "wow!", True)   # second message
