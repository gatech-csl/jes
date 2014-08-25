# oscServer.py
#
# Demonstrates how to create an OSC server program.
#

from osc import *

###### create an OSC input object ######
oscIn = OscIn( 57110 )        # receive messages from OSC clients on port 57110

# define two message handlers (functions) for incoming OSC messages
def simple(message):      
   print "Hello world!"

def complete(message):    
   OSCaddress = message.getAddress()
   args = message.getArguments()
   print "\nOSC Event:"
   print "OSC In - Address:", OSCaddress,   # print the time and address         
   for i in range( len(args) ):             # and any message arguments
      print ", Argument " + str(i) + ": " + str(args[i]),
   print

###### now, associate above functions with OSC addresses ######

# if the incoming OSC address is "/helloWorld", call this function
oscIn.onInput("/helloWorld", simple)  

# for any incoming OSC address (i.e., "/.*"), call this function
oscIn.onInput("/.*", complete)    