import unittest
import Picture
import Pixel
from java.awt import Color
from java.lang import ArrayIndexOutOfBoundsException
import javax.swing as swing
import media

# This class does a lot of assuming Pixel functions work
# Perhaps the pixel class tester should be run before this

class Test_Picture(unittest.TestCase):

    #def setUp(self):
        # No code needed here
        # Would run at the start of every individual test

#
# Timmy: I think these null tests are worthless since the book
#        doesn't ever use a null picture, it always uses
#        makePicture(filename)


#   def testPictureNull1(self):
#       '''Test Picture() constructor [1] - filename'''
#       self.pict = Picture()
#       self.assertEqual('%s'%self.pict.getFileName(), 'None', 'Filename %s != None' % self.pict.getFileName())

#   def testPictureNull2(self):
#       '''Test Picture() constructor [2] - extension'''
#       self.pict = Picture()
#       self.assertEqual('%s'%self.pict.getExtension(), 'None',  'File extension %s != None' % self.pict.getExtension())

#   def testPictureNull3(self):
#       '''Test Picture() constructor [3] - title'''
#       self.pict = Picture()
#       self.assertEqual('%s'%self.pict.getTitle(), 'None', 'Title %s != None' % self.pict.getTitle())

#   def testPictureNull4(self):
#       '''Test Picture() constructor [4] - width'''
#       self.pict = Picture()
#       self.assertEqual(self.pict.getWidth(), 0, 'Width %s != 0' % self.pict.getWidth())
#       self.assertNotEqual(self.pict.getWidth(), 1, 'Width is 1?')

#   def testPictureNull5(self):
#       '''Test Picture() constructor [5] - height'''
#       self.pict = Picture()
#       self.assertEqual(self.pict.getHeight(), 0, 'Height %s != 0' % self.pict.getHeight())

#   def testPictureNull6(self):
#       '''Test Picture() constructor [6] - toString'''
#       self.pict = Picture()
#       self.assertEqual(self.pict.toString(), 'Picture, filename null height 0 width 0', 
#                   'toString %s != Picture, filename null height 0 width 0' % self.pict.toString())

#   def testPictureNull(self):
#       '''Test Picture() constructor [all]'''
#       self.pict = Picture()
#       # NOTE: Must do a null check here by sending null to '%s' so it prints as 'None' and does not
#       #    end up throwing a null pointer exception
#       self.assertEqual('%s'%self.pict.getFileName(), 'None', 'Filename %s != None' % self.pict.getFileName())
#       self.assertEqual('%s'%self.pict.getExtension(), 'None',  'File extension %s != None' % self.pict.getExtension())
#       self.assertEqual('%s'%self.pict.getTitle(), 'None', 'Title %s != None' % self.pict.getTitle())
#       self.assertEqual(self.pict.getWidth(), 0, 'Width %s != 0' % self.pict.getWidth())
#       self.assertEqual(self.pict.getHeight(), 0, 'Height %s != 0' % self.pict.getHeight())
#       self.assertNotEqual(self.pict.getWidth(), 1, 'Width is 1?')
#       self.assertEqual(self.pict.toString(), 'Picture, filename None height 0 width 0', 
#                   'toString %s != Picture, filename None height 0 width 0' % self.pict.toString())

    def testPictureWdtHgt(self):
        '''Test Picture(width, height) constructor'''
        self.pict = Picture(500,500)
        # NOTE: Must do a null check here by sending null to '%s' so it prints as 'None' and does not
        #    end up throwing a null pointer exception
#       self.assertEqual('%s'%self.pict.getFileName(), 'None', 'Filename %s != None' % self.pict.getFileName())
#       self.assertEqual(self.pict.getExtension(), 'jpg', 'File extension %s != jpg' % self.pict.getExtension())
#       self.assertEqual(self.pict.getTitle(), 'New Picture', 'Title %s != New Picture' % self.pict.getTitle())
        self.assertEqual(media.getWidth(self.pict), 500, 'Width %s != 500' % self.pict.getWidth())
        self.assertEqual(media.getHeight(self.pict), 500, 'Height %s != 500' % self.pict.getHeight())
#       self.assertNotEqual(self.pict.getWidth(), 499, 'Width is 499?')
#       self.assertEqual(self.pict.toString(), 'Picture, filename null height 500 width 500', 
#                   'toString %s != Picture, filename null height 500 width 500' % self.pict.toString())

    def testTitleP(self):
        '''Test picture - changing title from Picture()'''
        self.pict = Picture()
        self.assertEqual('%s'%self.pict.getTitle(),'None','Title %s != None' % self.pict.getTitle())
        self.pict.setTitle("Blank object")
        self.assertNotEqual('%s'%self.pict.getTitle(), 'None', 'Title did not change')
        self.assertEqual(self.pict.getTitle(), 'Blank object', 'Title %s != Blank object' % self.pict.getTitle())

    def testTitlePII(self):
        '''Test picture - changing title from Picture(int,int)'''
        self.pict = Picture(20,20)
        self.assertEqual('%s'%self.pict.getTitle(),'None','Title %s != None' % self.pict.getTitle())
        self.pict.setTitle("Blank object")
        self.assertNotEqual('%s'%self.pict.getTitle(), 'None', 'Title did not change')
        self.assertEqual(self.pict.getTitle(), 'Blank object', 'Title %s != Blank object' % self.pict.getTitle())

    def testAddMessage(self):
        '''Test Picture.addMessage'''
        self.pict = Picture(150,50) 
        self.pict.addMessage("This is a test",25,25)
        self.pict.addText(media.red, 10, 10, "test")
        self.pict.addText(media.red, 10, 10, "test")
        self.pict.addTextWithStyle(media.red,10,10,"This is a test",media.makeStyle(media.mono,media.italic,18))
        print 'Temporarily disabled by timmy because it is annoying'
        #self.pict.show()
        #success = swing.JOptionPane.showConfirmDialog(None, 'Does the graphic say "This is a test"?', "TestAddMsgOP", swing.JOptionPane.YES_NO_OPTION)
        #self.pict.getPictureFrame().hide()
        #self.assertEqual(success, swing.JOptionPane.YES_OPTION, 'success is %s and we wanted %s'%(success,1))


#if __name__ == '__main__':
#    unittest.main()

#suite = unittest.makeSuite(Test_Picture)
#unittest.TextTestRunner(verbosity=2).run(suite)
