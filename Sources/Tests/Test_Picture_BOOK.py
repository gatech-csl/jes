import unittest
import Picture
import Pixel
import JESConfig
from java.awt import Color
from java.lang import ArrayIndexOutOfBoundsException
import javax.swing as swing

# This class is for testing the functions the book uses as examples
# Some of these methods are pulled from the slides

# This code is trying to Integration Test JES.  Use the other picture
# classes to Unit Test the infrastructure.  This will use the recommended
# JPG file format at all times.

class Test_Picture_BOOK(unittest.TestCase):

    #def setUp(self):
        # No code needed here
        # Would run at the start of every individual test

    def testDistance(self):
        '''Test Book - Color distances'''
        self.color1 = Color(81, 63, 51)
        self.color2 = Color(255, 51, 51)
        self.distance = Pixel.colorDistance(self.color1, self.color2)
        self.assertEqual(self.distance, 174.41330224498358, 'Distances: %s != %s' % (self.distance, 174.41330224498358))

    def testShow(self):
        '''Test Showing - YOU SHOULD NOW SEE A PICTURE WINDOW WITH BARBARA.JPG'''
        self.pict = Picture("barbara.jpg")
        self.pict.show()
        success = swing.JOptionPane.showConfirmDialog(None, 'Does a window show barbara.jpg?', 'TestShowPicOP', swing.JOptionPane.YES_NO_OPTION)
        self.assertEqual(success, swing.JOptionPane.YES_OPTION, 'Failed to show barbara.jpg in window.')

    def testExplore(self):
        '''Test Browsing - YOU SHOULD NOW SEE A PICTURE EXPLORER WINDOW WITH BARBARA.JPG'''
        self.pict = Picture("barbara.jpg")
        self.pict.explore()
        success = swing.JOptionPane.showConfirmDialog(None, 'Does the explorer start with barbara.jpg?', 'TestExplorerOP', swing.JOptionPane.YES_NO_OPTION)
        self.assertEqual(success, swing.JOptionPane.YES_OPTION, 'Failed to show barbara.jpg in explorer.')

    def testDecreaseRed(self):
        '''Test BOOK - Decrease red (by 50%)'''
	JESConfig.getInstance().setSessionWrapAround(0)
        self.pict = Picture("barbara.jpg")
        for p in self.pict.getPixels():
            value = p.getRed()
            p.setRed(int(value * 0.5))
        self.pict.write("testdecred.jpg")
        self.picttest1 = Picture("testdecred.jpg")
        self.picttest2 = Picture("barb-decred.jpg")
        self.assertEqual(self.picttest1.getWidth(),self.picttest2.getWidth(),'Widths are not the same (%s != %s)'%(self.picttest1.getWidth(),self.picttest2.getWidth()))
        self.assertEqual(self.picttest1.getHeight(),self.picttest2.getHeight(),'Heights are not the same (%s != %s)'%(self.picttest1.getHeight(),self.picttest2.getHeight()))
        for i in range(self.picttest1.getWidth()):
            for j in range(self.picttest1.getHeight()):
                self.assertEqual(self.picttest1.getBasicPixel(i,j), self.picttest2.getBasicPixel(i,j), 'Pixels (%s, %s) do not match (%s != %s) - see output file testdecred.jpg'%(i,j,self.picttest1.getBasicPixel(i,j),self.picttest2.getBasicPixel(i,j)))

    def testIncreaseRed(self):
        '''Test BOOK - Increase red (by 20%)'''
	JESConfig.getInstance().setSessionWrapAround(0)
        self.pict = Picture("barbara.jpg")
        for p in self.pict.getPixels():
            value = p.getRed()
            p.setRed(int(value * 1.2))
        self.pict.write("testincred.jpg")
        self.picttest1 = Picture("testincred.jpg")
        self.picttest2 = Picture("barb-incred.jpg")
        self.assertEqual(self.picttest1.getWidth(),self.picttest2.getWidth(),'Widths are not the same (%s != %s)'%(self.picttest1.getWidth(),self.picttest2.getWidth()))
        self.assertEqual(self.picttest1.getHeight(),self.picttest2.getHeight(),'Heights are not the same (%s != %s)'%(self.picttest1.getHeight(),self.picttest2.getHeight()))
        for i in range(self.picttest1.getWidth()):
            for j in range(self.picttest1.getHeight()):
                self.assertEqual(self.picttest1.getBasicPixel(i,j), self.picttest2.getBasicPixel(i,j), 'Pixels (%s, %s) do not match (%s != %s) - see output file testincred.jpg'%(i,j,self.picttest1.getBasicPixel(i,j),self.picttest2.getBasicPixel(i,j)))

    def testClearBlue(self):
        '''Test BOOK - Clear blue'''
        self.pict = Picture("barbara.jpg")
        for p in self.pict.getPixels():
            p.setBlue(0)
        self.pict.write("testclrblue.jpg")
        self.picttest1 = Picture("testclrblue.jpg")
        self.picttest2 = Picture("barb-clrblue.jpg")
        self.assertEqual(self.picttest1.getWidth(),self.picttest2.getWidth(),'Widths are not the same (%s != %s)'%(self.picttest1.getWidth(),self.picttest2.getWidth()))
        self.assertEqual(self.picttest1.getHeight(),self.picttest2.getHeight(),'Heights are not the same (%s != %s)'%(self.picttest1.getHeight(),self.picttest2.getHeight()))
        for i in range(self.picttest1.getWidth()):
            for j in range(self.picttest1.getHeight()):
                self.assertEqual(self.picttest1.getBasicPixel(i,j), self.picttest2.getBasicPixel(i,j), 'Pixels (%s, %s) do not match (%s != %s) - see output file testclrblue.jpg'%(i,j,self.picttest1.getBasicPixel(i,j),self.picttest2.getBasicPixel(i,j)))

    def testLighten(self):
        '''Test BOOK - Lighten'''
	JESConfig.getInstance().setSessionWrapAround(0)
        self.pict = Picture("barbara.jpg")
        for p in self.pict.getPixels():
            color = p.getColor()
            p.setColor(color.brighter())
        self.pict.write("testlighten.jpg")
        self.picttest1 = Picture("testlighten.jpg")
        self.picttest2 = Picture("barb-lighten.jpg")
        self.assertEqual(self.picttest1.getWidth(),self.picttest2.getWidth(),'Widths are not the same (%s != %s)'%(self.picttest1.getWidth(),self.picttest2.getWidth()))
        self.assertEqual(self.picttest1.getHeight(),self.picttest2.getHeight(),'Heights are not the same (%s != %s)'%(self.picttest1.getHeight(),self.picttest2.getHeight()))
        for i in range(self.picttest1.getWidth()):
            for j in range(self.picttest1.getHeight()):
                self.assertEqual(self.picttest1.getBasicPixel(i,j), self.picttest2.getBasicPixel(i,j), 'Pixels (%s, %s) do not match (%s != %s) - see output file testlighten.jpg'%(i,j,self.picttest1.getBasicPixel(i,j),self.picttest2.getBasicPixel(i,j)))

    def testDarken(self):
        '''Test BOOK - Darken'''
	JESConfig.getInstance().setSessionWrapAround(0)
        self.pict = Picture("barbara.jpg")
        for p in self.pict.getPixels():
            color = p.getColor()
            p.setColor(color.darker())
        self.pict.write("testdarken.jpg")
        self.picttest1 = Picture("testdarken.jpg")
        self.picttest2 = Picture("barb-darken.jpg")
        self.assertEqual(self.picttest1.getWidth(),self.picttest2.getWidth(),'Widths are not the same (%s != %s)'%(self.picttest1.getWidth(),self.picttest2.getWidth()))
        self.assertEqual(self.picttest1.getHeight(),self.picttest2.getHeight(),'Heights are not the same (%s != %s)'%(self.picttest1.getHeight(),self.picttest2.getHeight()))
        for i in range(self.picttest1.getWidth()):
            for j in range(self.picttest1.getHeight()):
                self.assertEqual(self.picttest1.getBasicPixel(i,j), self.picttest2.getBasicPixel(i,j), 'Pixels (%s, %s) do not match (%s != %s) - see output file testdarken.jpg'%(i,j,self.picttest1.getBasicPixel(i,j),self.picttest2.getBasicPixel(i,j)))

    def testNegative(self):
        '''Test BOOK - Negative'''
	JESConfig.getInstance().setSessionWrapAround(0)
        self.pict = Picture("barbara.jpg")
        for p in self.pict.getPixels():
            red = p.getRed()
            green = p.getGreen()
            blue = p.getBlue()
            negcolor = Color(255-red, 255-green, 255-blue)
            p.setColor(negcolor)
        self.pict.write("testnegative.jpg")
        self.picttest1 = Picture("testnegative.jpg")
        self.picttest2 = Picture("barb-negative.jpg")
        self.assertEqual(self.picttest1.getWidth(),self.picttest2.getWidth(),'Widths are not the same (%s != %s)'%(self.picttest1.getWidth(),self.picttest2.getWidth()))
        self.assertEqual(self.picttest1.getHeight(),self.picttest2.getHeight(),'Heights are not the same (%s != %s)'%(self.picttest1.getHeight(),self.picttest2.getHeight()))
        for i in range(self.picttest1.getWidth()):
            for j in range(self.picttest1.getHeight()):
                self.assertEqual(self.picttest1.getBasicPixel(i,j), self.picttest2.getBasicPixel(i,j), 'Pixels (%s, %s) do not match (%s != %s) - see output file testnegative.jpg'%(i,j,self.picttest1.getBasicPixel(i,j),self.picttest2.getBasicPixel(i,j)))

    def testGreyScale(self):
        '''Test BOOK - GreyScale'''
	JESConfig.getInstance().setSessionWrapAround(0)
        self.pict = Picture("barbara.jpg")
        for p in self.pict.getPixels():
            newRed = p.getRed() * 0.299
            newGreen = p.getGreen() * 0.587
            newBlue = p.getBlue() * 0.114
            luminance = int(newRed + newGreen + newBlue)
            p.setColor(Color(luminance,luminance,luminance))
        self.pict.write("testgreyscale.jpg")
        self.picttest1 = Picture("testgreyscale.jpg")
        self.picttest2 = Picture("barb-greyscale.jpg")
        self.assertEqual(self.picttest1.getWidth(),self.picttest2.getWidth(),'Widths are not the same (%s != %s)'%(self.picttest1.getWidth(),self.picttest2.getWidth()))
        self.assertEqual(self.picttest1.getHeight(),self.picttest2.getHeight(),'Heights are not the same (%s != %s)'%(self.picttest1.getHeight(),self.picttest2.getHeight()))
        for i in range(self.picttest1.getWidth()):
            for j in range(self.picttest1.getHeight()):
                self.assertEqual(self.picttest1.getBasicPixel(i,j), self.picttest2.getBasicPixel(i,j), 'Pixels (%s, %s) do not match (%s != %s) - see output file testgreyscale.jpg'%(i,j,self.picttest1.getBasicPixel(i,j),self.picttest2.getBasicPixel(i,j)))



#if __name__ == '__main__':
#    unittest.main()

#suite = unittest.makeSuite(Test_Picture_BOOK)
#unittest.TextTestRunner(verbosity=2).run(suite)
