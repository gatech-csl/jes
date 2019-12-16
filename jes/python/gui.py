################################################################################################################
# gui.py        Version 3.6        20-Feb-2018     Bill Manaris, Dana Hughes, David Johnson, and Kenneth Hanson

###########################################################################
#
# This file is part of Jython Music.
#
# Copyright (C) 2014 Bill Manaris, Dana Hughes, David Johnson, and Kenneth Hanson
#
#    Jython Music is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
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
# This library is based on Java's Swing GUI library.  It can be used to build
# GUIs in jython.  The purpose of this library is to provide a cleaner, simpler,
# easier-to-use alternative to Swing.  The gui.py library keeps simple things simple,
# and makes complicated things possible.  
#
# This package imports the Swing Java packages, and provides functions
# for creating widgets and drawable objects.  Event handler functions are passed as parameters.
# The concept of Java classes and listeners are hidden from the end-user (GUI programmer).  
# Only event handling functions (callbacks) need to be defined.
#
# REVISIONS:
#
#   3.6     20-Feb-2018 (bm)  Added guicontrols (simply import them at end). 
#
#   3.5     26-Dec-2015 (bm)  Added setX(), getX(), setY(), getY() functions to every object.
#						Also, changed mouse events to translate / remap coordinates
#                       for JPanel components, so, when a mouse event occurs with a GUI object's 
#                       JPanel, the global (enclosing Display) coordinates are communicated (instead
#                       of the internal JPanel coordinates, which were returned up until now).  
#                       This translation / remapping makes things more natural for the end-user (programmer),
#                       as it allows them to always work using global (enclosing Display) coordinates.  
#
#   3.4     01-Dec-2015 (bm)  Added Icon functions, setHeight(), setWidth(), getPixel(), setPixel(),
#						getPixels(), and setPixels().  This is to introduce consistency with functions 
#						available in Image library (see image.py). 
#
#   3.3     16-Feb-2015 (bm)  Added Display.close() function.  This will call onClose() callback
#                       if provided. 
#
#   3.2     19-Nov-2014 (bm)  Fixed bug in Icon resizing.  Now, we resize to best fit provided 
#                       dimensions (as opposed to maintaining image proportions at all costs).
#                       Also fixed bug in cleaning up objects after JEM's stop button is pressed -
#                       if list of active objects already exists, we do not redefine it - thus, we 
#                       do not lose older objects, and can still clean them up.
#
#   3.1     06-Nov-2014 (bm)  Added functionality to properly close displays and clean-up GUI objects
#                       via JEM's Stop button - see registerStopFunction().
#
#   3.0     01-Nov-2014 (bm)  Fixed Point() and drawPoint() to display properly.
#
#   2.99    23-Oct-2014 (bm)  Added Display.getItems() which returns a list of items currently
#                       on the display.  Also, for convenience, modified colorGradient() to 
#                       also work with java.awt.Color parameters, in which case it returns 
#                       a list of java.awt.Color colors.
#
#   2.98    02-Oct-2014 (bm)  Updated Label() to be able to set/get foreground (text) color,
#                       and background color.  
#
#   2.97    28-Aug-2014 (bm)  Added Arc() graphics object and Display.drawArc() function.  
#                       An arc specified by two diagonal corners, the start angle, and the end angle.  
#                       Angles are interpreted such that 0 degrees is at the three o'clock position. 
#                       A positive value indicates a counter-clockwise rotation while 
#                       a negative value indicates a clockwise rotation.
#
#                       Also added antialiasing in the rendering of GUI objects.  Nice!
#
#   2.96    02-May-2014 (bm) Added fixWorkingDirForJEM() solution to work with new JEM editor by Tobias Kohn.
#
#   2.95    28-Jan-2014 (bm) Using the imgscalr Java library for resizing images.
#
#   2.94    22-Nov-2013 (dj)  Added Display.addOrder() function.  This adds layering 
#                       capabilities to the standard add method.  The object is added to the 
#                       display at the specified order. Layers are ordered from smallest to 
#                       largest where 0 is the closet to the front of the display.
#
#   2.93    02-Jun-2013 (bm) Adjusted Point() to be a circle with radius 0 (vs. 1).
#
#   2.92    29-May-2013 (bm) Added colorGradient().  Removed Timer() and put it in each own
#                       library module, timer.py, which is imported here.
#
#   2.91    01-May-2013 (bm) Added Icon.crop(x, y, width, height) to crop icons from point x, y
#                       up to the provided width and height.
#
#   2.9     17-Apr-2013 (bm) Changed Checkbox callback function to accept one parameter, i.e.,
#                       the state of the checkbox (True means checked, False means unchecked)
#
#   2.8     10-Apr-2013 (bm) Add +1 to JPanel size for lines, circles, etc.  Also, added 
#                       getPosition() for all widgets, which returns a widget's (x, y) position, and 
#                       setPosition(x, y) which the widget's position (and, if on a display, also
#                       repositions the widget).  Also added display setPosition() and getPosition().  
#                       Added initial x and y position coordinates in Display constructor. 
#                       Finally, added Icon.rotate() - this however may crop rotated images.
#
#   2.7     07-Apr-2013 (bm) Various fixes, including making graphics object JPanels exactly the size
#                       of the graphics object (as opposed +1).  Also added, Display.setSize(), and
#                       Icon.getWidth() and getHeight(), which report the rigth size (as opposed to +1).
#
#   2.6     29-Mar-2013 (bm) callback functions for keyDown/keyUp are given the key code (e.g., VK_A
#                       or KeyEvent.VK_A).  Also added Display.removeAll() for quick clean up of display objects.
#                       Also added Widget.encloses() and Widget.intersects() for collision detection.
#                       Added unit test for animation (i.e., game engine example).
#
#   2.5     19-Mar-2013 (bm) Added a Timer class to schedule repeated tasks to be executed, without
#                       using sleep().  (The latter causes the Swing GUI event loop to sleep, locking
#                       up the GUI.)
#
#   2.4     12-Mar-2013 (bm) After a Widget (e.g., button) event is handled, focus is returned to 
#                       the parent display, so that more events (especially keyboard events) can be handled.
#
#   2.3     02-Mar-2013 (bm) Added thickness parameter in all graphics objects.  Also
#                       added Polygon() class.  Added several Display.draw functions
#                       for convenience, i.e., drawLine(), drawCircle(), drawPoint(), drawOval(),
#                       drawRectangle(), drawPolygon(), drawImage(), and drawLabel().  With these
#                       additions it takes one function call to create graphics objects,
#                       including labels (if needed, these functions return the created object,
#                       so that it may be moved, or deleted).  The drawLabel() function also
#                       takes color and font as parameters.  Finally, added Display.setColor()
#                       and getColor() to access the display's background color (if the setColor()
#                       is called without a parameter, a color selection widget opens up to
#                       pick a color - very convenient.
#
#                       Also, removed set/getThickness(), set/getFill() for drawable
#                       graphics objects - user can always create another object to change these.
#
#   2.2     27-Feb-2013 (bm) Added Display helper functions to show/hide display coordinates
#                       at mouse cursor (useful to discover coordinates of where to widgets 
#                       when building a GUI).  They are Display.showMouseCoordinates(), and
#                       Display.hideMouseCoordinates().
#
#   2.1     15-Feb-2013 (bm) Added Oval(); also Display.add(), move(), and delete().
#                       Removed thickness from Drawable, as it is very hard to impelement correctly
#                       (i.e., without cropping) given our inversion of the y-axis (i.e., having
#                       orgigin (0,0) at bottom, as opposed to top.
#
#   2.01    19-Jan-2013 (bm) Added JEM working directory fix (minor issue).
#
#   2.00    15-Dec-2012 (bm) When an item is moved (placed) from one display to another, it is
#                       explicitly removed from the first one.
#                       Added set/getColor(), set/getThickness(), set/getFill() for drawable
#                       graphics objects (e.g., Line, Circle, etc.) via Drawable superclass.
#                       Setting one of those attributes automatically redraws object.
#                       Finalized API for 2.0 release.
#
#   1.89    06-Dec-2012 (bm) Simplified menu creation - see addItem() and addItemList().
#                       Now, there is no need to create a menuItem anymore - we cut to the chase,
#                       i.e., we create a menu, add items to it (i.e., a string (name) and a function to call
#                       when item is selected), and add menu to the display.  Display updates itself
#                       to show new menus.  Menus appear on existing menu bar (no need to create one).
#                       So, now we just build a menu and add it.  Simpler, faster.
#
#   1.88    26-Nov-2012 (bm) Tested all regular Widgets (and added sample unit tests).
#
#   1.87    18-Nov-2012 (bm) Changed Display() to put new object in the display at beginning
#                       of z-order list - add() at index 0.
#
#   1.86    07-Nov-2012 (bm) Changed Display() to use the default JFrame's content pane.
#                       This seems to fix the problem with a "dead" display area 
#                       at the bottom (lowest 20 pixels or so).
#
#   1.85    01-Nov-2012 (bm) Refactored common code of widgets and graphics objects 
#                       into class Widget().
#
#   1.84    31-Oct-2012 (dth) Fixed bug with resizing widgets and graphics objects.
#
#   1.83    24-Oct-2012 (bm) Image class was renamed to Icon (to fix conflict with image.py).
#                       The two image classes are incompatible enough to keep separate.
#
#   1.82    24-Oct-2012 (bm) Image is created without specifying an initial position.
#                       Positioning is handled when placing() the image on a Display.
#
#   1.81    12-Oct-2012 (bm) Slider callback function now expects one parameter, the slider value.
#
#   1.8     21-Sep-2012 (bm) Fixed problem with adding submenus (they needed special treatment).
#                       (But what about PopUpMenu's?  Can they have submenus?  If so,
#                        we need to handle that as well.)
#                       Fixed problem with KEY_RELEASED.  Now we capture status of modifier keys.
#                       Also, we properly report the key pressed/released/typed (to the best
#                       of our abilities - some keys are modified in the keyboard driver,
#                       before they get to us - but everything else, we now can handle).
#
#   1.7     19-Sep-2012 (bm) Drawable objects are now specified using absolute coordinates
#                       (e.g., Line(x1, y1, x2, y2), etc. 
#                       Also, fixed minor bug with resizing Image() using only height argument.
#                       Also, fixed Display keyboard listener (now, keyboard events can be handled). 
#
#   1.6     14-Sep-2012 (bm) Added Display.setToolTipText() to use Display's internal JPanel.
#                       Fixed Display.getHeight() bug to return the height specified in constructor.
#                       Commented out Display.draw(), erase() - legacy code (to be removed?)
#
#   1.5     11-Sep-2012 (bm) Added a Point class.
#
#   1.4     05-Sep-2012 (bm) Renamed module as 'gui'.
#
#   1.3     01-Jun-2012 (dth) Add menus and resize shapes.
#
#   1.2.2   01-Jun-2012 (dth) Fixed Image to be scalable.
#
#   1.2.1   21-May-2012 (dth) Added onClose.  Modified instantiating event listeners in shapes 
#                       to wait until a callback function is provided (to allow events to fall
#                  through if not handled by the shape).
#
#   1.2     16-May-2012 (dth, keh) Implemented API changes.
#
#   1.1.1   14-May-2012 (dth) Modified mouse click to pass x and y coordinates of mouse to 
#                       user-defined function.
#
#
# TODO: 
#
# 0. Remove JButton, JPanel, etc. as a superclass for GUI widgets and graphics objects (i.e., make the
#    JButton an attribute of the Button class, etc.).  
#    Rationale:  If the end-user (programmer) accidentally redefines a JButton's functions (e.g., getX, etc.), 
#    the end-code breaks in unpredictable ways (that are hard to trace - make no sense to the end-programmer). 
#    The disadvantage is that we lose access to all inherited functions - we would know need to introduce 
#    appropriate wrappers for all needed ones and it's hard to anticipate which may be needed by every end-programmer). 
#
# 1. Make it possible to draw text in various orientations.  Explore Java Graphics drawString().
#    For now we use Label objects - also it's possible to use Icons (perhaps this is more enabling,
#    since it allows for all kinds of possibilities (via Photoshop, pixlr.com, etc.)
#
# 2. If a event-handler function (e.g., display.onMouseOMove()) is called with 'None', reset the
#    callback function to the nullFunction.  This way we can set and unset event handlers.
#
###############################################################################

import sys

###############################################################################
# Swing Javax Packages
###############################################################################

from java.awt import *
from java.awt.event import *
from javax.swing import *
from javax.swing.event import *
from javax.imageio import *
from java.io import *
from java.awt.image import *
from java.awt.geom import *

from org.imgscalr import Scalr

from java.awt.event.KeyEvent import *   # so that we can use either VK_A or KeyEvent.VK_A)

from timer import *    # import Timer class


# Is this needed?  It causes a naming conflict with jMusic's View class
#from javax.swing.text import *


###############################################################################
# Color
#
# Create a new color consisting of R, G, B (each 0-255), to be used with Widgets.
#
# for example:
#
# color = Color(255, 255, 255)    # same as Color.WHITE
#
# Also, use getRed(), getGreen(), getBlue()
#
# Available through the AWT library.

###############################################################################
# Color gradient
#
# A color gradient is a smooth color progression from one color to another, 
# which creates the illusion of continuity between the two color extremes.
# 
# The following auxiliary function may be used used to create a color gradient.
# This function returns a list of RGB colors (i.e., a list of lists) starting with color1
# (e.g., [0, 0, 0]) and ending (without including) color2 (e.g., [251, 147, 14], which is orange).
# The number of steps equals the number of colors in the list returned.  
#
# For example, the following creates a gradient list of 12 colors:
#
# >>> colorGradient([0, 0, 0], [251, 147, 14], 12)      
# [[0, 0, 0], [20, 12, 1], [41, 24, 2], [62, 36, 3], [83, 49, 4], [104, 61, 5], [125, 73, 7], 
# [146, 85, 8], [167, 98, 9], [188, 110, 10], [209, 122, 11], [230, 134, 12]]
#
# Notice how the above excludes the final color (i.e.,  [251, 147, 14]).  This allows to 
# create composite gradients (without duplication of colors).  For example, the following
#
# black = [0, 0, 0]         # RGB values for black
# orange = [251, 147, 14]   # RGB values for orange
# white = [255, 255, 255]   # RGB values for white
#
# cg = colorGradient(black, orange, 12) + colorGradient(orange, white, 12) + [white]
#
# creates a list of gradient colors from black to orange, and from orange to white.  
# Notice how the final color, white, has to be included separately (using list concatenation).  
# Now, gc contains a total of 25 unique gradient colors.
#
# For convenience, colorGradient() also works with java.awt.Color parameters, in which case
# it returns a list of java.awt.Color colors.
#

def colorGradient(color1, color2, steps):
   """
   Returns a list of RGB colors creating a "smooth" gradient between 'color1' 
   and 'color2'.  The amount of smoothness is determined by 'steps', which specifies
   how many intermediate colors to create. The result includes 'color1' but not
   'color2' to allow for connecting one gradient to another (without duplication 
   of colors).
   """
   gradientList = []   # holds RGB lists of individual gradient colors
   
   # check if using java.awt.Color
   if type(color1) == type(color2) and type(color2) == type(Color.RED):
   
      # extract RGB values
      red1, green1, blue1 = color1.getRed(), color1.getGreen(), color1.getBlue()
      red2, green2, blue2 = color2.getRed(), color2.getGreen(), color2.getBlue()
      
   else:  # assume RGB list
   
      # extract RGB values
      red1, green1, blue1 = color1
      red2, green2, blue2 = color2
   
   # find difference between color extremes
   differenceR = red2 - red1       # R component
   differenceG = green2 - green1   # G component
   differenceB = blue2 - blue1     # B component
   
   # interpolate RGB values between extremes
   for i in range(steps):
      gradientR = red1 + i * differenceR / steps
      gradientG = green1 + i * differenceG / steps
      gradientB = blue1 + i * differenceB / steps

      gradientList.append( [gradientR, gradientG, gradientB] )
   # now, gradient list contains all the intermediate colors, including color1 
   # but not color2
   
   # if original in java.awt.Color, convert result accordingly
   if type(color1) == type(Color.RED):
      gradientList = [Color(x[0], x[1], x[2]) for x in gradientList]
   
   return gradientList   # and return it


