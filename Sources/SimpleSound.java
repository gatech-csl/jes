import javax.sound.sampled.*;
import java.io.*;
import java.util.Vector;
import javazoom.jl.converter.*;

/**
 * The <code>SimpleSound</code> class is an implementation of the
 * Java Sound API specifically designed for use with students.
 * <br>
 * http://java.sun.com/products/java-media/sound/index.html
 * <p>
 * This class allows for easy playback, and manipulation of AU,
 * AIFF, and WAV files.
 * <p>
 * Code & ideas for this class related to playing and
 * viewing the sound were borrowed from the Java Sound Demo:
 * http://java.sun.com/products/java-media/sound/
 * samples/JavaSoundDemo/
 * <br>
 * Also, some code borrowed from Tritonus as noted.
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Ellie Harmon, ellie@cc.gatech.edu
 * @author Barbara Ericson ericson@mindspring.com
 *
 * Changes merged by Buck Scharfnorth 22 May 2008
 * default numberOfChannels left to 1
 * stopPlaying() method added
 *
 * _SoundIndexOffset added (29 Oct 2008) -Buck
 */
public class SimpleSound{

  ///////////////////////////// fields ////////////////////////

  /**
   * Constant for max negative value
   */
  public static final int MAX_NEG = -32768;

  /**
   * Constant for max positive value
   */
  public static final int MAX_POS = 32767;

  /**
   * Constant for the default sampling rate
   */
  public static final int SAMPLE_RATE = 22050;

  /**
   * Constant for the index base (0 or 1)
   */
  public static final int _SoundIndexOffset = 0;

  /**
   * Constant for the default sample size in bits
   * it is usual to have either 8 or 16
   */
  private static final int NUM_BITS_PER_SAMPLE = 16;

  /**
   * Flag to tell if in debug mode or not
   */
  private static final boolean DEBUG = false;

  /**
   * An array of bytes representing the sound.
   */
  private byte[] buffer;

  /**
   * Contains information about this sound such as its length,
   * format, and type.
   * @see AudioFormat
   */
  private AudioFileFormat audioFileFormat = null;

  /**
   * A collection of the threads that are playing this sound.
   */
  private Vector<Playback> playbacks = new Vector<Playback>();

  /**
   * The explorer for this sound, if it exists. If it exists, this
   * becomes the LineListener for output lines in the Playback class.
   * @see Playback
   */
  private SoundExplorer soundExplorer = null;

  /**
   * The name of the file from which this sound was created.  Gets
   * updated every time load from file is called.
   * @see #loadFromFile
   */
  private String fileName = null;

  ////////////////////////// constructors /////////////////////

  /**
   * Constructs a <code>SimpleSound</code> of 3 seconds long.
   */
  public SimpleSound()
  {
    this(SAMPLE_RATE * 3);
  }

  /**
   * Constructs a <code>SimpleSound</code> of the specified length.
   * This sound will simply consist of an empty byte array, and an
   * <code>AudioFileFormat</code> with the following values:
   * <ul>
   * <li><code>AudioFileFormat.Type.WAVE</code>
   * <li>22.05K sampling rate
   * <li>16 bit sample
   * <li>1 channel
   * <li>signed PCM encoding
   * <li>small-endian byte order
   * </ul>
   * Note that no new sound file is created, we only represent the
   * sound with a buffer and the AudioFileFormat.  If a file is
   * desired, then the method <code>writeToFile(String filename)
   * </code> must be called on this newly created sound.
   *
   * @param numFrames the number of samples in the sound
   * @see SimpleSound#write(String filename)
   */
  public SimpleSound(int numFrames)
  {
    int numChannels = 1;    // the number of channels in the sound
    int bytesPerSample = NUM_BITS_PER_SAMPLE / 8;

    /*
     Make a new sound with the default sampling rate, 16 bits,
     1 channel(==1 sample/frame), signed, smallEndian
     */
    AudioFormat audioFormat =
      new AudioFormat(SAMPLE_RATE, NUM_BITS_PER_SAMPLE,
                      numChannels, true, false);

    /*
     * The length in bytes is the number of channels
     * times the number of frames and times the number of bytes per
     * sample (2 bytes per sample)
     */
    int lengthInFrames = numChannels * numFrames;
    int lengthInBytes = lengthInFrames * bytesPerSample;

    /*
     Make a new WAV file format, with the AudioFormat described above
     */
    audioFileFormat =
      new AudioFileFormat(AudioFileFormat.Type.WAVE,
                          audioFormat, lengthInFrames);

    // create the buffer
    buffer = new byte[lengthInBytes];

  }

  /**
   * Constructs a <code>SimpleSound</code> of the specified length.
   * This sound will simply consist of an empty byte array, and an
   * <code>AudioFileFormat</code> with the following values:
   * <ul>
   * <li><code>AudioFileFormat.Type.WAVE</code>
   * <li>22.05K sampling rate
   * <li>16 bit sample
   * <li>1 channel
   * <li>signed PCM encoding
   * <li>small-endian byte order
   * </ul>
   * Note that no new sound file is created, we only represent the
   * sound with a buffer and the AudioFileFormat.  If a file is
   * desired, then the method <code>writeToFile(String filename)
   * </code> must be called on this newly created sound.
   *
   * @param numFrames the number of samples in the sound
   * @see SimpleSound#write(String filename)
   */
  public SimpleSound(int numFrames, int sampleRate)
  {
    int numChannels = 1;    // the number of channels in the sound
    int bytesPerSample = NUM_BITS_PER_SAMPLE / 8;

    /*
     Make a new sound with the default sampling rate, 16 bits,
     1 channel(==1 sample/frame), signed, smallEndian
     */
    AudioFormat audioFormat =
      new AudioFormat(sampleRate, NUM_BITS_PER_SAMPLE,
                      numChannels, true, false);

    /*
     * The length in bytes is the number of channels
     * times the number of frames and times the number of bytes per
     * sample (2 bytes per sample)
     */
    int lengthInFrames = numChannels * numFrames;
    int lengthInBytes = lengthInFrames * bytesPerSample;

    /*
     Make a new WAV file format, with the AudioFormat described above
     */
    audioFileFormat =
      new AudioFileFormat(AudioFileFormat.Type.WAVE,
                          audioFormat, lengthInFrames);

    // create the buffer
    buffer = new byte[lengthInBytes];

  }

