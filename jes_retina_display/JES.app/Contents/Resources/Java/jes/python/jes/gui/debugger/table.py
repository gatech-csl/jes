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
from javax.swing import JLabel, JTable
from javax.swing.table import AbstractTableModel, TableCellRenderer
from jes.gui.components.threading import threadsafe

CROP_MESSAGE = "# only the last %d steps are displayed"


class WatcherTable(JTable):
    def __init__(self, watcher):
        model = self.watcherModel = WatcherTableModel(watcher)
        super(WatcherTable, self).__init__(model)
        self.setDefaultRenderer(Object, WatcherCellRenderer(Color.green))


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

        self.displayedCropNotification = False

        watcher.onAddedVariable.connect(self._varsChanged)
        watcher.onRemovedVariable.connect(self._varsChanged)

        watcher.onRecorded.connect(self._frameAdded)
        watcher.onReset.connect(self._framesCleared)

    def getRowCount(self):
        return (len(self.watcher.records) +
                (1 if self.displayedCropNotification else 0))

    def getColumnCount(self):
        return self.fixedCount + len(self.watcher.variablesToTrack)

    def getColumnName(self, col):
        if col >= 0 and col < self.fixedCount:
            return self.fixedColumns[col]
        else:
            return "var: " + self._getVariableForColumn(col)

    def getValueAt(self, row, col):
        if self.displayedCropNotification:
            if row == 0 and col == 2:
                return CROP_MESSAGE % self.watcher.MAX_RECORDS
            elif row == 0:
                return ""
            else:
                row = row - 1

        count = len(self.watcher.records)
        if row >= 0 and row < count:
            rec = self.watcher.records[row]
            if col == 0:
                return rec.counter
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
    def _frameAdded(self, watcher, record, cropped, **_):
        if cropped:
            if not self.displayedCropNotification:
                self.displayedCropNotification = True
                if cropped == 1:
                    # Equivalent to inserting and deleting the first row.
                    self.fireTableRowsUpdated(0, 0)
                else:
                    self.fireTableRowsUpdated(0, 0)
                    self.fireTableRowsDeleted(1, cropped - 1)
            else:
                # These ranges are inclusive.
                # If 1 was cropped, we get 1, 1. 2 gives us 1, 2, and so on.
                self.fireTableRowsDeleted(1, cropped)

        lastIndex = len(watcher.records) - 1
        if self.displayedCropNotification:
            lastIndex = lastIndex + 1
        self.fireTableRowsInserted(lastIndex, lastIndex)

    @threadsafe
    def _framesCleared(self, watcher, **_):
        self.displayedCropNotification = False
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

