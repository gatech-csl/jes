#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information

import java.io.File as File
import sys
sys.path.append('.%sLib%s.' % (File.separator, File.separator))
sys.path.append('.%s.' % (File.separator))



from media import *

from math import acos
from math import asin
from math import atan 
from math import ceil
from math import cos
from math import exp
from math import floor
from math import log
from math import log10
from math import pow
from math import sin
from math import sqrt
from math import tan
from math import pi
import os.sep as pathSep


global __debugSystem__

__varsToFilter__ = {}




 
# this stuff has to be done last
# HACK ALERT 
# I need a list of all of the variables that are
# defined.  I use that list, __varsToFilter__, to
# hide the variables defined in this file
v = vars()
for key in v.keys():
    __varsToFilter__[ key ] = 1

del v
del key
class __JESNum__:
    def __init__(self,num):
        self.num = num

    def increment(self):
        self.num = self.num + 1

    def getNum(self):
        return self.num
################################################################################
# Function name: showVars
# Description: 
#     The function provided to our users, available through the command window,     
#     that will open a popup window containing all global and local variable.
#
################################################################################
def showVars(count = __JESNum__(1) ,varsToFilter = __varsToFilter__):
    # I just learned what a closure was, and I've been itching to use one
    #  just kidding.
    # The showVars function is a closure - the optional parameters grab
    # objects from the current scope.  A JESNum object is created when showVars
    # is defined.  That object is only visible to the showVars function
    # and keeps track of the number of times that showVars() has been called.


    import JESDebugWindow
    frame   = sys._getframe(1)
    localVars  = frame.f_locals.copy()
    globalVars = frame.f_globals.copy()

    JESDebugWindow.JESDebugWindow( localVars, \
                                   globalVars, \
                                   count.getNum(), \
                                   varsToFilter)
    count.increment()


del __JESNum__
del __varsToFilter__