  /**
   * Constructs a simple sound with the given sample size in bits and
   * type of endian (big or little)
   */
  public SimpleSound(int sampleSizeInBits, boolean isBigEndian)
  {
    // calculate the number of bytes in the sample
    int numBytesInSample = sampleSizeInBits/8;
    int numberOfChannels = 1;
    boolean signedFlag = true;

    // create the audio format
    AudioFormat audioFormat =
      new AudioFormat(SAMPLE_RATE, sampleSizeInBits,
                      numberOfChannels,
                      signedFlag, isBigEndian);

    // compute the length of the byte array
    int lengthInBytes =
      SAMPLE_RATE*numberOfChannels*5*numBytesInSample;

    // create the audio file format
    audioFileFormat =
      new AudioFileFormat(AudioFileFormat.Type.WAVE,
                          audioFormat,
                          lengthInBytes/
                          (numBytesInSample*numberOfChannels));

    // create the buffer
    buffer = new byte[lengthInBytes];
  }

  /**
   * Constructs a new SimpleSound from the given file.
   * @param fileName The File from which to create this sound.
   * @see SimpleSound#loadFromFile(String filename)
   */
  public SimpleSound(String fileName) throws SoundException
  {
    try {
      // load the sound from the file
      loadFromFile(fileName);
    } catch (Exception ex) {
      printError("Exception during load of file " + fileName + "\n Please ensure this file exists and uses a filetype supported by JES (wav, aiff, au).");
    }
  }

  /**
   * Constructor that creates a new SimpleSound by copying a passed SimpleSound
   * @param sound the sound to copy
   */
  public SimpleSound(SimpleSound sound)
  {
    this.audioFileFormat = sound.audioFileFormat;
    this.fileName = sound.fileName;
    this.playbacks = new Vector<Playback>();

    // copy the samples
    if (sound.buffer != null)
    {
      this.buffer = new byte[sound.buffer.length];
      for (int i = 0; i < sound.buffer.length; i++)
        this.buffer[i] = sound.buffer[i];
    }
  }

  ///////////////////////// accessors ///////////////////////////

  /**
   * Method that returns the byte array representation of this simple sound.
   * @return the sound represented as a byte array
   */
  public byte[] getBuffer()
  {
    return buffer;
  }

  /**
   * Method that returns the AudioFileFormat describing this simple sound.
   * @return the AudioFileFormat describing this sound
   * @see AudioFileFormat
   */
  public AudioFileFormat getAudioFileFormat()
  {
    return audioFileFormat;
  }

  /**
   * Method to get the sampling rate of this sound
   * @return the sampling rate in number of samples per second
   */
  public double getSamplingRate()
  {
    return audioFileFormat.getFormat().getSampleRate();
  }

  /**
   * Method that returns the SoundExplorer
   * @return the sound explorer
   */
  public SoundExplorer getSoundExplorer()
  {
    return soundExplorer;
  }

  /**
   * Method to return the byte array
   * @return an array of bytes which represents the simple sound
   * @see SimpleSound#getBuffer
   */
  public byte[] asArray()
  {
    return getBuffer();
  }

  /**
   * Method that returns the vector of playback threads currently
   * active on this sound.
   * @return the vector of playback threads for this simple sound
   */
  public Vector getPlaybacks()
  {
    return playbacks;
  }

  /**
   * Method that returns the name of the file this sound came from.
   * If this sound did not originate with a file, this value will
   * be null.
   * @return the file name associated with this sound or null
   * @see #loadFromFile(String fileName)
   */
  public String getFileName()
  {
    return fileName;
  }

  ////////////////////////////// modifiers ////////////////////////

  /**
   * Changes the byte array that represents this sound.
   * @param newBuffer a byte array representation of the new sound we
   * want this to represent.
   */
  public void setBuffer(byte[] newBuffer)
  {
    buffer = newBuffer;
  }

  /**
   * Changes the byte array that represents this sound.
   * @param newBuffer an integer with the number of bytes in the buffer
   */
  public void setBuffer(int newBuffer)
  {
    buffer = new byte[newBuffer];
  }

  /**
   * Changes the AudioFileFormat of this sound.
   * @param newAudioFileFormat the new audioFileFormat that describes
   * this sound.
   * @see AudioFileFormat
   */
  public void setAudioFileFormat(AudioFileFormat newAudioFileFormat)
  {
    audioFileFormat = newAudioFileFormat;
  }

  /**
   * Changes the explorer of this object.
   * @param soundExplorer the new SoundExplorer to use
   * @see SoundExplorer
   */
  public void setSoundExplorer(SoundExplorer soundExplorer)
  {
    this.soundExplorer = soundExplorer;
  }



  ///////////////////////// methods /////////////////////////////

  /**
   * Creates an <code>AudioInputStream</code> for this sound from the
   * <code>buffer</code> and the <code>audioFileFormat</code>.
   * @return an AudioInputStream representing this sound.
   * @see AudioInputStream
   */
  public AudioInputStream makeAIS()
  {
    AudioFileFormat.Type fileType = audioFileFormat.getType();
    ByteArrayInputStream bais = new ByteArrayInputStream(buffer);
    int frameSize = audioFileFormat.getFormat().getFrameSize();

    AudioInputStream audioInputStream =
      new AudioInputStream(bais, audioFileFormat.getFormat(),
                           buffer.length/frameSize);
    return audioInputStream;
  }

  /**
   * Invokes <code>printError(message, null)</code>
   *
   * @see SimpleSound#printError(String message, Exception e)
   * @throws SoundException Will throw under every circumstance.
   *                            This way we can catch the exception
   *                            in JES.
   */
  public void printError(String message) throws SoundException
  {
    printError(message, null);
  }

  /**
   * Prints the given String to the "standard" error output stream, then
   * prints a stack trace on the exception, and then exits the program.  If
   * the String is null, then nothing happens, the method just returns.  If
   * the Exception is null, then it prints the String and then exits the
   * program.
   *
   * @param message A description of the error
   * @param e The exception, if any, that was caught regarding the error
   * @throws SoundException Will throw under every circumstance.
   *                            This way we can catch the exception
   *                            in JES.
   */
  public void printError(String message, Exception e) throws SoundException
  {
    if(message != null)
    {
      //SimpleOutput.showError(message);
      System.err.println(message);
      if(e != null)
      {
        e.printStackTrace();
      }
      //so we can catch the error
      throw(new SoundException(message));
    }
  }

