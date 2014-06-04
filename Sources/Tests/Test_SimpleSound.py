import unittest
import Sound
import SimpleSound
import javax.sound.sampled.AudioFileFormat as AudioFileFormat
import javax.sound.sampled.AudioFileFormat.Type as AudioFileFormatType
import javax.sound.sampled.AudioFormat as AudioFormat
import javax.sound.sampled.AudioFormat.Encoding as AudioFormatEncoding
import java.lang.NegativeArraySizeException

########################################################################################################
#   UTILITY FUNCTIONS
########################################################################################################

''' lengthInBytes = sampleRate * numOfChannels * numSeconds * bytesPerSample 
    samples = lengthInBytes / bytesPerSample (formula gotten from SimpleSound.java)
                         or simply
    samples = sampleRate * numOfChannels * numSeconds'''

def getSamples(numSeconds, numChannels):
    return numSeconds*numChannels*22050
    
def createTestSound():
    simple = SimpleSound()
    audioFormat = AudioFormat(AudioFormat.Encoding.ALAW, 22050, 16, 1, 2, 22050, 0)
    AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
    simple.setAudioFileFormat(AFF)
    simple.setBuffer(6615*2)
    simple.write("testSound.wav")

########################################################################################################


########################################################################################################
#
#   SIMPLE SOUND
#
########################################################################################################

print '''Run Tests on SimpleSound()'''
class Test_SimpleSound(unittest.TestCase):

    def setUp(self):
        '''Test SimpleSound(), Create a SimpleSound of 3 seconds long\n'''
        self.simple = SimpleSound()
        
#   def testSamples(self):      
#       '''Verify a sound of 3 seconds long will have 66150 Samples'''
#       self.assertEquals(self.simple.getLength(),66150,
#           'Length (in Samples) is %s != %s' % (self.simple.getLength(), 66150))
            
    def testAudioFileFormat(self):
        '''Verify sound created is WAVE AudioFileFormat'''
        AFF = self.simple.getAudioFileFormat()
        self.assertEquals(AFF.getType(),  AudioFileFormat.Type.WAVE, 
            'AudioFileFormat is %s != WAVE' % AFF.getType())

    def testSamplingRate(self):
        '''Verify sound created has Sampling Rate of 22.05K'''
        self.assertEquals(self.simple.getSamplingRate(), 22050,
            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), 22050.0))

    def testBitSample(self):
        '''Verify sound created has 16 Bit Sample'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), 16,
            'Sample bit size is %s != 16' % AF.getSampleSizeInBits())

    def testChannels(self):     
        '''Verify sound created has one Channel'''
        self.assertEquals(self.simple.getChannels(), 1,
            'Num of Channels is %s != 1' % self.simple.getChannels())
        
    def testIsStereo(self):
        '''Verify sound created is not in Stereo'''
        self.assertEquals(self.simple.isStereo(), 0,
            'SimpleSound is in stereo')

    def testAudioFormatEncoding(self):
        '''Verify sound created has signed PCM encoding'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

    def testByteOrder(self):
        '''Verify sound created is Small-Endian Byte Order'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.isBigEndian(), 0,
            'Sound is Big-Endian Byte Order')
        
#suite = unittest.makeSuite(Test_SimpleSound)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(3 Seconds)'''
class Test_SimpleSound_3Secs(unittest.TestCase):

    def setUp(self):
        '''Test SimpleSound(3), Create a SimpleSound of 3 seconds long\n'''
        self.NUM_SECS = 3
        self.simple = SimpleSound(self.NUM_SECS)
        
#   def testSamples(self):      
#       '''Verify a sound of 3 seconds long will have 66150 Samples'''
#       self.assertEquals(self.simple.getLength(),getSamples(self.NUM_SECS,1),
#           'Length (in Samples) is %s != %s' % (self.simple.getLength(), getSamples(self.NUM_SECS,1)))
            
    def testAudioFileFormat(self):
        '''Verify sound created is WAVE AudioFileFormat'''
        AFF = self.simple.getAudioFileFormat()
        self.assertEquals(AFF.getType(),  AudioFileFormat.Type.WAVE, 
            'AudioFileFormat is %s != WAVE' % AFF.getType())

    def testSamplingRate(self):
        '''Verify sound created has Sampling Rate of 22.05K'''
        self.assertEquals(self.simple.getSamplingRate(), 22050,
            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), 22050.0))

    def testBitSample(self):
        '''Verify sound created has 16 Bit Sample'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), 16,
            'Sample bit size is %s != 16' % AF.getSampleSizeInBits())

    def testChannels(self):     
        '''Verify sound created has one Channel'''
        self.assertEquals(self.simple.getChannels(), 1,
            'Num of Channels is %s != 1' % self.simple.getChannels())
        
    def testIsStereo(self):
        '''Verify sound created is not in Stereo'''
        self.assertEquals(self.simple.isStereo(), 0,
            'SimpleSound is in stereo')

    def testAudioFormatEncoding(self):
        '''Verify sound created has signed PCM encoding'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

    def testByteOrder(self):
        '''Verify sound created is Small-Endian Byte Order'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.isBigEndian(), 0,
            'Sound is Big-Endian Byte Order')   

#suite = unittest.makeSuite(Test_SimpleSound_3Secs)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(8 Seconds)'''
class Test_SimpleSound_8Secs(unittest.TestCase):

    def setUp(self):
        '''Test SimpleSound(8), Create a SimpleSound of 8 seconds long\n'''
        self.NUM_SECS = 8
        self.simple = SimpleSound(self.NUM_SECS)
        
