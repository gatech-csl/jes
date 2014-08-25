# sliderControl.py
#
# It creates a simple slider control surface.

from gui import *

class SliderControl:

   def __init__(self, title="Slider", updateFunction=None, minValue=10, maxValue=1000, startValue=None, x=0, y=0):
      """Initializes a SliderControl object."""

      self.title = title    # holds the title of the control display
      self.updateFunction = updateFunction  # external function to call when slider is updated

      # determine slider start value
      if startValue == None:  # if startValue is undefined
         startValue = (minValue + maxValue) / 2   # start at middle point between min and max value

      # create slider
      self.slider = Slider(HORIZONTAL, minValue, maxValue, startValue, self.setValue)

      # create control surface display
      self.display = Display(self.title, 250, 50, x, y)

      # add slider to display
      self.display.add(self.slider, 25, 10)
      
      # finally, initialize value and title (using 'startValue')
      self.setValue( startValue ) 

   def setValue(self, value):
      """Updates the display title, and calls the external update function with given 'value'."""

      self.display.setTitle(self.title + " = " + str(value))
      self.updateFunction(value)
      
      
if __name__ == '__main__':
   
   # one example
   def printValue(value):
      print value

   control = SliderControl("Print", printValue)  # just the title and update function, all else using default values

   # another example (demonstrating how to change a global variable - more useful)
   testValue = -1
   
   def changeAndPrintValue(value):
      global testValue   
      
      testValue = value
      print testValue

   control1 = SliderControl("Change and Print", changeAndPrintValue, 0, 100, 50, 100, 100)  # modify program variable
   
   # and another one
   #from music import *
   from music import *    # for Play.note()
   
   def playNote(pitch):
      """Plays an 1-sec note with the provided pitch."""
      Play.note(pitch, 0, 1000)

   control2 = SliderControl("Play Note", playNote, 0, 100, 50, 200, 200)  # modify program variable
   