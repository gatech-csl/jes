import java.awt.print.Printable as Printable
import java.awt.print as jPrint
import java.awt.geom as geom
import java.text as text
import java.awt as awt
import java.util as util
import java.io as io
import JESProgram
import string
import os

class JESPrintableDocument(Printable):
    def __init__(self,fileToPrint, name):
        self.fileName=fileToPrint
        self.fnt= awt.Font("Monospaced",awt.Font.PLAIN, 12)
        self.page= "Page "
        self.date=  util.Date()
        self.today =text.SimpleDateFormat("MM.dd.yy/HH:mm").format(self.date)
        self.resval= 4
        self.name = name
        self.rememberedPageIndex   = -1
        self.rememberedFilePointer = -1
        self.rememberedEOF= 0
        try:
            self.raf = io.RandomAccessFile(self.fileName, "r")
        except:
            self.rememberedEOF = 1


    def print(self, g, pform, pageIndex):
        try:
            # For catching IOException
            if (pageIndex != self.rememberedPageIndex):
                # First time we've visited this page
                self.rememberedPageIndex = pageIndex
                #If encountered EOF on previous page, done
                if (self.rememberedEOF):
                    return Printable.NO_SUCH_PAGE
                # Save current position in input file
                self.rememberedFilePointer = self.raf.getFilePointer()
            else:
                self.raf.seek(self.rememberedFilePointer)
            x = int(pform.getImageableX() + 10)
            y = int(pform.getImageableY() + 12)
            yd = 6 * self.resval
            g2 = g
            fontWidth = g2.getFontMetrics().stringWidth(self.page)
            # Title lines
            g2.setColor(awt.Color.black)
            pageNumstr = "%d" % (pageIndex+1)
            g.drawString("User: "+self.name,x,y)
            g.drawString("JES: "+os.path.basename(self.fileName), x, y+12)
            g.drawString(self.page + pageNumstr,pform.getImageableWidth() / 2 + fontWidth+ 8, y)
            g.drawString(self.today + " h", + pform.getImageableWidth() - yd-6,y)
            g.drawLine(x, y + 18, int(x + pform.getImageableWidth()), y + 18)
            g.setColor(awt.Color.black)
            g.setFont(self.fnt)
            # Generate as many lines as will fit in imageable area
            y += 36
            while (y + 12< pform.getImageableY() + pform.getImageableHeight()):
               line = self.raf.readLine()
               if (line == None):
                   self.rememberedEOF = 1
                   break
               try:
                   g.drawString(line, x, y)
               except:
                   g.drawString(' ',x,y)
               y =y + 12
            return Printable.PAGE_EXISTS
        except:
            import sys
            a,b,c=sys.exc_info()
            print a,b,c
            return Printable.NO_SUCH_PAGE