###############################################################################
# Listeners
#
# These listener classes are intended to be hidden from the end-user.  These classes
# provide the bridge between the user-defined widget, Swing Listeners, and the
# user-defined event handler.  These listeners are created by the widgets
# themselves, so the user simply needs to pass the event handler function to
# the widget during construction.
#
# These are default listeners associated with the standard Swing widgets
# defined below to automatically generate the desired respones to an event, or
# ease defining an event handler by passing a function name to the constructor
# of the widget.
###############################################################################

# ButtonListener
#
# Listener for the Button, CheckBox and DropDownList widgets.  eventHandler is
# called when the Button or CheckBox is clicked, or a selection is made by the
# DropDownList.  Extends Swing's ActionListener class.

class ButtonListener(ActionListener):
   """
   Event handler for button clicks
   """

   def __init__(self, widget, eventFunction):
      """
      Points this listener to eventFunction when the button is pressed
      """
      self.eventFunction = eventFunction
      self.widget = widget    # widget owner of this event handler

   def actionPerformed(self, event = None):
      """
      Call the eventFunction and return focus to the widget's parent display
      """
      self.eventFunction()
      self.widget.display.display.requestFocusInWindow()  # give focus to parent display


# CheckboxListener
#
# Listener for the Checkbox widget.  eventHandler is called when the checkbox is
# changed - it is passed the current value of the checkbox (checked is True, unchecked is False).
# Extends Swing's ChangeListener class.

class CheckboxListener(ActionListener):
   """
   Event handler for checkboxes
   """

   def __init__(self, checkbox, eventFunction):
      """
      Points this listener to eventFunction when something happens
      """
      self.checkbox = checkbox   # remember which checkbox we are connected to, so we can poll it when a change happens
      self.eventFunction = eventFunction

   def actionPerformed(self, event = None):
      """
      Call the eventFunction and return focus to the checkbox's parent display
      """     
      checkboxValue = self.checkbox.isChecked()  # poll the checkbox
      self.eventFunction( checkboxValue )        # and pass its changed value to the event handler
      self.checkbox.display.display.requestFocusInWindow()  # give focus to parent display


# SliderListener
#
# Listener for the Slider widget.  eventHandler is called when the slider is
# moved - it is passed the current value of the slider.  Extends Swing's ChangeListener class.

class SliderListener(ChangeListener):
   """
   Event handler for sliders
   """

   def __init__(self, slider, eventFunction):
      """
      Points this listener to eventFunction when something happens
      """
      self.slider = slider   # remember which slider we are connected to, so we can poll it when a change happens
      self.eventFunction = eventFunction

   def stateChanged(self, event = None):
      """
      Call the eventFunction and return focus to the slider's parent display
      """     
      sliderValue = self.slider.getValue()   # poll the slider
      self.eventFunction( sliderValue )      # and pass its changed value to the event handler
      self.slider.display.display.requestFocusInWindow()  # give focus to parent display


# DropDownListListener
#
# Listener for the DropDownList widget.  eventHandler is called when an item is
# selected - it is passed the item.  Extends Swing's ActionListener class.

class DropDownListListener(ActionListener):
   """
   Event handler for drop-down lists
   """

   def __init__(self, dropDownList, eventFunction):
      """
      Points this listener to eventFunction when something happens
      """
      self.dropDownList = dropDownList   # remember which dropDownList we are connected to, so we can poll it when a change happens
      self.eventFunction = eventFunction

   def actionPerformed(self, event = None):
      """
      Call the eventFunction and return focus to the dropDownList's parent display
      """
      item = self.dropDownList.getSelectedItem()   # poll the drop-down list
      self.eventFunction( item )                   # and pass it to the event handler
      self.dropDownList.display.display.requestFocusInWindow()  # give focus to parent display


# TextFieldListener
#
# Listener for the TextField widget.  eventHandler is called when the user types 
# the Enter key..  Extends Swing's ActionListener class.

class TextFieldListener(ActionListener):
   """
   Event handler for drop-down lists
   """

   def __init__(self, textField, eventFunction):
      """
      Points this listener to eventFunction when something happens
      """
      self.textField = textField   # remember which textField we are connected to, so we can poll it when a change happens
      self.eventFunction = eventFunction

   def actionPerformed(self, event = None):
      """
      Call the eventFunction and return focus to the textField's parent display
      """
      text = self.textField.getText()   # retrieve the text contained in textField (without newline)
      self.eventFunction( text )        # and pass it to the event handler
      self.textField.display.display.requestFocusInWindow()  # give focus to parent display


# MenuItemListener
#
# Listener for a menu item being selected

class MenuItemListener(ActionListener):
   """
   Event handler for menu item selection
   """

   def __init__(self, callbackFunction):
      """
      Point this listener to the callback function when the menuitem is selected.
      """

      self.callback = callbackFunction


   def actionPerformed(self, event = None):
      """
      Call the callback function
      """

      self.callback()
      # NOTE:  Selecting a menu item does NOT seem to require giving focus to parent display


# KeyboardListener
#
# Listener for keyboard events.
# This listener only provides functionality for when a key is typed.  For the
# purpose of simplicity, there is no event handling for when a key is pressed
# (and held down), or released.

# constants for positions in modifierKeys list of booleans passed to keyboard handlers.
SHIFT_KEY   = 0
CONTROL_KEY = 1
ALT_KEY     = 2
META_KEY    = 3  

class KeyboardListener(KeyListener):
   """
   Event handler for keyboard function
   """

   def __init__(self):
      """
      Points this listener to the eventFunction when something happens
      """

      self.typedFunction = self.nullFunctionCharacterOnly
      self.pressedFunction = self.nullFunctionCharacterOnly
      self.releasedFunction = self.nullFunctionCharacterOnly
      #self.pressedFunction = self.nullFunctionCharacterPlusModifers  # we do not pass modifiers anymore - simpler to pass VT keycode instead
      #self.releasedFunction = self.nullFunctionCharacterPlusModifers

   def nullFunctionCharacterOnly(self, character):
      """
      nullFunction does nothing, and accepts a character.
      """   
      pass

#   def nullFunctionCharacterPlusModifers(self, key, modifierKeysState):
#      """
#      nullFunction does nothing, and accepts a character, and the state of the four modifier keys,
#      a list of four booleans, each for shiftDown, controlDown, altDown, metaDown in this order.
#      """   
#      pass

   def keyTyped(self, keyEvent):
      """
      When a key is typed
      """

# From Java API documentation -- http://docs.oracle.com/javase/1.4.2/docs/api/java/awt/event/KeyEvent.html
#      
#"Key typed" events are higher-level and generally do not depend on the platform or keyboard layout. They are generated when a Unicode character is entered, and are the preferred way to find out about character input. In the simplest case, a key typed event is produced by a single key press (e.g., 'a'). Often, however, characters are produced by series of key presses (e.g., 'shift' + 'a'), and the mapping from key pressed events to key typed events may be many-to-one or many-to-many. Key releases are not usually necessary to generate a key typed event, but there are some cases where the key typed event is not generated until a key is released (e.g., entering ASCII sequences via the Alt-Numpad method in Windows). No key typed events are generated for keys that don't generate Unicode characters (e.g., action keys, modifier keys, etc.). The getKeyChar method always returns a valid Unicode character or CHAR_UNDEFINED. For key pressed and key released events, the getKeyCode method returns the event's keyCode. For key typed events, the getKeyCode method always returns VK_UNDEFINED.
#

      # Get which key was pressed

      eventID = keyEvent.getID()
                    
      # Was a character typed?

      if eventID == KeyEvent.KEY_TYPED:

         # get the character typed
         character = keyEvent.getKeyChar()     # use this for key typed
         #keyCode = keyEvent.getKeyCode()
         #character = KeyEvent.getKeyText(keyCode).encode('utf8')
      
         #character = keyEvent.getKeyChar()         
         #keyCode = keyEvent.getKeyCode()            # use this for key pressed
         #character = KeyEvent.getKeyText(keyCode).encode('utf8')         
         #character = "key code = " + chr(keyCode) #+ " (" + KeyEvent.getKeyText(keyCode) + ")"       
         #character = chr(keyCode)      

         # also get state of modifier keys
         #shiftDown = keyEvent.isShiftDown()
         #controlDown = keyEvent.isControlDown()
         #altDown = keyEvent.isAltDown()
         #metaDown = keyEvent.isMetaDown()        

         # Call the function to handle this, passing the character which was typed,
         # and the state of the four modifier keys, a list of four booleans.

         #self.typedFunction(character, [shiftDown, controlDown, altDown, metaDown])
         self.typedFunction(character)

   def keyPressed(self, keyEvent):
      """
      When a key is pressed
      """

# From Java API documentation -- http://docs.oracle.com/javase/1.4.2/docs/api/java/awt/event/KeyEvent.html
#      
#"Key pressed" and "key released" events are lower-level and depend on the platform and keyboard layout. They are generated whenever a key is pressed or released, and are the only way to find out about keys that don't generate character input (e.g., action keys, modifier keys, etc.). The key being pressed or released is indicated by the getKeyCode method, which returns a virtual key code.
#
#Virtual key codes are used to report which keyboard key has been pressed, rather than a character generated by the combination of one or more keystrokes (such as "A", which comes from shift and "a").
#
#For example, pressing the Shift key will cause a KEY_PRESSED event with a VK_SHIFT keyCode, while pressing the 'a' key will result in a VK_A keyCode. After the 'a' key is released, a KEY_RELEASED event will be fired with VK_A. Separately, a KEY_TYPED event with a keyChar value of 'A' is generated.      
#

      # Get which key was pressed

      eventID = keyEvent.getID()

      # Was a character pressed?  

      if eventID == KeyEvent.KEY_PRESSED:
      
         # get the character pressed
         keyCode = keyEvent.getKeyCode()            # use this for key pressed
         #character = chr(keyCode)      
      
         # also get state of modifier keys
         #shiftDown = keyEvent.isShiftDown()
         #controlDown = keyEvent.isControlDown()
         #altDown = keyEvent.isAltDown()
         #metaDown = keyEvent.isMetaDown()
        
         # Call the function to handle this, passing the character which was pressed,
         # and the state of the four modifier keys, a list of four booleans.

         #self.pressedFunction(character, [shiftDown, controlDown, altDown, metaDown])   # returns a printable character (more usable, but misses some more "esoteric" characters)
         self.pressedFunction(keyCode)   # returns a VK number (e.g., KeyEvent.VK_A)


   def keyReleased(self, keyEvent):
      """
      When a key is released
      """

# From Java API documentation -- http://docs.oracle.com/javase/1.4.2/docs/api/java/awt/event/KeyEvent.html
#      
#"Key pressed" and "key released" events are lower-level and depend on the platform and keyboard layout. They are generated whenever a key is pressed or released, and are the only way to find out about keys that don't generate character input (e.g., action keys, modifier keys, etc.). The key being pressed or released is indicated by the getKeyCode method, which returns a virtual key code.
#
#Virtual key codes are used to report which keyboard key has been pressed, rather than a character generated by the combination of one or more keystrokes (such as "A", which comes from shift and "a").
#
#For example, pressing the Shift key will cause a KEY_PRESSED event with a VK_SHIFT keyCode, while pressing the 'a' key will result in a VK_A keyCode. After the 'a' key is released, a KEY_RELEASED event will be fired with VK_A. Separately, a KEY_TYPED event with a keyChar value of 'A' is generated.      
#

      # Get which key was released

      eventID = keyEvent.getID()

      # Was a character released?

      if eventID == KeyEvent.KEY_RELEASED:

         # get the character released
         keyCode = keyEvent.getKeyCode()            # use this for key released
         #character = chr(keyCode)       
      
         # also get state of modifier keys
         #shiftDown = keyEvent.isShiftDown()
         #controlDown = keyEvent.isControlDown()
         #altDown = keyEvent.isAltDown()
         #metaDown = keyEvent.isMetaDown()

         # Call the function to handle this, passing the character which was released,
         # and the state of the four modifier keys, a list of four booleans.

         #self.releasedFunction(character, [shiftDown, controlDown, altDown, metaDown])  # returns a printable character (more usable, but misses some more esoteric characters)
         self.releasedFunction(keyCode)   # returns a VK number (e.g., KeyEvent.VK_A)


# MouseClickListener
#
# Listener for mouse button events.
# This listener only provides functionality for when either mouse button is
# clicked.  For simplicity, there is no event handling for when the mouse button
# is pressed (and held), or released.  Nor is there event handling for when the
# mouse is located within the context (i.e., widget) of this listener.

class MouseClickListener(MouseListener):
   """
   A listener for when the mouse is clicked.  Ignores other mouse button operations
   """

   def __init__(self, remapCoordinates):
   #def __init__(self):

      self.remapCoordinates = remapCoordinates       # Who is this listening to?

      self.clickFunction = self.nullFunction
      self.pressFunction = self.nullFunction
      self.releaseFunction = self.nullFunction
      self.enterFunction = self.nullFunction
      self.exitFunction = self.nullFunction

      self.popupMenu = None

   def nullFunction(self, x, y):
      """
      nullFunction does nothing, accepts mouse coordinates.
      """
      pass

   def mousePressed(self, mouseEvent):
      """
      Mouse button is pressed (but not yet released)
      """

      x = mouseEvent.getX()
      y = mouseEvent.getY()

      (x, y) = self.remapCoordinates(x, y)

      if mouseEvent.isPopupTrigger():
         if self.popupMenu:
            self.popupMenu.show(mouseEvent.getComponent(), mouseEvent.getX(), mouseEvent.getY())
      else:
         self.pressFunction(x, y)

   def mouseReleased(self, mouseEvent):
      """
      Mouse button is released
      """

      x = mouseEvent.getX()
      y = mouseEvent.getY()

      (x, y) = self.remapCoordinates(x, y)

      if mouseEvent.isPopupTrigger():
         if self.popupMenu:
            self.popupMenu.show(mouseEvent.getComponent(), mouseEvent.getX(), mouseEvent.getY())
      else:
         self.releaseFunction(x, y)

   def mouseEntered(self, mouseEvent):
      """
      Mouse has entered the boundary of the object
      """

      x = mouseEvent.getX()
      y = mouseEvent.getY()

      (x, y) = self.remapCoordinates(x, y)

      self.enterFunction(x, y)

   def mouseExited(self, mouseEvent):
      """
      Mouse has exited the boundary of the object
      """

      x = mouseEvent.getX()
      y = mouseEvent.getY()

      (x, y) = self.remapCoordinates(x, y)

      self.exitFunction(x, y)

   def mouseClicked(self, mouseEvent):
      """
      Mouse button has been clicked.  Call the click function
      """

      x = mouseEvent.getX()
      y = mouseEvent.getY()

      (x, y) = self.remapCoordinates(x, y)

      if mouseEvent.isPopupTrigger():
         if self.popupMenu:
            self.popupMenu.show(mouseEvent.getComponent(), mouseEvent.getX(), mouseEvent.getY())
      else:
         self.clickFunction(x, y)
         
      # NOTE:  Here we could give focus to the object (may be useful for display objects)


# MouseMovementListener
#
# Listener for mouse motion events.
# This listener passes the coordinates of the mouse to the event handling
# function whenever the mouse is moved.  Mouse movement (i.e., with no mouse
# button pressed) and mouse dragging (i.e., when a mouse button is held down)
# are treated the same.

