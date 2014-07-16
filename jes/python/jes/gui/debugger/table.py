# -*- coding: utf-8 -*-
"""
jes.gui.debugger.table
======================
This provides the table that the JES watcher uses to display program
execution.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from java.awt import Color
from java.lang import Object
from javax.swing import JLabel, JTable, JScrollPane
from javax.swing.table import AbstractTableModel, TableCellRenderer
from jes.gui.swingutil import threadsafe

class WatcherTable(JTable):
    def __init__(self, watcher):
        model = self.watcherModel = WatcherTableModel(watcher)
        super(WatcherTable, self).__init__(model)
        self.setDefaultRenderer(Object, WatcherCellRenderer(Color.green))


class AutoScrollPane(JScrollPane):
    def __init__(self, component):
        super(AutoScrollPane, self).__init__(component)
        self.lastMaximum = None
        self.verticalScrollBar.model.stateChanged = self.stateChanged

    def stateChanged(self, event):
        brmodel = event.source
        if brmodel.maximum != self.lastMaximum:
            brmodel.value = brmodel.maximum
            self.lastMaximum = brmodel.maximum


def wrapInAutoScrollPane(table):
    pane = JScrollPane(table)

    def stateChanged(event):
        brmodel = event.source
        if brmodel.maximum <> self.lastScrollMaximum:
            brmodel.value = brmodel.maximum
            self.lastScrollMaximum = brmodel.maximum


class WatcherTableModel(AbstractTableModel):
    def __init__(self, watcher):
        self.watcher = watcher
        self.fixedColumns = ['step', 'line', 'instruction']
        self.fixedCount = len(self.fixedColumns)

        watcher.onAddedVariable.connect(self._varsChanged)
        watcher.onRemovedVariable.connect(self._varsChanged)

        watcher.onRecorded.connect(self._frameAdded)
        watcher.onReset.connect(self._framesCleared)

    def getRowCount(self):
        return len(self.watcher.records)

    def getColumnCount(self):
        return self.fixedCount + len(self.watcher.variablesToTrack)

    def getColumnName(self, col):
        if col >= 0 and col < self.fixedCount:
            return self.fixedColumns[col]
        else:
            return "var: " + self._getVariableForColumn(col)

    def getValueAt(self, row, col):
        count = len(self.watcher.records)
        if row >= 0 and row < count:
            rec = self.watcher.records[row]
            if col == 0:
                return row + 1
            elif col == 1:
                return rec.lineno
            elif col == 2:
                return rec.line
            else:
                var = self._getVariableForColumn(col)
                return rec.getVariable(var)
        else:
            raise ValueError("Java asked for nonexistent row %d (I have %d)" %
                             (row, count))

    def _getVariableForColumn(self, col):
        variables = self.watcher.variablesToTrack
        varIndex = col - self.fixedCount
        if varIndex >= 0 and varIndex < len(variables):
            return variables[varIndex]
        else:
            raise ValueError("Java asked for nonexistent column %d" % col)

    @threadsafe
    def _varsChanged(self, watcher, var, **_):
        self.fireTableStructureChanged()

    @threadsafe
    def _frameAdded(self, watcher, record, **_):
        lastIndex = len(watcher.records) - 1
        self.fireTableRowsInserted(lastIndex, lastIndex)

    @threadsafe
    def _framesCleared(self, watcher, **_):
        self.fireTableDataChanged()


class WatcherCellRenderer(JLabel, TableCellRenderer):
    def __init__(self, highlightColor):
        self.opaque = True
        self.highlightColor = highlightColor

    def getTableCellRendererComponent(self, table, value, isSelected, hasFocus, row, col):
        self.text = str(value)
        if row != table.rowCount - 1:
            self.background = Color.white
        else:
            self.background = self.highlightColor
        return self