#   def testSamples(self):      
#       '''Verify number of Samples in SimpleSound of length 8 seconds'''
#       self.assertEquals(self.simple.getLength(),getSamples(self.NUM_SECS,1),
#           'Length (in Samples) is %s != %s' % (self.simple.getLength(), getSamples(self.NUM_SECS,1)))
            
    def testAudioFileFormat(self):
        '''Verify sound created is WAVE AudioFileFormat'''
        AFF = self.simple.getAudioFileFormat()
        self.assertEquals(AFF.getType(),  AudioFileFormat.Type.WAVE, 
            'AudioFileFormat is %s != WAVE' % AFF.getType())

    def testSamplingRate(self):
        '''Verify sound created has Sampling Rate of 22.05K'''
        self.assertEquals(self.simple.getSamplingRate(), 22050,
            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), 22050.0))

    def testBitSample(self):
        '''Verify sound created has 16 Bit Sample'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), 16,
            'Sample bit size is %s != 16' % AF.getSampleSizeInBits())

    def testChannels(self):     
        '''Verify sound created has one Channel'''
        self.assertEquals(self.simple.getChannels(), 1,
            'Num of Channels is %s != 1' % self.simple.getChannels())
        
    def testIsStereo(self):
        '''Verify sound created is not in Stereo'''
        self.assertEquals(self.simple.isStereo(), 0,
            'SimpleSound is in stereo')

    def testAudioFormatEncoding(self):
        '''Verify sound created has signed PCM encoding'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

    def testByteOrder(self):
        '''Verify sound created is Small-Endian Byte Order'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.isBigEndian(), 0,
            'Sound is Big-Endian Byte Order')   

#suite = unittest.makeSuite(Test_SimpleSound_8Secs)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(0 Seconds)'''
class Test_SimpleSound_0Secs(unittest.TestCase):

    def setUp(self):
        '''Test SimpleSound(0), Create a SimpleSound of 0 seconds long\n'''
        self.NUM_SECS = 0
        self.simple = SimpleSound(self.NUM_SECS)
        
#   def testSamples(self):      
#       '''Verify number of Samples in SimpleSound of length 0 seconds'''
#       self.assertEquals(self.simple.getLength(),getSamples(self.NUM_SECS,1),
#           'Length (in Samples) is %s != %s' % (self.simple.getLength(), getSamples(self.NUM_SECS,1)))
            
    def testAudioFileFormat(self):
        '''Verify sound created is WAVE AudioFileFormat'''
        AFF = self.simple.getAudioFileFormat()
        self.assertEquals(AFF.getType(),  AudioFileFormat.Type.WAVE, 
            'AudioFileFormat is %s != WAVE' % AFF.getType())

    def testSamplingRate(self):
        '''Verify sound created has Sampling Rate of 22.05K'''
        self.assertEquals(self.simple.getSamplingRate(), 22050,
            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), 22050.0))

    def testBitSample(self):
        '''Verify sound created has 16 Bit Sample'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), 16,
            'Sample bit size is %s != 16' % AF.getSampleSizeInBits())

    def testChannels(self):     
        '''Verify sound created has one Channel'''
        self.assertEquals(self.simple.getChannels(), 1,
            'Num of Channels is %s != 1' % self.simple.getChannels())
        
    def testIsStereo(self):
        '''Verify sound created is not in Stereo'''
        self.assertEquals(self.simple.isStereo(), 0,
            'SimpleSound is in stereo')

    def testAudioFormatEncoding(self):
        '''Verify sound created has signed PCM encoding'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

    def testByteOrder(self):
        '''Verify sound created is Small-Endian Byte Order'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.isBigEndian(), 0,
            'Sound is Big-Endian Byte Order')   

#suite = unittest.makeSuite(Test_SimpleSound_0Secs)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(-1 Seconds)'''
class Test_SimpleSound_n1Secs(unittest.TestCase):

    def testException(self):
        '''Test SimpleSound(-1), Verify NegativeArrayException is Raised\n'''
        self.NUM_SECS = -1
        try:
            SimpleSound(self.NUM_SECS)
        except java.lang.NegativeArraySizeException:
            '''WORKS'''
        except:
            self.fail('Failed to raise NegativeArrayException')
        
#suite = unittest.makeSuite(Test_SimpleSound_n1Secs)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(100 Seconds)'''
class Test_SimpleSound_100Secs(unittest.TestCase):

    def setUp(self):
        '''Test SimpleSound(100), Create a SimpleSound of 100 seconds long\n'''
        self.NUM_SECS = 100
        self.simple = SimpleSound(self.NUM_SECS)

        
#   def testSamples(self):      
#       '''Verify number of Samples in SimpleSound of length 100 seconds'''
#       self.assertEquals(self.simple.getLength(),getSamples(self.NUM_SECS,1),
#           'Length (in Samples) is %s != %s' % (self.simple.getLength(), getSamples(self.NUM_SECS,1)))
            
    def testAudioFileFormat(self):
        '''Verify sound created is WAVE AudioFileFormat'''
        AFF = self.simple.getAudioFileFormat()
        self.assertEquals(AFF.getType(),  AudioFileFormat.Type.WAVE, 
            'AudioFileFormat is %s != WAVE' % AFF.getType())

    def testSamplingRate(self):
        '''Verify sound created has Sampling Rate of 22.05K'''
        self.assertEquals(self.simple.getSamplingRate(), 22050,
            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), 22050.0))

    def testBitSample(self):
        '''Verify sound created has 16 Bit Sample'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), 16,
            'Sample bit size is %s != 16' % AF.getSampleSizeInBits())

    def testChannels(self):     
        '''Verify sound created has one Channel'''
        self.assertEquals(self.simple.getChannels(), 1,
            'Num of Channels is %s != 1' % self.simple.getChannels())
        
    def testIsStereo(self):
        '''Verify sound created is not in Stereo'''
        self.assertEquals(self.simple.isStereo(), 0,
            'SimpleSound is in stereo')

    def testAudioFormatEncoding(self):
        '''Verify sound created has signed PCM encoding'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

    def testByteOrder(self):
        '''Verify sound created is Small-Endian Byte Order'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.isBigEndian(), 0,
            'Sound is Big-Endian Byte Order')   

#suite = unittest.makeSuite(Test_SimpleSound_100Secs)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

#print '''Run Tests on SimpleSound(16 Bits, SmallEndian)'''
#class Test_SimpleSound_16s(unittest.TestCase):

#    def setUp(self):
#        '''Test SimpleSound(16 Bits, SmallEndian)\n'''
#        self.NUM_SECS = 3
#        self.simple = SimpleSound(16,0)
        
#   def testSamples(self):      
#       '''Verify number of Samples in SimpleSound of length 16 Bits'''
#       self.assertEquals(self.simple.getLength(), getSamples(self.NUM_SECS,1),
#           'Length (in Samples) is %s != %s' % (self.simple.getLength(), getSamples(self.NUM_SECS,1)))
            
#    def testAudioFileFormat(self):
#        '''Verify sound created is WAVE AudioFileFormat'''
#        AFF = self.simple.getAudioFileFormat()
#        self.assertEquals(AFF.getType(),  AudioFileFormat.Type.WAVE, 
#            'AudioFileFormat is %s != WAVE' % AFF.getType())

#    def testSamplingRate(self):
#        '''Verify sound created has Sampling Rate of 22.05K'''
#        self.assertEquals(self.simple.getSamplingRate(), 22050,
#            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), 22050.0))

#    def testBitSample(self):
#        '''Verify sound created has 16 Bit Sample'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.getSampleSizeInBits(), 16,
#            'Sample bit size is %s != 16' % AF.getSampleSizeInBits())

