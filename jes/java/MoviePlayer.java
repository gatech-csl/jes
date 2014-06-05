import javax.swing.*;
import java.util.*;
import java.io.*;
import java.awt.Container;
import java.awt.BorderLayout;
import java.awt.Image;
import java.awt.event.*;

/**
 * Class that can play movies from multiple frames
 * <br>
 * Copyright Georgia Institute of Technology 2007
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class MoviePlayer
{

  ///////////////// fields ///////////////////////////

  private JFrame frame = new JFrame("Movie Player");
  private JLabel frameLabel = new JLabel("No images yet!");
  private AnimationPanel animationPanel = null;
  private String dir = null;

  //////////////////// constructors ////////////////////

  /**
   * Constructor that takes a list of pictures
   * @param pictureList the list of pictures to show
   */
  public MoviePlayer(List<Picture> pictureList)
  {
    animationPanel = new AnimationPanel(pictureList);
    Picture p = pictureList.get(0);
    String fileName =  p.getFileName();
    File f = new File(fileName);
    dir =  f.getParent() + "/";
    init();
  }

  /**
   * Constructor that takes a directory and shows a movie
   * from it
   * @param directory the directory with the frames
   */
  public MoviePlayer(String directory)
  {
    animationPanel = new AnimationPanel(directory);
    dir = directory;
    init();
  }

  /**
   * Constructor to create a movie player by asking
   * the user to pick the directory that contains
   * the JPEG frames
   */
  public MoviePlayer()
  {
    SimpleOutput.showInformation("Please pick a " +
                   "directory that contains the JPEG frames");
    String directory = FileChooser.pickADirectory();
    dir = directory;
    animationPanel = new AnimationPanel(directory);
    init();
  }

  /////////////////////// methods ////////////////////////////

  /**
   * Method to show the next image
   */
  public void showNext()
  {
   animationPanel.showNext();
   frameLabel.setText("Frame Number " +
                      animationPanel.getCurrIndex());
   frame.repaint();
  }

  /**
   * Method to show the previous image
   */
  public void showPrevious()
  {
    animationPanel.showPrev();
    frameLabel.setText("Frame Number " +
                       animationPanel.getCurrIndex());
    frame.repaint();
  }

  /**
   * Method to play the movie from the beginning
   */
  public void playMovie()
  {
    frameLabel.setText("Playing Movie");
    frame.repaint();
    animationPanel.showAll();
    frameLabel.setText("Frame Number " +
                       animationPanel.getCurrIndex());
    frame.repaint();
  }

   /**
   * Method to play the movie from the beginning
   * @param framesPerSecond the number of frames to show
   * per second
   */
  public void playMovie(int framesPerSecond)
  {
    animationPanel.setFramesPerSec(framesPerSecond);
    playMovie();
  }

  /**
   * Method to set the frames per second to show the movie
   * @param rate the number of frames to show per second
   */
  public void setFrameRate(int rate)
  {
    animationPanel.setFramesPerSec(rate);
  }

  /**
   * Method to delete all the frames before the
   * current one
   */
  public void delAllBefore()
  {
    animationPanel.removeAllBefore();
  }

  /**
   * Method to delete all the frames after the
   * current one
   */
  public void delAllAfter()
  {
    animationPanel.removeAllAfter();
  }

  /**
   * Method to write out the movie frames as a
   * Quicktime movie
   */
  public void writeQuicktime()
  {

    MovieWriter writer = new MovieWriter(animationPanel.getFramesPerSec(),
                                        dir);
    writer.writeQuicktime();
  }

   /**
   * Method to write out the movie frames as a
   * Quicktime movie
   */
  public void writeAVI()
  {
    MovieWriter writer = new MovieWriter(animationPanel.getFramesPerSec(),
                                        dir);
    writer.writeAVI();
  }

  /**
   * Method to add a picture to the movie
   * @param picture the picture to add
   */
  public void addPicture(Picture picture)
  {
    animationPanel.add(picture);
    showNext();
  }

  /**
   * Method to set up the gui
   */
  private void init()
  {
    frame.setAlwaysOnTop(true);
    frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
    Container container = frame.getContentPane();
    container.setLayout(new BorderLayout());
    JPanel buttonPanel = new JPanel();

    // add the animation panel
    container.add(animationPanel,BorderLayout.CENTER);

    // add the frame label to the north
    JPanel labelPanel = new JPanel();
    labelPanel.add(frameLabel);
    container.add(labelPanel,BorderLayout.NORTH);

    // add the button panel to the south
    container.add(new ButtonPanel(this),BorderLayout.SOUTH);

    // set the size of the frame
    frame.pack();

    // show the frame
    frame.setVisible(true);
  }

  /**
   * Method to set the visibility of the frame
   * @param flag the visibility of the frame
   */
  public void setVisible(boolean flag)
  {
    frame.setVisible(flag);
  }

  public static void main(String[] args)
  {
    MoviePlayer moviePlayer =
     new MoviePlayer();
    //new MoviePlayer("c:/temp/movie4/");
    moviePlayer.playMovie(16);
  }

}