class MouseMovementListener(MouseMotionListener):
   """
   A listener to handle when the mouse moves
   """

   def __init__(self, remapCoordinates):
   #def __init__(self):

      self.remapCoordinates = remapCoordinates

      self.moveFunction = self.nullFunction
      self.dragFunction = self.nullFunction

   def nullFunction(self, x, y):
      """
      nullFunction does nothing, accepts mouse coordinates.
      """
      pass

   def mouseMoved(self, mouseEvent):
      """
      Pass the new location to the handler
      """

      # Get the x and y coordinates

      x = mouseEvent.getX()
      y = mouseEvent.getY()

      (x, y) = self.remapCoordinates(x, y)

      # And call the move function

      self.moveFunction(x, y)

   def mouseDragged(self, mouseEvent):
      """
      Pass the new location to the handler
      """

      # Get the x and y coordinates

      x = mouseEvent.getX()
      y = mouseEvent.getY()

      (x, y) = self.remapCoordinates(x, y)

      # And call the move function

      self.dragFunction(x, y)


# DisplayListener
#
# Listener for closing the display.  Allows user to add a callback function
# to clean up still-running code.

class DisplayListener(WindowListener):
   """
   Listener for closing the window
   """

   def __init__(self, parentFrame):
      #WindowListener.__init__(self)  # window listener is an interface (not a class)
      self.closeCallback = self.nullFunction
      self.parentFrame = parentFrame

   def nullFunction(self):
      pass

   def windowActivated(self, event):
      pass

   def windowClosed(self, event):
      pass

   def windowClosing(self, event):
      self.closeCallback()
      pass

   def windowDeactivated(self, event):
      pass

   def windowDeiconified(self, event):
      pass

   def windowIconified(self, event):
      pass

   def windowOpened(self, event):
      pass
      

# ComponentChangeListener
#
# Used to automatically update components when resized or moved.
# This is needed, since changing the component's position or size 
# does not automatically change the Java Swing representation of the
# component's size or position

class ComponentChangeListener(ComponentListener):
   """
   Listener for when components change
   """
   
   def __init__(self):
      """     
      """     
      pass

   def componentHidden(self, event):
      """
      """     
      pass
#      print "Component Hidden"
     
   def componentMoved(self, event):
      """     
      """
      pass
#      print "Component Moved"

   def componentResized(self, event):
      """     
     """
#      print "Component Resized"
     
      component = event.getComponent()
      x, y = component.position
      if component.display:
         cp = component.display.getParent().getParent().getParent()
         cp.reposition(component, x, y)
     
   def componentShown(self, event):
      """     
      """
      pass
 #     print "Component Shown"


###############################################################################
# Widget
#
# Class to encapsulate common functionality (mainly event handling) for 
# widget objects.
#

class Widget():
   """
   This class defines common GUI widget functionality.
   """

   def __init__(self):
      """
      Set up instance variables.
      """
      self.display = None
      
      self.keyboardListener = None
      self.mouseClickListener = None
      self.mouseMovementListener = None
      self.componentChangeListener = ComponentChangeListener()

   def encloses(self, widget):
      """
      Determines whether or not this Widget encloses (contains) the specified Widget.
      """      
      return self.getBounds().contains( widget.getBounds() )

   def intersects(self, widget):
      """
      Determines whether or not this Widget and the specified Widget intersect.
      """      
      return self.getBounds().intersects( widget.getBounds() )

   def getX(self):
      """
      Returns the x coordinate of this Widget.
      """      
      return self.position[0]

   def setX(self, x):
      """
      Set the x coordinate of this Widget.
      """      
      self.setPosition(x, self.position[1])

   def getY(self):
      """
      Returns the y coordinate of this Widget.
      """      
      return self.position[1]

   def setY(self, y):
      """
      Set the y coordinate of this Widget.
      """      
      self.setPosition(self.position[0], y)

   def getPosition(self):
      """
      Returns the position of this Widget, i.e., the (x, y) tuple.
      """      
      return self.position

   def setPosition(self, x, y):
      """
      Set the position of this Widget.
      """      
      self.position = (x, y)
      
      # if this widget is already on a display, also reposition it
      if self.display:
         self.display.move(self, x, y)

   def onKeyType(self, callbackFunction):
      """
      Set up a callback function for when a key is typed.
      """

      if self.keyboardListener == None:
         self.keyboardListener = KeyboardListener()
         self.addKeyListener(self.keyboardListener)

      self.keyboardListener.typedFunction = callbackFunction
      
   def onKeyDown(self, callbackFunction):
      """
      Set up a callback function for when a key is pressed.
      """

      if self.keyboardListener == None:
         self.keyboardListener = KeyboardListener()
         self.addKeyListener(self.keyboardListener)

      self.keyboardListener.pressedFunction = callbackFunction

   def onKeyUp(self, callbackFunction):
      """
      Set up a callback function for when a key is released.
      """

      if self.keyboardListener == None:
         self.keyboardListener = KeyboardListener()
         self.addKeyListener(self.keyboardListener)

      self.keyboardListener.releasedFunction = callbackFunction

   # NOTE: This function is introduced here to take care of remapping coordinates
   # for JPanel components, so when a mouse event occurs with a GUI object's JPanel
   # the global (enclosing Display) coordinates are communicated (instead of the internal
   # JPanel coordinates, which are by default returned).  We are doing this translation /
   # remapping because it is more natural for the end-user (programmer) to think in terms
   # of global (enclosing Display) coordinates (as these are the coordinates they are dealing
   # with all the time).  This function may be overloaded by any GUI object (e.g., Circle)
   # that has a different way of thinking of its position on the enclosing Display (e.g., Circle's
   # consider their position to be relative to their center, and not the top-left corner, as
   # most (all?) other GUI objects).  Something to be aware of and careful when creating
   # new, special-case GUI objects (like Circle).
   def __remapCoordinates__(self, x, y):
      """
      Adjust the coordinates relative to the underlying display.
      """
      x = x + self.position[0]
      y = y + self.position[1]

      return x, y

   def onMouseClick(self, callbackFunction):
      """
      Set up a callback function for when the mouse is clicked.
      """

      if self.mouseClickListener == None:
         self.mouseClickListener = MouseClickListener(self.__remapCoordinates__)
         #self.mouseClickListener = MouseClickListener()
         self.addMouseListener(self.mouseClickListener)

      self.mouseClickListener.clickFunction = callbackFunction

   def onMouseDown(self, callbackFunction):
      """
      Set up a callback function for when the mouse button is pressed.
      """

      if self.mouseClickListener == None:
         self.mouseClickListener = MouseClickListener(self.__remapCoordinates__)
         #self.mouseClickListener = MouseClickListener()
         self.addMouseListener(self.mouseClickListener)

      self.mouseClickListener.pressFunction = callbackFunction

   def onMouseUp(self, callbackFunction):
      """
      Set up a callback function for when the mouse button is released.
      """

      if self.mouseClickListener == None:
         self.mouseClickListener = MouseClickListener(self.__remapCoordinates__)
         #self.mouseClickListener = MouseClickListener()
         self.addMouseListener(self.mouseClickListener)

      self.mouseClickListener.releaseFunction = callbackFunction

   def onMouseEnter(self, callbackFunction):
      """
      Set up a callback function for when the mouse enters the display.
      """

      if self.mouseClickListener == None:
         self.mouseClickListener = MouseClickListener(self.__remapCoordinates__)
         #self.mouseClickListener = MouseClickListener()
         self.addMouseListener(self.mouseClickListener)

      self.mouseClickListener.enterFunction = callbackFunction

   def onMouseExit(self, callbackFunction):
      """
      Set up a callback function for when the mouse exits the display.
      """

      if self.mouseClickListener == None:
         self.mouseClickListener = MouseClickListener(self.__remapCoordinates__)
         #self.mouseClickListener = MouseClickListener()
         self.addMouseListener(self.mouseClickListener)

      self.mouseClickListener.exitFunction = callbackFunction

   def onMouseMove(self, callbackFunction):
      """
      Set up a callback function for when the mouse is moved.
      """

      if self.mouseMovementListener == None:
         self.mouseMovementListener = MouseMovementListener(self.__remapCoordinates__)
         #self.mouseMovementListener = MouseMovementListener()
         self.addMouseMotionListener(self.mouseMovementListener)

      self.mouseMovementListener.moveFunction = callbackFunction

   def onMouseDrag(self, callbackFunction):
      """
      Set up a callback function for when the mouse is dragged.
      """

      if self.mouseMovementListener == None:
         self.mouseMovementListener = MouseMovementListener(self.__remapCoordinates__)
         #self.mouseMovementListener = MouseMovementListener()
         self.addMouseMotionListener(self.mouseMovementListener)

      self.mouseMovementListener.dragFunction = callbackFunction
      #self.mouseMovementListener.remapCoordinates = self.remapCoordinates  # used to map coordinates relative to underlying display

   def addPopupMenu(self, menu):

      if self.mouseClickListener == None:
         self.mouseClickListener = MouseClickListener(self.__remapCoordinates__)
         #self.mouseClickListener = MouseClickListener()
         self.addMouseListener(self.mouseClickListener)

      self.mouseClickListener.popupMenu = menu.__toJPopupMenu__()


###############################################################################
# Drawable
#
# Class to encapsulate common functionality (mainly color, fill, thickness) for 
# drawable gaphics objects.
#

class Drawable():
   """
   This class defines common GUI drawable object functionality.
   """

   def __init__(self, color=Color.BLACK, fill=False, thickness=1):
      """
      Create a drawable object.
      """

      self.color = color
      self.fill = fill
      self.thickness = thickness
 
   def setColor(self, color=None):
      """
      Change the color of the drawable object.  If no color provided, use dialog box to select.
      """
      
      if color == None:
         color = JColorChooser().showDialog(None, "Select a color", Color.ORANGE) 
         print color   # useful side-efect for discovering new colors

      self.color = color
      if self.display:
         self.display.contentPane.repaint()

   def getColor(self):
      """
      Returns the color of the drawable object.
      """
      return self.color

#   def setFill(self, fill=True):
#      """
#      Change the fill state of the drawable object.
#      """
#
#      self.fill = fill
#      if self.display:
#         self.display.contentPane.repaint()
#
#   def getFill(self):
#      """
#      Returns the fill state of the drawable object.
#      """
#      return self.fill
#
#   def setThickness(self, thickness=1):
#      """
#      Change the thickness of the drawable object.
#      """
#
#      self.thickness = thickness
#
#      if self.display:
#         self.display.contentPane.repaint()
#
#   def getThickness(self):
#      """
#      Returns the thickness of the drawable object.
#      """
#      return self.thickness


# __ActiveDisplays__ is used to keep track which displays are active, so we can close them properly
# and clean-up all contain GUI objects when JEM's Stop button is pressed 

try:

   __ActiveDisplays__          # if already defined (from an earlier run, do nothing, as it already contains material)
   
except:

   __ActiveDisplays__ = []     # first run - let's define it to hold active displays


###############################################################################
# Display
#
# Class for generating a GUI window.  A program may open several Displays.  
# Extends Swing's JFrame class.
#
# Methods:
#
# Display()
# Display(title)
# Display(title, width, height)
#   Creates a new Display.
#   --title - Gives the Display a Title (displayed at the top of the window)
#   --width - The width (in pixels) of the Display window.
#   --height - The height (in pixels) of the Display window.
#
# show()
#   Displays the window.  
#
# hide()
#   Hide the window.
#
# add(widget)
#   Adds a widget to the Display.  Widgets are positioned using FlowLayout.
#
# NOTE:  This class was originally called Window, but was renamed for simplicity
# due to the presence of a Window class in jMusic.
###############################################################################

from copy import copy   # used by Display.getItems()

class Display():
   """
   GUI Window to hold widgets.
   """

   def __init__(self, title = "", width = 600, height = 400, x=0, y=0, color = None):
      """
      Create a new window.
      """

      self.display = JFrame()        # create frame window
      self.display.setTitle(title)   # update the window title
      
      if color:    # did they specify a background color?
         self.display.setBackground(color)
      
      # create the container pane of the display (a JLabel inside a JFrame)
      container = JLabel()           # using JLabel (as opposed to JPanel) simplifes things
      container.setPreferredSize( Dimension(width, height) )   # give it preferred dimensions      

      # place container pane inside JFrame
      self.display.setContentPane(container)             # place it inside the JFrame
      self.contentPane = self.display.getContentPane()   # but also keep a direct handle to it
      
      # setup the menu area (always present, to simplify creation of menus by end-users)
      self.jMenuBar = JMenuBar()
      self.display.setJMenuBar( self.jMenuBar )
      
      # finalize visual aspects of display and show it
      self.display.setResizable(False)    # jFrame size is fixed at creation
      self.display.pack()                 # adjust everything to fit properly inside the JFrame
      self.setPosition(x, y)              # place it at the desired location on screen (0, 0 is top-left)
      self.display.setVisible(True)       # show display to the world
      
      # make sure the application does NOT exit when the window's closed
      self.display.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)   # clean up as much as possible 
      #self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)   # this closes JEM - so, we don't want that
      #self.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE)
      #self.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE)  # this does really nothing...
      
      # set up event listeners for display
      self.displayListener = DisplayListener(self)
      self.display.addWindowListener(self.displayListener)

      # Set up listeners
      self.keyboardListener = KeyboardListener()
      # keyboard events are apparently being sent to JFrame 
      self.display.addKeyListener(self.keyboardListener)     
      #self.contentPane.addKeyListener(self.keyboardListener)
      self.mouseClickListener = MouseClickListener(self.__remapCoordinates__)
      #self.mouseClickListener = MouseClickListener()
      # mouse events are apparently being sent to JPanel 
      self.contentPane.addMouseListener(self.mouseClickListener)
      self.mouseMovementListener = MouseMovementListener(self.__remapCoordinates__)
      #self.mouseMovementListener = MouseMovementListener()
      # mouse events are apparently being sent to JPanel 
      self.contentPane.addMouseMotionListener(self.mouseMovementListener)
      
      # remember all items placed on display - used by removeAll()
      self.items = []

      # remember that this display has been created and is active (so that it can be closed properly by JEM, if desired)
      __ActiveDisplays__.append(self)


   # NOTE: This function has been introduced to take care of remapping coordinates
   # for JPanel components, so when a mouse event occurs with a GUI object's JPanel
   # the global (enclosing Display) coordinates are communicated (instead of the internal
   # JPanel coordinates, which are by default returned).  However, since Display also 
   # uses the same internbal mechanism for handling mouse events (as normal GUI objects),
   # we need to introduce this dummy function here, so that everything will work as
   # defined by the MouseMotionListener API.
   def __remapCoordinates__(self, x, y):
      """
      No mapping is required for Display objects.
      """
      return x, y

   def close(self):
      """Closes the display."""
      # first, call the onClose() callback function (if any - default is the null function)
      # this is done here because the next statement, self.display.dispose(), will NOT call it.  A fix.
      self.displayListener.closeCallback()   

      self.display.dispose()

   def show(self):
      """Shows the display."""
      self.display.show()

   def hide(self):
      """Hides the display."""
      self.display.hide()

   def getItems(self):
      """Returns a deep copy of the items currently on the display."""
      return copy(self.items)

