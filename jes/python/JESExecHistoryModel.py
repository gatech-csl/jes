import javax.swing as swing
import javax.swing.table.AbstractTableModel as AbstractTableModel
from java.lang import Thread
from java.lang import Runnable

MAX_LINES = 200
CROPPED_MESSAGE = '<<LINES ABOVE WERE CROPPED>>'

class JESExecHistoryModel(AbstractTableModel):
    def __init__(self):
	self.lines = []
	self.vars = []
	self.nextLine = None

    #Required by table model interface
    def getRowCount(self):
	return len(self.lines)

    #Required by table model interface
    def getColumnCount(self):
	return 3 + len(self.vars)

    #Required by table model interface
    def getValueAt(self, row, col):
	line = self.lines[row]
	if col < len(line):
	    return self.lines[row][col]
        else:
	    return ''

    def getColumnName(self, col):
	if col == 0:
	    return 'step'
        elif col == 1:
	    return 'line'
        elif col == 2:
	    return 'instruction'
        else:
	    return 'var: ' + self.vars[col-3]

#DORN: NOT IMPLEMENTING THIS, BAD BAD
    def setColumnWidths(self, table):
	 x = ''
#        columnModel = table.columnModel
#        columnModel.getColumn(0).preferredWidth = 10   # step
#        columnModel.getColumn(1).preferredWidth = 10   # line number
#        columnModel.getColumn(2).preferredWidth = 150  # instruction
#        for i in range(len(self.vars)):
#            columnModel.getColumn(i + 3).setPreferredWidth(15)

#DORN:  NOt sure of this.
    def endExecution(self):
	if self.nextLine:
	    self.lines.append(self.nextLine)
    	    self.fireTableRowsInserted(len(self.lines)-1, len(self.lines)-1)
	    self.nexLine = None

#	    self.debugger.interpreter.program.gui.editor.document.removeLineHighlighting() # also update the editor currentline highlight

    def getVars(self):
	return self.vars


    def appendVariable(self, var):
	self.vars.append(var)
	self.fireTableStructureChanged()

    def removeVariable(self, var):
        self.vars.remove(var)
	self.fireTableStructureChanged()



    def addLine(self, line_no, instr, values):
	if self.nextLine:
	    
	    #If the number of steps is greater than MAX_LINES
	    if len(self.lines) > MAX_LINES:
		#If we have already started cropping lines
                if self.lines[0][1] == CROPPED_MESSAGE:
                    self.lines.remove(self.lines[1])
		    self.fireTableRowsDeleted(1,1)

		#We have not started cropping lines yet
                else:
                    line = ['-', CROPPED_MESSAGE]
                    self.lines[0] = line
		    self.fireTableRowsUpdated(0,0)


            
	    self.nextLine.extend(values) #Add the variable values to nextLine
            self.lines.append(self.nextLine) #Put nextLine in the list
	    self.fireTableRowsInserted(len(self.lines)-1, len(self.lines)-1)

                  
	self.nextLine = [] #Clear nextLine to begin filling it with next step
        
        #Set the step number
	if len(self.lines) > 0:
            self.nextLine.append(self.lines[len(self.lines)-1][0]+1)
        else:
            self.nextLine.append(1)
	    
	#Add the line number and instruction to the nextLine
        self.nextLine.append(line_no) 
        self.nextLine.append(instr)

    def clear(self):        
	self.nextLine = None
        numrows = len(self.lines)
	if numrows > 0:
            self.lines = []
	    self.fireTableRowsDeleted(0, numrows-1)


    