#    def testChannels(self):     
#        '''Verify sound created has one Channel'''
#        self.assertEquals(self.simple.getChannels(), 1,
#            'Num of Channels is %s != 1' % self.simple.getChannels())
        
#    def testIsStereo(self):
#        '''Verify sound created is not in Stereo'''
#        self.assertEquals(self.simple.isStereo(), 0,
#            'SimpleSound is in stereo')

#    def testAudioFormatEncoding(self):
#        '''Verify sound created has signed PCM encoding'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
#            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

#    def testByteOrder(self):
#        '''Verify sound created is Small-Endian Byte Order'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.isBigEndian(), 0,
#            'Sound is Big-Endian Byte Order')

#suite = unittest.makeSuite(Test_SimpleSound_16s)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

#print '''Run Tests on SimpleSound(8 Bits, SmallEndian)'''
#class Test_SimpleSound_8s(unittest.TestCase):

#    def setUp(self):
#        '''Test SimpleSound(8 Bits, SmallEndian)\n'''
#        self.NUM_SECS = 3
#        self.simple = SimpleSound(8,0)
        
#   def testSamples(self):      
#       '''Verify number of Samples in SimpleSound of length 16 Bits'''
#       self.assertEquals(self.simple.getLength(), getSamples(self.NUM_SECS,1),
#           'Length (in Samples) is %s != %s' % (self.simple.getLength(), getSamples(self.NUM_SECS,1)))
            
#    def testAudioFileFormat(self):
#        '''Verify sound created is WAVE AudioFileFormat'''
#        AFF = self.simple.getAudioFileFormat()
#        self.assertEquals(AFF.getType(),  AudioFileFormat.Type.WAVE, 
#            'AudioFileFormat is %s != WAVE' % AFF.getType())

#    def testSamplingRate(self):
#        '''Verify sound created has Sampling Rate of 22.05K'''
#        self.assertEquals(self.simple.getSamplingRate(), 22050,
#            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), 22050.0))

#    def testBitSample(self):
#        '''Verify sound created has 16 Bit Sample'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.getSampleSizeInBits(), 16,
#            'Sample bit size is %s != 16' % AF.getSampleSizeInBits())

#    def testChannels(self):     
#        '''Verify sound created has one Channel'''
#        self.assertEquals(self.simple.getChannels(), 1,
#            'Num of Channels is %s != 1' % self.simple.getChannels())
        
#    def testIsStereo(self):
#        '''Verify sound created is not in Stereo'''
#        self.assertEquals(self.simple.isStereo(), 0,
#            'SimpleSound is in stereo')

#    def testAudioFormatEncoding(self):
#        '''Verify sound created has signed PCM encoding'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
#            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

#    def testByteOrder(self):
#        '''Verify sound created is Small-Endian Byte Order'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.isBigEndian(), 0,
#            'Sound is Big-Endian Byte Order')

#suite = unittest.makeSuite(Test_SimpleSound_8s)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

#print '''Run Tests on SimpleSound(16 Bits, BigEndian)'''
#class Test_SimpleSound_16b(unittest.TestCase):

#    def setUp(self):
#        '''Test SimpleSound(8 Bits, SmallEndian)\n'''
#        self.NUM_SECS = 3
#        self.simple = SimpleSound(16,1)
        
#   def testSamples(self):      
#       '''Verify number of Samples in SimpleSound of length 16 Bits'''
#       self.assertEquals(self.simple.getLength(), getSamples(self.NUM_SECS,1),
#           'Length (in Samples) is %s != %s' % (self.simple.getLength(), getSamples(self.NUM_SECS,1)))
            
#    def testAudioFileFormat(self):
#        '''Verify sound created is WAVE AudioFileFormat'''
#        AFF = self.simple.getAudioFileFormat()
#        self.assertEquals(AFF.getType(),  AudioFileFormat.Type.WAVE, 
#            'AudioFileFormat is %s != WAVE' % AFF.getType())

#    def testSamplingRate(self):
#        '''Verify sound created has Sampling Rate of 22.05K'''
#        self.assertEquals(self.simple.getSamplingRate(), 22050,
#            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), 22050.0))

#    def testBitSample(self):
#        '''Verify sound created has 16 Bit Sample'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.getSampleSizeInBits(), 16,
#            'Sample bit size is %s != 16' % AF.getSampleSizeInBits())

#    def testChannels(self):     
#        '''Verify sound created has one Channel'''
#        self.assertEquals(self.simple.getChannels(), 1,
#            'Num of Channels is %s != 1' % self.simple.getChannels())
        
#    def testIsStereo(self):
#        '''Verify sound created is not in Stereo'''
#        self.assertEquals(self.simple.isStereo(), 0,
#            'SimpleSound is in stereo')

#    def testAudioFormatEncoding(self):
#        '''Verify sound created has signed PCM encoding'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
#            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

