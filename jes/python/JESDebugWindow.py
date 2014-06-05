#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information

#TODO - better type names
import java.awt as awt
import javax.swing as swing
import time
from java.awt.event import ActionListener

DEBUG_WINDOW_TITLE    = 'JES Watcher Window #%s - %H:%M:%S'
DEBUG_WINDOW_SIZE     = (400,400)
CLOSE_BUTTON_CAPTION  = 'Close'
VAR_L_NAME_COL_CAPTION  = 'Local Variables'
#VAR_G_NAME_COL_CAPTION  = 'Global Variables'
VAR_G_NAME_COL_CAPTION = 'Command Area Variables'
VAR_TYPE_COL_CAPTION  = 'Type'
VAR_VALUE_COL_CAPTION = 'Value'

INTEGER = 'org.python.core.PyInteger'
LONG    = 'org.python.core.PyLong'
FLOAT   = 'org.python.core.PyFloat'
COMPLEX = 'org.python.core.PyComplex'
STRING  = 'org.python.core.PyString'
TUPLE   = 'org.python.core.PyTuple'
LIST    = 'org.python.core.PyList'
DICTIONARY = 'org.python.core.PyDictionary'
FUNCTION = 'org.python.core.PyFunction'
CLASS   = 'org.python.core.PyClass'
MODULE  = 'org.python.core.PyModule'
NONE    = 'org.python.core.PyNone'

IMPROVED_TYPE_NAMES = {INTEGER:    'Integer',
                       NONE: 'None',
                       LONG:       'Long',
                       FLOAT:      'Float',
                       COMPLEX:    'Complex',
                       STRING:     'String',
                       TUPLE:      'Tuple',
                       LIST:       'List',
                       DICTIONARY: 'Dictionary',
                       FUNCTION:   'Function',
                       MODULE: 'Module',
                       CLASS:      'Class'}

         
                  
