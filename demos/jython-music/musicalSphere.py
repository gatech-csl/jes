# revolvingSphere.py
#
# Demonstrates how to create an animation of a 3D sphere using regular points 
# on a Display.  The sphere is modeled using points on a spherical coordinate
# system (see http://en.wikipedia.org/wiki/Spherical_coordinate_system).
# It converts from spherical 3D coordinates to cartesian 2D coordinates (mapping
# the z axis to color).  When a point passes the primary meridian (the imaginary
# vertical line closest to the viewer), a note is played based on its latitude
# (low to high pitch).  Also the point turns red momentarily.

#
# Based on code by Uri Wilensky (1998), distributed with NetLogo
# under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License.

from gui import *
#from music import *
from music import *
from random import *
from math import *
from sliderControl import *  

class MusicalSphere:
   """Creates a revolving sphere that plays music."""
   
   def __init__(self, radius, density, velocity=0.01, frameRate=30):
      """
      Construct a revolving sphere with given 'radius', 'density'
      number of points (all on the surface), moving with 'velocity' angular 
      (theta / azimuthal) velocity, at 'frameRate' frames (or movements) per
      second.  Each point plays a note when crossing the zero meridian (the
      sphere's meridian (vertical line) closest to the viewer).
      """

      # musical parameters
      self.instrument = XYLOPHONE
      self.scale = PENTATONIC_SCALE
      self.lowPitch = C2
      self.highPitch = C7 
      self.noteDuration = 100    # milliseconds

