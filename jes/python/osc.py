################################################################################################################
# osc.py       Version 1.6     07-Mar-2018     David Johnson and Bill Manaris

###########################################################################
#
# This file is part of Jython Music.
#
# Copyright (C) 2014-2018 David Johnson and Bill Manaris
#
#    Jython Music is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Jython Music is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Jython Music.  If not, see <http://www.gnu.org/licenses/>.
#
###########################################################################

#
# This module provides functionality for OSC communication between programs and OSC devices.
#
#
# REVISIONS:
#
#   1.6     07-Mar-2018 (bm) Now, we allow mutliple callback functions to be associated with the same 
#                       incoming OSC address.  This is was introduced to be consistent with the MidiIn API.
#
#   1.5     11-Feb-2016 (dj) Update in how we get host IP address in OscIn object to fix Mac OSX problem.
#
#   1.4     07-Dec-2014 (bm) Changed OscIn object functionality to allow registering of only *one*
#                       callback function per address (to mirror the corresponding MidiIn's object's
#                       behavior in the midi.py library).  The goal is to promote consistency of behavior
#                       between the two libraries.  Also, added MidiIn showMessages() and hideMessages() 
#                       to turn on and off printing of incoming OSC messages.  This allows to easily explore
#                       what messages are being send by a particular device (so that they can be mapped to 
#                       different functions).
#
#   1.3     19-Nov-2014 (bm) Fixed bug in cleaning up objects after JEM's stop button is pressed -
#                       if list of active objects already exists, we do not redefine it - thus, we 
#                       do not lose older objects, and can still clean them up.
#
#   1.2     06-Nov-2014 (bm) Added functionality to stop osc objects via JEM's Stop button
#                       - see registerStopFunction().
#
#   1.1     02-Dec-2013 (bm) Updated iiposed.com import statement to fix import error under 
#                       some Windows / Java combinations.
#
#   1.0     11-May-2013 (dj, bm) First implementation.
#

from com.illposed.osc import OSCListener, OSCMessage, OSCPacket, OSCPort, OSCPortIn, OSCPortOut

#from com.illposed.osc import *
#from com.illposed.osc.utility import *
import socket
from java.net import InetAddress

# used to keep track which osc objects are active, so we can stop them when
# JEM's Stop button is pressed

try:

   _ActiveOscInObjects_         # if already defined (from an earlier run, do nothing, as it already contains material)
   
except:

   _ActiveOscInObjects_  = []   # first run - let's define it to hold active objects
   _ActiveOscOutObjects_ = []   # first run - let's define it to hold active objects


#################### OscIn ##############################
#
# OscIn is used to receive messages from OSC devices.
#
# This class may be instantiated several times to create different OSC input objects (servers)
# to receive and handle OSC messages.
#
# The constructor expects the port number (your choice) to listen for incoming messages.
#
# When instantiated, the OscIn object outputs (print out) its host IP number and its port 
# (for convenience).  Use this info to set up the OSC clients used to send messages here.
#
# NOTE:  To send messages here you may use objects of the OscOut class below, or another OSC client, 
# such as TouchOSC iPhone client (http://hexler.net/software/touchosc).  

# The latter is most enabling, as it allows programs to be driven by external devices, such as
# smart phones (iPhone/iPad/Android).  This way you may build arbitrary musical instruments and 
# artistic installations.
#
# Picking port numbers:
# 
# Each OscIn object requires its own port.  So, pick port numbers not used by other applications.  
# For example, TouchOSC (a mobile app for Android and iOS devices), defaults to 8000 for sending OSC messages,
# and 9000 for receiving messages.  In general, any port from 1024 to 65535 may be used, as long as no other 
# application is using it.  If you have trouble, try changing port numbers.  The best bet is a port in 
# the range 49152 to 65535 (which is reserved for custom purposes).
#
# For example:
#
# oscIn = OscIn( 57110 )          # create an OSC input device (OSC server) on port 57110
#
# def simple(message):            # define a simple message handler (function)
#    print "Hello world!"
#
# oscIn.onInput("/helloWorld", simple)   # if the incoming OSC address is "/helloWorld", 
#                                        # call this function.
#
# def complete(message):          # define a more complete message handler
#     address = message.getAddress()
#     args = message.getArguments()
#     print "\nOSC Event:"
#     print "OSC In - Address:", address,   # print the time and address         
#     for i in range( len(args) ):          # and any message arguments (all on the same line)
#        print ", Argument " + str(i) + ": " + str(args[i]),
#     print
#
# oscIn.onInput("/.*", complete)   # all OSC addresses call this function
#

