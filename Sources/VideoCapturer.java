import java.awt.image.BufferedImage;
import java.awt.Rectangle;

/**
 * Interface for working with video capture
 * <br>
 * Copyright Georgia Institute of Technology 2007
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public interface VideoCapturer
{
  /**
   * Method that captures the screen
   * @return the captured buffered image
   */
  public Picture captureScreen() throws Exception;

  /**
   * Method that sets a region to capture
   * @param region the rectangular region to capture
   */
  public void setRegion(java.awt.Rectangle region);

  /** Method to start the capture */
  public void startCapture();

  /**
   * Method to start the capture and capture numSeconds of video
   * @param numSeconds the number of seconds to capture
   */
  public void startCapture(int numSeconds);

  /**
   * Method to stop the capture
   */
  public void stopCapture();

  /**
   * Method to play the captured movie
   */
  public void playMovie();

  /**
   * Method to get the frame sequencer
   * @return the frame sequencer used in the capture
   */
  public FrameSequencer getFrameSequencer();

  /**
   * Method to get the region to capture
   * @return the region to capture
   */
  public Rectangle getRegion();

  /**
   * Method to return the number of frames per second
   * @return the number of frames per second being captured
   */
  public int getFramesPerSecond();

  /**
   * Method to set the number of frames per second
   * @param frameRate the number of frames per second being captured
   */
  public void setFramesPerSecond(int frameRate);

}