  /**
   * Method to check if a sound is stereo (2 channels) or not
   * @return true if in stereo else false
   */
  public boolean isStereo()
  {
    if(audioFileFormat.getFormat().getChannels() == 1)
      return false;
    else
      return true;
  }

  ////////////////////////// File I/O ///////////////////////////////////

  /**
   * Method to write this sound to a file
   * @param fileName the name of the file to write to
   */
  public void write(String fileName) throws SoundException
  {
    try {
      writeToFile(fileName);
    }
    catch (SoundException ex) {
      printError("Couldn't write file to " + fileName);
    }
  }

  /**
   * Creates an audioInputStream from this sound, and then writes
   * this stream out to the file with the specified name.  If no
   * file exists, one is created.  If a file already exists, then it
   * is overwritten.  This does not check the extension of the
   * fileName passed in to make sure it agrees with the
   * <code>AudioFileFormat.Type</code> of this sound.
   *
   * @param outFileName The name of the file to write this sound to
   * @throws SoundException if any error is encountered while
   * writing to the file.
   */
  public void writeToFile(String outFileName)
    throws SoundException
  {

    /*
     get an audioInputStream that represents this sound.
     then, we will write from the stream to the file
     */
    AudioInputStream audioInputStream = makeAIS();
    AudioFileFormat.Type type = audioFileFormat.getType();

    try {
      audioInputStream.reset();
    }//try reset audioInputStream
    catch(Exception e)
    {
      printError("Unable to reset the Audio stream.  Please "+
                 "try again.", e);
    }//catch


    //get the file to write to
    File file = new File(outFileName);
    if(!file.exists())
    {
      //if the file doesn't exist, make one
      try
      {
        file.createNewFile();
      }//try
      catch(IOException e)
      {
        printError("That file does not already exist, and"+
                   "there were problems creating a new file" +
                   "of that name.  Are you sure the path" +
                   "to: " + outFileName + "exists?", e);
      }//catch
    }//if


    //write to the file
    try
    {
      if(AudioSystem.write(audioInputStream, type, file) == -1)
      {
        printError("Problems writing to file.  Please " +
                   "try again.");
      }

      // if the write was successful then set the file name to the
      // new name
      else
      {
        this.fileName = outFileName;
      }
    }//try
    catch(FileNotFoundException e)
    {
      printError("The file you specified did not already exist " +
                 "so we tried to create a new one, but were unable"+
                 "to do so.  Please try again.  If problems "+
                 "persit see your TA.", e);
    }
    catch(Exception e)
    {
      printError("Problems writing to file: " + outFileName, e);
    }//catch


    //close the input stream, we're done writing
    try
    {
      audioInputStream.close();
    }//try
    catch(Exception e)
    {
      printError("Unable to close the Audio stream.");
    }//catch

  }//writeToFile(String outFileName)


  /**
   * Resets the fields of this sound so that it now represents the
   * sound in the specified file.  If successful, the fileName
   * ariable is updated such that it is equivalent to
   * <code>inFileName</code>.
   *
   * @param inFileName the path and filename of the sound we want to
   *                   represent.
   * @throws SoundException if any problem is encountered while
   *                            reading in from the file.
   */
  public void loadFromFile(String inFileName) throws SoundException
  {

    // try to prevent a null pointer exception
    if(inFileName == null)
    {
      printError("You must pass in a valid file name.  Please try" +
                 "again.");
    }

    /* get the File object representing the file named inFileName
     * and make sure it exists */
    File file = new File(inFileName);
    if(!file.exists())
    {
      printError("The file: " + inFileName + " doesn't exist");
    }

    // create an audioInputStream from this file

    AudioInputStream audioInputStream;
    try {
      audioInputStream = AudioSystem.getAudioInputStream(file);
    } catch(Exception e) {
      printError("Unable to read from file " +
                 inFileName + ".  The file type is unsupported.  " +
                 "Are you sure you're using a WAV, AU, or " +
                 "AIFF file (some .wav files are encoded " +
                 "using mp3)?  Try using SimpleSound.convert(" +
                 "String oldName, String newName) and then " +
                 "try to read the new name.", e);
      return;
    }//catch

    /* We need to make an array representing this sound, so the
     * number of bytes we will be storing cannot be greater than
     * Integer.MAX_VALUE.  The JavaSound API also supports only
     * integer length frame lengths.
     * (See AudioFileFormat.getFrameLength().  I don't know why
     * this is inconsistent with AudioInputStream.getFrameLength().)
     */
    if((audioInputStream.getFrameLength() *
        audioInputStream.getFormat().getFrameSize()) >
       Integer.MAX_VALUE)
    {
      printError("The sound in file: " + inFileName +
                 " is too long."+
                 "  Try using a shorter sound.");
    }
    int bufferSize = (int)audioInputStream.getFrameLength() *
      audioInputStream.getFormat().getFrameSize();

    buffer = new byte[bufferSize];

    int numBytesRead = 0;
    int offset = 0;

    //read all the bytes into the buffer
    while(true)
    {
      try {
        numBytesRead =
          audioInputStream.read(buffer, offset, bufferSize);
        if(numBytesRead == -1)//no more data
          break;
        else
          offset += numBytesRead;
      } catch(Exception e) {
        printError("Problems reading the input stream.  "+
                   "You might want to try again using this "+
                   " file: " + inFileName + "or a different"+
                   " file.  If problems persist, ask your TA."
                     , e);
      }//catch
    }//while


    /* set the format of the file, assuming that the extension
     * is correct
     */
    if(inFileName.toLowerCase().endsWith(".wav"))
    {
      audioFileFormat =
        new AudioFileFormat(AudioFileFormat.Type.WAVE,
                            audioInputStream.getFormat(),
                            (int)audioInputStream.getFrameLength());
    }
    else if(inFileName.toLowerCase().endsWith(".au"))
    {
      audioFileFormat =
        new AudioFileFormat(AudioFileFormat.Type.AU,
                            audioInputStream.getFormat(),
                            (int)audioInputStream.getFrameLength());
    }
    else if (inFileName.toLowerCase().endsWith(".aif")||
             inFileName.toLowerCase().endsWith(".aiff"))
    {
      audioFileFormat =
        new AudioFileFormat(AudioFileFormat.Type.AIFF,
                            audioInputStream.getFormat(),
                            (int)audioInputStream.getFrameLength());
    }
    else
    {
      printError("Unsupported file type.  Please try again with a "+
                 "file that ends in .wav, .au, .aif, or .aiff");
    }

    if(DEBUG)
    {
      System.out.println("New sound created from file: " + fileName);
      System.out.println("\tendianness: " +
                         audioInputStream.getFormat().isBigEndian());
      System.out.println("\tencoding: " +
                         audioInputStream.getFormat().getEncoding());
    }

    this.fileName = inFileName;

  }//loadFromFile(String inFileName)

