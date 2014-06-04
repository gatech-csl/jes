import javax.sound.sampled.*;
import java.io.*;

/**
 * The class <code>Playback</code> extends from <code>Thread</code>
 * and allows for playback of a simple sound.  The thread doesn't die until
 * the sound is finished playing, however it is not blocking either.  It
 * will simply play the sound in the "background."
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author unknown undergrad
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class Playback extends Thread
{
  ///////////////// fields ////////////////////////////////////

  /**
   * Constant that is the default buffer size.
   * @see Sound#Sound()
   * @see Playback#run()
   */
  private static final int BUFFER_SIZE = 16384;

  /**
   * The source data line for the sound
   */
  private SourceDataLine line;

  /**
   * flag that says is the sound currently being played
   */
  private boolean playing = false;

  /**
   * The sound being played
   */
  private SimpleSound sound;

  ////////////////// Constructors //////////////////////////////////////

  /**
   * Constructor that takes the simple sound to be played
   * @param sound the simple sound to play
   */
  public Playback(SimpleSound sound)
  {
    this.sound = sound;
  }

  /**
   * Stop the playback
   */
  private void shutDown(String message, Exception e)
  {
    if (message != null)
    {
      System.err.println(message);
      e.printStackTrace();
    }
    playing = false;
  }

  /**
   * Stops this thread by breaking the while loop in the run method.
   * Used, for example, by the "stop" button in the SoundExplorer class.
   */
  public void stopPlaying()
  {
    playing = false;
  }

  /**
   * Method to return true if this playback thread is playing and
   * false otherwise
   * @return true if playing else false
   */
  public boolean getPlaying()
  {
    return playing;
  }

  /**
   * Starts this thread.  Gets an AudioInputStream, and writes is out
   * to a SourceDataLine.  If a SoundExplorer exists, upon creation of
   * the SourceDataLine, the soundExplorer is added as the LineListener.
   * When the thread finishes the run method, it removes itself from the
   * list of threads currently playing this sound.
   * @throws JavaSoundException if there were problems playing the sound.
   */
  public void run()
  {

    AudioFileFormat audioFileFormat = sound.getAudioFileFormat();
    SoundExplorer soundExplorer = sound.getSoundExplorer();

    //get something to play
    AudioInputStream audioInputStream = sound.makeAIS();
    if(audioInputStream == null)
    {
      shutDown("There is no input stream to play", null);
      return;
    }

    //reset stream to the begining
    try {
      audioInputStream.reset();
    } catch(Exception e) {
      shutDown("Problems resetting the stream\n", e);
      return;
    }

    /* define the required attributes for the line
     make sure a compatible line is supported */
    DataLine.Info info = new DataLine.Info(SourceDataLine.class,
                                           audioFileFormat.getFormat());
    if(!AudioSystem.isLineSupported(info))
    {
      shutDown("Line matching " + info + "not supported.", null);
      return;
    }

    //get and open the source data line for playback
    try {
      line = (SourceDataLine) AudioSystem.getLine(info);
      if(sound.getSoundExplorer() != null)
        line.addLineListener(soundExplorer);
      line.open(audioFileFormat.getFormat(), BUFFER_SIZE);
    } catch(LineUnavailableException e) {
      shutDown("Unable to open the line: ", e);
      return;
    }

    //play back the captured data
    int frameSizeInBytes = audioFileFormat.getFormat().getFrameSize();
    int bufferLengthInBytes = line.getBufferSize();
    int bufferLengthInFrames = bufferLengthInBytes / frameSizeInBytes;
    byte[] data = new byte[bufferLengthInBytes];
    int numBytesRead = 0;

    //start the source data line and begin playing
    line.start();
    playing = true;

    // the loop that actually writes the data out
    while(playing)
    {
      try {
        if((numBytesRead = audioInputStream.read(data))
             == -1)
        {
          break;//end of audioInputStream
        }
        int numBytesRemaining = numBytesRead;
        while(numBytesRemaining > 0)
        {
          numBytesRemaining -=
            line.write(data, 0, numBytesRemaining);
        }//while
      } catch(Exception e) {
        shutDown("Error during playback: ", e);
        break;
      }//catch
    }//while

    /* we reached the end of the stream or an error occurred.
     if we were playing, then let the data play out, else, skip to
     stopping and closing the line.
     */
    if(playing)
      line.drain();
    line.stop();
    line.close();
    line = null;
    shutDown(null, null);
    //if(sound.getDEBUG())
      //System.out.println("exiting run method");
    /*
     this thread is about to die.  remove itself from the collection
     of threads playing this sound
     */
    sound.removePlayback(this);

  }//run()

}//end class Playback