# a useful OSC meessage constant
ALL_MESSAGES = "/.*"    # matches all possible OSC addresses

class OscIn():

   def __init__(self, port = 57110):

      self.port = port                       # holds port to listen to (for incoming events/messages)
      self.oscPortIn = OSCPortIn(self.port)  # create port
      self.oscPortIn.startListening()        # and start it

      # also, get our host IP address (to output below, for the user's convenience)
      self.IPaddress = socket.gethostbyname(socket.gethostname())
      print "\nOSC Server started:"    
      print "Accepting OSC input on IP address", self.IPaddress, "at port", self.port
      print "(use this info to configure OSC clients)"
      print
      
      # create dictionary to hold registered callback functions, so that we can replace them
      # when a new call to onInput() is made for a given address - the dictionary key is the
      # address, and the dictionary value is the GenericListener created for this address,
      # so that may update the callback function it is associated with.
      self.oscAddressHandlers = {}
      
      self.showIncomingMessages = True   # print all incoming OSC messages by default

      # provide a default OSC message handler 
      # prints out all incoming OSC messages (if desired - see showMessages() and hideMessages())
      self.onInput(ALL_MESSAGES, self. _printIncomingMessage_)

      # remember that this OscIn has been created and is active (so that it can be stopped/terminated by JEM, if desired)
      _ActiveOscInObjects_.append(self)
      
      
   def onInput(self, OSCaddress, function):
      """
      Associate callback 'function' to OSC messages send to 'OSCaddress' on this device.  An 'OSCaddress'
      looks like a URL, e.g., "/first/second/third".
      """

      # register callback function for this OSC address
      if self.oscAddressHandlers.has_key( OSCaddress ):   # is there an existing hanlder already?
         
         # yes, so update it (i.e., update the GenericListener's functions attribute)
         self.oscAddressHandlers[ OSCaddress ].functions.append( function )
         
      else:
      
         # no, so add a new handler for this address
         handler = GenericListener( function )            # create the listener
         self.oscAddressHandlers[ OSCaddress ] = handler  # remember it
         self.oscPortIn.addListener(OSCaddress, handler)  # and add it to the OscIn object


   def _printIncomingMessage_(self, message):
      """It prints out the incoming OSC message (if desired)."""

      # determine if we need to print out the message
      if self.showIncomingMessages:   # echo print incoming OSC messages?
      
         # yes, so extract info
         OSCaddress = message.getAddress()
         args = message.getArguments()
         
         # and print out the message
         #print "\nOSC Event:"
         print "OSC In - Address:", '"' + str(OSCaddress) + '"',   # print the address         
         for i in range( len(args) ):                              # and any message arguments (all on the same line)
            if type(args[i]) == unicode:     # is the argument a string?
               print ", Argument " + str(i) + ': "' + args[i] + '"',   # yes, so use double quotes
            else:
               print ", Argument " + str(i) + ": " + str(args[i]),     # no, so print as is
         print

   def showMessages(self):
      """
      Turns on printing of incoming OSC messages (useful for exploring what OSC messages 
      are generated by a particular device).
      """
      self.showIncomingMessages = True

   def hideMessages(self):
      """
      Turns off printing of incoming OSC messages.
      """
      self.showIncomingMessages = False


############# helper class for OscIn #################
class GenericListener(OSCListener):

   def __init__(self, function = None):
      self.functions = [function]

   def acceptMessage(self, time, oscMessage):
      #self.function(time, oscMessage)  # *** for now, hide time, as it is not used
      for function in self.functions:
         function(oscMessage)


