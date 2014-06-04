import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.awt.Robot;

/**
 * Class that is Runnable to start Movie Capture and
 * stop it
 * <br>
 * Copyright Georgia Institute of Technology 2007
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class StartMovieCapture implements Runnable
{
  /** the frame sequencer to use to write out the frames */
  private FrameSequencer frameSequencer = null;
  /** the number of frames per second to capture */
  private int framesPerSecond = 16;
  /** the region to capture */
  private Rectangle region = null;
  /** the active thread */
  private Thread active = null;

  /**
   * Constructor that takes the frame sequencer, number of
   * frames per second, and the region to capture
   * @param sequencer the frame sequencer
   * @param framesPerSec the number of frames per second
   * @param area the region to capture
   */
  public StartMovieCapture(FrameSequencer sequencer,
                           int framesPerSec,
                           Rectangle area)
  {
    frameSequencer = sequencer;
    framesPerSecond = framesPerSec;
    region = area;
  }

  /**
   * Method to capture a movie until the stop
   * method is called and sets the active thread
   * to null
   */
  public void captureMovie()
  {
    boolean done = false;
    BufferedImage image = null;
    long startTime = 0;
    long endTime = 0;
    int timeToSleep = (int) (1000 / framesPerSecond);
    int actualTime = timeToSleep;
    int count = 0;
    Thread current = Thread.currentThread();
    while (current == active)
    {
      try {
        startTime = System.currentTimeMillis();
        image = new Robot().createScreenCapture(region);
        frameSequencer.addFrame(new Picture(image));
        endTime = System.currentTimeMillis();
        if (endTime - startTime < timeToSleep)
            Thread.sleep(timeToSleep-(endTime-startTime));
      } catch (Exception ex) {
        System.out.println("caught exception in StartMovieCapture");
        done = true;
      }
    }
  }


  /**
   * Method to start the thread
   */
  public void run()
  {
    active = Thread.currentThread();
    captureMovie();
  }

  /**
   * Method to stop the thread
   */
  public void stop()
  {
    active = null;
  }
}