  //////////////////////// Methods for playing the sound //////////

  /**
   * Creates a new Playback thread and starts it.  The thread is
   * guaranteed to finish playing the sound as long as the program
   * doesn't exit before it is done.  This method does not block,
   * however.  So, if you invoke <code>play()</code> multiple times
   * in a row, sounds will simply play on
   * top of eachother - "accidental mixing"
   *
   * @see Playback
   */
  public void play()
  {
    // create the thread, add it to the Vector, and start it
    Playback playback = new Playback(this);
    playbacks.add(playback);
    playback.start();
  }

  /**
   * Creates a new Playback thread, starts it, then waits for the
   * entire sound to finish playing before it returns.  This method
   * is guarranteed to play the entire sound, and does not allow for
   * any "accidental mixing"
   *
   * @see Playback
   */
  public void blockingPlayOld()
  {
    /* create the thread, add it to the Vector, start it, and wait
     until its done playing to return */
    Playback playback = new Playback(this);
    playbacks.add(playback);
    playback.start();
    //wait until the sound is done playing
    while(playback.isAlive()){;}
  }

  /**
   * Plays the sound, then sleeps for how
   * long the sound SHOULD last.
   **/
  public void blockingPlay()
  {
    this.play();
    try {
      double timeToSleep =
           1000 *
        (this.getLength()/this.getSamplingRate());
      Thread.sleep((int) timeToSleep);
    } catch (Exception ex) {
      System.out.println("Exception occurred: "+ex);
    }
  }

  /**
   * Checks the value of durInFrames to make sure that it is not
   * larger than Integer.MAX_VALUE to guarrantee safe casting.
   * Also checks the value of rate to make sure that it is not
   * larger than Float.MAX_VALUE before casting.
   *
   * @param rate a double representing the change in sampleRate
   * (==frameRate) for playing back this sound
   * @param durInFrames a double representing how much of this
   * sound we want to play.
   * @see SimpleSound#playAtRateInRange(float rate,
   *                                    int startFrame,
   *                                    int endFrame,
   *                                    boolean isBlocking)
   * @throws SoundException if there are problems playing the sound.
   */
  public void playAtRateDur(double rate, double durInFrames)
    throws SoundException
  {
    if(durInFrames > getLengthInFrames())
    {
      printError("The given duration in frames, " + durInFrames +
                 " is out of the playable range.  Try something " +
                 "between 1 and " + getLengthInFrames());
    }
    if(rate > Float.MAX_VALUE)
    {
      printError("The new sample rate, " + rate + "is out of the " +
                 "playable range.  Try something between " +
                 "0 and " + Float.MAX_VALUE);
    }
    playAtRateInRange((float)rate, 0, (int)durInFrames-1, false);
  }

  /**
   * First, checks the value of durInFrames to make sure that it is
   * not larger than Integer.MAX_VALUE to guarrantee safe casting.
   * Simmilarly, checks the value of rate to make sure that it is
   * not larger than FLoat.MAX_VALUE before casting.
   *
   * @param rate a double representing the change in sampleRate
   * (==frameRate) for playing back this sound
   * @param durInFrames a double representing how much of this sound
   * we want to play
   * @see SimpleSound#playAtRateInRange(float range,
   *                                    int startFrame,
   *                                    int endFrame,
   *                                    boolean isBlocking)
   * @throws SoundException if there are problems playing the sound.
   */
  public void blockingPlayAtRateDur(double rate, double durInFrames)
    throws SoundException
  {
    if(durInFrames > getLengthInFrames())
    {
      printError("The given duration in frames, " + durInFrames +
                 " is out of the playable range.  Try something " +
                 "between 1 and " + getLengthInFrames());
    }
    if(rate > Float.MAX_VALUE)
    {
      printError("The new sample rate, " + rate + "is out of the " +
                 "playable range.  Try something between " +
                 "0 and " + Float.MAX_VALUE);
    }

    playAtRateInRange((float)rate, 0, (int)durInFrames-1, true);

  }

  /**
   * Calls <code>playAtRateInRange(rate, startFrame, endFrame,
   * false) </code>.
   *
   * @param rate a float representing the change in sampleRate
   * (==frameRate) for playing back this sound
   * @param startFrame an int representing the frame at which we
   * want to begin playing the sound
   * @param endFrame an int representing the frame at which want
   * to stop playing the sound
   * @see SimpleSound#playAtRateInRange(float range,
   *                                    int startFrame,
   *                                    int endFrame,
   *                                    boolean isBlocking)
   * @throws SoundException if there are problems playing the sound.
   */
  public void playAtRateInRange(float rate, int startFrame,
                                int endFrame)
    throws SoundException
  {
    playAtRateInRange(rate, startFrame, endFrame, false);
  }

  /**
   * Calls <code>playAtRateInRange(rate, startFrame, endFrame, true)
   * </code>.
   *
   * @param rate a float representing the change in sampleRate
   * (==frameRate) for playing back this sound
   * @param startFrame an int representing the frame at which we want
   * to begin playing the sound
   * @param endFrame an int representing the frame at which want
   * to stop playing the sound
   * @see SimpleSound#playAtRateInRange(float range,
   *                                    int startFrame,
   *                                    int endFrame,
   *                                    boolean isBlocking)
   * @throws SoundException if there are problems playing the sound.
   */
  public void blockingPlayAtRateInRange(float rate, int startFrame,
                                        int endFrame)
    throws SoundException
  {
    playAtRateInRange(rate, startFrame, endFrame, true);
  }

