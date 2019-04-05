# -*- coding: utf-8 -*-
"""
jes.gui.filemanager.printing
============================
This lets you print files.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import JESPrintable
import string
import os
from java.awt import Font, Color
from java.awt.print import PrinterJob, PrinterException
from java.io import RandomAccessFile
from java.text import SimpleDateFormat
from java.util import Date

def printFile(filename, defaults=False):
    printerJob = PrinterJob.getPrinterJob()
    printerJob.setPrintable(JESPrintableDocument(filename))
    if defaults or printerJob.printDialog():
        printerJob.print()


class JESPrintableDocument(JESPrintable):
    def __init__(self, fileToPrint):
        self.fileName = fileToPrint
        self.today = SimpleDateFormat("yyyy.MM.dd HH:mm").format(Date())

        self.textFont = Font("Monospaced", Font.PLAIN, 12)

        # We use a RandomAccessFile because Java likes to seek around and
        # print pages multiple times.
        self.raf = RandomAccessFile(self.fileName, "r")

        # These keep track of what pages we've found so far,
        # and where in the file the pages start.
        # Page 0's starts out filled, and the following pages' are filled
        # at the end of its predecessor.
        self.pagePointers = []
        self.pageAfterEnd = None

        # Set the pointer for page 0.
        self.pagePointers.append(self.raf.getFilePointer())

    def printPage(self, g, pform, pageIndex):
        if pageIndex < len(self.pagePointers):
            # We already know where this page starts. Seek there.
            self.raf.seek(self.pagePointers[pageIndex])
        elif pageIndex >= self.pageAfterEnd:
            # We've found the end, and this page is after it.
            return JESPrintable.NO_SUCH_PAGE
        else:
            # We haven't gotten here yet.
            # Java will probably print each page multiple times,
            # and maybe even repeat pages after their successors,
            # but it should never print page n + 1 before page n.
            raise RuntimeError("Printing pages out of order")

        # Find our dimensions.
        minX = int(pform.getImageableX() + 10)
        width = int(pform.getImageableWidth() - 10)
        maxX = int(minX + width)
        midX = int(minX + width / 2)

        minY = int(pform.getImageableY() + 12)
        height = int(pform.getImageableHeight() - 12)
        maxY = int(minY + height)

        x, y = minX, minY

        # Title lines
        g.setColor(Color.black)
        # Left: filename
        titleString = "JES: " + os.path.basename(self.fileName)
        g.drawString(titleString, x, y)
        # Center: text
        pageNoString = "Page %d" % (pageIndex + 1)
        pageNoWidth = g.getFontMetrics().stringWidth(pageNoString)
        g.drawString(pageNoString, midX - (pageNoWidth / 2), y)
        # Right: date
        dateString = self.today
        dateWidth = g.getFontMetrics().stringWidth(dateString)
        g.drawString(dateString, maxX - dateWidth, y)
        # Line below header
        g.drawLine(minX, y + 6, maxX, y + 6)

        # OK, now the text.
        g.setColor(Color.black)
        g.setFont(self.textFont)

        # Generate as many lines as will fit in imageable area.
        y += 24
        while y + 12 < maxY:
            line = self.raf.readLine()
            if line is None:
                # We've already printed the last line.
                # Don't print another page.
                self.pageAfterEnd = pageIndex + 1
                return JESPrintable.PAGE_EXISTS
            try:
                g.drawString(line, x, y)
            except:
                # TBH I'm not sure what kind of exceptions happen here.
                # (If the line's too long, it'll just print over the margin.)
                # Unprintable characters maybe?
                g.drawString(' ', x, y)
            y = y + 12

        if pageIndex + 1 == len(self.pagePointers):
            # Hey, we've discovered the pointer to the next page!
            # Let's add it to the list so the next print call works.
            self.pagePointers.append(self.raf.getFilePointer())

        return JESPrintable.PAGE_EXISTS

