################################################################################################################
# guicontrols.py        Version 1.11     17-Mar-2018      Bill Manaris, Marge Marshall, Seth Stoudenmier, and Robert Ziehr
#

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

# This is a library of additional GUI widgets for receiving user input, geared mainly towards audio applications.
# It provides horizontal and vertical sliders, an XY pad, toggle (on/off) and push (on-while-pressing-only) buttons,
# and a rotary dial.  For each of these you control various color options, of course the funtionality that the slider
# is connected to, and the range of values (when it makes sense).

#####################
#
# REVISIONS:
#
#   1.11    17-Mar-2018 (bm, mm) Updated xyPad to remove a couple of drawing bugs and improve its customizability.
#
#   1.10    22-Feb-2017 (bm, mm) Updated Push, Toggle drawing to remove a bug.
#
#   1.9     25-Jan-2017 (bm) Updated Rotary drawing to remove a blemish (drawing inaccuracy) in the outline.
#
#   1.8     17-Jan-2017 (bm) Updated how HFader, YFader, Rotary, and XYPad capture x,y coordinates, 
#                       given gui.py's version 3.5 change to translate / remap mouse event coordinates
#                       (now,when a mouse event occurs with a GUI object's JPanel, the global (enclosing Display)
#                       coordinates are communicated (instead of the internal JPanel coordinates).  This gui.py
#                       change broke the above controls.  Now, they have been updated to work right.
#
#   1.7     25-Nov-2014 (bm) Updated documentation.
#
#   1.6     29-Oct-2014 (ss) Cleaned-up code.
#
#   1.5     23-Oct-2014 (ss, bm) Updated all controls to use external values (min and max) and cleaned up code.
#
#   1.4     07-Sep-2014 (bm) Updated Rotary control to use 'arcWidth'.  Updated HFader to use external
#                       values (min and max) and cleaned up code.  Updated setPosition() and introduced
#                       trackerWidth within XYPad.  Cleaned-up code.
#
#   1.3     28-Aug-2014 (ss, bm) Changed name to 'guicontrols.py'.
#
#   1.2     21-Dec-2013 (ss) Replaced need to specify orientation with sliders and renamed to VFader and HFader.
#                            Introduced Toggle, XYPad, and Push.
#
#   1.1     18-Oct-2013 (bm) Introduced HORIZONTAL orientation
#
#   1.0     02-Dec-2013 (bm, rz) Original implementation
#
#
# TO-DO:
#
#


##
#
# HFader
#
#   A horizontal fader specified by two diagonal corners, it min and max values, the function to call when the user interacts with it,
#   its various colors (background, foreground, and outline), and its outline thickness.
#
#   For example,
#
#   h = HFader(x1=50, y1=50, x2=300, y2=100, minValue=0, maxValue=999, startValue=350, updateFunction=printValue, foreground=Color.RED, background=Color.BLACK, outline=Color.BLUE)
#
##
#
# VFader
#
#   A vertical fader specified by two diagonal corners, min and max values, a start value, a function to call when the user 
#   interacts with it, its various colors (background, foreground, and outline), and its outline thickness.
#
#   For example,
#
#   v = VFader(x1=100, y1=200, x2=175, y2=350, minValue=0, maxValue=999, startValue=350, updateFunction=printValue, foreground=Color.RED, background=Color.BLACK, outline=Color.BLUE)
#
##
#
# Rotary
#
#   A rotary is is oriented vertically (with 0 and max at bottom).  It is specified by two diagonal corners, 
#   a min and max values, the function to call when the user interacts with it,
#   its various colors (background, foreground, and outline), its outline thickness, and the arc width 
#   (how wide the rotary is visually - a reasonable value is 300 degrees).
#
#   For example,
#
#   r = Rotary(x1=400, y1=250, x2=500, y2=350, minValue=0, maxValue=999, startValue=350, updateFunction=printValue, foreground=Color.RED, background=Color.BLACK, outline=Color.BLUE, thickness=3, arcWidth=300)
#
##
#
# Toggle
#
#   A rectangle toggle switch specified by two diagonal corners, a function to call when the user 
#   interacts with it, its various colors (background, foreground, and outline), and its outline thickness.
#
#   For example,
#
#   t = Toggle(x1=200, y1=200, x2=250, y2=250, startState=False, updateFunction=printToggle, foreground=Color.BLUE, background=Color.WHITE, outline=Color.YELLOW)
# 
##
#
# Push
#
#   A rectangle push-and-hold button specified by two diagonal corners, a function to call when the user 
#   interacts with it, its various colors (background, foreground, and outline), and its outline thickness.
#
#   For example,
#
#   p = Push(x1=50, y1=400, x2=100, y2=450, updateFunction=printToggle, foreground=Color.BLUE, background=Color.RED)  
#
##
#
# XYPad
#
#   An XY-pad specified by two diagonal corners, a function to call when the user 
#   interacts with it, its various colors (background, foreground, and outline), and its outline thickness.
#
#   For example,
#
#   xy = XYPad(x1=400, y1=50, x2=700, y2=200, updateFunction=printPosition, foreground=Color.BLACK, background=Color.WHITE)
#
#