#    def testByteOrder(self):
#        '''Verify sound created is Big-Endian Byte Order'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.isBigEndian(), 1,
#            'Sound is Small-Endian Byte Order')

#suite = unittest.makeSuite(Test_SimpleSound_16b)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

#print '''Run Tests on SimpleSound(8 Bits, BigEndian)'''
#class Test_SimpleSound_8b(unittest.TestCase):

#    def setUp(self):
#        '''Test SimpleSound(8 Bits, SmallEndian)\n'''
#        self.NUM_SECS = 3
#        self.simple = SimpleSound(8,1)
        
#   def testSamples(self):      
#       '''Verify number of Samples in SimpleSound of length 16 Bits'''
#       self.assertEquals(self.simple.getLength(), getSamples(self.NUM_SECS,1),
#           'Length (in Samples) is %s != %s' % (self.simple.getLength(), getSamples(self.NUM_SECS,1)))
            
#    def testAudioFileFormat(self):
#        '''Verify sound created is WAVE AudioFileFormat'''
#        AFF = self.simple.getAudioFileFormat()
#        self.assertEquals(AFF.getType(),  AudioFileFormat.Type.WAVE, 
#            'AudioFileFormat is %s != WAVE' % AFF.getType())

#    def testSamplingRate(self):
#        '''Verify sound created has Sampling Rate of 22.05K'''
#        self.assertEquals(self.simple.getSamplingRate(), 22050,
#            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), 22050.0))

#    def testBitSample(self):
#        '''Verify sound created has 16 Bit Sample'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.getSampleSizeInBits(), 8,
#            'Sample bit size is %s != 16' % AF.getSampleSizeInBits())

#    def testChannels(self):     
#        '''Verify sound created has one Channel'''
#        self.assertEquals(self.simple.getChannels(), 1,
#            'Num of Channels is %s != 1' % self.simple.getChannels())
        
#    def testIsStereo(self):
#        '''Verify sound created is not in Stereo'''
#        self.assertEquals(self.simple.isStereo(), 0,
#            'SimpleSound is in stereo')

#    def testAudioFormatEncoding(self):
#        '''Verify sound created has signed PCM encoding'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
#            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

#    def testByteOrder(self):
#        '''Verify sound created is Small-Endian Byte Order'''
#        AF = self.simple.getAudioFileFormat().getFormat()
#        self.assertEquals(AF.isBigEndian(), 1,
#            'Sound is Big-Endian Byte Order')

#suite = unittest.makeSuite(Test_SimpleSound_8b)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 3secs)'''
class Test_SimpleSound_s3(unittest.TestCase):

    def setUp(self):
        self.original = SimpleSound()
        self.simple = SimpleSound(self.original)

    def testSamples(self):      
        '''Verify number of Samples in Copy = Original'''
        self.assertEquals(self.simple.getLength(), self.original.getLength(),
            'Length (in Samples) is %s != %s' % (self.simple.getLength(), self.original.getLength()))
            
    def testAudioFileFormat(self):
        '''Verify AudioFileFormat in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        OAFF = self.original.getAudioFileFormat()
        self.assertEquals(AFF.getType(),  OAFF.getType(), 
            'AudioFileFormat is %s != %s' % (AFF.getType(), OAFF.getType()))

    def testSamplingRate(self):
        '''Verify Sampling Rate in Copy = Original'''
        self.assertEquals(self.simple.getSamplingRate(), self.original.getSamplingRate(),
            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), self.original.getSamplingRate()))

    def testBitSample(self):
        '''Verify Bit Sample in Copy = Original'''
        AF = self.simple.getAudioFileFormat().getFormat()
        OAF = self.original.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), OAF.getSampleSizeInBits(),
            'Sample bit size is %s != %s' % (AF.getSampleSizeInBits(), OAF.getSampleSizeInBits()))

    def testChannels(self):     
        '''Verify Channel(s) in Copy = Original'''
        self.assertEquals(self.simple.getChannels(), self.original.getChannels(),
            'Num of Channels is %s != %s' % (self.simple.getChannels(), self.original.getChannels()))
        
    def testIsStereo(self):
        '''Verify Stereo in Copy = Original'''
        self.assertEquals(self.simple.isStereo(), self.original.isStereo(),
            'Stereo is %s != %s' % (self.simple.isStereo(), self.original.isStereo()))

    def testAudioFormatEncoding(self):
        '''Verify Encoding in Copy = Original'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

    def testByteOrder(self):
        '''Verify Byte Order in Copy = Original'''
        AF = self.simple.getAudioFileFormat().getFormat()
        OAF = self.original.getAudioFileFormat().getFormat()
        self.assertEquals(AF.isBigEndian(), OAF.isBigEndian(),
            'Byte Order is %s != %s' % (AF.isBigEndian(), OAF.isBigEndian()))

#suite = unittest.makeSuite(Test_SimpleSound_s3)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 5secs)'''
class Test_SimpleSound_s5(unittest.TestCase):

    def setUp(self):
        self.original = SimpleSound(5)
        self.simple = SimpleSound(self.original)

    def testSamples(self):      
        '''Verify number of Samples in Copy = Original'''
        self.assertEquals(self.simple.getLength(), self.original.getLength(),
            'Length (in Samples) is %s != %s' % (self.simple.getLength(), self.original.getLength()))
            
    def testAudioFileFormat(self):
        '''Verify AudioFileFormat in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        OAFF = self.original.getAudioFileFormat()
        self.assertEquals(AFF.getType(),  OAFF.getType(), 
            'AudioFileFormat is %s != %s' % (AFF.getType(), OAFF.getType()))

    def testSamplingRate(self):
        '''Verify Sampling Rate in Copy = Original'''
        self.assertEquals(self.simple.getSamplingRate(), self.original.getSamplingRate(),
            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), self.original.getSamplingRate()))

    def testBitSample(self):
        '''Verify Bit Sample in Copy = Original'''
        AF = self.simple.getAudioFileFormat().getFormat()
        OAF = self.original.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), OAF.getSampleSizeInBits(),
            'Sample bit size is %s != %s' % (AF.getSampleSizeInBits(), OAF.getSampleSizeInBits()))

    def testChannels(self):     
        '''Verify Channel(s) in Copy = Original'''
        self.assertEquals(self.simple.getChannels(), self.original.getChannels(),
            'Num of Channels is %s != %s' % (self.simple.getChannels(), self.original.getChannels()))
        
    def testIsStereo(self):
        '''Verify Stereo in Copy = Original'''
        self.assertEquals(self.simple.isStereo(), self.original.isStereo(),
            'Stereo is %s != %s' % (self.simple.isStereo(), self.original.isStereo()))

    def testAudioFormatEncoding(self):
        '''Verify Encoding in Copy = Original'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))

    def testByteOrder(self):
        '''Verify Byte Order in Copy = Original'''
        AF = self.simple.getAudioFileFormat().getFormat()
        OAF = self.original.getAudioFileFormat().getFormat()
        self.assertEquals(AF.isBigEndian(), OAF.isBigEndian(),
            'Byte Order is %s != %s' % (AF.isBigEndian(), OAF.isBigEndian()))