#      # musical parameters (alternate)
      self.instrument = PIANO
      self.scale = MAJOR_SCALE
      self.lowPitch = C1
      self.highPitch = C6 
      self.noteDuration = 2000    # milliseconds (2 seconds)  

      Play.setInstrument(self.instrument, 0)   # set the instrument
      
      # visual parameters
      self.display = Display("3D Sphere", radius*3, radius*3)  # display to draw sphere
      self.display.setColor( Color.BLACK )  # set background color to black

      self.radius = radius       # how wide circle is      
      self.numPoints = density   # how many points to draw on sphere surface
      self.velocity = velocity   # how far it rotates per animation frame
      self.frameRate = frameRate # how many animation frames to do per second

      self.xCenter = self.display.getWidth() / 2   # to place circle at display's center
      self.yCenter = self.display.getHeight() / 2
      
      # sphere data structure (parallel lists)
      self.points      = []    # holds the points
      self.thetaValues = []    # holds the points' rotation (azimuthal angle)
      self.phiValues   = []    # holds the points' latitude (polar angle)
      
      # timer to drive animation
      delay = 1000 / frameRate   # convert from frame rate to timer delay (in milliseconds)
      self.timer = Timer(delay, self.movePoints)   # timer to schedule movement
      
      # control surface for animation frame rate
      xPosition = self.display.getWidth() / 3    # set initial position of display
      yPosition = self.display.getHeight() + 45
      self.control = SliderControl(title="Frame Rate", updateFunction=self.setFrameRate, 
                                   minValue=1, maxValue=120, startValue=self.frameRate, 
                                   x=xPosition, y=yPosition)

      # orange color gradient (used to display depth, the further away, the darker)
      black = [0, 0, 0]         # RGB values for black
      orange = [251, 147, 14]   # RGB values for orange
      white = [255, 255, 255]   # RGB values for white

      # create list of gradient colors from black to orange, and from orange to white
      # (a total of 25 colors)
      self.gradientColors = colorGradient(black, orange, 12) + colorGradient(orange, white, 12) + [white]  # remember to include the final color
      
      self.initSphere()      # create the circle

      self.start()           # and start rotating!
      
           
   def start(self):
      """Starts sphere animation."""
      self.timer.start()

   def stop(self):
      """Stops sphere animation."""
      self.timer.stop()

   def setFrameRate(self, frameRate=30):
      """Controls speed of sphere animation (by setting how many times per second to move points)."""

      delay = 1000 / frameRate   # convert from frame rate to delay between each update (in milliseconds)
      self.timer.setDelay(delay)

   def initSphere(self):
      """Generate a sphere of 'radius' out of points (placed on the surface of the sphere)."""
      
      for i in range(self.numPoints):     # create all the points
   
         # get random spherical coordinates for this point 
         r = self.radius                                  # all points are placed *on* the surface
         theta = mapValue( random(), 0.0, 1.0, 0.0, 2*pi) # random rotation (azimuthal angle)
         phi = mapValue( random(), 0.0, 1.0, 0.0, pi)     # random latitude (polar angle)
      
         # project from spherical to cartesian 3D coordinates (z is depth)
         x, y, z = self.sphericalToCartesian(r, phi, theta)  
            
         # convert depth (z) to color
         color = self.depthToColor(z, self.radius)      
      
         # create a point (with thickness 1) at these x, y coordinates 
         point = Point(x, y, color, 1)      
      
         # remember this point and its spherical coordinates (r equals self.radius for all points)
         # (append data for this point to the three parallel lists)
         self.points.append( point )      
         self.phiValues.append( phi )
         self.thetaValues.append( theta )

         # add this point to the display
         self.display.add( point )


   def sphericalToCartesian(self, r, phi, theta):
      """Convert spherical to cartesian coordinates."""   

      # adjust rotation so that theta is 0 at max z (i.e., closest to viewer)
      x = int( r * sin(phi) * cos(theta + pi/2) )   # horizontal axis (pixels are int)
      y = int( r * cos(phi) )                       # vertical axis
      z = int( r * sin(phi) * sin(theta + pi/2) )   # depth axis      

      # move sphere's center to display's center
      x = x + self.xCenter                 
      y = y + self.yCenter

      return x, y, z

   def depthToColor(self, depth, radius):
      """Map 'depth' to color using the 'gradientColors' RGB colors."""
   
      # create color based on position (points further away have less luminosity)
      colorIndex = mapValue(depth, -self.radius, self.radius, 0, len(self.gradientColors))  # map depth to color index
      colorRGB = self.gradientColors[colorIndex]                    # get corresponding RBG value
      color = Color(colorRGB[0], colorRGB[1], colorRGB[2])          # and create the color

      return color

   def movePoints(self):
      """Rotate points on y axis as specified by angular velocity."""
   
      for i in range(self.numPoints):
         point = self.points[i]                                   # get this point
         theta = (self.thetaValues[i] + self.velocity) % (2*pi)   # increment angle to simulate rotation
         phi = self.phiValues[i]                                  # get latitude (altitude)
 
         # convert from spherical to cartesian 3D coordinates
         x, y, z = self.sphericalToCartesian(self.radius, phi, theta)
         
         if self.thetaValues[i] > theta:   # did we just cross the primary meridian?
            color = Color.RED                  # yes, so sparkle for a split second
            pitch = mapScale(phi, 0, pi, self.lowPitch, self.highPitch, self.scale)  # phi is latitude
            dynamic = randint(0, 127)          # random dynamic
            Play.note(pitch, 0, self.noteDuration, dynamic)  # and play a note (based on latitude)
            
         else:   # we are not on the primary meridian, so
            # convert depth to color (points further away have less luminosity)
            color = self.depthToColor(z, self.radius)
      
         # adjust this point's position and color
         self.display.move(point, x, y)
         point.setColor(color)

         # now, remember this point's new theta coordinate
         self.thetaValues[i] = theta



#################################################
# create a display and a sphere

# create background display
#display = Display("3D Sphere", 600, 600)
#display.setColor( Color.BLACK )
#
## sphere dimension and density
#radius = display.getWidth()/3   # radius of rotating sphere

# create a sphere
#sphere = MusicalSphere(display, radius, density=radius*3, velocity=0.01, frameRate=30)
sphere = MusicalSphere(radius=200, density=200, velocity=0.01, frameRate=30)

