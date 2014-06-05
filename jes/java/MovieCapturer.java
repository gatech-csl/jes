import java.awt.AWTException;
import java.awt.Robot;
import java.awt.Toolkit;
import java.awt.image.BufferedImage;
import java.io.*;
import javax.imageio.ImageIO;

/**
 * Class that captures a movie to a series of jpg frames
 * <br>
 * Copyright Georgia Institute of Technology 2007
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class MovieCapturer implements VideoCapturer
{
  ////////////////// fields /////////////////////////////

  /** frame sequencer for writing out frames */
  private FrameSequencer frameSequencer = null;

  /** the number of frames per second */
  private int framesPerSec = 16;

  /** rectangular region to capture */
  private java.awt.Rectangle region = null;

  ////////////////// Constructors ////////////////////////

  /** Constructor that takes the directory to write the
    * frames to
    * @param directory the directory to write to
    */
  public MovieCapturer(String directory)
  {
    frameSequencer = new FrameSequencer(directory);
  }

  /**
   * Constructor that takes the directory to write to and
   * the base name to use for the files
   * @param directory the directory to write to
   * @param baseName the name to use for the files
   */
  public MovieCapturer(String directory, String baseName)
  {
    frameSequencer = new FrameSequencer(directory,baseName);
  }

  ////////////////////// Methods //////////////////////////

  /**
   * Method to get the current directory
   * @return the directory name
   */
  public FrameSequencer getFrameSequencer()
  { return this.frameSequencer; }

  /** Method to get the number of frames per second
    * @return the number of frames per second
    */
  public int getFramesPerSecond()
  { return this.framesPerSec; }

  /**
   * Method to set the number of frames per second
   * @param frameRate the number of frames per second
   */
  public void setFramesPerSecond(int frameRate)
  {
    this.framesPerSec = frameRate;
  }

  /**
   * Method to get the region to capture
   * @return the rectangular region to capture
   */
  public java.awt.Rectangle getRegion()
  { return this.region; }

  /**
   * Method to capture the entire screen
   * @return the captured buffered image
   */
  public Picture captureScreen() throws Exception
  {

     // capture the whole screen
     BufferedImage image = new Robot().createScreenCapture(
           new java.awt.Rectangle(Toolkit.getDefaultToolkit().getScreenSize()));
     Picture pict = new Picture(image);

     return pict;
  }

  /**
   * Method to capture a part of the screen
   * @param x1 the top left x
   * @param y1 the top left y
   * @param width the width of the rectangle to capture
   * @param height the height of the rectangle to capture
   * @return the captured buffered image
   */
  public Picture captureRegion(int x1, int y1,
                            int width, int height)
                      throws AWTException
  {

     // capture the whole screen
     BufferedImage screen = new Robot().createScreenCapture(
           new java.awt.Rectangle(x1,y1,width,height));
	 Picture pict = new Picture(screen);
     return pict;
  }

  /**
   * Method to capture a region of the screen
   * @return the region if there is one else the screen
   */
  public Picture captureRegion() throws Exception
  {
    if (region != null)
    {
      BufferedImage image =
      new Robot().createScreenCapture(region);
	  Picture pict = new Picture(image);
      return pict;
    }
    else return captureScreen();
  }

  /**
   * Method to capture a movie until the done
   * flag is set to true
   */
  public void captureMovie()
  {
    boolean done = false;
    Picture image = null;
    long startTime = 0;
    long endTime = 0;
    int timeToSleep = (int) (1000 / framesPerSec);
    while (!done)
    {
      try {
        startTime = System.currentTimeMillis();
        image = captureRegion();
        frameSequencer.addFrame(image);
        endTime = System.currentTimeMillis();
        Thread.sleep(timeToSleep - (endTime - startTime));
      } catch (Exception ex) {
      }
    }
  }

  /**
   * Method to run the captured movie
   */
  public void run()
  {
    captureMovie();
  }

  /**
   * Method to capture a movie for the passed
   * number of seconds
   * @param numSeconds the number of seconds to capture
   */
  public void captureMovie(int numSeconds)
  {
    Picture image = null;
    int timeToSleep = (int) (1000 / framesPerSec);
    long startTime = 0;
    long endTime = 0;
    for (int i = 0; i < framesPerSec * numSeconds; i++)
    {
      try {
        startTime = System.currentTimeMillis();
        image = captureRegion();
        frameSequencer.addFrame(image);
        endTime = System.currentTimeMillis();
        Thread.sleep(timeToSleep - (endTime - startTime));
      } catch (Exception ex) {
      }
    }
  }

  /**
   * Method to capture a movie until the done
   * flag is set to true
   * @param x1 the top left x value
   * @param y1 the top left y value
   * @param width the width of the region to capture
   * @param height the height of the region to capture
   */
  public void captureMovie(int x1, int y1,
                           int width, int height)
  {
    boolean done = false;
    long startTime = 0;
    long endTime = 0;
    Picture image = null;
    int timeToSleep = (int) (1000 / framesPerSec);
    while (!done)
    {
      try {
        startTime = System.currentTimeMillis();
        image = captureRegion(x1,y1,width,height);
        frameSequencer.addFrame(image);
        endTime = System.currentTimeMillis();
        Thread.sleep(timeToSleep - (endTime - startTime));
      } catch (Exception ex) {
      }
    }
  }

  /**
   * Method to capture a movie in a rectangular
   * region for the passed number of seconds
   * @param x1 the top left x value
   * @param y1 the top left y value
   * @param width the width of the region to capture
   * @param height the height of the region to capture
   * @param numSeconds the number of seconds to capture
   */
  public void captureMovie(int x1, int y1,
                           int width, int height,
                           int numSeconds)
  {
    long startTime = 0;
    long endTime = 0;
    Picture image = null;
    int timeToSleep = (int) (1000 / framesPerSec);
    for (int i = 0; i < numSeconds * framesPerSec; i++)
    {
      try {
        startTime = System.currentTimeMillis();
        image = captureRegion(x1,y1,width,height);
        frameSequencer.addFrame(image);
        endTime = System.currentTimeMillis();
        Thread.sleep(timeToSleep - (endTime - startTime));
      } catch (Exception ex) {
      }
    }
  }

  /**
   * Method to play the captured movie
   */
  public void playMovie()
  {
    frameSequencer.play(framesPerSec);
  }

  /**
   * Method to set the region to capture (makes
   * sure that the width and height is a multiple of
   * 4 for compression later
   * @param theRegion a rectangle that encloses the region to capture
   */
  public void setRegion(java.awt.Rectangle theRegion)
  {
    if (theRegion.getWidth() % 4 != 0 ||
        theRegion.getHeight() % 4 != 0)
    {
      int width = (int) theRegion.getWidth() / 4 * 4;
      int height = (int) theRegion.getHeight() / 4 * 4;
      this.region = new java.awt.Rectangle((int) theRegion.getX(),
                                          (int) theRegion.getY(),
                                          width,height);
    }
    else
    {
      this.region = theRegion;
    }
  }

 /**
  * Method to start capturing the movie
  */
 public void startCapture()
 {
   //this.done = false;
   captureMovie();
 }

 /**
  * Method to start captureing the movie and
  * continue for the passed number of seconds
  * @param numSeconds the number of seconds to capture
  */
 public void startCapture(int numSeconds)
 {
   captureMovie(numSeconds);
 }

 /**
  * Method to stop capturing the movie
  */
 public void stopCapture()
 {
   // need a separate thread to stop the capture
   //this.done = true;
 }

  public static void main(String args[])
  {
    MovieCapturer capturer = new MovieCapturer(
                 "c:/intro-prog-java/mediasources/aliceTest1/",
                                               "alice1");
    capturer.captureMovie(0,0,810,674,1);
    capturer.playMovie();
  }
}