#   def place(self, item, x=None, y=None):
#      """
#      Place an object in the display, at coordinates by x and y.
#      If the object already appears on another display it is removed from there, first.
#      """
#      
#      # If item appears in another display, remove it from there
#      # (an alternatve would be to make a copy, but this could lead to complications,
#      #  and it's harder).
#      if item.display != None:
#         item.display.remove(item)
#
#      # Put the object in the display (at beginning of z-order list - index 0)
#      self.contentPane.add(item, 0)         
#      item.display = self
#      
#      self.items.append( item )  # remember that this item has been added - used by removeAll()
#      
#      # if not position provided when placing
#      if x == None or y == None:
#         x, y = item.position            # get item's position
#         
#      self.reposition(item, x, y)        # and place it in the correct location
#
#      # reposition() redraws the display, so no need to do it here too
#      #self.contentPane.revalidate()
#      #self.contentPane.repaint()

   def place(self, item, x=None, y=None, order = 0):
      """
      Place an object in the display, at coordinates by x and y.
      If the object already appears on another display it is removed from there, first.
      """
      
      # If item appears in another display, remove it from there
      # (an alternatve would be to make a copy, but this could lead to complications,
      #  and it's harder).
      if item.display != None:
         item.display.remove(item)

      # Put the object in the display (at specified z-order - 0 means in front)
      self.contentPane.add(item, order)         
      item.display = self
      
      self.items.append( item )  # remember that this item has been added - used by removeAll()
      
      # if not position provided when placing
      if x == None or y == None:
         x, y = item.position            # get item's position
         
      self.reposition(item, x, y)        # and place it in the correct location

      # reposition() redraws the display, so no need to do it here too
      #self.contentPane.revalidate()
      #self.contentPane.repaint()

   def addOrder(self, item, order, x=None, y=None):
      """
      Same as add() but adds layering, i.e., places an object in the display, at coordinates by x and y
      at the order specified.  Layers are ordered from smallest to largest where 0 is the closest to the front. 
      If the object already appears on another display it is removed from there, first.
      """
      self.place(item, x, y, order)

   def add(self, item, x=None, y=None):
      """
      Same as place(), i.e., places an object in the display, at coordinates by x and y.
      If the object already appears on another display it is removed from there, first.
      """
      self.place(item, x, y)

   def reposition(self, item, x, y):
      """
      Change an object's location in the display
      """
      # Get the size of the item
      itemWidth = item.getPreferredSize().width
      itemHeight = item.getPreferredSize().height

      # Get the offset of the object (for things like circles)
      xOffset = item.offset[0]
      yOffset = item.offset[1]

      # Calculate position of the object
      xPosition = x - xOffset
      #yPosition = self.contentPane.height - itemHeight - y + yOffset
      yPosition = y - yOffset

      # place the JPanel containing the item
      item.setBounds(xPosition, yPosition, itemWidth, itemHeight)
      item.position = (x, y)

      # Redraw the display
      self.contentPane.revalidate()
      self.contentPane.repaint()
      
   def move(self, item, x, y):
      """
      Same as reposition(), i.e., changes an object's location in the display
      """
      self.reposition(item, x, y)

   def remove(self, item):
      """
      Remove the item from the display.
      """
      self.contentPane.remove(item)  # remove the item from the display
      item.display = None            # and the display from the item

      # Redraw the display
      self.contentPane.revalidate()
      self.contentPane.repaint()
 
   def removeAll(self):
      """
      Remove all items from the display.
      """
      self.contentPane.removeAll()  # remove all items from the display
      
      # Redraw the display (needed to clear out Widgets)
      self.contentPane.revalidate()
      self.contentPane.repaint()
 
   def delete(self, item):
      """
      Same as remove(item).
      """
      self.remove(item)              # remove the item from the display
      #del item
  
   # now, some other useful functions
   def setToolTipText(self, text):
      """
      Sets the tooltip text of the Display's internal JPanel (since JFrame 
      does NOT have tooltip capabilities.
      """
      self.contentPane.setToolTipText(text)

   def setColor(self, color=None):
      """
      Change the color of the display.  If no color provided, use dialog box to select.
      """
      
      if color == None:
         color = JColorChooser().showDialog(None, "Select a color", Color.ORANGE) 
         print color   # useful side-efect for discovering new colors

      self.display.setBackground(color)

   def getColor(self):
      """
      Returns the color of the display.
      """
      return self.display.getBackground()

   def setSize(self, width, height):
      """
      Sets the display size.
      """
      # NOTE: 23 pixels of the height will be reserved for the fixed top-menu area 
      # (regardless of whether we add any menus or not).  So let's add 23 to height.
      self.display.setSize(width, height+23)      

   def getHeight(self):
      """
      Returns the display height.
      """
      return self.contentPane.getHeight()      

   def getWidth(self):
      """
      Returns the display width.
      """
      return self.contentPane.getWidth()      

   def setTitle(self, title):
      """
      Sets the display title.
      """
      self.display.setTitle(title)      

   def getTitle(self):
      """
      Returns the display title.
      """
      return self.display.getTitle()      

   def setPosition(self, x, y):
      """
      Set the position of this display.
      """      
      self.display.setLocation(x, y)

   def getPosition(self):
      """
      Returns the position of this Widget, i.e., the (x, y) tuple.
      """      
      x = int(self.display.getLocation().getX())
      y = int(self.display.getLocation().getY())
      return (x, y)
      
   def addMenu(self, menu):
      """
      Add a menu to the menu bar
      """
      self.jMenuBar.add(menu.__toJMenu__())

      # redraw the display
      self.contentPane.revalidate()
      self.contentPane.repaint()

   def addPopupMenu(self, menu):
      """
      Add a popup menu to this display
      """
      self.mouseClickListener.popupMenu = menu.__toJPopupMenu__()
      
   # drawing functions (for convenience)
   def drawLine(self, x1, y1, x2, y2, color=Color.BLACK, thickness=1):
      """
      Draw a line between the points (x1, y1) and (x2, y2) with given color and thickness.
      
      Returns the line object (in case we want to move it or delete it later).
      """
      line = Line(x1, y1, x2, y2, color, thickness)   # create line
      self.add(line)                                  # add it      
      return line                                     # and return it

   def drawCircle(self, x, y, radius, color = Color.BLACK, fill = False, thickness=1):
      """
      Draw a circle at (x, y) with the given radius, color, fill, and thickness.
      
      Returns the circle object (in case we want to move it or delete it later).
      """
      circle = Circle(x, y, radius, color, fill, thickness)   # create circle
      self.add(circle)   # add it      
      return circle      # and return it

   def drawPoint(self, x, y, color = Color.BLACK, thickness=1):
      """
      Draw a point at (x, y) with the given color and thickness.
      
      Returns the point object (in case we want to move it or delete it later).
      """
      point = Point(x, y, color, thickness)   # create point
      self.add(point)   # add it      
      return point      # and return it

   def drawOval(self, x1, y1, x2, y2, color = Color.BLACK, fill = False, thickness = 1):
      """
      Draw an oval using the coordinates of its enclosing rectangle with the given color,
      fill, and thickness.
      
      Returns the oval object (in case we want to move it or delete it later).
      """
      oval = Oval(x1, y1, x2, y2, color, fill, thickness)   # create oval
      self.add(oval)   # add it      
      return oval      # and return it

   def drawArc(self, x1, y1, x2, y2, startAngle, endAngle, color = Color.BLACK, fill = False, thickness = 1):
      """
      Draw an arc using the provided coordinates, arc angles, color, fill, and thickness.
      
      Returns the arc object (in case we want to move it or delete it later).
      """
      arc = Arc(x1, y1, x2, y2, startAngle, endAngle, color, fill, thickness)   # create arc
      self.add(arc)   # add it      
      return arc      # and return it

   def drawRectangle(self, x1, y1, x2, y2, color = Color.BLACK, fill = False, thickness = 1):
      """
      Draw a rectangle using the provided coordinates, color, fill, and thickness.
      
      Returns the rectangle object (in case we want to move it or delete it later).
      """
      rec = Rectangle(x1, y1, x2, y2, color, fill, thickness)   # create rectangle
      self.add(rec)   # add it      
      return rec      # and return it

   def drawPolygon(self, xPoints, yPoints, color = Color.BLACK, fill = False, thickness = 1):
      """
      Draw a polygon using the provided coordinates, color, fill, and thickness.
      
      Returns the polygon object (in case we want to move it or delete it later).
      """
      poly = Polygon(xPoints, yPoints, color, fill, thickness)   # create polygon
      self.add(poly)   # add it      
      return poly      # and return it

   def drawIcon(self, filename, x, y, width = None, height = None):
      """
      Draw an icon (image) from the provided external file (.jpg or .png) at the given coordinates (top-left).
      Also rescale according to provided width and height (if any).
      
      Returns the icon object (in case we want to move it or delete it later).
      """
      icon = Icon(filename, width, height)   # load image (and rescale, if specified)
      self.add(icon, x, y)   # add it at given coordinates    
      return icon            # and return it

   def drawImage(self, filename, x, y, width = None, height = None):
      """
      Same as drawIcon().
      
      Returns the image object (in case we want to move it or delete it later).
      """
      return self.drawIcon(filename, x, y, width, height)

   def drawLabel(self, text, x, y, color = Color.BLACK, font = None):
      """
      Draw the text label on the display at the given coordinates (top-left) and with the provided
      color and font.
      
      Returns the label object (in case we want to move it or delete it later).
      """

      # Font example - Font("Serif", Font.ITALIC, 16)
      #
      # see http://docs.oracle.com/javase/tutorial/2d/text/fonts.html#logical-fonts

      label = Label(text, LEFT, color)   # create label
      if font:                     # did they provide a font?
         label.setFont(font)          # yes, so set it
      self.add(label, x, y)        # add it at given coordinates    
      return label                 # and return it

   def drawText(self, text, x, y, color = Color.BLACK, font = None):
      """
      Same as drawLabel().
      
      Returns the label object (in case we want to move it or delete it later).
      """
      return self.drawLabel(text, x, y, color, font)


   # event handling functions   
   def onKeyType(self, callbackFunction):
      """
      Set up a callback function for when a key is typed.
      """
      self.keyboardListener.typedFunction = callbackFunction

   def onKeyDown(self, callbackFunction):
      """
      Set up a callback function for when a key is pressed.
      """
      self.keyboardListener.pressedFunction = callbackFunction

   def onKeyUp(self, callbackFunction):
      """
      Set up a callback function for when a key is released.
      """
      self.keyboardListener.releasedFunction = callbackFunction

   def onMouseClick(self, callbackFunction):
      """
      Set up a callback function for when the mouse is clicked.
      """
      self.mouseClickListener.clickFunction = callbackFunction

   def onMouseDown(self, callbackFunction):
      """
      Set up a callback function for when the mouse button is pressed.
      """
      self.mouseClickListener.pressFunction = callbackFunction

   def onMouseUp(self, callbackFunction):
      """
      Set up a callback function for when the mouse button is released.
      """
      self.mouseClickListener.releaseFunction = callbackFunction

   def onMouseEnter(self, callbackFunction):
      """
      Set up a callback function for when the mouse enters the display.
      """
      self.mouseClickListener.enterFunction = callbackFunction

   def onMouseExit(self, callbackFunction):
      """
      Set up a callback function for when the mouse exits the display.
      """
      self.mouseClickListener.exitFunction = callbackFunction

   def onMouseMove(self, callbackFunction):
      """
      Set up a callback function for when the mouse is moved.
      """
      self.mouseMovementListener.moveFunction = callbackFunction

   def onMouseDrag(self, callbackFunction):
      """
      Set up a callback function for when the mouse is dragged.
      """
      self.mouseMovementListener.dragFunction = callbackFunction
      self.mouseMovementListener.remapCoordinates = self.remapCoordinates  # needed by listener (does nothing for displays)

   def onClose(self, callbackFunction):
      self.displayListener.closeCallback = callbackFunction

   # define helper functions to show/hide display coordinates at mouse cursor 
   # (useful to discover coordinates of where to widgets when building a GUI)
   def showMouseCoordinates(self):
      """
      Shows mouse coordinates using the display tooltip.
      """      
      # define function to update display tooltip when mouse coordinates change
      showCoordinatesFunction = lambda x, y: self.setToolTipText(str(x) + ", " + str(y))
      
      # Here we remember the original callback function (if any), in order to restore it in hideMouseCoordinates()
      try:  
         # Have we been called before?  (If so do nothing - we have already stored the original mouse listener 
         # move function.)
         self.mouseMovementListener.originalFunction    
      except AttributeError:
         # This is the first time we are called, so remember the current mouse listener move function
         # to restore it later - in hideMouseCoordinates(). 
         self.mouseMovementListener.originalFunction = self.mouseMovementListener.moveFunction  

      # set our own function to be called when mouse moves
      self.onMouseMove( showCoordinatesFunction )

   def hideMouseCoordinates(self):
      """
      Stops showing mouse coordinates using the display tooltip.
      """      
      # hide tool tip
      self.setToolTipText( None )
      
      try:  
         # restore previous function to be called when mouse moves
         self.onMouseMove( self.mouseMovementListener.originalFunction )
      except AttributeError:
         # this will happen if they called us before ever calling showMouseCoordinates()
         pass   #  nothing to restore
         
   def remapCoordinates(self, x, y):
      """
      Leave coordinates as is - we are a display (needed for mouse drag).
      """
      return x, y


######################################################################################
# If running inside JEM, register function that stops everything, when the Stop button
# is pressed inside JEM.
######################################################################################

# function to stop and clean-up all active displays
def __stopActiveDisplays__():

   global __ActiveDisplays__

   # first, remove and clear all GUI objects contained in each display
   for display in __ActiveDisplays__:
   
      # first, dispose all items in the display
      for guiObject in display.getItems():
         display.remove(guiObject)   # remove it from display
         del guiObject               # and delete it from Jython
      
      # now dispose the display itself
      display.display.dispose()      # bye, bye

   # also empty list, so things can be garbage collected
   __ActiveDisplays__ = []   # remove access to deleted items   

# now, register function with JEM (if possible)
try:

    # if we are inside JEM, registerStopFunction() will be available
    registerStopFunction(__stopActiveDisplays__)   # tell JEM which function to call when the Stop button is pressed

except:  # otherwise (if we get an error), we are NOT inside JEM 

    pass    # so, do nothing.




###############################################################################
# Menu
#
# Class for creating a menu (for use as a popup menu or with a menubar).
#
# Methods:
#
# Menu()
#   Creates a new Menu.  It uses either Swing's JMenu or JPopupMenu
#
# addMenuItem(menuItem)
#   Adds an item to the menu.  The name of the menu item is what is displayed
#   in the menu, and the callbackFunction is called when selected.
###############################################################################

class Menu:
   """
   Create a menu (either for use in a menubar, or as a popup)
   """

   def __init__(self, name):
      """ 
      Create a new menu.
      """
      self.menuItems = []         # A list of menu items
      self.name = name

      self.menu = None
      self.popupmenu = None

   def enable(self):
      """
      Enable the menu
      """
      if self.menu:
         self.menu.enable()
      if self.popupmenu:
         self.popupmenu.enable()

   def disable(self):
      """
      Disable the menu
      """
      if self.menu:
         self.menu.disable()
      if self.popupmenu:
         self.popupmenu.disable()

   def addItem(self, item = "", eventFunction = None):
      """
      Add an item to the menu.
      """
      # create Menu item and add it
      menuItem = MenuItem(item, eventFunction)
      self.menuItems.append(menuItem)  

   def addItemList(self, itemList = [""], eventFunctionList = [None]):
      """
      Add a list of items and corresponding callback functions to the menu.
      """      
      for i in range( len(itemList) ):    
         # create a Menu item and add it
         menuItem = MenuItem(itemList[i], eventFunctionList[i])
         self.menuItems.append(menuItem)  

   def addSubMenu(self, menu):
      """
      Add a (sub)menu as an item to the menu.
      """
      self.menuItems.append(menu)  

   def addSeparator(self):
      """
      Add a separator to the menu
      """
      self.menuItems.append("SEPARATOR")

   # Deprecated in favor of new, simpler way (see addItem() and addItemList()).
   # Still useful, however, if we need to disable a single menu item (this way the end-programmer
   # maintains a handle to a particular menu item).
   def addMenuItem(self, menuItem):   
      """
      Add an item to the menu.
      """
      self.menuItems.append(menuItem)  

   def __toJMenu__(self):
      """
      Return a JMenu version of this menu
      """
      self.menu = JMenu(self.name)

      for menuItem in self.menuItems:
         if menuItem == "SEPARATOR":
            self.menu.addSeparator()
         elif isinstance(menuItem, Menu):  # a submenu?
            #print "a submenu..."
            self.menu.add( menuItem.__toJMenu__() )  # recursive call
         else:
            self.menu.add(menuItem)

      return self.menu

   def __toJPopupMenu__(self):
      """
      Return a JPopupMenu version of this menu
      """
      self.popupmenu = JPopupMenu()

      for menuItem in self.menuItems:
         if menuItem == "SEPARATOR":
            self.popupmenu.addSeparator()
         #elif isinstance(menuItem, Menu):  # a submenu?
         #   #print "a submenu..."
         #   self.menu.add( menuItem.__toJPopupMenu__() )  # recursive call
         else:
            self.popupmenu.add(menuItem)

      return self.popupmenu


