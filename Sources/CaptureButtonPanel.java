import java.awt.*;
import java.awt.event.*;
import java.util.*;
import javax.swing.*;
import javax.swing.event.*;
import java.awt.image.BufferedImage;
import java.net.*;

/**
 * Class that holds buttons for video capture<br>
 * Copyright Georgia Institute of Technology 2005
 * @author Barb Ericson ericson@cc.gatech.edu
 *
 * Line 199: warning: [deprecation] stop() in java.lang.Thread has been deprecated
 * Buck Scharfnorth 22 May 2008
 */
public class CaptureButtonPanel extends JPanel
{

  ///////////////////// Public Attributes ////////////////////////

  ////////////////////// Private Attributes //////////////////////

  /** help button */
  private JButton helpButton;
  /** button to capture the screen */
  private JButton captureScreenButton; // screen capture button
  /** button to start picking a region to capture */
  private JButton pickRegionButton; // pick the region button
  /** button to start the capture */
  private JButton startButton; // start capture button
  /** button to play the captured movie */
  private JButton playButton; // play movie button
  /** button to stop the video capture */
  private JButton stopButton; // stop capture button
  /** model class that handles the video capture */
  private VideoCapturer videoHandler = null; // the video capturer handler
  /** model class that handles the screen display and region pick */
  private RegionInterface regionHandler = null; // area to select region
  /** thread for video capture */
  private Thread t = null;
  /** text field for the directory to write to */
  private JTextField dirTextField = null;
  /** list for the frame rate */
  private JList frameRateList = null;
  /** label for frame rate */
  private JLabel frameRateLabel = null;
  /** label for directory */
  private JLabel directoryLabel = null;

  //////////////////////// Constructors ////////////////////////////

  /** Constructor that takes no arguments */
  public CaptureButtonPanel ()
  {
    // initialize the panel
    init();
  }

  /** Constructor that takes the object that handles the video
    * capture and the object that handles the region selection
   * @param theHandler    the handler of the video capture
   * @param regionIntHandler the handler of the region selection
   */
  public CaptureButtonPanel (VideoCapturer theHandler,
                      RegionInterface regionIntHandler)
  {
    // set the handler
    videoHandler = theHandler;
    regionHandler = regionIntHandler;

    // initialize the panel
    init();
  }

  /////////////////// Private Methods ///////////////////////////////

  /** Method to initialize the panel */
  private void init()
  {
    this.setLayout(new BorderLayout());
    JPanel buttonPanel = new JPanel();
    JPanel infoPanel = new JPanel();

    // set up info panel
    directoryLabel = new JLabel("Directory: ");
    FrameSequencer frameSequencer = videoHandler.getFrameSequencer();
    String dir = frameSequencer.getDirectory();
    dirTextField = new JTextField(dir,Math.max(20,dir.length()));
    dirTextField.setToolTipText("Directory to write the movie frames to");
    dirTextField.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent e) {
        FrameSequencer frameSequencer = videoHandler.getFrameSequencer();
        String dir = dirTextField.getText();
        frameSequencer.setDirectory(dir);
      }
    });
    infoPanel.add(directoryLabel);
    infoPanel.add(dirTextField);
    frameRateLabel = new JLabel("Frames per Second: ");
    infoPanel.add(frameRateLabel);

    String[] rates = {"16","24","30"};
    frameRateList = new JList(rates);
    JScrollPane scrollPane = new JScrollPane(frameRateList);
    frameRateList.setSelectedIndex(0);
    frameRateList.setVisibleRowCount(1);
    frameRateList.setToolTipText("The number of frames per second in the movie");
    frameRateList.addListSelectionListener(new ListSelectionListener() {
      public void valueChanged(ListSelectionEvent e) {
        String rate = (String) frameRateList.getSelectedValue();
        videoHandler.setFramesPerSecond(Integer.parseInt(rate));
      }
    });
    infoPanel.add(scrollPane);

    // add help button
    helpButton = new JButton("Help");
    helpButton.setToolTipText("Click here to see help");
    helpButton.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent e) {
        showHelp();
      }
    });
    infoPanel.add(helpButton);
    //infoPanel.add(frameRateTextField);

    // set up button panel

    // create the capture screen button
    captureScreenButton = new JButton("Capture Screen");
    captureScreenButton.setToolTipText("Click here to capture the"+
                                       " screen image and show it below");
    buttonPanel.add(captureScreenButton);
    captureScreenButton.addActionListener(new ActionListener() {
      public void actionPerformed (ActionEvent e) {
        if (videoHandler != null && regionHandler != null)
          try {
          regionHandler.setBackgroundImage(videoHandler.captureScreen());
          pickRegionButton.setEnabled(true);
          repaint();
        } catch (Exception ex) {
        }
      }
    });

    // create the pick region button
    pickRegionButton = new JButton("Pick Region");
    pickRegionButton.setToolTipText("Click here to pick a region to capture."+
                               "  Then click on the top left corner and "+
                          "drag the cursor to the bottom right of the region");
    pickRegionButton.setEnabled(false);
    buttonPanel.add(pickRegionButton);
    pickRegionButton.addActionListener(new ActionListener() {
      public void actionPerformed (ActionEvent e) {
        if (regionHandler != null)
        {
           regionHandler.clearShapes();
           startButton.setEnabled(true);
        }
      }
    });