class JESDebugWindow(swing.JFrame, ActionListener):
################################################################################
# Function name: __init__
# Parameters:
#     -varsToDisplay: collection of variables to be displayed.
#     -windowNumber: window number (or ID) which can be used to differentiate
#                    one window from another.
# Return:
#     An instance of the JESDebugWindow class.
# Description:
#     Creates an instance of the JESDebugWindow class and displays it.
################################################################################
    def __init__(self,localVars, globalVars, windowNumber, varsToFilter):
        import time
        self.varsToFilter = varsToFilter

        now = time.localtime(time.time())
        self.title = time.strftime(DEBUG_WINDOW_TITLE, now)
        self.title = self.title % windowNumber
        self.size = DEBUG_WINDOW_SIZE
        self.contentPane.setLayout(swing.BoxLayout(self.contentPane,
                                                   swing.BoxLayout.Y_AXIS))

        #Load the variables from varsToDisplay into an array for the JTable


        #Create panels and button, and place them on the frame
        closeButton = swing.JButton(CLOSE_BUTTON_CAPTION, actionListener=self)

        bottomPanel = swing.JPanel()
        bottomPanel.add(closeButton)

        (topPane, bottomPane) = self.buildContentPane(localVars, globalVars)
        self.contentPane.add(topPane)
        self.contentPane.add(bottomPane)
        self.contentPane.add(bottomPanel)

        self.setDefaultCloseOperation(1)
        self.setVisible(1)


    def buildContentPane(self, localVars, globalVars):

        
        # TODO
        # replace varVal.__class__.__name__ with something more meaningful
        # and scan for things without "__class__" or "__name__" fields
        # some swing components don't have them

        localVarsDict  = self.__buildVarDict__(localVars)
        globalVarsDict = self.__buildVarDict__(globalVars)

        localVarsDict  = self.filterVars(localVarsDict)
        globalVarsDict = self.filterVars(globalVarsDict)

        localVarsDict  = self.sortVars(localVarsDict)
        globalVarsDict = self.sortVars(globalVarsDict)

        localVarsDict = self.improveTypeNames(localVarsDict)
        globalVarsDict = self.improveTypeNames(globalVarsDict)


        
        #Create the TableModel and JTable components
        localTableModel = swing.table.DefaultTableModel(localVarsDict, [VAR_L_NAME_COL_CAPTION,
                                                                        VAR_TYPE_COL_CAPTION,
                                                                        VAR_VALUE_COL_CAPTION])

        
        globalTableModel = swing.table.DefaultTableModel(globalVarsDict, [VAR_G_NAME_COL_CAPTION,
                                                                        VAR_TYPE_COL_CAPTION,
                                                                        VAR_VALUE_COL_CAPTION])
        
        localVarTable = swing.JTable(localTableModel)
        localVarTable.getColumnModel().getColumn(0).setPreferredWidth(1);

        globalVarTable = swing.JTable(globalTableModel)
        globalVarTable.getColumnModel().getColumn(0).setPreferredWidth(1);


        topPane = swing.JScrollPane(localVarTable)
        bottomPane = swing.JScrollPane(globalVarTable)
        return (topPane, bottomPane)

    ###############################################################################
    # improveTypeNames
    #
    # accepts the "varsDict" array, and replaces the string in the type name field
    # with something more readable.  "org.core.PyInteger" becomes "Integer", for
    # example.
    #
    # params: varsDict- an array, where each element of the array is a 3-tuple of
    #                   format is [ [ <variable name>, <type>, <value>] ,
    #                               [,,] , ... ]
    # return: the same array, but the strings in the second field have been
    #         replaced
    ###############################################################################
    def improveTypeNames(self, varsDict):

        for var in varsDict:
            
            if IMPROVED_TYPE_NAMES.has_key(var[1]):
                var[1] = IMPROVED_TYPE_NAMES[ var[1] ]

        return varsDict
    

    ###############################################################################
    # filterVars
    #
    # uses the varsToFilter dictionary to remove from the visible debug window
    # any variables that are part of the debug system.
    #
    # param: varsDict - the array that will be displayed in the debug window
    #
    #        varsToFilter - not a parameter; part of the object;
    #                       if a variable appears in varsToFilter, then it will
    #                       be removed from the list
    #  return: newVarsDict - the dictionary without the "hidden" variables
    ###############################################################################
    def filterVars(self,varsDict):

        newVarsDict= []
        for i in range( len( varsDict) ):
            if self.varsToFilter.has_key( varsDict[i][0] ) and \
                   varsDict[i][0] != 'showVars':
                pass
            else:
                newVarsDict.append( varsDict[i])
                
        return newVarsDict

    #############################################################################
    # sortVars
    #
    # sorts the variables list varsDict
    # 
    #
    # param - varsDict - the array that will be displayed in the debug window
    # return- varsDict - now sorted
    #
    ############################################################################## 
    def sortVars(self,varsDict):
        varsDict.sort( self.compareFun )
        return varsDict

    ##########################################################################
    # compareFun
    #
    # the function passed to varsDict's sort function
    # used to tell the sort function how which variables are bigger than which
    #
    # param - x,y - two variables that will be compared
    # return- [-1,0,1]
    ###########################################################################
    def compareFun(self,x,y):
        
        xTypeSortNum = self.getTypeSortNum(x[1])
        yTypeSortNum = self.getTypeSortNum(y[1])

        if   xTypeSortNum < yTypeSortNum:
            return -1
        
        elif xTypeSortNum > yTypeSortNum:
            return 1

        if   x[0] < y[0]:
            return -1
        elif x[0] > y[0]:
            return 1

        return 0

    #############################################################################
    # getTypeSortNum
    #
    # helps the compareFun order the variables based on their type
    #
    # param - x - the type of a variable
    # return - an integer on the set {1,2,3,4,5}
    #############################################################################
    def getTypeSortNum(self,x):
        if x == INTEGER or \
           x == LONG    or \
           x == FLOAT   or \
           x == COMPLEX or \
           x == STRING  or \
           x == TUPLE   or \
           x == LIST    or \
           x == DICTIONARY:
            
            return 1

        if x == FUNCTION:
            return 3
        if x == CLASS:
            return 4
        if x == MODULE:
            return 5

        return 2
################################################################################
# Function name: actionPerformed
# Parameters:
#     -event: event object that represents action that occured
# Description:
#     This function closes the debug window when the close button is pressed.  
################################################################################
    def actionPerformed(self, event):
        actionCommand = event.getActionCommand()

        if actionCommand == CLOSE_BUTTON_CAPTION:
            self.setVisible(0)


################################################################################
# Function name: __buildVarDict__
# Parameters:
#     -varsToDisplay: the dictionary of variable to display
# Return:
#     An array of three value collections (variable name, variable class name,
#     and variable value)
# Description:
#     Accepts a hash table of items and returns an an array.  The array is to
#     be shown in the debug window;  This will ignore variables that don't
#     have __class__ fields.
################################################################################
    def __buildVarDict__(self, varsToDisplay ):
        varDict = []
        for varName, varVal in varsToDisplay.items():
            
            try:
                varDict += [[varName, varVal.__class__.__name__, varVal]]

            except:
                # some objects (swing objects, say) don't have the class field
                # this is a crude way to avoid that generating errors
                pass
            
        return varDict