###############################################################################
# MenuItem
#
# Class for create a new menu item
#
###############################################################################

class MenuItem(JMenuItem):
   """
   A single entry for a menu
   """

   def __init__(self, name, callbackFunction):
      """
      Create a new menu item
      """
      JMenuItem.__init__(self, name)
      listener = MenuItemListener(callbackFunction)
      self.addActionListener(listener)


###############################################################################
# Label
#
# Class for creating text labels.  An extention of Swing's JLabel.
#
# Methods:
#
# Label(text)
# Label(text, alignment, foregroundColor, backgroundColor)
#   Create a new label containing the text.  The alignment may be LEFT,
#   CENTER (default), or RIGHT.  The two colors, if provided, refer to
#   the text color and the background color.
#
# setFont(font), e.g., setFont( Font("Serif", Font.ITALIC, 16) )
#
# setText(text)
#   Sets the text contained in the text field (as a string).
#
# getText()
#   Returns the text contained in the text field (as a string).
#
# setBackgroundColor(color)
#   Change the color of the label's background.
#
# getBackgroundColor()
#   Returns the color of the label.
#
# setForegroundColor(color)
#   Change the color of the label's text.
#
# getForegroundColor()
#   Returns the color of the label's text.
#
###############################################################################

LEFT = SwingConstants.LEFT
CENTER = SwingConstants.CENTER
RIGHT = SwingConstants.RIGHT

class Label(JLabel, Widget):
   """
   A widget to contain text.
   """

   def __init__(self, text, alignment = LEFT, foregroundColor = None, backgroundColor = None):
      """
      Create the text label
      """
      JLabel.__init__(self, text, alignment)
      Widget.__init__(self)                     # set up listeners, etc.

      self.offset = (0,0)
      self.position = (0,0)
      self.display = None

      self.setSize(self.getPreferredSize())
      
      # remember default foreground and background color
      self.backgroundColor = backgroundColor
      self.foregroundColor = foregroundColor
      
      # set colors, if necessary
      if self.backgroundColor != None:
         self.setBackgroundColor( self.backgroundColor )
      if self.foregroundColor != None:
         self.setForegroundColor( self.foregroundColor )       
         
   def setBackgroundColor(self, color=None):
      """
      Change the color of the label's background.  If no color provided, use dialog box to select.
      """
      
      if color == None:
         color = JColorChooser().showDialog(None, "Select a color", Color.ORANGE) 
         print color   # useful side-efect for discovering new colors

      # labels need to be opaque to show their background color, so, since we want show a background color
      # we first need to make the label opaque
      self.setOpaque(True)
      self.backgroundColor = color    # remember it
      self.setBackground(color)       # and set it (using jLabel's appropriate function)

   def getBackgroundColor(self):
      """
      Returns the color of the label.
      """
      
      # if background is not set, return the color of the display
      if self.backgroundColor == None and self.display != None:
         color = self.display.getColor()
      else:
         color = self.backgroundColor
      
      return color

   def setForegroundColor(self, color=None):
      """
      Change the color of the label's text.  If no color provided, use dialog box to select.
      """
      
      if color == None:
         color = JColorChooser().showDialog(None, "Select a color", Color.ORANGE) 
         print color   # useful side-efect for discovering new colors

      self.foregroundColor = color    # remember it
      self.setForeground(color)       # and set it (using jLabel's appropriate function)

   def getForegroundColor(self):
      """
      Returns the color of the label's text.
      """
      
      return self.foregroundColor


###############################################################################
# Button
#
# Class for creating pushbuttons.  Extends Swing's JButton class.
#
# Methods:
#
# Button(label, event)
#   Creates a new pushbutton widget.
#   --label - A text label to be placed on the button.
#   --event - The user-defined event-handling function called when this button
#             is clicked.
###############################################################################

class Button(JButton, Widget):
   """
   Push Button
   """

   def __init__(self, label, eventFunction):
      """
      Create a new button
      """
      JButton.__init__(self, label)
      Widget.__init__(self)                     # set up listeners, etc.

      self.offset = (0,0)
      self.position = (0,0)
      self.display = None

      if eventFunction:
#***         buttonListener = ButtonListener(eventFunction)
         buttonListener = ButtonListener(self, eventFunction)    # passing self to send focus back to parent display when done handling the event
         self.addActionListener(buttonListener)


###############################################################################
# Checkbox
#
# Class for creating checkboxes.  Extends Swing's JCheckBox class.
#
# Methods:
#
# Checkbox()
# Checkbox(label)
# Checkbox(label, event)
#   Creates a new checkbox.
#   --label - A text label placed to the right of the checkbox
#   --event - The user-defined function called when this checkbox is checked or unchecked.  This is optional.
#
# isChecked()
#   Returns True if the Checkbox is checked, False if unchecked.
#
# check()
#   Sets the Checkbox to checked.
# uncheck()
#   Sets the Checkbox to unchecked.
###############################################################################

class Checkbox(JCheckBox, Widget):
   """
   Checkbox
   """

   def __init__(self, label="", eventFunction = None):
      """
      Create a new checkbox
      """
      JCheckBox.__init__(self, label)
      Widget.__init__(self)                     # set up listeners, etc.

      self.offset = (0,0)
      self.position = (0,0)
      self.display = None

      if eventFunction:
#         checkboxListener = ButtonListener(eventFunction)
         checkboxListener = CheckboxListener(self, eventFunction)    # passing self to send focus back to parent display when done handling the event
         self.addActionListener(checkboxListener)

   def isChecked(self):
      """
      Return True if this box is checked
      """
      return self.isSelected()

   def check(self):
      """
      Sets the checkbox to checked. This does NOT cause 'eventFunction' (if any) to be called.
      """
      self.setSelected(True)

   def uncheck(self):
      """
      Sets the checkbox to unchecked. This does NOT cause 'eventFunction' (if any) to be called.
      """
      self.setSelected(False)


###############################################################################
# Slider
#
# Class for creating sliders.  Extends Swing's JSlider class.
#
# Methods:
#
# Slider()
# Slider(orientation)
# Slider(orientation, lower, upper, start)
# Slider(orientation, lower, upper, start, eventHandler)
#   Creates a new slider.
#   --orientation - HORIZONTAL or VERTICAL.  By default, HORIZONTAL
#   --lower - An integer representing the lowest value the slider may represent.  
#              By default, 0.
#   --upper - An integer representing the highest value the slider may represent.  
#             By default, 100.
#             NOTE: lower and upper are inclusive.
#   --start - The beginning position of the slider.  By default, 50.
#   --eventHandler - The user-defined function, which is called whenever the
#             slider is changed.  This function would need to use the getValue()
#            function to get the new value of the slider.
#
# getValue()
#   Returns the current value of the slider.
###############################################################################

# Some constants

HORIZONTAL = JSlider.HORIZONTAL
VERTICAL = JSlider.VERTICAL

class Slider(JSlider, Widget):
   """
   Slider
   """

   #def __init__(self, eventHandler = None, lower = 0, upper = 100,
   #             start = None, orientation = HORIZONTAL):
   def __init__(self, orientation = HORIZONTAL, lower = 0, upper = 100,
                start = None, eventHandler = None):
      """
      Create a new Slider
      orientation - HORIZONTAL or VERTICAL
      lower - the lowest value the slider may take
      upper - the highest value the slider may take
      start - the beginning point of the slider
      """

      # adjust start position
      if start == None:
         start = (upper + lower) / 2   # set slider half way, initially
         
      JSlider.__init__(self, orientation, lower, upper, start)
      Widget.__init__(self)                     # set up listeners, etc.

      self.offset = (0,0)
      self.position = (0,0)
      self.display = None

      if eventHandler:
         #sliderListener = SliderListener(eventHandler)
         sliderListener = SliderListener(self, eventHandler)  # also, pass this object, so we can poll it
         self.addChangeListener(sliderListener)


###############################################################################
# DropDownList
#
# Class for adding a drop-down list of items, one of which can be selected.  
# Extends JComboBox.
#
# Methods:
#
# DropDownList()
#   Create a new drop-down list.
#
# addItem(item)
#   Adds a new item to the drop-down list.
#   --item - a string.
#
# addItemList(itemList)
#   Adds a list of strings to the drop-down list (instead of adding them one at
#   a time with addItem()).
#   --itemList - a list of items (strings) to be displayed in the drop-down list.
#
# getSelectedItem()
#   Returns the value of the currently selected item in this box (as a string).
###############################################################################

class DropDownList(JComboBox, Widget):
   """
   Drop-down List
   """
   def __init__(self, items = [""], eventHandler = None):
      """
      Create a new drop-down list
      """
      JComboBox.__init__(self)
      Widget.__init__(self)             # set up listeners, etc.

      self.offset = (0,0)
      self.position = (0,0)
      self.display = None
      
      self.__addItemList__(items)       # add provided items

      if eventHandler:
         #dropdownListener = DropDownListListener(eventHandler)
         dropdownListener = DropDownListListener(self, eventHandler)  # also, pass this object, so we can poll it
         self.addActionListener(dropdownListener)

   def __addItemList__(self, items):
      """
      Adds a list of items to the drop-down list
      """
      for item in items:
         self.addItem(item)


###############################################################################
# Font
#
# For example,
#
# Font("Serif", Font.ITALIC, 16)
#
# See http://docs.oracle.com/javase/tutorial/2d/text/fonts.html#logical-fonts


###############################################################################
# TextField
#
# Class for adding an input text field.  Extends Swing's JTextField class.
#
# Methods:
#
# TextField()
# TextField(text)
# TextField(text, columns)
# TextField(text, columns, eventHanlder)
#   Creates an empty text field with the specified initial text (a string),
#   and number of columns (a string).  Default is "" (empty string) and 8.
#
#
# eventHandler, if present, is passed the text entered by user (without the newline character
#   that trigger the call.
#
# setFont(), e.g., setFont( Font("Serif", Font.ITALIC, 16) )
#
# getText()
#   Returns the text contained in the text field (as a string).
#
# setText()
#   Sets the text contained in the text field (as a string).
###############################################################################

class TextField(JTextField, Widget):
   """
   Text field
   """

   def __init__(self, text = "", columns = 8,  eventHandler = None):
      """
      Create a new text field
      """
      JTextField.__init__(self, text, columns)
      Widget.__init__(self)                     # set up listeners, etc.

      self.offset = (0,0)
      self.position = (0,0)
      self.display = None

      if eventHandler:
         textFieldListener = TextFieldListener(self, eventHandler)  # also, pass this object, so we can poll it
         self.addActionListener(textFieldListener)


###############################################################################
# TextArea
#
# Class for adding an input text area.  Extends Swing's JTextArea class.
#
# Methods:
#
# TextArea()
# TextArea(text)
# TextArea(text, rows, columns)
#   Creates an empty text field with the specified initial text (a string),
#   and number of rows and columns.  Default is "" (empty string) and 5, 40.
#
# setFont(), e.g., setFont( Font("Serif", Font.ITALIC, 16) )
#
# getText()
#   Returns the text contained in the text field (as a string).
#
# setText()
#   Returns the text contained in the text area (as a string).
#
# setLineWrap()
#   Sets whether the text area will wrap lines or not.  If the setting is off, 
#   then a horizontal scroll bar will appear, as needed.
###############################################################################

class TextArea(JScrollPane, Widget):
   """
   Text area (provides vertical scrolling, as needed.)
   """

   def __init__(self, text = "", rows = 5, columns = 40):
      """
      Create a new text area
      """
      self.textArea = JTextArea(text, rows, columns)  # create the text area

      JScrollPane.__init__(self, self.textArea)       # wrap the text area in a scroll pane
      #JScrollPane.__init__(self)       # wrap the text area in a scroll pane
      Widget.__init__(self)                     # set up listeners, etc.

      # adjust scroll pane container
      #self.
      self.offset = (0,0)
      self.position = (0,0)
      self.display = None
      
      self.textArea.setEditable(True)
      self.setLineWrap(True)                # wrap lines that are too long (no horizontal scroll bar)
      self.textArea.setWrapStyleWord(True)  # wrap lines at word boundaries rather than at character boundaries

   def setLineWrap(self, setting = True):
      """
      Sets whether the text area will wrap lines or not.  If the setting is off, 
      then a horizontal scroll bar will appear, as needed.
      """
      self.textArea.setLineWrap(setting) 

   # NOTE:  No event handler is associated with this widget.  It is intended to be used in association with
   #        another widget (e.g., Button or MenuItem - to grab contents and redirect them elsewhere).
   # Therefore, we do not need to worry about doing anything special to give focus to the parent display
   # for event handling.  This will be taken care by the event handler of the associated widget (e.g., Button 
   # or MenuItem).


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


###############################################################################
# Icon
#
# Creates an icon to be added to a display specifying its left-bottom corner.
#
# NOTE:  We use the class name Icon here to avoid conflict with the additional provided library
#        image.py, which defines a similar class called Image.  Since we provide a shorthand
#        Display function called drawImage() which uses this Icon class, we are probably OK,
#        i.e., we can let both classes gui.Icon and image.Image coexist without confusion.
#

from math import *
#from java.awt import Rectangle as jRectangle   # used in Icon.rotate()

class Icon(JPanel, Widget):
   """
   Create an image object from provided filename, and resize according to width and height.
   """

   def __init__(self, filename, width = None, height = None):
      """
      """
      JPanel.__init__(self)
      Widget.__init__(self)                     # set up listeners, etc.

      # JEM working directory fix (see above)
      filename = fixWorkingDirForJEM( filename )   # does nothing if not in JEM
     
      # ***
      #print "fixWorkingDirForJEM( filename ) =", filename

      self.fileName = filename
      self.offset = (0,0)                # How much to compensate 
      self.position = (0,0)              # assume placement at a Display's origin
      self.display = None
      
      self.degrees = 0                   # used for icon rotation 

      self.icon = ImageIO.read(File(filename))
      iconWidth = self.icon.getWidth(None)
      iconHeight = self.icon.getHeight(None)
      
      # keep a deep copy of the image (useful for repeated scalings - we always scale from original
      # for higher quality)
      self.originalIcon = BufferedImage(self.icon.getWidth(), self.icon.getHeight(), self.icon.getType())
      self.originalIcon.setData( self.icon.getData() )
            
            
      # Does the user want to resize icon?
      if width == None and height == None:            # If not, use icon's width and height
         width = iconWidth
         height = iconHeight
      
      elif width > 0 and height == None:              # only width given

         height = iconHeight * width / iconWidth    # scale height proportionally to width

         # The user wanted to resize the icon, so resize it
         self.icon = self.__resizeIcon__(width, height)

         # Width and height has changed
         width = self.icon.getWidth(None)
         height = self.icon.getHeight(None)

      elif width == None and height > 0:              # only height given

         width = iconWidth * height / iconHeight    # scale width proportionally to height

         # The user wanted to resize the icon, so resize it
         self.icon = self.__resizeIcon__(width, height)

         # Width and height has changed
         width = self.icon.getWidth(None)
         height = self.icon.getHeight(None)

      elif width > 0 and height > 0:                 # both given (user wants to change aspect ratio?)

         # The user wanted to resize the icon, so resize it
         self.icon = self.__resizeIcon__(width, height)

         # Width and height has changed
         width = self.icon.getWidth(None)
         height = self.icon.getHeight(None)

      # Set the width of the panel to match that of the icon

      #self.setPreferredSize(Dimension(width+1, height+1))
      self.setPreferredSize(Dimension(width, height))
      #self.setSize(width, height)
 
