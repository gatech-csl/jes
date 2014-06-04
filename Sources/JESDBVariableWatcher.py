import sys
import javax.swing as swing
import javax.swing.SwingUtilities as SwingUtilities
import javax.swing.table.AbstractTableModel as AbstractTableModel
import javax.swing.table.TableColumnModel as TableColumnModel
import java.awt as awt
import java.awt.EventQueue as EventQueue
import java.lang.Object as Object
import JESDebugger
import java.util.Hashtable as Hashtable
import JESGutter
import JESExecHistoryModel as JESExecHistoryModel
import java.io.FileWriter as FileWriter #Added by Brian for debugging
import media
import java.lang.System as System
from java.lang import Thread
from java.lang import Runnable


BUTTON_SIZE=(50,50)
HIGHLIGHT_COLOR = awt.Color.green

def variableDialog(ui):
    var = swing.JOptionPane.showInputDialog(ui, 'Please type the variable to watch')
    return var

def pickVariable(ui, vars):
    if len(vars) > 0:
        var = swing.JOptionPane.showInputDialog(ui,
                                                "Choose Variable to remove",
                                                "Input",
                                                swing.JOptionPane.INFORMATION_MESSAGE,
                                                None,
                                                vars,
                                                vars[0])
        return var
    else:
        swing.JOptionPane.showMessageDialog(ui,
                                           'There are no variables to remove',
                                           'Error',
                                           swing.JOptionPane.ERROR_MESSAGE)
        return None

#-------------------------------------------------------------------------------
class DBControlPanel(swing.JPanel):
    def __init__(self, debugger):
        self.lastValue = None
        self.debugger = debugger
        MAX_SPEED = debugger.MAX_SPEED
        self.slider = swing.JSlider(swing.JSlider.HORIZONTAL, 0, MAX_SPEED,
                                    self.debugger.speed,
                                    stateChanged=self.stateChanged)
        self.last_speed = self.debugger.speed
        labels = Hashtable()
        labels.put(0, swing.JLabel('slow'))
        labels.put(MAX_SPEED, swing.JLabel('fast'))
        self.slider.labelTable = labels
        self.slider.paintLabels = 1

        self.addButton = swing.JButton(swing.ImageIcon('images/plus.jpg'),
                                       actionPerformed=self.actionPerformed,
                                       toolTipText='add Variable',
                                       preferredSize=BUTTON_SIZE)
        self.deleteButton = swing.JButton(swing.ImageIcon('images/minus.jpg'),
                                       actionPerformed=self.actionPerformed,
                                       toolTipText='remove Variable',
                                       preferredSize=BUTTON_SIZE)
        self.stepButton = swing.JButton(swing.ImageIcon('images/boot.jpg'),
                                        actionPerformed=self.actionPerformed,
                                        toolTipText='step',
                                        preferredSize=BUTTON_SIZE)
	self.pauseIcon = swing.ImageIcon('images/pause.jpg')
	self.runIcon = swing.ImageIcon('images/run.jpg')
        self.runButton = swing.JButton(self.runIcon,
                                        actionPerformed=self.actionPerformed,
                                        toolTipText='run',
                                       preferredSize=BUTTON_SIZE)
        self.fullspeedButton = swing.JButton(swing.ImageIcon('images/fullspeed.jpg'),
                                        actionPerformed=self.actionPerformed,
                                        toolTipText='full speed',
                                       preferredSize=BUTTON_SIZE)
        self.stopButton = swing.JButton(swing.ImageIcon('images/stop.jpg'),
                                        actionPerformed=self.actionPerformed,
                                        toolTipText='stop',
                                        preferredSize=BUTTON_SIZE)
        self.setLayout(swing.BoxLayout(self, swing.BoxLayout.X_AXIS))
        self.add(self.slider)
        self.add(self.addButton)
        self.add(self.deleteButton)
        #self.add(self.stepButton) # These two lines commented out by Brian O because of removed Pause functionality -- 23 June 2008
        #self.add(self.runButton)
        self.add(self.fullspeedButton)
        self.add(self.stopButton)
	self.initialButtonState()

    def stateChanged(self, e):
        value = self.slider.getValue()
        self.debugger.speed = value
        if value == 0:
            self.stepButton.setEnabled(1)
            self.pauseState()
        elif self.lastValue == 0:
            self.stepButton.setEnabled(0)
            self.run()
        self.lastValue = value

    def actionPerformed(self, e):
        source = e.getSource()
        if source == self.runButton:
	    if source.icon == self.runIcon:
		self.run()
	    else:
                self.pause()
        elif source == self.fullspeedButton:
	    self.fullspeed()
        elif source == self.stopButton:
	    self.debugger.stopThread()
	    self.stop()
	elif source == self.stepButton:
	    self.step()
	elif source == self.addButton:
            self.debugger.watcher.watchVariable()
        elif source == self.deleteButton:
            self.debugger.watcher.unwatchVariable()

    def refreshSlider(self):
        self.slider.value = self.debugger.speed
            
    def run(self):
        self.runButton.icon = self.pauseIcon
        self.runButton.toolTipText = 'pause'
        if self.debugger.speed == 0:
            self.debugger.setSpeed(self.last_speed)
        self.runButton.enabled = 1
        self.fullspeedButton.enabled = 1
        self.stepButton.enabled = 0
        self.stopButton.enabled = 1
        self.addButton.enabled = 0
        self.deleteButton.enabled = 0
        self.debugger.step()

    def pause(self):
        self.last_speed = self.debugger.speed
        self.debugger.setSpeed(0)
        self.pauseState()

    def stop(self):
	self.initialButtonState()

    def fullspeed(self):
        # kinda like run, but full speed
        self.runButton.icon = self.pauseIcon
        self.runButton.toolTipText = 'pause'
        self.debugger.setSpeed(self.debugger.MAX_SPEED)
        self.fullspeedButton.enabled = 1 
        self.runButton.enabled = 1
        self.stepButton.enabled = 0
        self.stopButton.enabled = 1
        self.addButton.enabled = 0
        self.deleteButton.enabled = 0
        self.debugger.step()

    def initialButtonState(self):
        self.stepButton.enabled = 0
        self.runButton.enabled = 0
        self.stopButton.enabled = 0
        self.addButton.enabled = 1
        self.deleteButton.enabled = 1
        self.fullspeedButton.enabled = 0

    def pauseState(self):
        self.runButton.icon = self.runIcon
        self.runButton.toolTipText = 'run'
        self.stepButton.enabled = 1
        self.runButton.enabled = 1
        self.fullspeedButton.enabled = 1
        self.addButton.enabled = 1
        self.deleteButton.enabled = 1
        self.stopButton.enabled = 1