#suite = unittest.makeSuite(Test_SimpleSound_s5)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound ALAW_ENCODING )'''
class Test_SimpleSound_AIFC(unittest.TestCase):

    def setUp(self):
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.ALAW, 22050, 16, 1, 16,22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testAudioFormatEncoding(self):
        '''Verify Encoding is ALAW'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.ALAW,
            'Encoding is %s != ALAW' % (AF.getEncoding()))      

    def testAudioFormatEncoding(self):
        '''Verify Encoding in Copy = Original'''
        AF = self.simple.getAudioFileFormat().getFormat()
        OAF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), OAF.getEncoding(),
            'Encoding is %s != %s' % (AF.getEncoding(), OAF.getEncoding()))

#suite = unittest.makeSuite(Test_SimpleSound_AIFC)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound PCM_SIGNED_ENCODING )'''
class Test_SimpleSound_PCMSIGNED(unittest.TestCase):

    def setUp(self):
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, 1, 16,22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testAudioFormatEncoding(self):
        '''Verify Encoding is PCM_SIGNED'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.PCM_SIGNED,
            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))        

    def testAudioFormatEncoding(self):
        '''Verify Encoding in Copy = Original'''
        AF = self.simple.getAudioFileFormat().getFormat()
        OAF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), OAF.getEncoding(),
            'Encoding is %s != %s' % (AF.getEncoding(), OAF.getEncoding()))

#suite = unittest.makeSuite(Test_SimpleSound_PCMSIGNED)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound PCM_UNSIGNED_ENCODING )'''
class Test_SimpleSound_PCMUNSIGNED(unittest.TestCase):

    def setUp(self):
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_UNSIGNED, 22050, 16, 1, 16,22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testAudioFormatEncoding(self):
        '''Verify Encoding is PCM_UNSIGNED'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.UNPCM_SIGNED,
            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))        

    def testAudioFormatEncoding(self):
        '''Verify Encoding in Copy = Original'''
        AF = self.simple.getAudioFileFormat().getFormat()
        OAF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), OAF.getEncoding(),
            'Encoding is %s != %s' % (AF.getEncoding(), OAF.getEncoding()))

#suite = unittest.makeSuite(Test_SimpleSound_PCMUNSIGNED)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound ULAW )'''
class Test_SimpleSound_ULAW(unittest.TestCase):

    def setUp(self):
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.ULAW, 22050, 16, 1, 16,22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testAudioFormatEncoding(self):
        '''Verify Encoding is PCM_SIGNED'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.ULAW,
            'Encoding is %s != PCM_SIGNED' % (AF.getEncoding()))        

    def testAudioFormatEncoding(self):
        '''Verify Encoding in Copy = Original'''
        AF = self.simple.getAudioFileFormat().getFormat()
        OAF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), OAF.getEncoding(),
            'Encoding is %s != %s' % (AF.getEncoding(), OAF.getEncoding()))

#suite = unittest.makeSuite(Test_SimpleSound_ULAW)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 22.05K SamplingRate )'''
class Test_SimpleSound_22KSR(unittest.TestCase):

    def setUp(self):
        self.samplingRate = 22050
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, self.samplingRate, 16, 1, 16,22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testSamplingRate(self):
        '''Verify SamplingRate is 22050'''
        self.assertEquals(self.simple.getSamplingRate(), self.samplingRate,
            'SamplingRate is %s != %s' % (self.simple.getSamplingRate(), self.samplingRate))

    def testAudioFormatSamplingRate(self):
        '''Verify SamplingRate in Copy = Original'''
        self.assertEquals(self.simple.getSamplingRate(), self.original.getSamplingRate(),
            'SamplingRate is %s != %s' % (self.simple.getSamplingRate(), self.original.getSamplingRate()))

#suite = unittest.makeSuite(Test_SimpleSound_22KSR)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 5K SamplingRate )'''
class Test_SimpleSound_5KSR(unittest.TestCase):

    def setUp(self):
        self.samplingRate = 5000
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, self.samplingRate, 16, 1, 16,22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testSamplingRate(self):
        '''Verify SamplingRate is 5000'''
        self.assertEquals(self.simple.getSamplingRate(), self.samplingRate,
            'SamplingRate is %s != %s' % (self.simple.getSamplingRate(), self.samplingRate))

    def testAudioFormatSamplingRate(self):
        '''Verify SamplingRate in Copy = Original'''
        self.assertEquals(self.simple.getSamplingRate(), self.original.getSamplingRate(),
            'SamplingRate is %s != %s' % (self.simple.getSamplingRate(), self.original.getSamplingRate()))