#   def copy(self):
#
#      
#   def __getCopy__(self):
#      """
#      Returns a deep copy of the icon.
#      """
#   
#      # create a deep copy of the image
#      newIcon = BufferedImage(self.icon.getWidth(), self.icon.getHeight(), self.icon.getType())
#      newIcon.setData( self.icon.getData() )
#      
#      return newIcon


   def __resizeIcon__(self, width, height):
      """
      Returns a scaled version of the icon.
      """
      iconWidth = self.icon.getWidth(None)
      iconHeight = self.icon.getHeight(None)
      
      # for higher quality work from the original (useful in repeated scalings)

      # create the scaled icon
      #scaledIcon = Scalr.resize(self.originalIcon, Scalr.Method.ULTRA_QUALITY, Scalr.Mode.AUTOMATIC,
      #                          width, height, Scalr.OP_ANTIALIAS)
      #scaledIcon = Scalr.resize(self.originalIcon, Scalr.Method.QUALITY, Scalr.Mode.AUTOMATIC,
      #                          width, height, Scalr.OP_ANTIALIAS)
      #scaledIcon = Scalr.resize(self.originalIcon, Scalr.Method.SPEED, Scalr.Mode.AUTOMATIC,
      #                          width, height, Scalr.OP_ANTIALIAS)
      #scaledIcon = Scalr.resize(self.originalIcon, Scalr.Method.BALANCED, Scalr.Mode.AUTOMATIC,
      #                          width, height, Scalr.OP_ANTIALIAS)
      
      # use this to adjust image dimensions as expected (all above, retain proportions of image)
      scaledIcon = Scalr.resize(self.originalIcon, Scalr.Method.BALANCED, Scalr.Mode.FIT_EXACT,
                                width, height, Scalr.OP_ANTIALIAS)

      return scaledIcon

   def getPixel(self, col, row):
      """Returns a list of the RGB values for this pixel, e.g., [255, 0, 0].""" 
      
      # Obsolete - convert the row so that row zero refers to the bottom row of pixels.
      #row = self.height - row - 1

      color = Color(self.icon.getRGB(col, row))  # get pixel's color
      return [color.getRed(), color.getGreen(), color.getBlue()]  # create list of RGB values (0-255)

   def setPixel(self, col, row, RGBlist):
      """Sets this pixel's RGB values, e.g., [255, 0, 0].""" 
      
      # Obsolete - convert the row so that row zero refers to the bottom row of pixels.
      #row = self.height - row - 1

      color = Color(RGBlist[0], RGBlist[1], RGBlist[2])  # create color from RGB values
      self.icon.setRGB(col, row, color.getRGB())

      # some pixels have changed, so refresh display
      if self.display:
         self.display.display.repaint()

   def getPixels(self):
      """Returns a 2D list of pixels (col, row) - each pixel is a list of RGB values, e.g., [255, 0, 0].""" 
      
      pixels = []                      # initialize list of pixels
      #for row in range(self.height-1, 0, -1):   # load pixels from image      
      for row in range(0, self.getHeight()):   # load pixels from image      
         pixels.append( [] )              # add another empty row
         for col in range(self.getWidth()):    # populate row with pixels    
            # RGBlist = self.getPixel(col, row)   # this works also (but slower)    
            color = Color(self.icon.getRGB(col, row))  # get pixel's color
            RGBlist = [color.getRed(), color.getGreen(), color.getBlue()]  # create list of RGB values (0-255)
            pixels[-1].append( RGBlist )   # add a pixel as (R, G, B) values (0-255, each)

      # now, 2D list of pixels has been created, so return it
      return pixels

   def setPixels(self, pixels):
      """Sets image to the provided 2D list of pixels (col, row) - each pixel is a list of RGB values, e.g., [255, 0, 0].""" 
      
      height = len(pixels)        # get number of rows
      width  = len(pixels[0])     # get number of columns (assume all columns have same length
      
      #for row in range(self.height-1, 0, -1):   # iterate through all rows      
      for row in range(0, height):   # iterate through all rows     
         for col in range(width):    # iterate through every column on this row
         
            RGBlist = pixels[row][col]
            #self.setPixel(col, row, RGBlist)   # this works also (but slower)
            color = Color(RGBlist[0], RGBlist[1], RGBlist[2])  # create color from RGB values
            self.icon.setRGB(col, row, color.getRGB())

      # some pixels have changed, so refresh display
      if self.display:
         self.display.display.repaint()

   def setSize(self, width, height):
      """
      Change the size of this icon.
      """

      # The user wanted to resize the icon, so resize it
      self.icon = self.__resizeIcon__(width, height)
      
      # Set the width of the panel to match that of the icon
      self.setPreferredSize(Dimension(width, height))

      if self.display:
         # refresh JPanel placement on display
         xPosition, yPosition = self.position
         self.setBounds(xPosition, yPosition, width, height)
         self.display.display.repaint()

   def setWidth(self, width):
      """
      Change the width of this icon.
      """
      self.setSize( width, self.getHeight() )

   def setHeight(self, height):
      """
      Change the width of this icon.
      """
      self.setSize( self.getWidth(), height )

   def getWidth(self):
      """
      Returns the width of this icon.
      """
      return self.icon.getWidth(None)
      
   def getHeight(self):
      """
      Returns the height of this icon.
      """
      return self.icon.getHeight(None)

   def crop(self, x, y, width, height):
      """
      Crop the icon starting at point x, y and using the provided width and height.
      """

      # crop it!
      # (see http://stackoverflow.com/questions/2386064/how-do-i-crop-an-image-in-java)
      self.icon = self.icon.getSubimage(x, y, width, height)

      # Set the width of the panel to match that of the icon
      self.setPreferredSize(Dimension(width, height))

      if self.display:
         # refresh JPanel placement on display
         xPosition, yPosition = self.position
         self.setBounds(xPosition, yPosition, width, height)
         self.display.display.repaint()
         

#   def __rotateIcon__(self, degrees):
#      """
#      Returns a rotated version of the icon.
#      """
#      
#      # Now, create the rotated icon.  See the following link:
#      # http://stackoverflow.com/questions/4156518/rotate-an-image-in-java
#     
#      angle = radians(degrees)
#
#      w = self.getWidth()
#      h = self.getHeight()
#      sine = abs(sin(angle))
#      cosine = abs(cos(angle))
#      neww = int( floor(w*cosine+h*sine) )
#      newh = int( floor(h*cosine+w*sine) )
#      
#      # Make a new icon
#      rotatedIcon = BufferedImage(neww, newh, Transparency.TRANSLUCENT)
#      # Grab something to draw on
#      g = rotatedIcon.createGraphics()
#      g.rotate(angle, w/2, h/2)
#      g.drawRenderedImage(self.icon, None)
#      g.dispose()
#      return rotatedIcon

   def rotate(self, degrees):
      """
      Rotates the image angle degrees.
      """
      
      # Actually, we do not rotate self.image.  We rotate the rendering of it - see paint()
      
      self.degrees = self.degrees + degrees  # accumulate rotation

# NOTE:  Trying to resize JPanel so it doesn't crop rotated image - but it doesn't work
#        as expected... Hmmmm, what to do?
#      # resize JPanel to fit image
#      angle = radians(self.degrees)
#      width = self.getWidth()
#      height = self.getHeight()
#      sine = abs(sin(angle))
#      cosine = abs(cos(angle))
#      
#      # calculate rotated icon's width and height (given rotation angle)
#      newWidth = int( floor( width*cosine + height*sine ) )
#      newHeight = int( floor( height*cosine + width*sine ) )
#      self.setPreferredSize(Dimension(newWidth, newHeight))
#      print newWidth, newHeight

      if self.display:
         self.display.display.repaint()
      

   def paint(self, graphics2DContext):
      """
      Paint me on the display.
      """

      # rotate rendring of icon as needed
      #icon = self.__rotateIcon__(self.degrees)
      x = self.getWidth()/2
      y = self.getHeight()/2
      angle = radians(self.degrees)
      graphics2DContext.rotate(angle, x, y)  # rotate icon

      # draw it!  (unforunately, this may crop icon)
      #graphics2DContext.drawImage(icon, 0, 0, None)
      graphics2DContext.drawImage(self.icon, 0, 0, None)
      
      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation 

#   def paint(self, graphicsContext):
#      """
#      Paint me on the display.
#      """
#      # Draw it!
#      graphicsContext.drawImage(self.icon, 0, 0, None)
#      
#      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation 


#   def paint(self, graphicsContext):
#      """
#      Paint self.icon on the display.
#      """
#
#      # But first, do any needed rotation.  See the following link:
#      # http://stackoverflow.com/questions/4156518/rotate-an-image-in-java
#     
#      angle = radians(self.degrees)
#
#      # do preliminary stuff for efficiency
#      width = self.getWidth()
#      height = self.getHeight()
#      sine = abs(sin(angle))
#      cosine = abs(cos(angle))
#      
#      # calculate rotated icon's width and height (given rotation angle)
#      newWidth = int( floor( width*cosine + height*sine ) )
#      newHeight = int( floor( height*cosine + width*sine ) )
#      
#      # make a buffer to store a rotated copy of the original icon (we do NOT
#      # modify self.icon, only its copy)
#      rotatedIcon = BufferedImage(newWidth, newHeight, Transparency.TRANSLUCENT)
#      
#      # create a temporary graphics context for drawing a rotated copy of self.icon
#      # (Java docs warn against using default graphics context for this - hence the temp graphics context)
#      g = rotatedIcon.createGraphics()
#      g.rotate(angle, width/2, height/2)   # rotate using icon's center as rotation point
#      g.drawRenderedImage(self.icon, None) # now 'rotatedIcon' has been rendered
#      g.dispose()   # not needed anymore
#
#      # Draw it!
#      graphicsContext.drawImage(rotatedIcon, 0, 0, None)
#      
#      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation 


###############################################################################
# Drawable Objects
#
# These classes are all used by Display's paint method.  The paint method will
# call the paint method of each of these to create an image on the display
#

# Line
#
# Creates a line to be added to a display.

class Line(JPanel, Widget, Drawable):
   """
   A simple line specified through its end points.
   """

   def __init__(self, x1, y1, x2, y2, color = Color.BLACK, thickness = 1):
      """
      Create a new line
      """
      JPanel.__init__(self)
      Widget.__init__(self)                            # set up listeners, etc.
      Drawable.__init__(self, color, True, thickness)  # set up color, fill (always True for lines), thickness, etc.

      # NOTE: Line will be draw inside a JPanel (a rectangle) that as big as the line dimensions, i.e.,
      # the JPanel tightly encloses the line.  This means the original line coordinates have to be mapped
      # the internal JPanel coordinates (0,0 is at top left), and also to the JPanel's position within
      # the display (when the Line object is eventually added to a display).
       
      # handle various line orientations (different quadrants)
      dx = abs(x2-x1)
      dy = abs(y2-y1)
      self.halfThick = self.thickness/2   # adjustment for drawing

      self.offset = (0,0)        # offset of object placement relative to the first (x,y) point (no offset for lines)

      # let's determine the top-left corner of the line's enclosing box (note that even a diagonal line
      # will have an enclosing box that's parallel to the screen).
      x = min(x1, x2)    # get left-most line x coordinate
      y = min(y1, y2)    # get left-most line y coordinate
      
      self.position = ( x-self.halfThick, y-self.halfThick )  # position of the JPanel in the display (when added)
      self.display = None

      # set hight and width of the JPanel to the dimensions of the bounding box for this line (JPanel needs to be
      # big enough so that the line is drawn completely in it (i.e., it is not cropped)
      self.setPreferredSize(Dimension( dx+self.thickness+1,  dy+self.thickness+1 ))
      self.setSize( dx+self.thickness+1,  dy+self.thickness+1 )
      #self.setPreferredSize(Dimension( dx+self.thickness,  dy+self.thickness ))
      #self.setSize( dx+self.thickness,  dy+self.thickness )
      
      # is line orientation (i.e., think of a clock hour-hand) is 6-9 o'clock or 9-12 o'clock?
      if x1 > x2:  
         self.startX_JPanel = dx
         self.endX_JPanel   = 0
      else:
         self.startX_JPanel = 0
         self.endX_JPanel = dx
         
      # is line orientation (i.e., think of a clock hour-hand) is 9-12 o'clock or 12-3 o'clock?
      if y1 > y2:  
         self.startY_JPanel = dy
         self.endY_JPanel   = 0
      else:
         self.startY_JPanel = 0
         self.endY_JPanel = dy

   def paint(self, graphics2DContext):
      """
      Paint me on the display
      """

      # set color and draw it
      graphics2DContext.setPaint(self.color)   
      # using CAP_BUTT for line ends, to ensure that lines "line" up regardless of thickness
      # (see http://www.zetcode.com/gfx/java2d/basicdrawing/)
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND) )
      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
      graphics2DContext.drawLine(self.startX_JPanel+self.halfThick, self.startY_JPanel+self.halfThick, self.endX_JPanel+self.halfThick, self.endY_JPanel+self.halfThick)
      
      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation 


# Circle
#
# Creates a circle to be added to a display.

class Circle(JPanel, Widget, Drawable):
   """
   A simple circle
   """
   
   def __init__(self, x, y, radius, color = Color.BLACK, fill = False, thickness=1):
      """
      Create a new circle
      """
      JPanel.__init__(self)
      Widget.__init__(self)                 # set up listeners, etc.
      Drawable.__init__(self, color, fill, thickness)  # set up color, fill, thickness, etc.

      self.radius = radius
      self.diameter = self.radius*2
      self.halfThick = self.thickness/2   # adjustment for drawing

      # NOTE: Circle will be draw inside a JPanel (a rectangle) that as big as the circle's dimensions, i.e.,
      # the JPanel tightly encloses the circle.  This means the original coordinates have to be mapped
      # the internal JPanel coordinates (0,0 is at top left), and also to the JPanel's position within
      # the display (when the Circle object is eventually added to a display).

      self.offset = (self.radius, self.radius)   # offset circle inside JPanel according to its center
      self.position = (x-self.halfThick, y-self.halfThick)
      self.display = None

      # JPanel should be big enough to enclose the circle
      self.setPreferredSize(Dimension( self.diameter+self.thickness+1, self.diameter+self.thickness+1))
      self.setSize( self.diameter+self.thickness+1, self.diameter+self.thickness+1)
      #self.setPreferredSize(Dimension( self.diameter+self.thickness, self.diameter+self.thickness))
      #self.setSize( self.diameter+self.thickness, self.diameter+self.thickness)
 

   # NOTE: Here we overload the Widget __remapCoordinates__() function, since Circle objects have
   # their own special way to think of their position in an enclosing Display, i.e., NOT relative to
   # their top-left corner, but relative to their center.
   def __remapCoordinates__(self, x, y):
      """
      Adjust the coordinates relative to the underlying display.
      """
      x = x + self.position[0] - self.radius
      y = y + self.position[1] - self.radius

      return x, y

   def paint(self, graphics2DContext):
      """
      Paint me on the display
      """

      # set color, and draw it
      graphics2DContext.setPaint(self.color)        
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_BUTT, BasicStroke.JOIN_ROUND) )
      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
      graphics2DContext.drawOval(0+self.halfThick, 0+self.halfThick, self.diameter, self.diameter)
      if self.fill:    # do we need to fill the circle?
         graphics2DContext.fillOval(0+self.halfThick, 0+self.halfThick, self.diameter, self.diameter)
      
      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation 


# Point
#
# Creates a point to be added to a display.

class Point(Circle):
   """
   A simple point
   """

   def __init__(self, x, y, color=Color.BLACK, thickness=1):
      """
      Create a new point
      """
      # a point is a circle of radius = thickness
      Circle.__init__(self, x, y, thickness, color, True, 0)


