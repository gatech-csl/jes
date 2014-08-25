# randomCircles.py
#
# Demonstrates how to draw random circles on a GUI display.
#

from gui import *
from random import *    

numberOfCircles = 1000    # how many circles to draw     

# create display
d = Display("Random Circles", 600, 400)     

# draw various filled circles with random position, radius, color
for i in range(numberOfCircles):

   # create a random circle, and place it on the display
   
   # get random position and radius
   x = randint(0, d.getWidth()-1)      # x may be anywhere on display
   y = randint(0, d.getHeight()-1)     # y may be anywhere on display
   radius = randint(1, 40)             # random radius (1-40 pixels)
   
   # get random color (RGB)
   red = randint(0, 255)               # random R (0-255)
   green = randint(0, 255)             # random G (0-255)
   blue = randint(0, 255)              # random B (0-255)
   color = Color(red, green, blue)     # build color from random RGB
   
   # create a filled circle from random values
   c = Circle(x, y, radius, color, True) 

   # finally, add circle to the display
   d.add(c)
   
# now, all circles have been added   
 