#suite = unittest.makeSuite(Test_SimpleSound_5KSR)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 16 SampleSize )'''
class Test_SimpleSound_16sample(unittest.TestCase):

    def setUp(self):
        self.sampleSizeBits = 16
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, self.sampleSizeBits, 1, 16,22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testSampleSize(self):
        '''Verify SampleSize is 16'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), self.sampleSizeBits,
            'SampleSize is %s != %s' % (AF.getSampleSizeInBits(), self.sampleSizeBits))

    def testAudioFormatSamleSize(self):
        '''Verify SampleSize in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        OAFF = self.original.getAudioFileFormat()
        OAF = OAFF.getFormat()
        self.assertEquals(AF.getSampleSizeInBits(),OAF.getSampleSizeInBits(),
            'SampleSize is %s != %s' % (AF.getSampleSizeInBits(),OAF.getSampleSizeInBits()))

#suite = unittest.makeSuite(Test_SimpleSound_16sample)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 8 SampleSize )'''
class Test_SimpleSound_8sample(unittest.TestCase):

    def setUp(self):
        self.sampleSizeBits = 8
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, self.sampleSizeBits, 1, 16,22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testSampleSize(self):
        '''Verify SampleSize is 8'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), self.sampleSizeBits,
            'SampleSize is %s != %s' % (AF.getSampleSizeInBits(), self.sampleSizeBits))

    def testAudioFormatSampleSize(self):
        '''Verify SampleSize in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        OAFF = self.original.getAudioFileFormat()
        OAF = OAFF.getFormat()
        self.assertEquals(AF.getSampleSizeInBits(),OAF.getSampleSizeInBits(),
            'SampleSize is %s != %s' % (AF.getSampleSizeInBits(),OAF.getSampleSizeInBits()))

#suite = unittest.makeSuite(Test_SimpleSound_8sample)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 1 Channel )'''
class Test_SimpleSound_1c(unittest.TestCase):

    def setUp(self):
        self.channels = 1
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, self.channels, 16,22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testChannels(self):
        '''Verify Channels is 1'''
        self.assertEquals(self.simple.getChannels(), self.channels,
            'SamplingRate is %s != %s' % (self.simple.getChannels(), self.channels))

    def testAudioFormatChannels(self):
        '''Verify Channels in Copy = Original'''
        self.assertEquals(self.simple.getChannels(), self.original.getChannels(),
            'Channels is %s != %s' % (self.simple.getChannels(), self.original.getChannels()))

#suite = unittest.makeSuite(Test_SimpleSound_1c)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 2 Channel )'''
class Test_SimpleSound_2c(unittest.TestCase):

    def setUp(self):
        self.channels = 2
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, self.channels, 16,22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testChannels(self):
        '''Verify Channels is 2'''
        self.assertEquals(self.simple.getChannels(), self.channels,
            'Channels is %s != %s' % (self.simple.getChannels(), self.channels))

    def testAudioFormatChannels(self):
        '''Verify Channels in Copy = Original'''
        self.assertEquals(self.simple.getChannels(), self.original.getChannels(),
            'Channels is %s != %s' % (self.simple.getChannels(), self.original.getChannels()))

#suite = unittest.makeSuite(Test_SimpleSound_2c)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 2 FrameSize )'''
class Test_SimpleSound_2frame(unittest.TestCase):

    def setUp(self):
        self.frameSizeBytes = 2
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, 1, self.frameSizeBytes, 22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testFrameSize(self):
        '''Verify FrameSize is 2'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.getFrameSize(), self.frameSizeBytes,
            'FrameSize is %s != %s' % (AF.getFrameSize(), self.frameSizeBytes))

    def testAudioFormatFrameSize(self):
        '''Verify FrameeSize in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        OAFF = self.original.getAudioFileFormat()
        OAF = OAFF.getFormat()
        self.assertEquals(AF.getFrameSize(),OAF.getFrameSize(),
            'FrameSize is %s != %s' % (AF.getFrameSize(),OAF.getFrameSize()))

#suite = unittest.makeSuite(Test_SimpleSound_2frame)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 1 FrameSize )'''
class Test_SimpleSound_1frame(unittest.TestCase):

    def setUp(self):
        self.frameSizeBytes = 1
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, 1, self.frameSizeBytes, 22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testFrameSize(self):
        '''Verify FrameSize is 1'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.getFrameSize(), self.frameSizeBytes,
            'FrameSize is %s != %s' % (AF.getFrameSize(), self.frameSizeBytes))

    def testAudioFormatFrameSize(self):
        '''Verify FrameSize in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        OAFF = self.original.getAudioFileFormat()
        OAF = OAFF.getFormat()
        self.assertEquals(AF.getFrameSize(),OAF.getFrameSize(),
            'FrameSize is %s != %s' % (AF.getFrameSize(),OAF.getFrameSize()))

#suite = unittest.makeSuite(Test_SimpleSound_1frame)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 22K FrameRate )'''
class Test_SimpleSound_22KFR(unittest.TestCase):

    def setUp(self):
        self.frameRate = 22050
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, 1, 2, self.frameRate, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testFrameRate(self):
        '''Verify FrameRate is 22k'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.getFrameRate(), self.frameRate,
            'FrameRate is %s != %s' % (AF.getFrameRate(), self.frameRate))

    def testAudioFormatFrameRate(self):
        '''Verify FrameRate in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        OAFF = self.original.getAudioFileFormat()
        OAF = OAFF.getFormat()
        self.assertEquals(AF.getFrameRate(),OAF.getFrameRate(),
            'FrameRate is %s != %s' % (AF.getFrameRate(),OAF.getFrameRate()))

#suite = unittest.makeSuite(Test_SimpleSound_22KFR)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound 5K FrameRate )'''
class Test_SimpleSound_5KFR(unittest.TestCase):

    def setUp(self):
        self.frameRate = 5000
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, 1, 2, self.frameRate, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testFrameRate(self):
        '''Verify FrameRate is 5k'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.getFrameRate(), self.frameRate,
            'FrameRate is %s != %s' % (AF.getFrameRate(), self.frameRate))

    def testAudioFormatFrameRate(self):
        '''Verify FrameRate in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        OAFF = self.original.getAudioFileFormat()
        OAF = OAFF.getFormat()
        self.assertEquals(AF.getFrameRate(),OAF.getFrameRate(),
            'FrameRate is %s != %s' % (AF.getFrameRate(),OAF.getFrameRate()))