# Oval
#
# Creates an oval to be added to a display.

class Oval(JPanel, Widget, Drawable):
   """
   A simple oval
   """

   def __init__(self, x1, y1, x2, y2, color = Color.BLACK, fill = False, thickness = 1):
      """
      Create a new oval using the coordinates of its enclosing rectangle.
      """
      JPanel.__init__(self)
      Widget.__init__(self)                 # set up listeners, etc.
      Drawable.__init__(self, color, fill, thickness)  # set up color, fill, thickness, etc.

      # NOTE: Oval will be draw inside a JPanel (a rectangle) that as big as the oval's enclosing box,
      # i.e., the JPanel tightly encloses the oval.  This means the original oval coordinates have to be 
      # mapped the internal JPanel coordinates (0,0 is at top left), and also to the JPanel's position within
      # the display (when the Oval object is eventually added to a display).
       
      dx = abs(x2-x1)     # width
      dy = abs(y2-y1)     # height
      self.halfThick = self.thickness/2   # adjustment for drawing

      self.offset = (0,0)        # offset of object placement relative to the first (x,y) point (no offset for rectangles)

      # let's determine the top-left corner of the oval's enclosing box.
      x = min(x1, x2)    # get left-most line x coordinate
      y = min(y1, y2)    # get left-most line y coordinate
      self.position = ( x-self.halfThick, y-self.halfThick )  # position of the JPanel in the display (when added)
      self.display = None

      # JPanel should be big enough to contain the enclosing box
      self.setPreferredSize(Dimension( dx+self.thickness+1,  dy+self.thickness+1 ))
      self.setSize( dx+self.thickness+1,  dy+self.thickness+1 )
      #self.setPreferredSize(Dimension( dx+self.thickness,  dy+self.thickness ))
      #self.setSize( dx+self.thickness,  dy+self.thickness )

      # make sure we end up with top-left and bottom-right corners
      self.startX_JPanel = 0 + self.halfThick
      self.startY_JPanel = 0 + self.halfThick
      self.endX_JPanel = dx
      self.endY_JPanel = dy

   def paint(self, graphics2DContext):
      """
      Paint me on the display
      """
      
      # set color, rounded ends, and draw it
      graphics2DContext.setPaint(self.color)        
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )
      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
      graphics2DContext.drawOval(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel)
      if self.fill:    # do we need to fill the rectangle?
         graphics2DContext.fillOval(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel)
      
      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation 


# Rectangle
#
# Creates a rectangle to be added to a display.

class Rectangle(JPanel, Widget, Drawable):
   """
   A simple rectangle specified by two diagonal corners.
   """

   def __init__(self, x1, y1, x2, y2, color = Color.BLACK, fill = False, thickness=1):
      """
      Create a new rectangle
       """
     
      JPanel.__init__(self)
      Widget.__init__(self)                 # set up listeners, etc.
      Drawable.__init__(self, color, fill, thickness)  # set up color, fill, thickness, etc.

      # NOTE: Rectangle will be draw inside a JPanel (a rectangle) that as big as the rectangle's dimensions,
      # i.e., the JPanel tightly encloses the rectangle.  This means the original rectangle coordinates have
      # to be mapped the internal JPanel coordinates (0,0 is at top left), and also to the JPanel's position
      # within the display (when the Rectangle object is eventually added to a display).
       
      dx = abs(x2-x1)     # width
      dy = abs(y2-y1)     # height
      self.halfThick = self.thickness/2   # adjustment for drawing

      self.offset = (0,0)        # offset of object placement relative to the first (x,y) point (no offset for rectangles)

      # let's determine the top-left corner
      x = min(x1, x2)    # get left-most line x coordinate
      y = min(y1, y2)    # get left-most line y coordinate
      self.position = ( x-self.halfThick, y-self.halfThick )  # position of the JPanel in the display (when added)
      self.display = None

      # JPanel should be big enough to contain the rectangle
      self.setPreferredSize(Dimension( dx+self.thickness+1,  dy+self.thickness+1 ))
      self.setSize( dx+self.thickness+1,  dy+self.thickness+1 )
      #self.setPreferredSize(Dimension( dx+self.thickness,  dy+self.thickness ))
      #self.setSize( dx+self.thickness,  dy+self.thickness )

      # make sure we end up with top-left and bottom-right corners
      self.startX_JPanel = 0 + self.halfThick
      self.startY_JPanel = 0 + self.halfThick
      self.endX_JPanel = dx
      self.endY_JPanel = dy

   def paint(self, graphics2DContext):
      """
      Paint me on the display
      """

      # set color, rounded ends, and draw it
      graphics2DContext.setPaint(self.color)        
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )
      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
      graphics2DContext.drawRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel)
      if self.fill:    # do we need to fill the rectangle?
         graphics2DContext.fillRect(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel)
      
      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation 

         
# Arc
#
# Creates an arc to be added to a display.

class Arc(JPanel, Widget, Drawable):
   """
   An arc specified by two diagonal corners, the start angle, and the end angle.  Angles are interpreted such that 0 degrees is 
   at the three o'clock position. A positive value indicates a counter-clockwise rotation while 
   a negative value indicates a clockwise rotation.
   """

   def __init__(self, x1, y1, x2, y2, startAngle, endAngle, color = Color.BLACK, fill = False, thickness=1):
      """
      Create a new arc
      """
     
      JPanel.__init__(self)
      Widget.__init__(self)                 # set up listeners, etc.
      Drawable.__init__(self, color, fill, thickness)  # set up color, fill, thickness, etc.

      # NOTE: Arc will be draw inside a JPanel (a rectangle) that as big as the rectangle's dimensions,
      # i.e., the JPanel tightly encloses the rectangle.  This means the original rectangle coordinates have
      # to be mapped the internal JPanel coordinates (0,0 is at top left), and also to the JPanel's position
      # within the display (when the Rectangle object is eventually added to a display).
       
      dx = abs(x2-x1)     # width
      dy = abs(y2-y1)     # height
      self.halfThick = self.thickness/2   # adjustment for drawing

      self.offset = (0,0)        # offset of object placement relative to the first (x,y) point (no offset for rectangles)

      # let's determine the top-left corner
      x = min(x1, x2)    # get left-most line x coordinate
      y = min(y1, y2)    # get left-most line y coordinate
      self.position = ( x-self.halfThick, y-self.halfThick )  # position of the JPanel in the display (when added)
      self.display = None

      # JPanel should be big enough to contain the rectangle
      self.setPreferredSize(Dimension( dx+self.thickness+1,  dy+self.thickness+1 ))
      self.setSize( dx+self.thickness+1,  dy+self.thickness+1 )
      #self.setPreferredSize(Dimension( dx+self.thickness,  dy+self.thickness ))
      #self.setSize( dx+self.thickness,  dy+self.thickness )

      # make sure we end up with top-left and bottom-right corners
      self.startX_JPanel = 0 + self.halfThick
      self.startY_JPanel = 0 + self.halfThick
      self.endX_JPanel = dx
      self.endY_JPanel = dy
      
      # remember angles
      self.startAngle = startAngle
      self.arcAngle = endAngle - startAngle  # calculate arcAngle (as needed by drawArc() and fillArc()
      

   def paint(self, graphics2DContext):
      """
      Paint me on the display
      """

      # set color, rounded ends, and draw it
      graphics2DContext.setPaint(self.color)        
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )
      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
      graphics2DContext.drawArc(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel, self.startAngle, self.arcAngle)
      if self.fill:    # do we need to fill the arc?
         graphics2DContext.fillArc(self.startX_JPanel, self.startY_JPanel, self.endX_JPanel, self.endY_JPanel, self.startAngle, self.arcAngle)
      
      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation 


# Polygon
#
# Creates a polygon to be added to a display.

from jarray import array   # needed to convert Python lists to Java arrays (below)

class Polygon(JPanel, Widget, Drawable):
   """
   A polygon specified by two parallel lists of x and y coordinates.
   """

   def __init__(self, xPoints, yPoints, color = Color.BLACK, fill = False, thickness=1):
      """
      Create a new polygon
       """
     
      JPanel.__init__(self)
      Widget.__init__(self)                 # set up listeners, etc.
      Drawable.__init__(self, color, fill, thickness)  # set up color, fill, thickness, etc.

      # NOTE: Polygon will be draw inside a JPanel (a rectangle) that as big as the polygon's dimensions,
      # i.e., the JPanel tightly encloses the polygon.  This means the original polygon coordinates have
      # to be mapped the internal JPanel coordinates (0,0 is at top left), and also to the JPanel's position
      # within the display (when the polygon object is eventually added to a display).
       
      dx = max(xPoints)-min(xPoints)     # width
      dy = max(yPoints)-min(yPoints)     # height
      self.halfThick = self.thickness/2   # adjustment for drawing

      # let's determine the top-left corner of the enclosing box
      minX = min(xPoints)    # get left-most line x coordinate
      minY = min(yPoints)    # get left-most line y coordinate

      self.offset = (0,0)        # offset of object placement relative to the first (x,y) point (no offset for polygons)

      self.position = ( minX-self.halfThick, minY-self.halfThick )  # position of the JPanel in the display (when added)
      self.display = None

      # JPanel should be big enough to contain the polygon
      self.setPreferredSize(Dimension( dx+self.thickness+1,  dy+self.thickness+1 ))
      self.setSize( dx+self.thickness+1,  dy+self.thickness+1 )
      #self.setPreferredSize(Dimension( dx+self.thickness,  dy+self.thickness ))
      #self.setSize( dx+self.thickness,  dy+self.thickness )

      # adjust points for thickness and positioning within panel
      self.xPoints = [x + self.halfThick - minX for x in xPoints]
      self.yPoints = [y + self.halfThick - minY for y in yPoints]
            
      # convert to Java arrays (needed by drawPolygon() and fillPolygon() functions below)
      self.xPoints = array(self.xPoints, 'i')
      self.yPoints = array(self.yPoints, 'i')
      
   def paint(self, graphics2DContext):
      """
      Paint me on the display
      """

      # set color, rounded ends, and draw it
      graphics2DContext.setPaint(self.color)        
      graphics2DContext.setStroke( BasicStroke(self.thickness, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND) )
      graphics2DContext.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
      graphics2DContext.drawPolygon(self.xPoints, self.yPoints, len(self.xPoints))
      if self.fill:    # do we need to fill the rectangle?
         graphics2DContext.fillPolygon(self.xPoints, self.yPoints, len(self.xPoints))
      
      Toolkit.getDefaultToolkit().sync()  # sync graphics for animation 



###### GUI CONTROLS ###################################

# import additional GUI controls (new as of v3.6) 
from guicontrols import *

                       

###### Unit Tests ###################################

if __name__ == "__main__":

   # let's create a few displays and place some things on them.

### FIRST DISPLAY TEST ###

   # create display
   display1 = Display("First Display", 600, 400, 0, 0)     
   display1.show()     
   
   display1.setToolTipText("I am a display")  # add tooltip
    
   # a circle       
   circle1 = Circle(150, 150, 5)
   display1.place(circle1)
   
   # a line
   line1 = Line(100, 50, 300, 400)
   display1.place(line1)
    
   # more circles
   circle2 = Circle(0, 0, 100)
   display1.place(circle2)
   circle3 = Circle(100, 100, 100)
   display1.place(circle3)  
    
   # a circle       
   circle4 = Circle(0, 0, 5)
   display1.place(circle4, 0, 0)
   
   # another line             
   line2 = Line(0, 0, 300, 400)   
   display1.place(line2)       
    
   # a point
   point1 = Point(200, 200)
   display1.place(point1)
      
   # a rectangle
   rectangle1 = Rectangle(0, 0, 300, 250)
   display1.place(rectangle1)
   rectangle1.setColor(Color.ORANGE)
   #rectangle1.setColor(Color.BLACK) 
   
   # a few icons (with resizing)
   icon1 = Icon("musicalNote.jpg", width=50)
   display1.place(icon1, 0, 0)
   icon2 = Icon("musicalNote.jpg", height=50)
   display1.place(icon2, 50, 50)
   icon3 = Icon("musicalNote.jpg", width=50, height=50)
   display1.place(icon3, 100, 100)
   icon4 = Icon("musicalNote.jpg")
   display1.place(icon4, 0, 0)
   
   # add a few tooltips
   # NOTE - tooltips work best with rectangular objects (since the 
   # tootltip is associated with the bounding box (this can look really confusing
   # on a line, or circle)
   icon4.setToolTipText("I am a note")     # add tooltip
   
   # Test Label
   label1 = Label("hi!                                     ")
   display1.place(label1, 300, 300)
   
   # display keyboard listener
   def echo(key):
      label1.setText("key = " + str(key) + ", char = '" + chr(key) + "'")
      print "key, char = ", key, chr(key)
#      label1.setText("key = " + str(key))
#      print "key, char = ", key

   display1.onKeyDown( echo ) # echo keystrokes typed
   display1.onKeyUp( echo ) # echo keystrokes typed
#   display1.onKeyType( echo ) # echo keystrokes typed
   
   # callback to remove last image from display,
   # when mouse is pressed
   def removeImage(x, y):
      display1.remove(icon4)

   # register callback
   display1.onMouseClick( removeImage )  # remove last image when mouse clicked   
   
   
### SECOND DISPLAY TEST ###

   from music import *
   
   # create display
   display2 = Display("Second Display - GUI Widgets", 600, 400, 50, 50)     
   display2.show()     
   
   # Test Label
   l1 = Label("hi!                ")
   display2.place(l1, 520, 40)
   
   l1.setSize(40, 80)   # resize label  (*** setSize should call repaint, etc.)
   display2.place(l1, 520, 40)
   
   # define a function to handle display keyboard press/release events
   def echo1(key):
      """Display keyboard press/release events on label l1."""
      l1.setText("key =" + str(key))

   # when a key is typed on display2, call the above function to update label l1       
   display2.onKeyDown( echo1 ) # echo keys pressed
   #display2.onKeyUp( echo1 ) # echo keys released

   # also when a mouse action occurs, call the above function to update label l1       
   # with the mouse coordinates
   def printMouseCoordinates(x, y):
      l1.setText( "(" + str(x) + ", " + str(y) + ")" )
      
   display2.onMouseClick( printMouseCoordinates )
   display2.onMouseDrag( printMouseCoordinates )
   display2.onMouseMove( printMouseCoordinates )
   
   # Now, let's create two buttons, one that starts a note, another that ends it
   
   # To operate, each button requires a function that performs what 
   # the button does when pressed.  When defining the buttons, we
   # associate them with the proper function.
   
   def startA4():
      Play.noteOn(A4)
      
   def endA4():
      Play.noteOff(A4)
      
   button1 = Button("Start note", startA4)
   button2 = Button("End note", endA4)
   
   # now, place them on the display, so they can be used
   display2.place(button1, 30, 40)
   display2.place(button2, 140, 40)
   
   
   # create a slider and label pair (label displays slider's value)
   l2 = Label("slider =        ")
   display2.place(l2, 40, 150)
   
   def updateLabel( value ):
      l2.setText( "slider = " + str(value) )
      
   #Slider(orientation, lower, upper, start, eventHandler)
   s2 = Slider( eventHandler = updateLabel )
   display2.place(s2, 40, 100)
   
   
   # DropDownList test
   l3 = Label("selected item =                ")
   display2.place(l3, 250, 150)
   
   def updateLabel3( value ):
      l3.setText( "selected item = " + value )
   
   ddl = DropDownList(["", "first", "second", "third"], updateLabel3 )
   #ddl.addItemList( ["", "first", "second", "third"] )
   display2.place(ddl, 250, 100)

   # TextField test
   l4 = Label("text field =                                   ")
   display2.place(l4, 20, 350)
   
   def updateLabel4( value ):
      l4.setText( "text field = " + value )
      tf.setText("")   # clear the text field (a bit awkward - but necessary)
   
   # TextField(columns, text, eventHanlder)
   tf = TextField("type and hit <ENTER> ", 18, updateLabel4 )
   display2.place(tf, 20, 300)
   
   # or, we could leave the textField without an event handler, and instead
   # define a button, which, when pressed (i.e., its event handler) grabs
   # the textField's text and does whatever needs to be done with it.

   # TextArea test
   
   # TextArea(rows, columns, text)
   ta = TextArea("", 7, 15)
   display2.place(ta, 400, 250)
   
   # add a couple of menus
   m = Menu("Test")

   def oneFunction():    # callback function for item one 
     l3.setText("one")

   def twoFunction():    # callback function for item two
     l3.setText("two")

   def threeFunction():  # callback function for item three
     l3.setText("three")

   # build menu (i.e., add items to it)
   m.addItem("one", oneFunction)
   m.addSeparator()   # ---------------------------
   m.addItemList(["two", "three"], [twoFunction, threeFunction])
   m.addSeparator()   # ---------------------------

   # create a submenu...
   m1 = Menu("submenu")
   m1.addItemList(["one", "two", "three"], [oneFunction, twoFunction, threeFunction])
   
   m.addSubMenu(m1)  # and add it to the menu
   
   display2.addMenu(m)  # add the menu to the display