  /**
   * Plays the specified segment of this sound at the given sample
   * rate.  Then it saves the old fields (buffer and audioFileFormat)
   * of this sound into temporary variables, and setting the fields
   * of this sound to modified values.  Then it creates a Playback
   * thread on this sound (with the modified values) and starts the
   * thread.  The values for buffer and audioFileFormat are restored
   * to their original values before the method returns.
   *
   * @param rate The change in the sampleRate (==frameRate) for
   * playing back this sound.  The old SampleRate is multiplied by
   * this value.  So, if rate = 2, the sound will play twice as fast
   * (half the length), and if rate = .5, the sound will play half as
   *             fast (twice the length).
   * @param startFrame The index of the frame where we want to begin
   * play
   * @param endFrame The index of the frame where we want to end play
   * @param isBlocking If true, this method waits until the thread is
   * done playing the sound before returning.  If false, it
   *                   simply starts the thread and then returns.
   * @throws SoundException if there are any problems playing the
   * sound.
   */
  public void playAtRateInRange(float rate, int startFrame,
                                int endFrame, boolean isBlocking)
    throws SoundException
  {

    /*before we get started, lets try to check for some obvious
     * errors.  maybe we can avoid some of those pesky array out of
     * bounds exceptions.
     */
    if(endFrame >= getAudioFileFormat().getFrameLength())
    {
      printError("You are trying to play to index: " + (endFrame+_SoundIndexOffset) +
                 ".  The sound only has " +
                 getAudioFileFormat().getFrameLength() +
                 " samples total.");
    }
    if(startFrame < _SoundIndexOffset)
    {
      printError("You cannot start playing at index " +
                 (startFrame+_SoundIndexOffset) +
                 ".  Choose " + _SoundIndexOffset + " to start at the begining.");
    }
    if(endFrame < startFrame)
    {
      printError("You cannot start playing at index " +
                 (startFrame+_SoundIndexOffset) + " and stop playing at index " +
                 (endFrame+_SoundIndexOffset) + ".  The start index must be before" +
                 "the stop index.");
    }


    /*
     we want to save the current buffer and audioFileFormat
     so we can return to them when we're finished.
     */
    byte[] oldBuffer = buffer;
    AudioFileFormat oldAFF = getAudioFileFormat();

    //just to make the code easier to read
    int frameSize = getAudioFileFormat().getFormat().getFrameSize();
    int durInFrames = (endFrame - startFrame) + 1;
    if(DEBUG)
      System.out.println("\tnew durInFrames = " + durInFrames);

    //we want to make a new buffer, only as long as we need
    int newBufferSize = durInFrames * frameSize;

    byte[] newBuffer = new byte[newBufferSize];
    for(int i = 0; i <  newBufferSize; i++)
    {
      newBuffer[i] = oldBuffer[(startFrame*frameSize) + i];
    }

    //now we want to make a new audioFormat with the same information
    //except a different rate
    AudioFormat newAF =
      new AudioFormat(oldAFF.getFormat().getEncoding(),
                      oldAFF.getFormat().getSampleRate() * rate,
                      oldAFF.getFormat().getSampleSizeInBits(),
                      oldAFF.getFormat().getChannels(),
                      oldAFF.getFormat().getFrameSize(),
                      oldAFF.getFormat().getFrameRate() * rate,
                      oldAFF.getFormat().isBigEndian());

    //now put that new AudioFormat into a new AudioFileFormat with
    //the changed duration in frames
    AudioFileFormat newAFF =
      new AudioFileFormat(oldAFF.getType(), newAF, durInFrames);


    /*
     change the values in this Sound
     */
    setBuffer(newBuffer);
    setAudioFileFormat(newAFF);
    if(DEBUG)
    {
      System.out.println("playAtRateInRange(" + rate + ", " +
                         startFrame + ", " + endFrame + ", " +
                         isBlocking + ")");
      System.out.println("\t(length of sound = " +
                         getAudioFileFormat().getFrameLength() + ")");
    }

    /*
     play the modified sound
     */
    Playback playback = new Playback(this);
    playbacks.add(playback);
    playback.start();

    if(isBlocking)
      while(playback.isAlive()){;}//wait until the thread exits

    /*
     we need to wait until the thread is done with the values
     before we change them back.  The playing flag is set to false
     until the loop begins in which data is actually written out.
     see Playback#run()
     */
    while(!playback.getPlaying()){;}

    setBuffer(oldBuffer);//restore the buffer
    setAudioFileFormat(oldAFF);//restore the file format
  }

  /**
   * Stops playing the sound by calling the stopPlaying()
   * method of all Playback threads belonging to the sound.
   */
  public void stopPlaying()
  {
    //stop all playback threads related to this sound
    for(int i = 0; i < this.getPlaybacks().size(); i++)
    {
      ((Playback)this.getPlaybacks().elementAt(i)).stopPlaying();
    }
  }

  /**
   * Deletes the specified playback object from the Vector.  This
   * should only be called from within the run() method of an
   * individual playback thread.
   *
   * @see Playback#run()
   */
  public void removePlayback(Playback playbackToRemove)
  {
    if(playbacks.contains(playbackToRemove))
    {
      playbacks.remove(playbackToRemove);
      playbackToRemove = null;
    }
  }




  ////////////////////// getting sound information /////////////////

  /**
   * Returns an array containing all of the bytes in the specified
   * frame.
   *
   * @param frameNum the index of the frame to access
   * @return the array containing all of the bytes in frame
   *         <code>frameNum</code>
   * @throws SoundException if the frame number is invalid.
   */
  public byte[] getFrame(int frameNum) throws SoundException
  {
    if(frameNum >= getAudioFileFormat().getFrameLength())
    {
      printError("That index "+ (frameNum) +", does not exist. "+
                 "The last valid index is "+
                 (getAudioFileFormat().getFrameLength() -1));
    }

    int frameSize = getAudioFileFormat().getFormat().getFrameSize();
    byte[] theFrame = new byte[frameSize];
    for (int i = 0; i < frameSize; i++)
    {
      theFrame[i] = buffer[frameNum*frameSize+i];
    }
    return theFrame;
  }


  /**
   * Obtains the length of the audio data contained in the file,
   * expressed in sample frames.
   *
   * @return the number of sample frames of audio data in the file
   */
  public int getLengthInFrames()
  {
    return getAudioFileFormat().getFrameLength();
  }

  /**
   * Returns the number of samples in this sound
   * @return the number of sample frames
   */
  public int getNumSamples()
  {
    return getAudioFileFormat().getFrameLength();
  }

  /**
   * Method to create and return a SoundSample object for the given
   * frame number
   * @return a SoundSample object for this frame number
   */
  public SoundSample getSample(int frameNum)
  {
    return new SoundSample(this,frameNum);
  }