#-------------------------------------------------------------------------------
class JESDBVariableWatcher(swing.JPanel):
    def __init__(self, debugger):
	self.debugger = debugger
	self.controlPanel = DBControlPanel(self.debugger)
	self.history = JESExecHistoryModel.JESExecHistoryModel()
	self.table = WatcherTable(self.history)
	self.rendererComponent = swing.JLabel(opaque=1)
	self.table.setDefaultRenderer(Object, MyRenderer())
	self.history.setColumnWidths(self.table)
	self.scrollPane = swing.JScrollPane(self.table) 
        self.scrollPane.verticalScrollBar.model.stateChanged = self.stateChanged
        self.setLayout(awt.BorderLayout())
        self.add(self.scrollPane, awt.BorderLayout.CENTER)
        self.add(self.controlPanel, awt.BorderLayout.NORTH)
        self.lastScrollMaximum = None
        
    def stateChanged(self, event):
        brmodel = event.source
        if brmodel.maximum <> self.lastScrollMaximum:
            brmodel.value = brmodel.maximum
            self.lastScrollMaximum = brmodel.maximum

    def watchVariable(self):
        var = variableDialog(self)
        if var:
            self.history.appendVariable(var)

    def unwatchVariable(self):
        var = pickVariable(self, self.debugger.watcher.getVariables())
        if var:
            self.history.removeVariable(var)

    def endExecution(self):
	self.history.endExecution()

#-------------------------------------------------------------------------------
class MyRenderer(swing.JLabel, swing.table.TableCellRenderer):
    def __init__(self):
        self.opaque = 1
        
    def getTableCellRendererComponent(self, table, value, isSelected, hasFocus, row, col):
        self.text = str(value)
        if row <> table.rowCount - 1:
            self.background = awt.Color.white
        else:
            self.background = HIGHLIGHT_COLOR
        return self

#-------------------------------------------------------------------------------
class WatcherTable(swing.JTable):
    def __init__(self, model):
    	    #self.times = 0;
	    swing.JTable.__init__(self, model)


    def tableChanged(self, event):
        #print "WatcherTable, tableChanged: " + Thread.currentThread().getName()
	#self.times = self.times + 1
	#print "Count ", self.times
	swing.JTable.tableChanged(self, event)
        if event.getFirstRow() == swing.event.TableModelEvent.HEADER_ROW:
            self.model.setColumnWidths(self)
#-------------------------------------------------------------------------------