#suite = unittest.makeSuite(Test_SimpleSound_5KFR)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound small endian )'''
class Test_SimpleSound_se(unittest.TestCase):

    def setUp(self):
        self.isBigEndian = 0
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, 1, 2, 22050, self.isBigEndian)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testIsBigEndian(self):
        '''Verify isBigEndian is false'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.isBigEndian(), self.isBigEndian,
            'isBigEndian is %s != %s' % (AF.isBigEndian(), self.isBigEndian))

    def testAudioFormatIsBigEndian(self):
        '''Verify isBigEndian in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        OAFF = self.original.getAudioFileFormat()
        OAF = OAFF.getFormat()
        self.assertEquals(AF.isBigEndian(), OAF.isBigEndian(),
            'isBigEndian is %s != %s' % (AF.isBigEndian(), OAF.isBigEndian()))

#suite = unittest.makeSuite(Test_SimpleSound_se)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound small endian )'''
class Test_SimpleSound_be(unittest.TestCase):

    def setUp(self):
        self.isBigEndian = 1
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, 1, 2, 22050, self.isBigEndian)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, 6615)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testIsBigEndian(self):
        '''Verify isBigEndian is true'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.isBigEndian(), self.isBigEndian,
            'isBigEndian is %s != %s' % (AF.isBigEndian(), self.isBigEndian))

    def testAudioFormatIsBigEndian(self):
        '''Verify isBigEndian in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        OAFF = self.original.getAudioFileFormat()
        OAF = OAFF.getFormat()
        self.assertEquals(AF.isBigEndian(), OAF.isBigEndian(),
            'isBigEndian is %s != %s' % (AF.isBigEndian(), OAF.isBigEndian()))

#suite = unittest.makeSuite(Test_SimpleSound_be)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound frameLength )'''
class Test_SimpleSound_fl(unittest.TestCase):

    def setUp(self):
        self.frameLength = 6615
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, 1, 2, 22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, self.frameLength)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testFrameLength(self):
        '''Verify FrameLength is 6615'''
        AFF = self.simple.getAudioFileFormat()
        self.assertEquals(AFF.getFrameLength(), self.frameLength,
            'FrameLength is %s != %s' % (AFF.getFrameLength(), self.frameLength))

    def testAudioFormatFrameLength(self):
        '''Verify FrameLength in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        OAFF = self.original.getAudioFileFormat()
        self.assertEquals(AFF.getFrameLength(), AFF.getFrameLength(),
            'FrameLength is %s != %s' % (AFF.getFrameLength(), AFF.getFrameLength()))

#suite = unittest.makeSuite(Test_SimpleSound_fl)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound frameLength )'''
class Test_SimpleSound_fl2(unittest.TestCase):

    def setUp(self):
        self.frameLength = 13230
        self.original = SimpleSound()
        audioFormat = AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 22050, 16, 1, 2, 22050, 0)
        AFF = AudioFileFormat(AudioFileFormat.Type.WAVE, audioFormat, self.frameLength)
        self.original.setAudioFileFormat(AFF)
        self.simple = SimpleSound(self.original)
        
    def testFrameLength(self):
        '''Verify FrameLength is 13230'''
        AFF = self.simple.getAudioFileFormat()
        self.assertEquals(AFF.getFrameLength(), self.frameLength,
            'FrameLength is %s != %s' % (AFF.getFrameLength(), self.frameLength))

    def testAudioFormatFrameLength(self):
        '''Verify FrameLength in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        OAFF = self.original.getAudioFileFormat()
        self.assertEquals(AFF.getFrameLength(), AFF.getFrameLength(),
            'FrameLength is %s != %s' % (AFF.getFrameLength(), AFF.getFrameLength()))

#suite = unittest.makeSuite(Test_SimpleSound_fl2)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(SimpleSound Blip )'''
class Test_SimpleSound_blip(unittest.TestCase):

    def setUp(self):
        self.original = SimpleSound("Blip.wav")
        self.simple = SimpleSound(self.original)

    def testSamples(self):      
        '''Verify number of Samples in Copy = Original'''               
        self.assertEquals(self.simple.getLength(), self.original.getLength(),
            'Length (in Samples) is %s != %s' % (self.simple.getLength(), self.original.getLength()))

    def testAudioFileFormat(self):
        '''Verify AudioFileFormat in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        oAFF = self.original.getAudioFileFormat()
        self.assertEquals(AFF.getType(),  oAFF.getType(), 
            'AudioFileFormat is %s != %s' % (AFF.getType(), oAFF.getType()))

    def testSamplingRate(self):
        '''Verify Sampling Rate in Copy = Original'''           
        self.assertEquals(self.simple.getSamplingRate(), self.original.getSamplingRate(), 
            'Sampling rate is %s != %s' % (self.simple.getSamplingRate(), self.original.getSamplingRate()))

    def testBitSample(self):
        '''Verify Bit Sample in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        oAFF = self.original.getAudioFileFormat()
        AF = AFF.getFormat()
        OF = oAFF.getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), OF.getSampleSizeInBits(), 
            'Sample bit size is %s != %s' % (AF.getSampleSizeInBits(), OF.getSampleSizeInBits()))

    def testChannels(self):     
        '''Verify Channel(s) in Copy = Original'''
        self.assertEquals(self.simple.getChannels(), self.original.getChannels(), 
            'Num of Channels is %s != %s' % (self.simple.getChannels(),self.original.getChannels()))

    def testIsStereo(self):
        '''Verify Stereo in Copy = Original'''      
        self.assertEquals(self.simple.isStereo(), self.original.isStereo(), 
            'SimpleSound stereo not the same')

    def testAudioFormatEncoding(self):
        '''Verify Encoding in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        oAFF = self.original.getAudioFileFormat()
        AF = AFF.getFormat()
        OF = oAFF.getFormat()
        self.assertEquals(AF.getEncoding(), OF.getEncoding(), 
            'Encoding is %s != %s' % (AF.getEncoding(),OF.getEncoding()))

    def testAudioFormatIsBigEndian(self):
        '''Verify isBigEndian in Copy = Original'''
        AFF = self.simple.getAudioFileFormat()
        oAFF = self.original.getAudioFileFormat()
        AF = AFF.getFormat()
        OF = oAFF.getFormat()
        self.assertEquals(AF.isBigEndian(), OF.isBigEndian(), 
            'Byte Order is %s != %s' % (AF.isBigEndian(),OF.isBigEndian()))

    def testFileName(self):
        '''Verify FileName in Copy = Original'''                        
        self.assertEquals(self.simple.getFileName(), self.original.getFileName(), 
            'FileName is %s != %s' % (self.simple.getFileName(), self.original.getFileName()))

    def testByteOrder(self):
        '''Verify Byte Order in Copy = Original'''          
        simpleBuffer = self.simple.getBuffer()
        originalBuffer = self.original.getBuffer()
        if(len(simpleBuffer) == len(originalBuffer)):
            for byte in simpleBuffer:
                self.assertEquals(simpleBuffer[byte], originalBuffer[byte], 'ByteBuffer is different at byte %s' % byte)
        else:
            self.fail('ByteBuffers are different length')
            
#suite = unittest.makeSuite(Test_SimpleSound_blip)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on SimpleSound(File testSound )'''
class Test_SimpleSound_testSound(unittest.TestCase):

    def setUp(self):
        createTestSound()
        self.simple = SimpleSound("testSound.wav")
        
    def testAudioFormatEncoding(self):
        '''Verify Encoding is ALAW'''
        AF = self.simple.getAudioFileFormat().getFormat()
        self.assertEquals(AF.getEncoding(), AudioFormat.Encoding.ALAW,
            'Encoding is %s != ALAW' % (AF.getEncoding()))

    def testSamplingRate(self):
        '''Verify SamplingRate is 22050'''
        self.assertEquals(self.simple.getSamplingRate(), 22050,
            'SamplingRate is %s != %s' % (self.simple.getSamplingRate(), 22050))

    def testSampleSize(self):
        '''Verify SampleSize is 16'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.getSampleSizeInBits(), 16,
            'SampleSize is %s != %s' % (AF.getSampleSizeInBits(), 16))

    def testChannels(self):
        '''Verify Channels is 1'''
        self.assertEquals(self.simple.getChannels(), 1,
            'SamplingRate is %s != %s' % (self.simple.getChannels(), 1))

    def testFrameSize(self):
        '''Verify FrameSize is 2'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.getFrameSize(), 2,
            'FrameSize is %s != %s' % (AF.getFrameSize(), 2))

    def testFrameRate(self):
        '''Verify FrameRate is 22k'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.getFrameRate(), 22050,
            'FrameRate is %s != %s' % (AF.getFrameRate(), 22050))

    def testIsBigEndian(self):
        '''Verify isBigEndian is false'''
        AFF = self.simple.getAudioFileFormat()
        AF = AFF.getFormat()
        self.assertEquals(AF.isBigEndian(), 0,
            'isBigEndian is %s != %s' % (AF.isBigEndian(), 0))

    def testAudioFileFormat(self):
        '''Verify sound created is WAVE AudioFileFormat'''
        AFF = self.simple.getAudioFileFormat()
        self.assertEquals(AFF.getType(),  AudioFileFormat.Type.WAVE, 
            'AudioFileFormat is %s != WAVE' % AFF.getType())

    def testFrameLength(self):
        '''Verify FrameLength is 6615'''
        AFF = self.simple.getAudioFileFormat()
        self.assertEquals(AFF.getFrameLength(), 6615,
            'FrameLength is %s != %s' % (AFF.getFrameLength(), 6615))
        
#suite = unittest.makeSuite(Test_SimpleSound_testSound)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on AsArray'''
class Test_AsArray(unittest.TestCase):

    def testAsArray(self):
        '''Test SimpleSound asArray'''
        bytes = [2,3,4,5,6,7,8,9,10]
        simple = SimpleSound()
        simple.setBuffer(bytes)
        simpleArray = simple.asArray()
        
        self.assertEquals(len(bytes), len(simpleArray), 
            'Length of array is %s != %s' % (len(bytes), len(simpleArray)))

        if(len(bytes) == len(simpleArray)):
            for index in range(len(bytes)):
                self.assertEquals(simpleArray[index], bytes[index], 
                    'Array is different at index %s' % index)