  /**
   * Method to create and return an array of SoundSample objects
   * @return the array of SoundSample objects
   */
  public SoundSample[] getSamples()
  {
    int numSamples = getLengthInFrames();
    SoundSample[] samples = new SoundSample[numSamples];
    for (int i=0; i < numSamples; i++)
      samples[i] = new SoundSample(this,i);
    return samples;
  }

  /**
   * Method to report an index exception for this sound
   * @param index the index
   * @param ex the exception (unused)
   */
  private void reportIndexException(int index, Exception ex)
  {
    System.out.println("The index " + index +
                       " isn't valid for this sound");
  }

  /**
   * Method to get the sample at the passed index and handle
   * any SoundExceptions
   * @param index the desired index
   * @return the sample value
   */
  public int getSampleValueAt(int index)
  {
    int value = 0;

    try {
      value = getSampleValue(index);
    } catch (Exception ex) {
      reportIndexException(index, ex);
    }
    return value;
  }

  /**
   * If this is a mono sound, obtains the single sample contained
   * within this frame, else obtains the first (left) sample
   * contained in the specified frame.
   *
   * @param frameNum the index of the frame to access
   * @return an integer representation of the bytes contained within
   * the specified frame
   * @throws SoundException if the frame number is invalid.
   */
  public int getSampleValue(int frameNum) throws SoundException
  {
    //Before we get started, lets make sure that frame exists
    if(frameNum >= getAudioFileFormat().getFrameLength())
    {
      printError("You are trying to access the sample at index: "
                 + (frameNum) + ", but the last valid index is at " +
                 (getAudioFileFormat().getFrameLength() - 1));
    }
    else if(frameNum < 0)
    {
      printError("You asked for the sample at index: " + (frameNum) +
                 ".  This number is less than zero.  Please try" +
                 "again using an index in the range [0," +
                 (getAudioFileFormat().getFrameLength() - 1) +"]");
    }

    AudioFormat format = getAudioFileFormat().getFormat();
    int sampleSizeInBits = format.getSampleSizeInBits();
    boolean isBigEndian = format.isBigEndian();

    byte[] theFrame = getFrame(frameNum);

    if(format.getEncoding().equals(AudioFormat.Encoding.PCM_SIGNED))
    {
      //since we're always returning the left sample,
      //we don't care if we're mono or stereo, left is
      //always first in the frame
      if(sampleSizeInBits == 8)//8 bits == 1 byte
        return theFrame[0];
      else if(sampleSizeInBits == 16)
        return TConversionTool.bytesToInt16(theFrame, 0,
                                            isBigEndian);
      else if(sampleSizeInBits == 24)
        return TConversionTool.bytesToInt24(theFrame, 0,
                                            isBigEndian);
      else if(sampleSizeInBits == 32)
        return TConversionTool.bytesToInt32(theFrame, 0,
                                            isBigEndian);
      else
      {
        printError("Unsupported audio encoding.  The sample "+
                   "size is not recognized as a standard "+
                   "format.");
        return -1;
      }
    }
    else if(format.getEncoding().equals(AudioFormat.Encoding.PCM_UNSIGNED))
    {
      if(sampleSizeInBits == 8)
        return TConversionTool.unsignedByteToInt(theFrame[0])-
        (int)Math.pow(2,7);
      else if(sampleSizeInBits == 16)
        return TConversionTool.unsignedByteToInt16(theFrame, 0,
                                                   isBigEndian)-
        (int)Math.pow(2, 15);
      else if(sampleSizeInBits == 24)
        return TConversionTool.unsignedByteToInt24(theFrame, 0,
                                                   isBigEndian)-
        (int)Math.pow(2, 23);
      else if(sampleSizeInBits == 32)
        return TConversionTool.unsignedByteToInt32(theFrame, 0,
                                                   isBigEndian)-
        (int)Math.pow(2, 31);
      else
      {
        printError("Unsupported audio encoding.  The sample "+
                   "size is not recognized as a standard "+
                   "format.");
        return -1;
      }
    }
    else if(format.getEncoding().equals(AudioFormat.Encoding.ALAW))
    {
      return TConversionTool.alaw2linear(buffer[0]);
    }
    else if(format.getEncoding().equals(AudioFormat.Encoding.ULAW))
    {
      return TConversionTool.ulaw2linear(buffer[0]);
    }
    else
    {
      printError("unsupported audio encoding: " +
                 format.getEncoding() + ".  Currently only PCM, " +
                 "ALAW and ULAW are supported.  Please try again" +
                 "with a different file.");
      return -1;
    }
  }//getSample(int)

  /**
   * Obtains the left sample of the audio data contained at the specified
   * frame.
   *
   * @param frameNum the index of the frame to access
   * @return an int representation of the bytes contained in the specified
   *         frame.
   * @throws SoundException if the frameNumber is invalid
   */
  public int getLeftSample(int frameNum) throws SoundException
  {
    //default is to getLeftSample

    return getSampleValue(frameNum);
  }

