import java.util.*;
import java.text.*;
import java.io.*;
import java.awt.Image;

/**
 * Class used to save frames in a movie to a directory and
 * show frames from a movie.  This
 * class tracks the directory, base file name, current
 * frame number, and whether this sequence is being shown.
 * <br>
 * Copyright Georgia Institute of Technology 2005
 * @author Barbara Ericson ericson@cc.gatech.edu
 */
public class FrameSequencer
{
  //////////////////// Fields ///////////////////////////////////

  /** stores the directory to write the frames to */
  private String directory;

  /** stores the base file name for each frame file */
  private String baseName = "frame";

  /** stores the current frame number */
  private int frameNumber = 1;

  /** true if this sequence is being shown */
  private boolean shown = false;

  /** the movie player used to show this sequence */
  private MoviePlayer moviePlayer = null;

  /** List of all the pictures so far */
  private List<Picture> pictureList = new ArrayList<Picture>();

  /** Use this to format the number for the frame */
  private NumberFormat numberFormat =
    NumberFormat.getIntegerInstance();

  //////////////////// Constructors /////////////////////////////

  /**
   * Constructor that takes a directory name
   * @param directory the directory to save the frames to
   */
  public FrameSequencer(String directory)
  {
    this.directory = directory;
    initFormatter();
    validateDirectory();
  }

  /**
   * Constructor that takes a directory name and a base file name
   * @param directory the directory to save the frames to
   * @param baseName the base file name to use for the frames
   */
  public FrameSequencer(String directory, String baseName)
  {
    // use the other constructor to set the directory
    this(directory);

    // set the base file name
    this.baseName = baseName;
  }

  ///////////////////// Methods ////////////////////////////////

  /**
   * Method to get the directory to write the frames to
   * @return the directory to write the frames to
   */
  public String getDirectory() { return directory; }

  /**
   * Method to set the directory to write the frames to
   * @param dir the directory to use
   */
  public void setDirectory(String dir)
  {
    directory = dir;
    initFormatter();
    validateDirectory();
  }

  /**
   * Method to get the base name
   * @return the base file name for the movie frames
   */
  public String getBaseName() { return baseName; }

  /**
   * Method to set the base name
   * @param name the new base name to use
   */
  public void setBaseName(String name) { baseName = name; }

  /**
   * Method to get the frame number
   * @return the next frame number for the next picture
   * added
   */
  public int getFrameNumber() { return frameNumber; }

  /**
   * Method to check if the frame sequence is being shown
   * @return true if shown and false otherwise
   */
  public boolean isShown() { return shown; }

  /**
   * Method to set the shown flag
   * @param value the value to use
   */
  public void setShown(boolean value) { shown = value; }

  /**
   * Method to get the number of frames in this sequence
   * @return the number of frames
   */
  public int getNumFrames() { return pictureList.size(); }

  /**
   * Method to get the movie player to use to show this sequence
   * @return the movie player used to show this (may be null)
   */
  public MoviePlayer getMoviePlayer() { return moviePlayer; }

  /**
   * Method to initialize the number formatter to show 4 digits
   * with no commas
   */
  private void initFormatter()
  {
    numberFormat.setMinimumIntegerDigits(4);
    numberFormat.setGroupingUsed(false);
  }

  /**
   * Method to validate the directory (make
   * sure it ends with a separator character
   */
  private void validateDirectory()
  {
    char end = directory.charAt(directory.length() - 1);
    if (end != '/' && end != '\\')
      directory = directory + '/';
    File directoryFile = new File(directory);
    if (!directoryFile.exists())
      directoryFile.mkdirs();
  }

  /**
   * Method to add a picture to the frame sequence
   * @param picture the picture to add
   */
  public void addFrame(Picture picture)
  {

    // add this picture to the list
    pictureList.add(picture);

    // get the file name
    String fileName = directory + baseName +
      numberFormat.format(frameNumber) + ".jpg";

    // set the file name
    picture.setFileName(fileName);

    // write out this frame
    picture.write(fileName);

    // if this sequence is being shown update the frame
    if (shown)
    {
      if (moviePlayer != null)
        moviePlayer.addPicture(picture);
      else
        moviePlayer = new MoviePlayer(pictureList);
    }

    // increment the frame number
    frameNumber++;
  }

  /**
   * Method to delete the last frame
   */
  public void deleteLastFrame()
  {
    frameNumber--;
    File f = new File(directory + baseName +
      numberFormat.format(frameNumber) + ".jpg");
    boolean result = f.delete();
    if (result != true)
      System.out.println("trouble removing last frame");
    pictureList.remove(pictureList.size() - 1);
  }

  /**
   * Method to show the frame sequence
   */
  public void show()
  {
    if (shown != true)
    {
      // set it to true
      shown = true;

      // if there is a picture show the last one
      if (pictureList.size() > 0)
      {
        int lastIndex = pictureList.size() - 1;
        Picture lastPicture = (Picture) pictureList.get(lastIndex);
        moviePlayer = new MoviePlayer(pictureList);
        moviePlayer.setVisible(true);
      }
      else
        System.out.println("There are no frames to show yet.  " +
                           "When you add a frame it will be shown");
    }
  }

  /**
   * Method to play the frames (pictures) added so far
   * @param framesPerSecond the number of frames to show per second
   * between frames
   */
  public void play(int framesPerSecond)
  {
    if (pictureList.size() > 0)
    {
      shown = true;
      if (moviePlayer == null)
        moviePlayer = new MoviePlayer(pictureList);
      moviePlayer.playMovie(framesPerSecond);
    }
  }

  public static void main(String[] args)
  {
    String dir = "c:/intro-prog-java/movies/rectangle/";
    FrameSequencer frameSequencer =
      new FrameSequencer(dir);
    //frameSequencer.play(1000/30);
    //frameSequencer.play();
  }

} // end of class