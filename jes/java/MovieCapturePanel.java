import java.awt.*;
import java.awt.event.*;
import java.util.*;
import javax.swing.*;

/**
 * Class MovieCapturePanel: a panel used to capture a movie
 * Copyright Georgia Institute of Technology 2007
 * <br>
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class MovieCapturePanel extends JPanel
{

  /////////////////////// Private Attributes /////////////////////

  /** captured screen area and pick region area */
  private ShapeComponent shapeComponent = new ShapeComponent(500,500);
  /** panel with buttons to control capture */
  private CaptureButtonPanel buttonPanel = null;
  /** class that holds information on the capture */
  private MovieCapturer movieCapturer = null;

  ////////////////////// Constructors /////////////////////////////

  /** A constructor that takes a directory to write the
    * frames to
    * @param directory the directory to write to
    */
  public MovieCapturePanel (String directory)
  {
    init(directory);
  }

  /**
   * Constructor that takes no arguments
   */
  public MovieCapturePanel()
  {
    String directory = SimpleInput.getString(
        "Directory to write the movie frames to (use / or \\\\ in path).");
    init(directory);
  }

  //////////////////// Private Methods /////////////////////////////////

  /* Method to initialize the panel
   * @param directory the directory to write to
   */
  private void init(String directory)
  {
    /** set up the parts */
    MovieCapturer movieCapturer = new MovieCapturer(directory);
    buttonPanel = new CaptureButtonPanel(movieCapturer,shapeComponent);
    shapeComponent.setVideoCapture(movieCapturer);

    // use a border layout
    setLayout(new BorderLayout());

    // add the button panel to the north section of the border layout
    add(buttonPanel,BorderLayout.NORTH);

    // add the shape canvas to the center section of the border layout
    add(shapeComponent, BorderLayout.CENTER);
  }

  ////////////////////// Main Method for Testing ////////////////////////
  public static void main (String argv[])
  {
    // create a frame (main application window)
    JFrame frame = new JFrame("Frame-based Movie Capturer");
    frame.setAlwaysOnTop(true);
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    // create a Shape Panel
    MovieCapturePanel panel = new MovieCapturePanel();

    // add the shapePanel to the frame
    frame.getContentPane().add(panel);
    frame.pack();         // shrink to fit preferred size
    frame.setVisible(true); // show the frame
  }

}


