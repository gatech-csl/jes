################################################################################################################
# image.py    Version 1.5     19-May-2014     Bill Manaris

###########################################################################
#
# This file is part of Jython Music.
#
# Copyright (C) 2014 Bill Manaris
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
# Provides functions to read and write image files.
#
# Inspired by http://introcs.cs.princeton.edu/java/stdlib/Picture.java.html
#
# Revisions:
#
#   1.5     19-Nov-2014 (bm) Added functionality to stop osc objects via JEM's Stop button
#                       - see registerStopFunction().  Also, fixed bug in cleaning up objects -
#                       if list of active objects already exists, we do not redefine it - thus, we 
#                       do not lose older objects, and can still clean them up.
#
#   1.4     02-May-2014 (bm) Added fixWorkingDirForJEM() solution to work with new JEM editor by Tobias Kohn.
#
#   1.3     17-Mar-2013 (bm) Origin moved to top-left (for consistency with other systems).
#
#   1.2     10-Feb-2013 (bm) Now Image() constructor accepts a filename, as well as a width and a height.
#                       If the filename argument is a string, then it is treated as a filename
#                       to be opened.  If filename is an int, it is treated as width, and the second
#                       argument is treated as height of a blank image to be created.  This way, we
#                       do not need Read.image() from the music library anymore (which was creating
#                       an unnecessary content coupling between the two libraries - image and music.py).
#                       Also, added show() and hide().
#
#   1.1     05-Sep-2012 (bm) Renamed package to 'image'.
#
#   1.0.1	21-May-2012	(bm) Changed origin of image to lower-left corner.
#
#   1.0	    16-Nov-2011	(bm) Original version.
#

from java.awt import Color
from java.awt.image import BufferedImage
from java.io import File
from javax.imageio import ImageIO

from javax.swing import ImageIcon, JFrame, JLabel

######################################################################################
# JEM working directory fix
#
# JEM (written partially in Java) does not allow changing current directory.
# So, when we have the user's desired working directory we CANNOT use it to read/write
# jMusic media files, unless we add it as a prefix here to every Read/Write operation.
# We do so only if the filepath passed to Read/Write is just a filename (as opposed
# to a path).
#
# Let's define some useful stuff here, for this fix

import os.path

def fixWorkingDirForJEM( filename ):
   """It prefixes the provided filename with JEM's working directory, if available,
      only if filename is NOT an absolute path (in which case the user truly knows
      where they want to store it).
   """
   
   try:

      JEM_getMainFilePath   # check if function JEM_getMainFilePath() is defined (this happens only inside JEM) 
      
      # get working dir, if JEM is available
      workDir = JEM_getMainFilePath()
      
      # two cases for filename: 
      # 
      # 1. a relative filepath (e.g., just a filename, or "../filename")
      # 2. an absolute filepath
      
      if os.path.isabs( filename ):          # if an absolute path, the user knows what they are doing 
         return filename                     # ...so, do nothing
      else:                                  # else (if a relative pathname),
         return workDir + filename           # ...fix it
   
   except:   
      # if JEM is not available, do nothing (e.g., music.py is being run outside of JEM)
      return filename


# used to keep track which image objects are active, so we can close them when
# JEM's Stop button is pressed - this way everything timed to happen into
# the future (notes, animation, etc.) stops

try:

   _ActiveImages_         # if already defined (from an earlier run, do nothing, as it already contains material)
   
except:

   _ActiveImages_ = []    # first run - let's define it to hold active objects


######################################################################################
class Image:
   """Holds an image of RGB pixels accessed by column and row indices (col, row).  
      Origin (0, 0) is at upper left."""
      
