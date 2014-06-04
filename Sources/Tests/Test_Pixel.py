#########################################################################
#
# Text_Pixel class for use with the TestExecute utility.
# there's not much to test in the pixel class that isn't hit many times
# in the picture tests, but this covers all # the functions designed for
# use by students with the Pixel class.
#
# the only case where it crosses into the picture world a little too much
# is testWritePixel, where we open an image, modify a pixel, write the
# modified image to a temp file, open the temp file and make sure the
# change was stored correctly.  The remaining tests are straight forward
#
# In all of the functions we try to use only the high level functions
# that the students would use. These will in turn test the hierarchy
# of member class member functions from python to java.
#
#########################################################################

import os
import unittest
from media import *
import java.awt.Color


class Test_Pixel(unittest.TestCase):

    def setUp(self):
        #this makes sure we use the current directory when we open file
        setTestMediaFolder()

        #change these to use different test files/values
        self.consts = {'XVAL': 2, 'YVAL': 2, 'RED':0xff0000, 'GREEN':0xff00, 'BLUE':0xff, 'PICNAME': "9by9.bmp", '1RED': 212, '1BLUE': 100, '1GREEN': 40, '1ALPHA':142, 'TMPFILE':'pixtmp.bmp', 'MAXRGB': 255}

        #now we open the 9by9 bitmap and get the middle pixel (2,2)
        #all these indexes are 1 based.
        self.pic1 = Picture()
        self.pic1.loadImage(self.consts['PICNAME'])
        self.pix1 = getPixel(self.pic1, self.consts['XVAL'], self.consts['YVAL'])

    #underneath it's actually a 0 based array, but we need to make sure
    #it returns (2,2) since that's what the student will expect
    def testConstruct(self):
        self.assertEqual(getX(self.pix1), self.consts['XVAL'], 'Pixel values not set properly in Pixel Constructor.')
        self.assertEqual(getY(self.pix1), self.consts['YVAL'], 'Pixel values not set properly in Pixel Constructor.')
        self.assertEqual(self.pix1.getX(), self.consts['XVAL'], 'Pixel values not set properly in Pixel Constructor.')
        self.assertEqual(self.pix1.getY(), self.consts['YVAL'], 'Pixel values not set properly in Pixel Constructor.')

    #following 3 tests for the basic gets/sets
    def testGetSetRed(self):
        setRed(self.pix1, self.consts['1RED'])
        self.assertEqual(self.consts['1RED'], getRed(self.pix1), 'Pixel did not modify red value properly.')

    def testGetSetGreen(self):
        setGreen(self.pix1, self.consts['1GREEN'])
        self.assertEqual(self.consts['1GREEN'], getGreen(self.pix1), 'Pixel did not modify green value properly.')

    def testGetSetBlue(self):
        setBlue(self.pix1, self.consts['1BLUE'])
        self.assertEqual(self.consts['1BLUE'], getBlue(self.pix1), 'Pixel did not modify blue value properly.')

    #this tests to make sure we properly handle setting values
    #outside 0-255 RGB range
    def testOverUnderSet(self):
        setRed(self.pix1, 400)
        setBlue(self.pix1, -10)
        self.assertEqual(self.consts['MAXRGB'], getRed(self.pix1), 'Pixel did not handle too high setColor value')
        self.assertEqual(0, getBlue(self.pix1), 'Pixel did not handle -negative setcolor value.')

    #make sure we handle boundarie properly
    def testWhiteBlack(self):
        #make sure white pixel 255s work
        self.pix1 = getPixel(self.pic1, 0, 0)
        self.assertEqual(self.consts['MAXRGB'], getRed(self.pix1), 'Pixel did not handle red 255 in a white pixel')
        self.assertEqual(self.consts['MAXRGB'], getGreen(self.pix1), 'Pixel did not handle green 255 in a white pixel.')
        self.assertEqual(self.consts['MAXRGB'], getBlue(self.pix1), 'Pixel did not handle blue 255 in a white pixel.')

        #make sure black 0 vals work
        self.pix2 = getPixel(self.pic1, 2, 2)
        self.assertEqual(0, getRed(self.pix2), 'Pixel did not handle 0 Red val in a black pixel.')
        self.assertEqual(0, getGreen(self.pix2), 'Pixel did not handle 0 Green value in a black pixel.')
        self.assertEqual(0, getBlue(self.pix2), 'Pixel did not handle 0 Blue value in a black pixel.')

    #this is reliant on all the other gets/sets but make sure we can
    #set/get all 3 rgb values at once. also tests the comparison
    #op overload for the Color class indirectlyj
    def testGetSetColor(self):
        color1 = Color(self.consts['1RED'],self.consts['1GREEN'],self.consts['1BLUE'])
        setColor(self.pix1, color1)
        color2 = getColor(self.pix1)
        self.assert_(color1 == color2, 'Pixel did not setColor correctly.')

    #here we test that when we modify a pixel, write the file, then bring the file back in
    #the pixel has retained the new modified values.
    def testPixWrite(self):
        color1 = Color(self.consts['1RED'],self.consts['1GREEN'],self.consts['1BLUE'])
        setColor(self.pix1, color1)
        writePictureTo(self.pic1, self.consts['TMPFILE'])
        self.pic2 = Picture()
        self.pic2.loadImage(self.consts['TMPFILE'])
        self.pix2 = getPixel(self.pic2, self.consts['XVAL'], self.consts['YVAL'])
        os.remove(self.consts['TMPFILE'])
        self.assert_(getColor(self.pix1) == getColor(self.pix2), 'Pixel change did not properly save to file.  You may need to delete %s from the working directory.' % (self.consts['TMPFILE']))