//    JLabel label = new JLabel("Number of Seconds to Capture: ");
//    secField = new JTextField("3",3);
//    add(label);
//    add(secField);

    // create the start capture button
    startButton = new JButton("Start Capture");
    startButton.setToolTipText("Click here to start the video capture");
    startButton.setEnabled(false);
    buttonPanel.add(startButton);
    startButton.addActionListener(new ActionListener() {
      public void actionPerformed (ActionEvent e) {
        if (videoHandler != null)
        {
          java.awt.Rectangle region = videoHandler.getRegion();
          FrameSequencer frameSequencer = videoHandler.getFrameSequencer();
          int framesPerSec = videoHandler.getFramesPerSecond();
          t = new Thread(new StartMovieCapture(frameSequencer,
                                                      framesPerSec,
                                                      region));
          startButton.setEnabled(false);
          stopButton.setEnabled(true);
          t.start();
        }
      }
    });

    // create the stop capture button
    stopButton = new JButton("Stop Capture");
    stopButton.setToolTipText("Click here to stop the video capture");
    stopButton.setEnabled(false);
    buttonPanel.add(stopButton);
    stopButton.addActionListener(new ActionListener() {
      public void actionPerformed (ActionEvent e) {
        if (videoHandler != null && t != null)
        {
          t.stop();
          t = null;
          startButton.setEnabled(true);
          stopButton.setEnabled(false);
          playButton.setEnabled(true);
        }
      }
    });

    // create the play movie button
    playButton = new JButton("Play Movie");
    playButton.setToolTipText("Click here to play the captured video");
    playButton.setEnabled(false);
    buttonPanel.add(playButton);
    playButton.addActionListener(new ActionListener() {
      public void actionPerformed (ActionEvent e) {
        if (videoHandler != null)
          videoHandler.playMovie();
      }
    });

    this.add(infoPanel,BorderLayout.NORTH);
    this.add(buttonPanel,BorderLayout.SOUTH);
  }

  /**
   * Method to show help
   */
  public void showHelp()
  {
    String name = null;
     try {
       // get the URL for where we loaded this class
       Class currClass = Class.forName("CaptureButtonPanel");
       URL classURL = currClass.getResource("CaptureButtonPanel.class");
       JFrame helpFrame = new JFrame("Help");
       helpFrame.setAlwaysOnTop(true);
//       name = classURL.getPath();
//       int pos = name.lastIndexOf("/");
//       name = "file:///" +
//         name.substring(1,pos) +
//            "/help/CaptureAliceMovie.html";
       URL url = new URL(classURL,"help/CaptureAliceMovie.html");
       JEditorPane pane =
         new JEditorPane(url);
       JScrollPane scrollPane = new JScrollPane(pane);
       helpFrame.setSize(new Dimension(900,800));
       helpFrame.getContentPane().add(scrollPane);
       helpFrame.setVisible(true);
     } catch (Exception ex) {
      System.out.println("I am sorry " +
       "but there was a problem with the help url: "+
                         name);
    }
  }

  ///////////////////// Main Method for Testing /////////////////////////
  public static void main (String argv[])
  {
    // create a frame
    JFrame frame = new JFrame();

    // create a ButtonPanel
    CaptureButtonPanel buttonPanel = new CaptureButtonPanel();

    // add the buttonPanel to the frame
    frame.getContentPane().add(buttonPanel);
    frame.pack(); // shrink to fit preferred size
    frame.setVisible(true); // show the frame
  }

}