  /**
   * Obtains the right sample of the audio data contained at the specified
   * frame.
   *
   * @param frameNum the index of the frame to access
   * @return an int representation of the bytes contained in the specified
   *         frame.
   * @throws SoundException if the frameNumber is invalid, or
   *                            the encoding isn't supported.
   */
  public int getRightSample(int frameNum) throws SoundException
  {
    //Before we get started, lets make sure that frame exists
    if(frameNum >= getAudioFileFormat().getFrameLength())
    {
      printError("You are trying to access the sample at index: "
                   + (frameNum) + ", but the last valid index is at " +
                 (getAudioFileFormat().getFrameLength() - 1));
    }
    else if(frameNum < 0)
    {
      printError("You asked for the sample at index: "+(frameNum+1) +
                 ".  This number is less than zero.  Please try" +
                 " again using an index in the range [0," +
                 (getAudioFileFormat().getFrameLength()-1) + "].");
    }

    AudioFormat format = getAudioFileFormat().getFormat();
    int channels;
    if((channels = format.getChannels())==1)
    {
      printError("Only stereo sounds have different right and left" +
                 " samples.  You are using a mono sound, try " +
                 "getSample("+(frameNum)+") instead");
      return -1;
    }
    int sampleSizeInBits = format.getSampleSizeInBits();
    boolean isBigEndian = format.isBigEndian();

    byte[] theFrame = getFrame(frameNum);

    if(format.getEncoding().equals(AudioFormat.Encoding.PCM_SIGNED))
    {
      if(sampleSizeInBits == 8)//8 bits == 1 byte
        return theFrame[1];
      else if(sampleSizeInBits == 16)
        return TConversionTool.bytesToInt16(theFrame, 2, isBigEndian);
      else if(sampleSizeInBits == 24)
        return TConversionTool.bytesToInt24(theFrame, 3, isBigEndian);
      else if(sampleSizeInBits == 32)
        return TConversionTool.bytesToInt32(theFrame, 4, isBigEndian);
      else
      {
        printError("Unsupported audio encoding.  The sample"+
                   " size is not recognized as a standard"+
                   " format.");
        return -1;
      }
    }
    else if(format.getEncoding().equals(AudioFormat.Encoding.PCM_UNSIGNED))
    {
      if(sampleSizeInBits == 8)
        return TConversionTool.unsignedByteToInt(theFrame[1]);
      else if(sampleSizeInBits == 16)
        return TConversionTool.unsignedByteToInt16(theFrame, 2, isBigEndian);
      else if(sampleSizeInBits == 24)
        return TConversionTool.unsignedByteToInt24(theFrame, 3, isBigEndian);
      else if(sampleSizeInBits == 32)
        return TConversionTool.unsignedByteToInt32(theFrame, 4, isBigEndian);
      else
      {
        printError("Unsupported audio encoding.  The sample"+
                   " size is not recognized as a standard" +
                   " format.");
        return -1;
      }
    }
    else if(format.getEncoding().equals(AudioFormat.Encoding.ALAW))
    {
      return TConversionTool.alaw2linear(buffer[1]);
    }
    else if(format.getEncoding().equals(AudioFormat.Encoding.ULAW))
    {
      return TConversionTool.ulaw2linear(buffer[1]);
    }
    else
    {
      printError("unsupported audio encoding: " +
                 format.getEncoding() + ".  Currently only PCM, " +
                 "ALAW and ULAW are supported.  Please try again" +
                 "with a different file.");
      return -1;
    }
  }



  /**
   * Obtains the length of this sound in bytes.  Note, that this number is not
   * neccessarily the same as the length of this sound's file in bytes.
   *
   * @return the sound length in bytes
   */
  public int getLengthInBytes()
  {
    return buffer.length;
  }

  /**
   * Method to return the length of the sound as the number of samples
   * @return the length of the sound as the number of samples
   */
  public int getLength()
  {
    return getNumSamples();
  }

  /**
   * Obtains the number of channels of this sound.
   *
   * @return the number of channels (1 for mono, 2 for stereo), or
   * <code>AudioSystem.NOT_SPECIFIED</code>
   * @see AudioSystem#NOT_SPECIFIED
   */
  public int getChannels()
  {
    return getAudioFileFormat().getFormat().getChannels();
  }


  /**************************************************************************/
  /************************** CHANGING THE SOUND ****************************/
  /**************************************************************************/

  /**
   * Changes the value of each byte of the specified frame.
   *
   * @param frameNum the index of the frame to change
   * @param theFrame the byte array that will be copied into this sound's
   *                 buffer in place of the specified frame.
   * @throws SoundException if the frameNumber is invalid.
   */
  public void setFrame(int frameNum, byte[] theFrame) throws SoundException
  {
    if(frameNum >= getAudioFileFormat().getFrameLength())
    {
      printError("That frame, number "+frameNum+", does not exist. "+
                 "The last valid frame number is " +
                 (getAudioFileFormat().getFrameLength() - 1));
    }
    int frameSize = getAudioFileFormat().getFormat().getFrameSize();
    if(frameSize != theFrame.length)
      printError("Frame size doesn't match, line 383.  This should" +
                 " never happen.  Please report the problem to a TA.");
    for(int i = 0; i < frameSize; i++)
    {
      buffer[frameNum*frameSize+i] = theFrame[i];
    }
  }

  /**
   * Method to set the sample value at the passed index to the passed value
   * @param index the index
   * @param value the new value
   */
  public void setSampleValueAt(int index, int value)
  {
    try {
      setSampleValue(index,value);
    } catch (Exception ex) {
      reportIndexException(index,ex);
    }
  }