#################### OscOut ##############################
#
# OscOut is used to send messages to OSC devices.
#
# This class may be instantiated several times to create different OSC output objects (clients)
# to send OSC messages.
#
# The constructor expects the IP address and port number of the OSC device to which we are sending messages.
#
# For example:
#
# oscOut = OscOut( "localhost", 57110 )   # connect to an OSC device (OSC server) on this computer listening on port 57110
#
# oscOut.sendMessage("/helloWorld")        # send a simple OSC message
#
# oscOut.sendMessage("/itsFullOfStars", 1, 2.3, "wow!", True)   # send a more detailed OSC message
#

class OscOut():

   def __init__(self, IPaddress = "localhost", port = 57110):
      self.IPaddress = InetAddress.getByName(IPaddress)    # holds IP address of OSC device to connect with
      self.port = port                                     # and its listening port
      self.portOut = OSCPortOut(self.IPaddress, self.port) # create the connection

   def sendMessage(self, oscAddress, *args):
      """
      Sends an OSC message consisting of the 'oscAddress' and corresponding 'args' to the OSC output device.
      """

      # HACK: For some reason, float OSC arguments do not work, unless they are explictly converted to Java Floats.
      #       The following list comprehension does the trick.
      from java.lang import Float
      
      # for every argument, if it is a float cast it to a Java Float, otherwise leave unchanged
      args = [Float(x) if isinstance(x, float) else x for x in args]
      
      #print "sendMessage args = ", args
      oscMessage = OSCMessage( oscAddress, args )          # create OSC message from this OSC address and arguments
      self.portOut.send(oscMessage)                        # and send it to the OSC device that's listening to us

      # remember that this OscIn has been created and is active (so that it can be stopped/terminated by JEM, if desired)
      _ActiveOscOutObjects_.append(self)
      

# TO DO??: Do we need a sendBundle() for time-stamped, bunded OSC messages?
#          To resolve - what does the timestamp mean?  When to execute?  
#          For answers, see - http://opensoundcontrol.org/spec-1_0
#
#   def sendBundle(self, timestamp, listOscAddresses, listArguments):
#      """
#      Sends a bundle of OSC messages 
#      """
#


######################################################################################
# If running inside JEM, register function that stops everything, when the Stop button
# is pressed inside JEM.
######################################################################################

# function to stop and clean-up all active Osc objects
def _stopActiveOscObjects_():

   global _ActiveOscInObjects_, _ActiveOscOutObjects_

   # first, stop OscIn objects
   for oscIn in _ActiveOscInObjects_:
      oscIn.oscPortIn.stopListening()
      oscIn.oscPortIn.close()

   # now, stop OscOut objects
   for oscOut in _ActiveOscOutObjects_:
      oscOut.portOut.close()

   # then, delete all of them
   for oscObject in (_ActiveOscInObjects_ + _ActiveOscOutObjects_):
      del oscObject

   # also empty list, so things can be garbage collected
   _ActiveOscInObjects_ = []   # remove access to deleted items   
   _ActiveOscInObjects_ = []   # remove access to deleted items   

# now, register function with JEM (if possible)
try:

    # if we are inside JEM, registerStopFunction() will be available
    registerStopFunction(_stopActiveOscObjects_)   # tell JEM which function to call when the Stop button is pressed

except:  # otherwise (if we get an error), we are NOT inside JEM 

    pass    # so, do nothing.

   
   
#################### Unit Testing ##############################

if __name__ == '__main__':

   ###### create an OSC input object ######
   oscIn = OscIn( 57110 )        # get input from OSC devices on port 57110

   # define two message handlers (functions) for OSC input messages
   def simple(message):      
      print "Hello world!"

   # tell OSC input object which functions to call for which OSC addresses
   oscIn.onInput("/helloWorld", simple)   # if the incoming OSC message's address is "/helloWorld" call this function 



   ###### create an OSC output object ######
   oscOut = OscOut( "localhost", 57110 )    # send output to the OSC device on "localhost" listening at port 57110 
                                            # (i.e., the above OSC input object)
   
   # send a couple of messages
   oscOut.sendMessage("/helloWorld")        # message without arguments
   oscOut.sendMessage("/itsFullOfStars", 1, 2.35, "wow!", True)   # message with arguments