from gui import *

class HFader(Rectangle):
   """
   A horizontal fader specified by two diagonal corners, it min and max values, the function to call when the user interacts with it,
   its various colors (background, foreground, and outline), and its outline thickness.
   """

   def __init__(self, x1, y1, x2, y2, minValue=0, maxValue=999, startValue=None, updateFunction=None,
                foreground=Color.RED, background=Color.BLACK, outline=Color.BLACK,
                thickness=3):
      """
      Create a new horizontal fader
      """

      # ensure min and max values (which define the external range) are fine, and complain if not
      if not (minValue < maxValue):
         raise ValueError("Min value, " + str(minValue) + ", must be less than or equal to max value, " + str(maxValue) + ".")

      if startValue !=None and not (minValue <= startValue <= maxValue):
         raise ValueError("Start value, " + str(startValue) + ", must be between min and max value.")

      # initialize Rectangle data and behavior
      Rectangle.__init__(self, x1, y1, x2, y2, outline, False, thickness)

      # remember the fader's top-left x coordinate
      self.topLeftXCoordinate = min(x1, x2)

      # remember the fader's range in the external world
      self.minValue = minValue
      self.maxValue = maxValue

      # initialize slider start value
      if startValue == None:
         startValue = (minValue + maxValue)/2    # start in the middle

      # remember callback function
      self.eventHandler = updateFunction

      # remember various colors
      self.foreground = foreground
      self.background = background
      self.outline = outline

      # remember thickness
      self.thickness = thickness

      # create internal fader value (holds internal range, which depends on GUI x, y coordinates)
      self.faderValue = 0

      # set fader's initial value
      self.setValue(startValue)

      # register callback function to update fader view
      self.onMouseDown( self.__updateFader__ )
      self.onMouseDrag( self.__updateFader__ )


   def getValue(self):
      """Returns the current value of the fader."""

      # map the fader value from the internal range to the external world range
      externalValue = mapValue(self.faderValue, 0, self.endX_JPanel, self.minValue, self.maxValue)

      return externalValue


   def setValue(self, externalValue):
      """Sets the current value of the fader to 'externalValue' - 'externalValue' is in external world coordinates."""

      # ensure value is within the external range, and complain if not
      if not (self.minValue <= externalValue <= self.maxValue):
         raise ValueError("New Value, " + str(externalValue) + ", is outside expected range (" + str(self.minValue) + " to " + str(self.maxValue) + ").")

      # map value from the external coordinates to the internal ones (actual range of the
      # fader on the display)
      internalValue = mapValue(externalValue, self.minValue, self.maxValue, 0, self.endX_JPanel)

      # and set fader value
      self.faderValue = internalValue

      # if we have (been assigned to) a display, let's repaint ourselves to update the changed fader fill
      if self.display != None:
         self.display.contentPane.repaint()

      # also call event handler (if any) with the new value in external world coordinates - very important!
      if self.eventHandler != None:
         self.eventHandler( externalValue )


   def __updateFader__(self, x, y):
      """Callback function for adjusting the fader via mouse movement (over the fader)."""

      # update the fader value
      #newValue = x                               # store new fader value
      newValue = x - self.topLeftXCoordinate          # store new fader value
      newValue = max(newValue, 0)                # ensure we get no negative values (if mouse drags left of fader)
      newValue = min(newValue, self.endX_JPanel) # ensure we stay within max value (if mouse drags right of fader)

      # next, we set the fader value using setValue() which expects external coordinates

      # convert to external world coordinates (expected by setValue())
      externalValue = mapValue(newValue, 0, self.endX_JPanel, self.minValue, self.maxValue)

      # now, set the fader value
      self.setValue( externalValue )


   def paint(self, graphics2DContext):
      """
      Paint me on the display.  A rectangle fader consists of three rectangles, the background rectangle,
      the volume-fill rectangle, and the outline rectangle.  These are drawn in this order to create the
      visual effect of a unified control.
      """

      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)

      # set rounded ends
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )

      # draw background rectangle
      graphics2DContext.setPaint(self.background)
      graphics2DContext.fillRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel+1) # +1 to fix blemish at the bottom

      # draw volume-filled rectangle
      graphics2DContext.setPaint(self.foreground)
      graphics2DContext.fillRect(self.startX_JPanel, self.startY_JPanel, self.faderValue, self.endY_JPanel)

      # draw outline rectangle
      graphics2DContext.setPaint(self.outline)
      graphics2DContext.drawRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel+1) # +1 to fix blemish at the bottom

      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation


class VFader(Rectangle):
   """
   A vertical fader specified by two diagonal corners, min and max values, a start value, a function to call when the user
   interacts with it, its various colors (background, foreground, and outline), and its outline thickness.
   """

   def __init__(self, x1, y1, x2, y2, minValue=0, maxValue=999, startValue=None, updateFunction=None, foreground=Color.RED,
   background=Color.BLACK, outline=Color.BLACK, thickness=3):
      """
      Create a new rectangle fader
      """

      # ensure min and max values (which define the external range) are fine, and complain if not
      if not (minValue < maxValue):
         raise ValueError("Min value, " + str(minValue) + ", must be less than or equal to max value, " + str(maxValue) + ".")

      if startValue != None and not (minValue <= startValue <= maxValue):
         raise ValueError("Start value, " + str(startValue) + ", must be between min and max value.")

      # initialize Rectangle data and behavior
      Rectangle.__init__(self, x1, y1, x2, y2, outline, False, thickness)

      # remember the fader's top-left y coordinate
      self.topLeftYCoordinate = min(y1, y2)

      # remember the fader's range in the external world
      self.minValue = minValue
      self.maxValue = maxValue

      # initialize the slider start value
      if startValue == None:
         startValue = (minValue + maxValue)/2   # start in the middle

      # remember callback function
      self.eventHandler = updateFunction

      # remember various colors
      self.foreground = foreground
      self.background = background
      self.outline = outline

      # remember thickness
      self.thickness = thickness

      # create initial fader value (holds internal range, which depends on GUI x, y coordinates)
      self.faderValue = 0

      # set fader's initial value
      self.setValue(startValue)

      # register callback function to update fader view
      self.onMouseDown( self.__updateFader__ )
      self.onMouseDrag( self.__updateFader__ )


   def getValue(self):
      """Returns the current value of the fader."""

      # map the fader value from the internal range to the external world range
      externalValue = mapValue(self.faderValue, 0, self.endY_JPanel, self.minValue, self.maxValue)
      return externalValue


   def setValue(self, externalValue):
      """Sets the current value of the fader to 'externalValue' - 'externalValue' is in external world coordinates."""

      # ensure value is within the external range, and complain if not
      if not (self.minValue <= externalValue <= self.maxValue):
         raise ValueError("New Value, " + str(externalValue) + ", is outside expected range (" + str(self.minValue) + " to " + str(self.maxValue) + ").")

      # map value from the external coordinates to the internal ones (actual range of the
      # fader on the display)
      internalValue = mapValue(externalValue, self.minValue, self.maxValue, 0, self.endY_JPanel)

      # and set fader value
      self.faderValue = internalValue

      # if we have (been assigned to) a display, let's repaint ourselves to update the changed fader fill
      if self.display != None:
         self.display.contentPane.repaint()

      # also call event handler (if any) with the new value in external world coordinates - very important!
      if self.eventHandler != None:
         self.eventHandler( externalValue )


   def __updateFader__(self, x, y):
      """Callback function for adjusting the fader via mouse movement (over the fader)."""

      # update the fader value
      #newValue = self.endY_JPanel - y            # store new fader value
      newValue = self.endY_JPanel - y + self.topLeftYCoordinate            # store new fader value

      newValue = max(newValue, 0)                # ensure we get no negative values (if mouse drags left of fader)
      newValue = min(newValue, self.endY_JPanel) # ensure we stay within max value (if mouse drags right of fader)

      # next, we set the fader value using setValue() which expects external coordinates

      # convert to external world coordinates (expected by setValue())
      externalValue = mapValue(newValue, 0, self.endY_JPanel, self.minValue, self.maxValue)

      # now, set the fader value
      self.setValue( externalValue )


   def paint(self, graphics2DContext):
      """
      Paint me on the display.  A rectangle fader consists of three rectangles, the background rectangle,
      the volume-fill rectangle, and the outline rectangle.  These are drawn in this order to create the
      visual effect of a unified control.
      """

      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)

      # set rounded ends
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )

      # draw background rectangle
      graphics2DContext.setPaint(self.background)
      graphics2DContext.fillRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel+1) # +1 to fix blemish at the bottom

      # draw volume-filled rectangle
      graphics2DContext.setPaint(self.foreground)
      graphics2DContext.fillRect(self.startX_JPanel, (self.endY_JPanel-self.startY_JPanel)-self.faderValue+self.thickness, self.endX_JPanel, self.endY_JPanel)

      # draw outline rectangle
      graphics2DContext.setPaint(self.outline)
      graphics2DContext.drawRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel+1) # +1 to fix blemish at the bottom

      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation


class Rotary(Arc):
   """
   A rotary is is oriented vertically (with 0 and max at bottom).  It is specified by two diagonal corners,
   a min and max values, the function to call when the user interacts with it,
   its various colors (background, foreground, and outline), its outline thickness, and the arc width
   (how wide the rotary is visually - a reasonable value is 300 degrees).
   """

   def __init__(self, x1, y1, x2, y2, minValue=0, maxValue=999, startValue=None, updateFunction=None,
                foreground=Color.RED, background=Color.BLACK, outline=Color.BLUE,
                thickness=3, arcWidth=300):
      """
      Create a new rotary.
      """

      # ensure min and max values (which define the external range) are fine, and complain if not
      if not (minValue < maxValue):
         raise ValueError("Min value, " + str(minValue) + ", must be less than or equal to max value, " + str(maxValue) + ".")

      if startValue != None and not (minValue <= startValue <= maxValue):
         raise ValueError("Start value, " + str(startValue) + ", must be between min and max value.")

      # NOTE: The startAngle specifies how wide the rotary's area/shape (arc covered by it) is.
      #       The larger the angle, the wider the rotary's arc.  However, since this angle is
      #       symmetrical with the endAngle, it can span only between 90 and 270.

      # rotary cannot overlap with itself or be non-existent, so ensure start angle is meaningful
      if not (0 <= arcWidth <= 360):      # out of range?
         raise ValueError("Rotary start angle, " + str(startAngle) + ", is outside expected range (0 to 360).")

      # NOTE: In Java (and in what follows) arc angles are interpreted such that 0 degrees
      #       is at the 3 o'clock position. A positive value indicates a counter-clockwise rotation,
      #       while a negative value indicates a clockwise rotation.

      # initialize rotary's internal angles
      self.startAngle = 270 - (360 - arcWidth)/2   # 0 is at 3 o'clock (e.g., 240 is approx. at 7 o'clock)
      self.endAngle   = 180 - self.startAngle      # symmetrical to startAngle (e.g., approx. at 5 o'clock)

      # initialize Arc data and behavior
      # Arc(x1, y1, x2, y2, startAngle, endAngle, color, fill, thickness)
      Arc.__init__(self, x1, y1, x2, y2, self.startAngle, self.endAngle, outline, False, thickness)

      # remember the rotary's top-left x, y coordinates
      self.topLeftXCoordinate = min(x1, x2)
      self.topLeftYCoordinate = min(y1, y2)

      # remember the rotary's range in the external world
      self.minValue = minValue
      self.maxValue = maxValue

      # initialize rotary start value
      if startValue == None:
         startValue = (minValue + maxValue)/2

      # remember callback function
      self.eventHandler = updateFunction

      # remember various colors
      self.foreground = foreground
      self.background = background
      self.outline = outline

      # remember thickness
      self.thickness = thickness

      # end angle in rotary units (continuous from 0 to some angle <= 360)
      self.relativeEndAngle = abs(self.endAngle - self.startAngle)    # same as 'arcWidth'

      # calculate center of rotary control
      self.originX = self.endX_JPanel / 2
      self.originY = self.endY_JPanel / 2

      # create initial rotary angle; set to 0 so it starts on self.startAngle
      self.rotaryAngle = 0

      # set rotary's initial value
      self.setValue(startValue)

      # register callback function to update rotary view
      self.onMouseDown( self.__updateRotary__ )
      self.onMouseDrag( self.__updateRotary__ )


   def getValue(self):
      """Returns the current value of the rotary."""

      # map the rotary value from the internal range to the external world range
      externalValue = mapValue(self.rotaryAngle, 0, self.relativeEndAngle, self.minValue, self.maxValue)
      return externalValue


   def setValue(self, externalValue):
      """Sets the current value of the rotary."""

      # ensure value is within the external range and complain if not
      if not (self.minValue <= externalValue <= self.maxValue):
         raise ValueError("New value, " + str(externalValue) + ", is outside expected range (" + str(self.minValue) + "to " + str(self.maxValue) + ").")

      # map value from the external coordinates to the internal ones (actual range of the
      # rotary on the display)
      internalValue = mapValue(externalValue, self.minValue, self.maxValue, 0, self.relativeEndAngle)

      # update rotary value (0 to max rotary value) - ignore otherwise
      if 0 <= internalValue <= self.relativeEndAngle:
         self.rotaryAngle = internalValue

      # if we have (been assigned to) a display, let's repaint ourselves to update the changed fader fill
      if self.display != None:
         self.display.contentPane.repaint()

      # also call event handler (if any) - very important!
      if self.eventHandler != None:
         self.eventHandler( externalValue )


   def __updateRotary__(self, x, y):
      """Callback function for adjusting the rotary via mouse movement (over the rotary)."""

      # convert mouse click point to rotary angle (in radians)
      newX = x - self.topLeftXCoordinate          # store new fader value
      newY = self.endY_JPanel - y + self.topLeftYCoordinate            # store new fader value

      #newValue = atan2(y - self.originY, self.originX - x)
      #newValue = atan2(newY - self.originY, self.originX - newX)
      newValue = atan2(self.originY - newY, self.originX - newX)
      newValue = degrees( newValue ) # convert to degrees (+180 gets values in range 0-360)

      # now, let's convert from atan2 coordinates (which are -0 to -180 for 9 o'clock to 3 o'clock - top quadrants,
      # and 0 to 180 for 9 o'clock to 3 o'clock - bottom quadrants)...
      # to rotary coordinates with 0 at 6 o'clock working clockwise to 360, again, at 6 o'clock.
      # (The following is a little ugly, but does the job well.)
      if 0 >= newValue > -180:      # top quadrants between 9 o'clock and 3 o'clock?
         newValue = mapValue(newValue, -180, 0, 270, 90)
      elif 0 < newValue <= 90:     # bottom quadrant between 9 o'clock and 6 o'clock?
         newValue = mapValue(newValue, 0, 90, 90, 0)
      elif 90 < newValue <= 180:    # bottom quadrant between 6 o'clock and 3 o'clock?
         newValue = mapValue(newValue, 90, 180, 360, 270)
      else:
         raise ValueError("Value, " + str(newValue) + ", is outside expected range.")

      # now, let's adjust for rotary coordinates (assumes that rotary is oriented vertically -
      # with 0 and max at bottom)
      newValue = newValue - (360 - self.startAngle + self.endAngle)/2 + self.thickness

      # check if user clicked within active rotary area (if so update rotary, else do nothing)
      if 0 <= newValue <= self.relativeEndAngle:

         # convert to external world coordinates (expected by setValue())
         externalValue = mapValue(newValue, 0, self.relativeEndAngle, self.minValue, self.maxValue)

         # now, set the rotary value
         self.setValue( externalValue )


   def paint(self, graphics2DContext):
      """
      Paint me on the display.  A rotary consists of three arcs, the background arc,
      the volume-fill arc, and the outline arc.  These are drawn in this order to create the
      visual effect of a unified control.
      """

      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)

      # set rounded ends
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )

      # draw background arc
      graphics2DContext.setPaint(self.background)
      #graphics2DContext.fillArc(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel, self.startAngle+self.thickness, -self.relativeEndAngle-self.thickness)
      graphics2DContext.fillArc(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel, self.startAngle, self.endAngle-self.startAngle-self.thickness)

      # draw volume-filled arc
      graphics2DContext.setPaint(self.foreground)
      graphics2DContext.fillArc(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel, self.startAngle, -int(self.rotaryAngle))

      # draw outline arc
      graphics2DContext.setPaint(self.outline)
      graphics2DContext.drawArc(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel, self.startAngle, self.endAngle-self.startAngle-self.thickness/2)

      # draw two lines to complete outline
      graphics2DContext.setPaint(self.outline)

      # This involves some trigonometry (in order to keep everything relative to self.startAngle)

      # first, calculate startAngle's arc distance from vertical axis (in radians)
      # (NOTE: This is expensive to do it in here, as this calculation is repeated with *every* update.
      #        However, it is ugly to do it elsewhere.)
      angleFromVertical = radians(270-self.startAngle)

      # draw line to the left of vertical axis
      #graphics2DContext.drawLine(int(self.endX_JPanel/2*(1-sin(-angleFromVertical))), int(self.endY_JPanel/2*(1+cos(-angleFromVertical))), self.originX, self.originY)
      graphics2DContext.drawLine(int(self.endX_JPanel/2*(1-sin(-angleFromVertical)))-self.thickness/2, int(self.endY_JPanel/2*(1+cos(-angleFromVertical)))+self.thickness/2, self.originX, self.originY)

      # draw line to the right of vertical axis
      #graphics2DContext.drawLine(int(self.endX_JPanel/2*(1-sin(angleFromVertical))), int(self.endY_JPanel/2*(1+cos(angleFromVertical))), self.originX, self.originY)
      graphics2DContext.drawLine(int(self.endX_JPanel/2*(1-sin(angleFromVertical)))+self.thickness/2, int(self.endY_JPanel/2*(1+cos(angleFromVertical)))+self.thickness/2, self.originX, self.originY)

      # draw inside arc (circle)
      #graphics2DContext.setPaint(self.outline)
      #graphics2DContext.fillArc(self.endX_JPanel * 5/16, self.endY_JPanel * 6/16, self.endX_JPanel * 3/8, self.endY_JPanel * 3/8, 0, 360)

      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation



class Toggle(Rectangle):
   """
   A rectangle toggle switch specified by two diagonal corners, a function to call when the user
   interacts with it, its various colors (background, foreground, and outline), and its outline thickness.
   """

   def __init__(self, x1, y1, x2, y2, startState=False, updateFunction=None, foreground=Color.RED, background=Color.BLACK, outline=None, thickness=3):
      """
      Create a new rectangle toggle.
      """

      # initialize Rectangle data and behavior
      Rectangle.__init__(self, x1, y1, x2, y2, outline, False, thickness)

      # remember callback function
      self.eventHandler = updateFunction

      # remember state of the toggle
      self.state = startState

# *** Why is (below) this different from the others? ***

      # remember various colors
      self.foreground = foreground
      self.background = background
      if not outline:                      #Keeps the border and the center color the same unless told otherwise
         self.outline = foreground
      else:
         self.outline = outline

      # remember thickness
      self.thickness = thickness

      # register callback function to update toggle view
      self.onMouseClick( self.__updateToggle__ )


   def getValue(self):
      """Returns the current value of the toggle."""
      return self.state


   def setValue(self, newValue):
      """Sets the current value of the toggle."""

      # ensure value is allowed for the toggle switch
      if newValue != True and newValue != False:
         raise ValueError("Input of " + str(newValue) + " is not the required type of boolean.")

      # sets the value of the toggle to the opposite of its current state
      self.state = newValue

      # if we have (been assigned to) a display, let's repaint ourselves to update the changed fader fill
      if self.display != None:
         self.display.contentPane.repaint()

      # also call event handler (if any) - very important!
      if self.eventHandler != None:
         self.eventHandler( self.state )


   def __updateToggle__(self, x, y):
      """Callback function for adjusting the toggle."""

      # updates toggle to the opposite of its current state
      newValue = not self.state

      # now, set the toggle value
      self.setValue( newValue )


   def paint(self, graphics2DContext):
      """
      Paint me on the display.  A rectangle toggle consists of three rectangles, the background rectangle,
      the inner (toggle portion) rectangle, and the outline rectangle.  These are drawn in this order to create the
      visual effect of a unified control.
      """

      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)

      # set rounded ends
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )

      # draw background rectangle
      graphics2DContext.setPaint(self.background)
      graphics2DContext.fillRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel)

      # draws/removes inner rectangle
      if self.state:
         graphics2DContext.setPaint(self.foreground)
         graphics2DContext.fillRect(self.startX_JPanel+self.thickness, self.startY_JPanel+self.thickness, self.endX_JPanel-self.thickness*2+1, self.endY_JPanel-self.thickness*2+1)
      else:
         graphics2DContext.setPaint(None)

      # draw outline rectangle
      graphics2DContext.setPaint(self.outline)
      graphics2DContext.drawRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel)

      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation



class Push(Rectangle):
   """
   A rectangle push-and-hold button specified by two diagonal corners, a function to call when the user
   interacts with it, its various colors (background, foreground, and outline), and its outline thickness.
   """

   def __init__(self, x1, y1, x2, y2, updateFunction = None, foreground = Color.RED, background = Color.BLACK, outline = None, thickness=3):
      """
      Create a new push button
      """

      # initialize Rectangle data and behavior
      Rectangle.__init__(self, x1, y1, x2, y2, outline, False, thickness)

      # remember callback function
      self.eventHandler = updateFunction

      # initialize state of push button
      self.state = False

# *** Why is this (below) different form the others?  Which way is best? ***

      # remember various colors
      self.foreground = foreground
      self.background = background
      if not outline:                      #Keeps the border and the center color the same unless told otherwise
         self.outline = foreground
      else:
         self.outline = outline

      # remember thickness
      self.thickness = thickness

      # register callback function to update push view
      self.onMouseDown( self.__updatePush__ )
      self.onMouseUp( self.__updatePush__ )


   def getValue(self):
      """Returns the current value of the push button."""
      return self.state


   def setValue(self, newValue):
      """Sets the current value of the push button."""

      # ensure value is allowed for the toggle switch
      if newValue != True and newValue != False:
         raise ValueError("Input of " + str(newValue) + " is not the required type of boolean.")

      # sets the value of the push button to the opposite of its current state
      self.state = newValue

      # if we have (been assigned to) a display, let's repaint ourselves to update the changed fader fill
      if self.display != None:
         self.display.contentPane.repaint()

      # also call event handler (if any) - very important!
      if self.eventHandler != None:
         self.eventHandler( self.state )


   def __updatePush__(self, x, y):
      """Callback function for adjusting the push button."""

      # updates push button to the opposite of its current state
      newValue = not self.state

      # now, set the push button value
      self.setValue( newValue )


   def paint(self, graphics2DContext):
      """
      Paint me on the display.  A rectangle push button consists of three rectangles, the background rectangle,
      the inner rectangle, and the outline rectangle.  These are drawn in this order to create the
      visual effect of a unified control.
      """

      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)

      # set rounded ends
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )

      # draw background rectangle
      graphics2DContext.setPaint(self.background)
      graphics2DContext.fillRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel)

      # draws/removes inner rectangle
      if self.state:
         graphics2DContext.setPaint(self.foreground)
         graphics2DContext.fillRect(self.startX_JPanel+self.thickness, self.startY_JPanel+self.thickness, self.endX_JPanel-self.thickness*2+1, self.endY_JPanel-self.thickness*2+1)
      else:
         graphics2DContext.setPaint(None)

      # draw outline rectangle
      graphics2DContext.setPaint(self.outline)
      graphics2DContext.drawRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel)

      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation



class XYPad(Rectangle):
   """
   An XY-pad specified by two diagonal corners, a function to call when the user
   interacts with it, its various colors (background, foreground, and outline), its outline thickness, and tracker radius.
   """

   def __init__(self, x1, y1, x2, y2, updateFunction = None, foreground = Color.RED, background = Color.BLACK, 
                outline = None, outlineThickness = 2, trackerRadius=10, crosshairsThickness = None):
      """
      Create a new xy pad
      """

      # initialize Rectangle data and behavior
      Rectangle.__init__(self, x1, y1, x2, y2, foreground, False, outlineThickness)

      # tracker width
      self.trackerRadius = trackerRadius

      # remember callback function
      self.eventHandler = updateFunction

      # remember the XYPad's top-left x, y coordinates
      self.topLeftXCoordinate = min(x1, x2)
      self.topLeftYCoordinate = min(y1, y2)

      # remember the position of the tracker
      self.xPos = 0
      self.yPos = 0

      # remember various colors and thickness
      self.foreground = foreground
      self.background = background
      if not outline:                      # keep border and center color same unless told otherwise
         self.outline = foreground
      else:
         self.outline = outline

      # remember thickness
      self.outlineThickness = outlineThickness

      if not crosshairsThickness:           # keep crosshairs and outline thickness same unless told otherwise
         self.crosshairsThickness = outlineThickness
      else:
         self.crosshairsThickness = crosshairsThickness


      # register callback function to update XYPad view
      self.onMouseDown( self.__updateXYPad__ )
      self.onMouseDrag( self.__updateXYPad__ )


   def getPosition(self):
      """Return the x and y coordinate of the XY Pad."""
      return self.xPos, self.yPos


   def setPosition(self, newX, newY):
      """Sets the current position of the XY pad."""

      # ensure values stay within the XY Pad
      newX = max(newX, 0)
      newX = min(newX, self.endX_JPanel)

      newY = max(newY, 0)
      newY = min(newY, self.endY_JPanel)

      # update tracker position
      self.xPos = newX
      self.yPos = newY

      # if we have (been assigned to) a display, let's repaint ourselves to update the changed fader fill
      if self.display != None:
         self.display.contentPane.repaint()

      # also call event handler (if any) - very important!
      if self.eventHandler != None:
         self.eventHandler( self.xPos, self.yPos )


   def __updateXYPad__(self, x, y):
      """Callback function for adjusting the XY Pd."""

      # updates values for position of XY Pad tracker
      #newX = x
      #newY = y
      newX = x - self.topLeftXCoordinate   # store new fader value
      newY = y - self.topLeftYCoordinate   # store new fader value

      # now, set the toggle switch value
      self.setPosition( newX, newY )


   def paint(self, graphics2DContext):
      """
      Paint me on the display.  An XY Pad consists of five parts. The background rectangle, the outline rectangle, the small rectangle tracker, and the two crossing lines. These are drawn in this order to create the visual effect of a unified control.
      """

      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)

      # set outline thickness and rounded ends
      graphics2DContext.setStroke( BasicStroke(self.outlineThickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )

      # draw background rectangle
      graphics2DContext.setPaint(self.background)
      graphics2DContext.fillRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel+1) # +1 to fix blemish at the bottom

      # draws small center circle (tracker)
      graphics2DContext.setPaint(self.foreground)
      graphics2DContext.fillOval(self.xPos-self.trackerRadius/2, self.yPos-self.trackerRadius/2, self.trackerRadius, self.trackerRadius+1)

      # draw outline rectangle
      graphics2DContext.setPaint(self.outline)
      graphics2DContext.drawRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel+1) # +1 to fix blemish at the bottom

      # set crosshairs thickness and rounded ends
      graphics2DContext.setStroke( BasicStroke(self.crosshairsThickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )

      # draws the crosshairs lines
      graphics2DContext.setPaint(self.foreground)
      if self.crosshairsThickness > 0:
         graphics2DContext.drawLine(self.startX_JPanel, self.yPos+1, self.endX_JPanel, self.yPos+1)  # horizontal line
         graphics2DContext.drawLine(self.xPos, self.startY_JPanel+1, self.xPos, self.endY_JPanel+1)  # vertical line

      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation




###### Unit Tests ###################################

if __name__ == "__main__":

   # let's create a display and place some things on it.
   d = Display("", 800, 500)

   # Prints the value of the sliders as they move
   def printValue( value ):
      print value

   # Testing the boolean values of toggle switch
   def printToggle( value ):
      if value:
         print "Yes"
      elif not value:
         print "No"
      else:
         print "Impossible!"

   def printPosition( x, y):
      print "(" + str(x) + ", " + str(y) + ")"

   # Creating and initializing the horizontal slider
   h = HFader(x1=50, y1=50, x2=300, y2=100, minValue=0, maxValue=999, startValue=350, updateFunction=printValue, foreground=Color.RED, background=Color.BLACK, outline=Color.BLUE)
   d.add(h)

   # Creating and initializing the vertical slider
   v = VFader(x1=100, y1=200, x2=175, y2=350, minValue=0, maxValue=999, startValue=350, updateFunction=printValue, foreground=Color.RED, background=Color.BLACK, outline=Color.BLUE)
   d.add(v)

   # Creating and initializing the toggle switch
   t1 = Toggle(x1=300, y1=300, x2=375, y2=375, startState=True, updateFunction=printToggle)
   d.add(t1)

   # Creating and initializing the toggle switch with specified colors
   t2 = Toggle(x1=200, y1=200, x2=250, y2=250, startState=False, updateFunction=printToggle, foreground=Color.BLUE, background=Color.WHITE, outline=Color.YELLOW, thickness = 5)
   d.add(t2)

   xy = XYPad(x1=400, y1=50, x2=700, y2=200, updateFunction=printPosition, foreground=Color.BLACK, background=Color.WHITE)
   d.add(xy)

   p = Push(x1=50, y1=400, x2=100, y2=450, updateFunction=printToggle, foreground=Color.BLUE, background=Color.RED, thickness = 12)
   d.add(p)

   p2 = Push(x1=125, y1=400, x2=175, y2=450, updateFunction=printToggle, foreground=Color.GREEN, background=Color.BLUE)
   d.add(p2)

   r = Rotary(x1=400, y1=250, x2=500, y2=350, minValue=0, maxValue=999, startValue=350, updateFunction=printValue, foreground=Color.RED, background=Color.BLACK, outline=Color.BLUE, thickness=3,
   arcWidth=300)
   d.add(r)