# QUESTION:  For efficiency, should we also extract and save self.pixels (at image reading time)?
# Also make setPixel(), getPixel(), setPixels() and getPixels() work on/with self.pixels.  
# And when writing, use code in current setPixels() to update image buffer, before writing it out?
# This is something to try.
   
   def __init__(self, filename, width=None, height=None): 
      """Create an image from a file, or an empty (black) image with specified dimensions."""
      
      # Since Python does not allow constructors with different signatures,
      # the trick is to reuse the first argument as a filename or a width.
      # If it is a string, we assume they want is to open a file.
      # If it is an int, we assume they want us to create a blank image.
      
      if type(filename) == type(""):  # is it a string?
         self.filename = filename        # treat is a filename
         self.image = BufferedImage(1, 1, BufferedImage.TYPE_INT_RGB)  # create a dummy image
         self.read(filename)             # and read external image into ti
                  
      elif type(filename) == type(1): # is it a int?
      
         # create blank image with specified dimensions
         self.filename = "Untitled"
         self.width = filename       # holds image width (shift arguments)
         self.height = width         # holds image height
         self.image = BufferedImage(self.width, self.height, BufferedImage.TYPE_INT_RGB)  # holds image buffer (pixels)
      else:
         raise  TypeError("Image(): first argument must a filename (string) or an blank image width (int).")
         
      # display image
      self.display = JFrame()      # create frame window to hold image
      icon = ImageIcon(self.image) # wrap image appropriately for displaying in a frame
      container = JLabel(icon)         
      self.display.setContentPane(container)  # and place it

      self.display.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
      self.display.setTitle(self.filename)
      self.display.setResizable(False)
      self.display.pack()
      self.display.setVisible(True)

      # remember that this image has been created and is active (so that it can be stopped/terminated by JEM, if desired)
      _ActiveImages_.append(self)

 
   def getWidth(self):
      """Returns the width of the image.""" 
      
      return self.width
      
   def getHeight(self):
      """Returns the height of the image.""" 
      
      return self.height
      
   def getPixel(self, col, row):
      """Returns a list of the RGB values for this pixel, e.g., [255, 0, 0].""" 
      
      # Obsolete - convert the row so that row zero refers to the bottom row of pixels.
      #row = self.height - row - 1

      color = Color(self.image.getRGB(col, row))  # get pixel's color
      return [color.getRed(), color.getGreen(), color.getBlue()]  # create list of RGB values (0-255)

   def setPixel(self, col, row, RGBlist):
      """Sets this pixel's RGB values, e.g., [255, 0, 0].""" 
      
      # Obsolete - convert the row so that row zero refers to the bottom row of pixels.
      #row = self.height - row - 1

      color = Color(RGBlist[0], RGBlist[1], RGBlist[2])  # create color from RGB values
      self.image.setRGB(col, row, color.getRGB())


   def getPixels(self):
      """Returns a 2D list of pixels (col, row) - each pixel is a list of RGB values, e.g., [255, 0, 0].""" 
      
      pixels = []                      # initialize list of pixels
      #for row in range(self.height-1, 0, -1):   # load pixels from image      
      for row in range(0, self.height):   # load pixels from image      
         pixels.append( [] )              # add another empty row
         for col in range(self.width):    # populate row with pixels    
            # RGBlist = self.getPixel(col, row)   # this works also (but slower)    
            color = Color(self.image.getRGB(col, row))  # get pixel's color
            RGBlist = [color.getRed(), color.getGreen(), color.getBlue()]  # create list of RGB values (0-255)
            pixels[-1].append( RGBlist )   # add a pixel as (R, G, B) values (0-255, each)

      # now, 2D list of pixels has been created, so return it
      return pixels

   def setPixels(self, pixels):
      """Sets image to the provided 2D list of pixels (col, row) - each pixel is a list of RGB values, e.g., [255, 0, 0].""" 
      
      self.height = len(pixels)        # get number of rows
      self.width  = len(pixels[0])     # get number of columns (assume all columns have same length
      
      #for row in range(self.height-1, 0, -1):   # iterate through all rows      
      for row in range(0, self.height):   # iterate through all rows     
         for col in range(self.width):    # iterate through every column on this row
         
            RGBlist = pixels[row][col]
            #self.setPixel(col, row, RGBlist)   # this works also (but slower)
            color = Color(RGBlist[0], RGBlist[1], RGBlist[2])  # create color from RGB values
            self.image.setRGB(col, row, color.getRGB())

   def read(self, filename): 
      """Read an image from a .png, .gif, or .jpg file. as 2D list of RGB pixels."""
      
      # JEM working directory fix (see above)
      filename = fixWorkingDirForJEM( filename )   # does nothing if not in JEM
	  
      # ***
      #print "fixWorkingDirForJEM( filename ) =", filename

      file = File(filename)    # read file from current directory
      self.image = ImageIO.read(file)
      self.width  = self.image.getWidth(None)
      self.height = self.image.getHeight(None)
      
      pixels = []   # initialize list of pixels
      
      # load pixels from image
      for row in range(self.height):
         pixels.append( [] )   # add another empty row
         for col in range(self.width):   # now, populate row with pixels
            color = Color(self.image.getRGB(col, row))  # get pixel's color
            RGBlist = [color.getRed(), color.getGreen(), color.getBlue()]  # create list of RGB values (0-255)
            pixels[-1].append( RGBlist )   # add a pixel as (R, G, B) values (0-255, each)

      # now, pixels have been loaded from image file, so create an image
      self.setPixels(pixels)
      
   def write(self, filename):
      """Saves the pixels to a file (.png or .jpg)."""
      
      # JEM working directory fix (see above)
      filename = fixWorkingDirForJEM( filename )   # does nothing if not in JEM
	  
      # ***
      #print "fixWorkingDirForJEM( filename ) =", filename

      # get suffix
      suffix = filename[-3:]   
      suffix = suffix.lower()
      
      if suffix == "jpg" or suffix =="png":
         ImageIO.write(self.image, suffix, File(filename))  # save, and also
         self.filename = filename               # update image filename
         self.display.setTitle(self.filename)   # update display title            
      else:
         print "Filename must end in .jpg or .png"

   def show(self):
      """It displays the image."""
      
      self.display.setVisible(True)
      #self.display.repaint()          # draw it

   def hide(self):
      """It hides the image."""
      
      self.display.setVisible(False)
      

######################################################################################
# If running inside JEM, register function that stops everything, when the Stop button
# is pressed inside JEM.
######################################################################################

# function to stop and clean-up all active images
def _stopActiveImages_():

   global _ActiveImages_

   # first, hide them
   for image in _ActiveImages_:
      image.hide()

   # then, delete them
   for image in _ActiveImages_:
      del image

   # also empty list, so things can be garbage collected
   _ActiveImages_ = []   # remove access to deleted items   

# now, register function with JEM (if possible)
try:

    # if we are inside JEM, registerStopFunction() will be available
    registerStopFunction(_stopActiveImages_)   # tell JEM which function to call when the Stop button is pressed

except:  # otherwise (if we get an error), we are NOT inside JEM 

    pass    # so, do nothing.