  /**
   * Changes the value of the sample found at the specified frame.  If this
   * sound has more than one channel, then this defaults to setting only the
   * first (left) sample.
   *
   * @param frameNum the index of the frame where the sample should be changed
   * @param sample an int representation of the new sample to put in this
   *               sound's buffer at the specified frame
   * @throws SoundException if the frameNumber is invalid, or
   *                            another problem is encountered
   */
  public void setSampleValue(int frameNum, int sample) throws SoundException
  {
    AudioFormat format = getAudioFileFormat().getFormat();
    int sampleSizeInBits = format.getSampleSizeInBits();
    boolean isBigEndian = format.isBigEndian();

    byte[] theFrame = getFrame(frameNum);

    if(format.getEncoding().equals(AudioFormat.Encoding.PCM_SIGNED))
    {
      if(sampleSizeInBits == 8)//8 bits = 1 byte = first cell in array
      {
        theFrame[0] = (byte)sample;
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 16)//2 bytes, first 2 cells in array
      {
        TConversionTool.intToBytes16(sample, theFrame, 0, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 24)
      {
        TConversionTool.intToBytes24(sample, theFrame, 0, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 32)
      {
        TConversionTool.intToBytes32(sample, theFrame, 0, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else
      {
        printError("Unsupported audio encoding.  The sample"+
                   "size is not recognized as a standard format");
      }
    }//if format == PCM_SIGNED
    else if(format.getEncoding().equals(AudioFormat.Encoding.PCM_UNSIGNED))
    {
      if(sampleSizeInBits == 8)
      {
        theFrame[0] = TConversionTool.intToUnsignedByte(sample);
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 16)
      {
        TConversionTool.intToUnsignedBytes16(sample, theFrame, 0, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 24)
      {
        TConversionTool.intToUnsignedBytes24(sample, theFrame, 0, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 32)
      {
        TConversionTool.intToUnsignedBytes32(sample, theFrame, 0, isBigEndian);
        setFrame(frameNum, theFrame);
      }

      else
      {
        printError("Unsupported audio encoding.  The sample"+
                   " size is not recognized as a standard "+
                   "format.");
      }
    }
    else if(format.getEncoding().equals(AudioFormat.Encoding.ALAW))
    {
      if((sample>Short.MAX_VALUE)||(sample<Short.MIN_VALUE))
        printError("You are trying to set the sample value to: "+
                   sample + ", but the maximum value for a sample"+
                   " in this format is: "+Short.MAX_VALUE+
                   ", and the minimum value is: "+Short.MIN_VALUE+
                   ".  Please choose a value in that range.");
      theFrame[0] = TConversionTool.linear2alaw((short)sample);
      setFrame(frameNum, theFrame);
    }
    else if(format.getEncoding().equals(AudioFormat.Encoding.ULAW))
    {

      if((sample>Short.MAX_VALUE)||(sample<Short.MIN_VALUE))
        printError("You are trying to set the sample value to: "+
                   sample + ", but the maximum value for a sample"+
                   " in this format is: "+Short.MAX_VALUE+
                   ", and the minimum value is: "+Short.MIN_VALUE+
                   ".  Please choose a value in that range.");
      theFrame[0] = TConversionTool.linear2ulaw((short)sample);
      setFrame(frameNum, theFrame);
    }
    else
    {
      printError("unsupported audio encoding: " +
                 format.getEncoding() + ".  Currently only PCM, " +
                 "ALAW and ULAW are supported.  Please try again" +
                 "with a different file.");
    }
  }//setSample(int, int)

  /**
   * Method to set the left sample value at the passed index to the passed value
   * @param frameNum the index of the frame where the sample should be changed
   * @param sample an integer representation of the new sample
   */
  public void setLeftSample(int frameNum, int sample) throws SoundException
  {
    setSampleValue(frameNum, sample);
  }

  /**
   * Method to set the right sample value at the passed index to the passed value
   * @param frameNum the index of the frame where the sample should be changed
   * @param sample an integer representation of the new sample
   */
  public void setRightSample(int frameNum, int sample) throws SoundException
  {
    AudioFormat format = getAudioFileFormat().getFormat();
    int sampleSizeInBits = format.getSampleSizeInBits();
    boolean isBigEndian = format.isBigEndian();

    if(format.getChannels() == 1)
      printError("this is a mono sound.  only stereo sounds have" +
                 " different left and right samples.");

    byte[] theFrame = getFrame(frameNum);

    if(format.getEncoding().equals(AudioFormat.Encoding.PCM_SIGNED))
    {
      //right will always be the second in the frame
      if(sampleSizeInBits == 8)
      {
        theFrame[1] = (byte)sample;
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 16)
      {
        TConversionTool.intToBytes16(sample, theFrame, 2, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 24)
      {
        TConversionTool.intToBytes24(sample, theFrame, 3, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 32)
      {
        TConversionTool.intToBytes32(sample, theFrame, 4, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else
      {
        printError("Unsupported audio encoding.  The sample"+
                   "size is not recognized as a standard format");
      }
    }//if format == PCM_SIGNED
    else if(format.getEncoding().equals(AudioFormat.Encoding.PCM_UNSIGNED))
    {
      if(sampleSizeInBits == 8)
      {
        theFrame[1] = TConversionTool.intToUnsignedByte(sample);
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 16)
      {
        TConversionTool.intToUnsignedBytes16(sample, theFrame, 2, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 24)
      {
        TConversionTool.intToUnsignedBytes24(sample, theFrame, 3, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else if(sampleSizeInBits == 32)
      {
        TConversionTool.intToUnsignedBytes32(sample, theFrame, 4, isBigEndian);
        setFrame(frameNum, theFrame);
      }
      else
      {
        printError("Unsupported audio encoding.  The sample"+
                   " size is not recognized as a standard"+
                   " format");
      }
    }
    else if(format.getEncoding().equals(AudioFormat.Encoding.ALAW))
    {
      if((sample>Short.MAX_VALUE)||(sample<Short.MIN_VALUE))
        printError("You are trying to set the sample value to: "+
                   sample + ", but the maximum value for a sample"+
                   " in this format is: "+Short.MAX_VALUE+
                   ", and the minimum value is: "+Short.MIN_VALUE+
                   ".  Please choose a value in that range.");
      theFrame[1] = TConversionTool.linear2alaw((short)sample);
      setFrame(frameNum, theFrame);
    }
    else if(format.getEncoding().equals(AudioFormat.Encoding.ULAW))
    {
      if((sample>Short.MAX_VALUE)||(sample<Short.MIN_VALUE))
        printError("You are trying to set the sample value to: "+
                   sample + ", but the maximum value for a sample"+
                   " in this format is: "+Short.MAX_VALUE+
                   ", and the minimum value is: "+Short.MIN_VALUE+
                   ".  Please choose a value in that range.");
      theFrame[1] = TConversionTool.linear2ulaw((short)sample);
      setFrame(frameNum, theFrame);
    }
    else
    {
      printError("unsupported audio encoding: " +
                 format.getEncoding() + ".  Currently only PCM, " +
                 "ALAW and ULAW are supported.  Please try again" +
                 "with a different file.");
    }
  }//setRightSample(int, int)

  /**
   * Method to open a sound viewer on a copy of this sound
   */
  public void explore()
  {
    SimpleSound sound = new SimpleSound(this);
    new SoundExplorer(sound,this.isStereo());
  }

  //TODO: is there a reason this is here?
  /**
   * Method to play a note using MIDI
   * @param key the piano key to play
   * @param duration how long to play the note
   * @param intensity how hard to strike the note from (0-127)
   */
  public static void playNote(int key, int duration, int intensity)
  {
  }

  /**
   * Method to convert a mp3 sound into a wav sound
   * @param mp3File the file name of the mp3 to convert
   * @param wavFile the file name to save the wav to
   */
  public static void convert(String mp3File, String wavFile)
  {
    try {
      Converter converter = new Converter();
      converter.convert(mp3File,wavFile);
    } catch (Exception ex) {
      SimpleOutput.showError("Couldn't covert the file " + mp3File);
    }
  }

  ////////////////////// String methods ///////////////////////////////

  /**
   * Obtains a string representation of this JavaSound.
   * @return a String representation of this JavaSound.
   */
  public String toString()
  {
    String output = "SimpleSound";

    // if there is a file name then add that to the output
    if (fileName != null)
      output = output + " file: " + fileName;

    // add the length
    output = output + " length: " + getLengthInBytes();

    return output;
  }

} // end of SimpleSound class