### THIRD DISPLAY TEST ###

   from music import *
   
   # create display
   display3 = Display("Third Display - Music", 600, 400, 100, 100)     
   display3.show()     
   
   def playMidiNote1():
      Play.midi( Note(A4, QN) )
      
   def playMidiNote2():
      Play.midi( Note(C5, QN) )

   button1 = Button("Start A4", playMidiNote1)
   button2 = Button("Start C5", playMidiNote2)
   
   # now, place them on the display, so they can be used
   display3.place(button1, 30, 40)
   display3.place(button2, 30, 70)
   
   # also test two checkboxes
   def playMidiNote3(checkboxState):
      if checkboxState:    # is the checkbox set?
         Play.noteOn(A4)      # if so, start note
      else:                # otherwise
         Play.noteOff(A4)     # stop note

   def playMidiNote4(checkboxState):
      if checkboxState:    # is the checkbox set?
         Play.noteOn(C5)      # if so, start note
      else:                # otherwise
         Play.noteOff(C5)     # stop note

   checkbox1 = Checkbox("Toggle A4", playMidiNote3)
   checkbox2 = Checkbox("Toggle C5", playMidiNote4)

   # now, place them on the display, so they can be used
   display3.place(checkbox1, 30, 140)
   display3.place(checkbox2, 30, 160)
 
   
### FOURTH DISPLAY TEST ###

   # create display
   display4 = Display("Fourth Display - Graphics objects", 600, 400, 150, 150)     
   display4.show()     
   
   # Line tests
#   line1 = Line(100, 150, 200, 300)  # x1 < x2 and y1 < y2   (orientation 3-6 o'clock)
#   display4.add(line1) 
#   line1 = Line(200, 150, 100, 300)  # x1 > x2 and y1 < y2   (orientation 6-9 o'clock)
#   display4.add(line1)             
#   line1 = Line(150, 300, 250, 150)  # x1 < x2 and y1 > y2   (orientation 12-3 o'clock)
#   display4.add(line1)             
#   line1 = Line(250, 300, 150, 150)  # x1 > x2 and y1 > y2   (orientation 9-12 o'clock)
#   display4.add(line1) 

   #  more convenient   
   display4.drawLine(100, 150, 200, 300)  # x1 < x2 and y1 < y2   (orientation 3-6 o'clock)
   display4.drawLine(200, 150, 100, 300)  # x1 > x2 and y1 < y2   (orientation 6-9 o'clock)
   display4.drawLine(150, 300, 250, 150)  # x1 < x2 and y1 > y2   (orientation 12-3 o'clock)
   display4.drawLine(250, 300, 150, 150)  # x1 > x2 and y1 > y2   (orientation 9-12 o'clock)
   
   # pairs of lines (RED with thickness 10, and BLACK with thickness 1 superimposed)
   # various orientations
#   l1 = Line(50, 50, 100, 100, Color.RED, 10)
#   display4.add(l1)                          
#   l1 = Line(50, 50, 100, 100, Color.BLACK)  
#   display4.add(l1)                        
#   l1 = Line(50, 150, 150, 150, Color.RED, 10)
#   display4.add(l1)                           
#   l1 = Line(50, 150, 150, 150, Color.BLACK)  
#   display4.add(l1)                         
#   l1 = Line(50, 200, 50, 300, Color.BLACK) 
#   display4.add(l1)                        
#   l1 = Line(50, 200, 50, 300, Color.RED, 10)
#   display4.add(l1)                          
#   l1 = Line(50, 200, 50, 300, Color.BLACK)  
#   display4.add(l1)          
#   l1 = Line(80, 300, 200, 200, Color.RED, 10)   
#   display4.add(l1)                           
#   l1 = Line(80, 300, 200, 200, Color.BLACK)  
#   display4.add(l1)      

   # more convenient way   
   display4.drawLine(50, 50, 100, 100, Color.RED, 10)
   display4.drawLine(50, 50, 100, 100, Color.BLACK)  
   display4.drawLine(50, 150, 150, 150, Color.RED, 10)
   display4.drawLine(50, 150, 150, 150, Color.BLACK)  
   display4.drawLine(50, 200, 50, 300, Color.BLACK) 
   display4.drawLine(50, 200, 50, 300, Color.RED, 10)
   display4.drawLine(50, 200, 50, 300, Color.BLACK)  
   display4.drawLine(80, 300, 200, 200, Color.RED, 10)   
   display4.drawLine(80, 300, 200, 200, Color.BLACK)  

   # Circle tests
#   c1 = Circle(150, 150, 20, Color.RED, False, 15)
#   display4.add(c1)
#   c1 = Circle(150, 150, 20)
#   display4.add(c1)

   # more convenient way   
   display4.drawCircle(150, 150, 20, Color.RED, False, 15)
   display4.drawCircle(150, 150, 20)
   
   # Point tests
#   p1 = Point(250, 250, Color.ORANGE, 5)
#   display4.add(p1)
#   p1 = Point(250, 250) 
#   display4.add(p1)

   # more convenient way   
   display4.drawPoint(250, 250, Color.ORANGE, 5)
   display4.drawPoint(250, 250) 
   
   # Rectangle tests
#   rec1 = Rectangle(50, 50, 150, 100, Color.ORANGE, False, 15)
#   display4.add(rec1)                                         
#   rec1 = Rectangle(50, 50, 150, 100)                         
#   display4.add(rec1)                

   # more convenient way   
   display4.drawRectangle(50, 50, 150, 100, Color.ORANGE, False, 15)
   display4.drawRectangle(50, 50, 150, 100)                         
                  
   # Oval tests
#   o1 = Oval(300, 50, 400, 100, Color.ORANGE, False, 15)
#   display4.add(o1)                                         
#   o1 = Oval(300, 50, 400, 100)                         
#   display4.add(o1)                

   # more convenient way   
   display4.drawOval(300, 50, 400, 100, Color.ORANGE, False, 15)
   display4.drawOval(300, 50, 400, 100)                         

   # Polygon tests
#   p = Polygon([312, 366, 510, 443], [244, 210, 312, 346], Color.ORANGE, False, 15) 
#   display4.add(p)
#   p = Polygon([312, 366, 510, 443], [244, 210, 312, 346])                         
#   display4.add(p)
    
   # more convenient way   
   display4.drawPolygon([312, 366, 510, 443], [244, 210, 312, 346], Color.ORANGE, False, 15) 
   display4.drawPolygon([312, 366, 510, 443], [244, 210, 312, 346])                         
   
   # drawLabel test (notice how the draw function also returns the drawn object - we used it below)
   label = display4.drawLabel("hi", 100, 100, Color.RED, Font("Serif", Font.ITALIC, 40))     
   
   from random import randint
   
   class RandomMover():
   
      def __init__(self, object, delay):
      
         self.object = object              # object to move
         
         timer = Timer(delay, self.move)   # timer to schedule movement
         timer.start()                     # start movement!
         
      def move(self):
         """Called by timer to move self.object."""
      
         # ask the object's display to move the item by a small random displacement
         display = self.object.display    # get the object's display
         x, y = self.object.position      # get object's current x, y coordinates
         
         # get new x, y coordinates (random displacement)
         x = x + randint(0, 10)
         y = y + randint(0, 10)
         
         # make sure we stay within display area
         x = x % display.getWidth()
         y = y % display.getHeight()
         
         display.move( self.object, x, y )  # and move it
         
   m = RandomMover( label, 100 )  # move label randomly every 100 milliseconds


### FIFTH DISPLAY TEST ###

   from random import *         

   # create display (actually, a small superset of display)
   
   class GameEngine(Display):
      """Build a game engine based on a display, and consisting of a timer and interacting objects."""
      
      def __init__(self, title = "", width = 600, height = 400, frameRate=30):
      
         Display.__init__(self, title, width, height)
         
         self.objects = []      # keep track of game objects (to be updated)
    
         # create timer
         delay = 1000 / frameRate                 # convert from frame rate to delay between each update (in milliseconds)
         self.timer = Timer(delay, self.update)   # timer to schedule movement

      def start(self):
         """Starts animation."""         
         self.timer.start()   # start movement!

      def stop(self):
         """Stops animation."""
         self.timer.stop()   # stop movement!
         
      def add(self, object):
         """Adds another object to the game."""
         
         self.objects.append( object )  # let's remember it
         Display.add(self, object)      # also add it to the display

      def update(self):
         """Updates objects."""
         
         # check for collisions (and let colliding objects know)
         for i in range( len(self.objects) ):
         
            # check if this object is colliding with any of the remaining objects
            this = self.objects[i]
            remaining = self.objects[i+1:]
            for other in remaining:
            
               if this.intersects(other):  # found collision?
               
                  # let objects know they have collided, in case they needs to do something (e.g., explode)
                  this.collide( other )   
                  #other.collide( this )    # since this generates a sound, let's call only one of them
                  
                  # swap velocities between the two objects
                  # NOTE:  This could be more involved to take mass into account, e.g.,
                  #        see http://processing.org/learning/topics/circlecollision.html
                  this.velocity, other.velocity = other.velocity, this.velocity
                  
                  # and update positions, until they are not overlapping anymore (to NOT get stuck!)
                  # NOTE:  Every now and then, this can cause some weird motion artifacts, but it's a simple
                  #        way to avoid object clumping (i.e., objects getting stuck inside one-another, caused
                  #        by continuous reversal of velocities, if objects continue to intersect after one update).
                  while this.intersects(other):
                     this.update()
                     other.update()
                  # now, we have handled the collision between these two objecs (by moving them apart)
             
         # ask objects to update their actions
         for object in self.objects:
            object.update()
  
  
   # create ball (a superset of Circle)
   class Ball(Circle):
      """Creates a ball based on a circle."""
   
      def __init__(self, x, y, radius, color, initVelocityX=1.0, initVelocityY=1.0):
         """Initialize ball using initial velocity (x, y)."""

         # initialize superclass (i.e., create circle)      
         Circle.__init__(self, x, y, radius, color, True)   # ball is a filled, red circle

         # set ball attributes
         self.radius = radius                            # ball radius
         self.velocity = [initVelocityX, initVelocityY]  # velocity [x, y]
         self.gravity = 0.28                             # acceleration due to gravity
         self.friction = 0.9                             # slow-down factor as a result of bouncing off the display border - has to be <= 1.0 - (should we call this "lubricity"?)
         
         # set what to do when we are clicked by the mouse
         self.onMouseClick( self.clicked )
         
         # sound effects
         self.blopSound = AudioSample("Blop-Mark_DiAngelo-SoundBible.com-79054334.wav")
         self.ricochetSound = AudioSample("Ricochet Of A Bullet-SoundBible.com-377161548.wav")

      def collide(self, other):
         """Called when we collide with another.  For now, just plays sound."""

         self.blopSound.play()   # play sound effect
      
      def update(self):
         """Move ball one step (determined by velocity and dt)."""
      
         try:
            self.display   # check if we have been added to a display
         except:
            raise RuntimeError("Ball.move(): Undefined display... You need to add ball to a display first.")
            
         x, y = self.getPosition()      # get ball's current x, y coordinates
         
         # stay within display borders 
         if x > self.display.getWidth() - self.radius:  # hit right wall of display?
            x = self.display.getWidth() - self.radius            # place ball at edge (in case we surpassed it - to NOT get stuck!)
            self.velocity[0] = -self.velocity[0] * self.friction # and bounce (invert x velocity component), slowing down a bit

         if x < 0 + self.radius:   # hit left wall of display?
            x = 0 + self.radius                                  # place ball at edge (in case we surpassed it - to NOT get stuck!)         
            self.velocity[0] = -self.velocity[0] * self.friction # and bounce (invert x velocity component), slowing down a bit

         if y > self.display.getHeight() - self.radius:  # hit bottom wall of display?       
            y = self.display.getHeight() - self.radius           # place ball at edge (in case we surpassed it - to NOT get stuck!)
            self.velocity[1] = -self.velocity[1] * self.friction # and bounce! (invert y velocity component), slowing down a bit
                                       
         if y < 0 + self.radius:   # hit top wall of display?
            y = 0 + self.radius                                  # place ball at edge (in case we surpassed it - to NOT get stuck!)         
            self.velocity[1] = -self.velocity[1] * self.friction # and bounce! (invert y velocity component), slowing down a bit
                              
         # adjust velocity based on acceleration due to gravity
         self.velocity[1] = self.velocity[1] + self.gravity   # applies only to y component

         # get new x, y coordinates (add displacement due to velocity)
         x = int(x + self.velocity[0])
         y = int(y + self.velocity[1])
         
         self.setPosition(x, y)  # and move to new position

      def clicked(self, x, y):
         """Executed when the ball is clicked with the mouse (x, y are the mouse coordinates).  
            For now, we make the ball (randomly) jump in the air, and play sound."""
            
         # NOTE:  This uses magic numbers - not good.  Perhaps use self.initialVelocity here?
         
         self.velocity[0] += randint(-10, 10)      # new x velocity (random displacement)
         self.velocity[1] = self.velocity[1] - 10  # new y velocity - jump in the air! (0 is at top of display)
 
         self.ricochetSound.play()    # play sound effect


   # initialize the game engine (display) - parameters are title, width. height frameRate (frames/sec)
   g = GameEngine("Fifth Display - Animation - Bouncing Balls with Sound (Shoot them too!)", 800, 600, 30)
    
   numBalls = 3  # how many balls to include in the simulation

   # create many balls
   for i in range(numBalls):
      # create a ball
      b = Ball( randint(0, g.getWidth()),  # initial x position (anywhere on display)
                randint(0, g.getHeight()), # initial y position (anywhere on display)
                randint(10, 70),           # random radius (ranges from 40 to 70 pixels)
                Color( randint(0, 255), randint(0, 255), randint(0, 255) ), # random color 
                randint(-10, 10),          # initial x velocity (anywhere from -10 to 10 pixels/frame)
                randint(-10, 10) )         # initial y velocity (anywhere from -10 to 10 pixels/frame)
      
      # and add it to the engine          
      g.add( b )
   # now all the balls have been created
   
   # so, start the engine!
   g.start()


### SIXTH DISPLAY TEST ###

   # create display
   display6 = Display("Sixth Display - Arc objects", 800, 800, 150, 150)     
   display6.show() 
   
   # draw some arcs
   display6.drawArc(400, 250, 500, 350, 240, 60) 
   display6.drawArc(200, 250, 300, 350, 180, 0)  
   display6.drawArc(5, 250, 105, 350, 90, 270) 
   display6.drawArc(5, 450, 105, 550, 90, -90) 
   display6.drawArc(200, 450, 300, 550, 240, -60)