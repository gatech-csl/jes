import unittest
import SimpleSound
import media
import Sound

class Test_Sound_BookExamples(unittest.TestCase):

    def testIncreaseVol(self):
        '''Test Increase Volume'''
        
        f = 'Blip.wav'
        media.setTestMediaFolder()
        sound = media.makeSound(f)

        samples = media.getSamples(sound)
        i = 0

        while i < media.getLength(sound):
        # for sample in media.getSamples(sound):
            value = media.getSampleValueAt(sound, i)                 
            media.setSample( media.getSampleObjectAt(sound, i),(value*2.0))
            i = i+1
        
        original = media.makeSound(f)

        counter = 0     
        while counter < media.getLength(sound):
            newval = int(round(media.getSampleValueAt(original, counter)*2.0))
            if (newval > 32767):
                newval = 32767
            if(newval < -32768):
                newval = -32768
            if(media.getSampleValueAt(sound,counter)!=newval):
                self.fail("Sample %s not increased properly" % counter)
            counter += 1
                
    def testDecreaseVolume(self):
        '''Test Decrease Volume'''
        
        f = 'Blip.wav'
        media.setTestMediaFolder()
        sound = media.makeSound(f)
        # samples = media.getSamples(sound)
        i = 0
        counter = 0

        print "changing"

        # while i <= media.getLength(sound):
        for sample in media.getSamples(sound):
            value = media.getSample(sample)
            media.setSample( sample ,(value*0.5))

        print "comparing"
        original = media.makeSound(f)

        counter = 0     
        while counter < media.getLength(sound):
            if( int(media.getSampleValueAt(sound,counter)) != int(media.getSampleValueAt(original,counter)*0.5) ):
                self.fail("Sample %s not decreased properly" % counter)
                    #print "%s != %s at %s" % (media.getSampleValueAt(sound,counter), (media.getSampleValueAt(original,counter)*2.0), counter)
            counter += 1
                        
    def testNormalize(self):
        '''Test Normalize Volume'''

        largest = 0
        f = 'Blip.wav'
        media.setTestMediaFolder()
        sound = media.makeSound(f)

        #for sample in media.getSamples(sound):
        counter = 0     
        while counter < media.getLength(sound):
            sample = media.getSampleObjectAt(sound, counter)
            largest = max(largest, abs(media.getSample(sample)), media.getSample(sample))
            counter += 1

        amplification = 32767.0 / largest

        counter = 0     
        while counter < media.getLength(sound):
            sample = media.getSampleObjectAt(sound, counter)
            louder =  amplification * media.getSample(sample)  
            media.setSample(sample, louder)
            counter += 1
                
        original = media.makeSound(f)
        
        counter = 0     
        while counter < media.getLength(sound):
            if( int(media.getSampleValueAt(sound,counter)) != int(media.getSampleValueAt(original,counter)*amplification)):
                self.fail("Sample %s not normalized properly" % counter)
                    #print "%s != %s at %s" % (media.getSampleValueAt(sound,counter), (media.getSampleValueAt(original,counter)*amplification), counter)
            counter += 1
                        
    def testMedia(self):
        f = "preamble.wav"
        media.setTestMediaFolder()
        sound = media.makeSound(f)
        self.assertEquals(sound.getLength(), 421110)
        #self.assertEquals(media.getSamples(sound), 421110)
        self.assertEquals(media.getSampleValueAt(sound,0),36)
        self.assertEquals(media.getSampleValueAt(sound,1),29)
        #self.assertEquals(media.getLength(sound),220568)
        self.assertEquals(media.getSamplingRate(sound),22050.0)
        self.assertEquals(media.getSampleValueAt(sound,220567),44)