#suite = unittest.makeSuite(Test_AsArray)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on Buffer'''
class Test_Buffer(unittest.TestCase):

    def testBuffer(self):
        '''Test SimpleSound getBuffer setBuffer'''
        bytes = [2,3,4,5,6,7,8,9,10]
        simple = SimpleSound()
        simple.setBuffer(bytes)
        simpleBuffer = simple.getBuffer()
        
        self.assertEquals(len(bytes), len(simpleBuffer), 
            'Length of buffer is %s != %s' % (len(bytes), len(simpleBuffer)))

        if(len(bytes) == len(simpleBuffer)):
            for index in range(len(bytes)):
                self.assertEquals(simpleBuffer[index], bytes[index], 
                    'Buffer is different at index %s' % index)

#suite = unittest.makeSuite(Test_Buffer)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################

print '''Run Tests on from Book'''
class Test_Book(unittest.TestCase):
    
    def setUp(self):
        self.simple = SimpleSound("preamble.wav")

    def testPreamble_length(self):
        '''Test Preamble Length'''
        frame = self.simple.getFrame(1)
        self.assertEquals(self.simple.getLength(), 421110,
            'Length of sound is %s != 421110' % self.simple.getLength)

    def testGetSampleValueAt(self):
        self.assertEquals(self.simple.getSampleValueAt(1),29,
            'Value At Sample is %s != 36' % self.simple.getSampleValueAt(1))
            
        self.assertEquals(self.simple.getSampleValueAt(2),22,
            'Value At Sample is %s != 36' % self.simple.getSampleValueAt(2))

#suite = unittest.makeSuite(Test_Book)
#results = unittest.TextTestRunner(verbosity=2).run(suite)

########################################################################################################        
