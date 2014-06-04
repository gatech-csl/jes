import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.Vector;
import javax.sound.sampled.*;
import java.lang.Math;
import java.awt.geom.*;

/**
 * This class allows you to explore a Sound.  You can see the line drawing
 * of the sound samples and play all or part of a sound.  You can zoom in to see
 * all the samples in the sound or zoom out to see the entire sound.  You
 * can click on the sound wave to see the value at that index.
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Keith McDermottt, gte047w@cc.gatech.edu
 * @author Barb Ericson ericson@cc.gatech.edu
 *
 * Modified 19 July 2007 Pamela Cutter Kalamazoo College
 *   Modified the code so that a sound would display correctly,
 *    using either a 0 or a 1 as the base.  Set the base to
 *    be 1, since that is consistent with how students work with
 *    sounds.
 *
 * Kalamazoo code merged by Buck Scharfnorth 22 May 2008
 */
public class SoundExplorer implements MouseMotionListener, ActionListener,
  MouseListener, LineListener
{
  private static final String zoomInHint =
     "Click to see all the samples (the number of samples between pixels is 1)";
  /** set to true for debugging and false for normal */
  private boolean DEBUG = false;

  ///////    main parts of the gui  /////////////////////////////

  /** the main window */
  private JFrame soundFrame;
  /** panel that contains the buttons to play all or part of a sound and show
   * selection information */
  private JPanel playPanel;
  /** scroll pane that holds the sound panel */
  private JScrollPane scrollSound;
  /** The panel that shows the sound wave */
  private JPanel soundPanel;

  //////////   general information  ////////////////////////////
  /** the sound displayed in this window */
  private SimpleSound sound;

  /**
   * Whether to display the sound in stereo - NOT neccessarily
   * whether or not the sound is in stereo
   */
  private boolean inStereo;

  /////////////////// parts of the play panel ////////////////

  /** label that shows the start index for the selection */
  private JLabel startIndexLabel;
  /** label that shows the stop index for the selection */
  private JLabel stopIndexLabel;
  /** panel that holds the play buttons */
  private JPanel buttonPanel;
  /** button to play the entire sound */
  private JButton playEntireButton;
  /** button to play the current selection */
  private JButton playSelectionButton;
  /** button to play the sound before the current index (inclusive) */
  private JButton playBeforeButton;
  /** button to play the sound after the current index (inclusive) */
  private JButton playAfterButton;
  /** button to clear the selection */
  private JButton clearSelectionButton;
  /** button to stop playing the sound */
  private JButton stopButton;

  //info related to the play panel
  private boolean selectionPrevState;


  //////////////// parts of the sound panel /////////////

  /** outer panel for left sound */
  private JPanel leftSoundPanel;
  /** outer panel for right sound (if stereo) */
  private JPanel rightSoundPanel;
  /** panel just used to center the left sample panel */
  private JPanel leftSampleWrapper;
  /** panel just used to center the right sample panel */
  private JPanel rightSampleWrapper;
  /** panel that displays the left sound wave */
  private SamplingPanel leftSamplePanel;
  /** panel that displays the right sound wave */
  private SamplingPanel rightSamplePanel;

  ////////////////  parts of the information panel //////////////

  /** the current index information panel */
  private JPanel infoPanel;
  /** the current index label */
  private JLabel indexLabel;
  /** the number of samples per pixel field */
  private JTextField numSamplesPerPixelField;
  /** text field to display the current index value */
  private JTextField indexValue;
  /** label for the left sample value */
  private JLabel leftSampleLabel;
  /** text field that shows the value for the left sample at the current index */
  private JTextField leftSampleValue;
  /** label for the right sample value */
  private JLabel rightSampleLabel;
  /** text field that shows the value for the right sample at the current index */
  private JTextField rightSampleValue;
  /** panel that holds the zoom button */
  private JPanel zoomButtonPanel;
  /** zoom in and out button */
  private JButton zoomButton;
  /** button to go to the previous index */
  private JButton prevButton;
  /** button to go to the next index */
  private JButton nextButton;
  /** button to go to the last index */
  private JButton lastButton;
  /** button to go to the first index */
  private JButton firstButton;

  //info related to the sound panel
  /** width of the displayed sound in pixels when fully zoomed out */
  private int zoomOutWidth;
  /** width of the displayed sound in pixels when fully zoomed in (framesPerPixel = 1) */
  private int zoomInWidth;
  /** current width of the sound in pixels */
  private int sampleWidth;
  /** current height of the sound in pixels */
  private int sampleHeight;
  //private int labelHeight;
  private int soundPanelHeight;

  /** number of samples (frames) (amount to add to index to get to next pixel) */
  private float framesPerPixel;
  //private int cushion;
  /** current position in pixels */
  private int currentPixelPosition;
  /** start at 0 or 1 base */
  private int base = SimpleSound._SoundIndexOffset;

  //info related to event handling
  private int mousePressed;
  private int mouseReleased;
  private int mousePressedX;
  private int mouseReleasedX;
  private boolean mouseDragged;
  private int startFrame;
  private int stopFrame;
  private int selectionStart;
  private int selectionStop;

  ///CONSTANTS///
  private static final String currentIndexText = "Current Index: ";
  private static final String startIndexText = "Start Index: ";
  private static final String stopIndexText = "Stop Index: ";
  private static final Color selectionColor = Color.gray;
  private static final Color backgroundColor = Color.black;
  private static final Color waveColor = Color.white;
  private static final Color barColor = Color.cyan;

  ///////////////////////// class fields ///////////////////////////
  private static String leftSampleText = "Sample Value: ";
  private static String rightSampleText = "Right (Bottom) Sample Value: ";

  /**
   * Constructor that takes a sound and a boolean flag
   * @param sound the sound to view
   * @param inStereo true if you want to show it in stereo
   */
  public SoundExplorer(SimpleSound sound, boolean inStereo)
  {
    this.sound = sound;
    this.inStereo = inStereo;

    if(inStereo)
      leftSampleText = "Left (Top) Sample Value: ";

    //this causes the Sound class to add this SoundExplorer
    //as the line listener for any SourceDataLines created so
    //we can monitor starting and stopping to enable/disable
    //play and stop buttons
    sound.setSoundExplorer(this);

    //used for determining difference between a mouse release
    //after a click and a mouse release after a drag.  upon dragging,
    //we want to select a region, upon clicking, only move the
    //vertical bar
    mouseDragged = false;
    selectionStart = -1;
    selectionStop = -1;

    //size of the sampling panel
    zoomOutWidth = 640;
    zoomInWidth = sound.getLengthInFrames();
    sampleWidth = zoomOutWidth;
    framesPerPixel = sound.getLengthInFrames() / sampleWidth;
    sampleHeight = 201;
    //labelHeight = 50;

    //cushion so that the sampling panel isn't flush against the
    //left side - we want a small border so it looks neater
    //cushion = 10;

    //the current pixel position
    currentPixelPosition = 0;

    //display everything
    createWindow();
  }

  /**
   * Method to print out exception information
   * @param ex the exception object
   */
  private void catchException(Exception ex)
  {
    System.err.println(ex.getMessage());
  }

  /**
   * Method to set the title on the main window
   * @param s the string to use as the title
   */
  public void setTitle(String s)
  {
    soundFrame.setTitle(s);
  }

  /**
   * Method to create the main window
   */
  private void createWindow()
  {
    String fileName = sound.getFileName();
    if(fileName==null)
      fileName = "no file name";

    soundFrame = new JFrame(fileName);

//    if(inStereo)
//    {
//      soundFrame.
//        setSize(new Dimension
//                  (zoomOutWidth+cushion,
//                   2*(sampleHeight+cushion)+labelHeight+100));
//    }
//    else
//    {
//      soundFrame.
//        setSize(new Dimension
//                  (zoomOutWidth+cushion,
//                   sampleHeight+cushion+labelHeight+100));
//    }
    // get the sound frame content pane and save it
    Container frameContainer = soundFrame.getContentPane();

    frameContainer.setLayout(new BorderLayout());
    soundFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
    //also on close we need to remove the soundView listener?

    //creates the play panel
    createPlayPanel();
    frameContainer.add(playPanel, BorderLayout.NORTH);

    //creates the sound panel
    createSoundPanel();

    //creates the scrollpane for the sound
    scrollSound = new JScrollPane();
    scrollSound.setViewportView(soundPanel);
    frameContainer.add(scrollSound, BorderLayout.CENTER);
    //scrollSound.setVerticalScrollBarPolicy
     // (JScrollPane.VERTICAL_SCROLLBAR_NEVER);
    //scrollSound.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS );

    //creates the info panel - this displays the current index
    //and sample values
    createInfoPanel();

    frameContainer.add(infoPanel, BorderLayout.SOUTH);

    // set the size based on the size of the contents
    soundFrame.pack();
    soundFrame.setResizable(false);
    soundFrame.setVisible(true);


  }//createWindow()

  /**
   * Method to create the button and add it to the passed panel
   * @param name the label for the button
   * @param enabled if true set button enabled else disable it
   * @param panel the panel to add the button to
   */
  private JButton makeButton(String name, boolean enabled, JPanel panel)
  {
    JButton j = new JButton(name);
    j.addActionListener(this);
    j.setEnabled(enabled);
    panel.add(j);
    return j;
  }

  /**
   * Method to clear the selection information
   */
  private void clearSelection()
  {
    selectionStart = -1;
    selectionStop = -1;
    startIndexLabel.setText(startIndexText + "N/A");
    stopIndexLabel.setText(stopIndexText + "N/A");
    soundFrame.getContentPane().repaint();
    playSelectionButton.setEnabled(false);
    clearSelectionButton.setEnabled(false);
  }

  /**
   * Method to create the panel that has the buttons for playing all or
   * part of the sound.  Also shows information about the selection (if one)
   */
  private void createPlayPanel()
  {

    // set up the play panel
    playPanel = new JPanel();
    //playPanel.setPreferredSize(new Dimension(zoomOutWidth, 60));
    playPanel.setLayout(new BorderLayout());

    // create the selection panel items
    JPanel selectionPanel = new JPanel();
    startIndexLabel = new JLabel(startIndexText + "N/A");
    stopIndexLabel = new JLabel(stopIndexText + "N/A");
    playSelectionButton = makeButton("Play Selection", false, selectionPanel);
    clearSelectionButton = makeButton("Clear Selection",false,selectionPanel);
    clearSelectionButton.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent e) {
        clearSelection();
      }
    });
    selectionPanel.add(startIndexLabel);
    selectionPanel.add(stopIndexLabel);

    // set up the button panel
    buttonPanel = new JPanel();
    playEntireButton = makeButton("Play Entire Sound", true, buttonPanel);
    selectionPrevState = false;
    playBeforeButton = makeButton("Play Before", false, buttonPanel);
    playAfterButton = makeButton("Play After", true, buttonPanel);
    stopButton = makeButton("Stop", false, buttonPanel);

    // add tool tip text
    playBeforeButton.setToolTipText("Play sound up to the current index");
    playAfterButton.setToolTipText("Play sound starting at the current index");
    playEntireButton.setToolTipText("Play the entire sound");
    playSelectionButton.setToolTipText("Play sound between start and stop index");
    stopButton.setToolTipText("Stop playing the sound");
    clearSelectionButton.setToolTipText("Click to clear (remove) the selection");

    // add the button panel and selection panel to the play panel
    playPanel.add(buttonPanel, BorderLayout.NORTH);
    playPanel.add(selectionPanel,BorderLayout.SOUTH);

  }//createPlayPanel()

  /**
   * Method to create the panel for displaying the sound wave(s)
   */
  private void createSoundPanel()
  {
    //the main panel, we'll add everything to this at the end
    soundPanel = new JPanel();
    if(inStereo)
      soundPanel.setLayout(new GridLayout(2,1));
    else
      soundPanel.setLayout(new GridLayout(1,1));

    /*
     do all the stuff to display the left channel.  we'll only
     make the stuff to display the right channel if neccessary.
     everything will go into the leftSoundPanel, which is then
     added to the main soundPanel
     */
    leftSoundPanel = new JPanel();
    leftSoundPanel.setLayout(new BorderLayout());
    leftSoundPanel.setPreferredSize
      //(new Dimension(sampleWidth, sampleHeight+cushion));
      (new Dimension(sampleWidth, sampleHeight));

    /*
     the sampling panel - this is where the wave form displays.
     we put it in a wrapper so that it looks centered within the
     main soundPanel
     */
    leftSampleWrapper = new JPanel();//so its centered
    leftSamplePanel = new SamplingPanel(true);
    leftSamplePanel.addMouseMotionListener(this);
    leftSamplePanel.addMouseListener(this);
    leftSampleWrapper.add(leftSamplePanel);
    leftSampleWrapper.
      //setPreferredSize(new Dimension(sampleWidth, sampleHeight+ cushion));
      setPreferredSize(new Dimension(sampleWidth, sampleHeight));

    /*
     put all the pieces into the left sound panel:
     the sample at the top, below it we want the
     current index on the left
     zoom button in the middle (unless its stereo - then the zoom button
     goes in the right sound panel)
     and current sample value on the right
     */
    leftSoundPanel.add(leftSampleWrapper, BorderLayout.NORTH);

    soundPanel.add(leftSoundPanel);

    //soundPanelHeight = sampleHeight+cushion;
    soundPanelHeight = sampleHeight;

    if(inStereo)
    {
      rightSoundPanel = new JPanel();
      rightSoundPanel.setLayout(new BorderLayout());
      rightSoundPanel.setPreferredSize
        //(new Dimension(sampleWidth, sampleHeight+cushion));
      (new Dimension(sampleWidth, sampleHeight));

      rightSampleWrapper = new JPanel();
      rightSamplePanel = new SamplingPanel(false);
      rightSamplePanel.addMouseMotionListener(this);
      rightSamplePanel.addMouseListener(this);
      rightSampleWrapper.add(rightSamplePanel);
      rightSampleWrapper.setPreferredSize
        //(new Dimension(sampleWidth, sampleHeight+cushion));
        (new Dimension(sampleWidth, sampleHeight));


      rightSoundPanel.add(rightSampleWrapper, BorderLayout.NORTH);

      soundPanel.add(rightSoundPanel);

      //soundPanelHeight = 2*(sampleHeight+cushion);
      soundPanelHeight = 2*(sampleHeight);
    }

    soundPanel.setPreferredSize(new Dimension(zoomOutWidth,soundPanelHeight));
    soundPanel.setSize(soundPanel.getPreferredSize());
  }

  /**
   * Method to update the index values to the current index position
   */
  private void updateIndexValues()
  {
    // calculate the current sample (frame) index
    int curFrame = (int)(currentPixelPosition * framesPerPixel)+base;

    // update the display of the current sample (frame) index
    indexValue.setText(Integer.toString(curFrame));

    // update the number of samples per (between) pixels field
    if (numSamplesPerPixelField != null)
      numSamplesPerPixelField.setText(Integer.toString((int) framesPerPixel));

    // try to update the value(s) at the current sample index
    try
    {
      leftSampleValue.setText(Integer.toString(sound.getLeftSample(curFrame-base)));
      if(inStereo)
        rightSampleValue.setText(Integer.toString(sound.getRightSample(curFrame-base)));
    }
    catch(Exception ex)
    {
      catchException(ex);
    }
  }

  /**
   * Method to set up the index panel.  This panel has buttons for going to
   * the first index, previous index, the current index label, the current index
   * value or values (if in stereo), next index button, and a last index button
   * @param indexPanel the panel to set-up
   */
  private void setUpIndexPanel(JPanel indexPanel)
  {
    JPanel topPanel = new JPanel();
    Box vertBox = Box.createVerticalBox();

     // create the image icons for the buttons
    Icon prevIcon = new ImageIcon(SoundExplorer.class.getResource("leftArrow.gif"),
                                  "previous index");
    Icon nextIcon = new ImageIcon(SoundExplorer.class.getResource("rightArrow.gif"),
                                  "next index");
    Icon firstIcon = new ImageIcon(SoundExplorer.class.getResource("endLeft.gif"),
                                   "first index");
    Icon lastIcon = new ImageIcon(SoundExplorer.class.getResource("endRight.gif"),
                                  "last index");

    // create the arrow buttons
    prevButton = new JButton(prevIcon);
    firstButton = new JButton(firstIcon);
    nextButton = new JButton(nextIcon);
    lastButton = new JButton(lastIcon);

    // set the tool tip text
    prevButton.setToolTipText("Click to view previous index (sample at previous pixel)");
    firstButton.setToolTipText("Click to view first index (sample at first pixel)");
    nextButton.setToolTipText("Click to view next index (sample at next pixel)");
    lastButton.setToolTipText("Click to view last index (sample at last pixel)");

    // set the preferred sizes of the buttons
    prevButton.setPreferredSize(new Dimension(prevIcon.getIconWidth() + 2,
                                              prevIcon.getIconHeight() + 2));
    firstButton.setPreferredSize(new Dimension(firstIcon.getIconWidth() + 2,
                                               firstIcon.getIconHeight() + 2));
    nextButton.setPreferredSize(new Dimension(nextIcon.getIconWidth() + 2,
                                              nextIcon.getIconHeight() + 2));
    lastButton.setPreferredSize(new Dimension(lastIcon.getIconWidth() + 2,
                                               lastIcon.getIconHeight() + 2));


    // handle previous button press
    prevButton.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent evt) {
        currentPixelPosition--;
        if (currentPixelPosition < 0)
          currentPixelPosition = 0;
        updateIndexValues();
        checkScroll();
        soundFrame.getContentPane().repaint();
      }
    });

    // handle next button press
    nextButton.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent evt) {
        currentPixelPosition++;
        if (currentPixelPosition * framesPerPixel >= sound.getNumSamples())
          currentPixelPosition = (int) ((sound.getNumSamples() - 1) / framesPerPixel);
        updateIndexValues();
        checkScroll();
        soundFrame.getContentPane().repaint();
      }
    });

    // handle first button press
    firstButton.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent evt) {
        currentPixelPosition = 0;
        updateIndexValues();
        checkScroll();
        soundFrame.getContentPane().repaint();
      }
    });

    // handle last button press
    lastButton.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent evt) {
        currentPixelPosition = (int) ((sound.getNumSamples() - 1) / framesPerPixel);
        updateIndexValues();
        checkScroll();
        soundFrame.getContentPane().repaint();
      }
    });

    // create the index value textfield
    indexValue = new JTextField(Integer.toString(base),8);
    indexValue.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent e) {

        // zoom in around user entered value
        handleZoomIn(Integer.parseInt(indexValue.getText()));

        // update the values for the pixel at the current index
        updateIndexValues();
      }
    });

    // create the left sample value and right sample value textfields
    leftSampleValue = new JTextField(8);
    leftSampleValue.setEditable(false);
    rightSampleValue = new JTextField(8);
    rightSampleValue.setEditable(false);

    // create the labels
    indexLabel = new JLabel(currentIndexText);
    leftSampleLabel = new JLabel(leftSampleText);
    rightSampleLabel = new JLabel(rightSampleText);
    updateIndexValues();

    // add the buttons and label to the top panel
    topPanel.add(firstButton);
    topPanel.add(prevButton);
    topPanel.add(indexLabel);
    topPanel.add(indexValue);
    topPanel.add(leftSampleLabel);
    topPanel.add(leftSampleValue);
    if (inStereo) {
      topPanel.add(rightSampleLabel);
      topPanel.add(rightSampleValue);
    }
    topPanel.add(nextButton);
    topPanel.add(lastButton);

    // create bottom panel
    JPanel bottomPanel = new JPanel();
    bottomPanel.add(new JLabel("The number of samples between pixels: "));
    numSamplesPerPixelField = new JTextField(Integer.toString((int) framesPerPixel),8);
    numSamplesPerPixelField.setToolTipText("Click here to zoom in (decrease) or out (increase))");
    numSamplesPerPixelField.addActionListener(new ActionListener() {
      public void actionPerformed(ActionEvent e) {

        // zoom in around user entered value
        handleFramesPerPixel(Integer.parseInt(numSamplesPerPixelField.getText()));

        // update the values for the pixel at the current index
        updateIndexValues();
      }
    });
    bottomPanel.add(numSamplesPerPixelField);


    // add the top panel to the box
    vertBox.add(topPanel);
    vertBox.add(bottomPanel);

    // add the vertical box to the index panel
    indexPanel.add(vertBox);

  }

  /**
   * Method to create the information panel which holds the index information, the value
   * for the current index, and the zoom button
   */
  private void createInfoPanel()
  {
    // create the information panel and set the layout
    infoPanel = new JPanel();
    infoPanel.setLayout(new BorderLayout());

    // create the index panel and set it up
    JPanel indexPanel = new JPanel();
    indexPanel.setLayout(new FlowLayout());
    setUpIndexPanel(indexPanel);

    // create a zoom panel with a zoom button
    zoomButtonPanel = new JPanel();
    zoomButton = makeButton("Zoom In", true, zoomButtonPanel);
    zoomButton.setToolTipText(zoomInHint);

    infoPanel.add(BorderLayout.NORTH,indexPanel);
    infoPanel.add(BorderLayout.SOUTH,zoomButtonPanel);

  }

  /**
   * Handle a mouse click event
   * @param e the mouse event
   */
  public void mouseClicked(MouseEvent e)
  {
    currentPixelPosition = e.getX();

    if(currentPixelPosition==0)
    {
      playBeforeButton.setEnabled(false);
      playAfterButton.setEnabled(true);
    }
    else if(currentPixelPosition < sampleWidth)
    {
      playBeforeButton.setEnabled(true);
      playAfterButton.setEnabled(true);
    }
    else if(currentPixelPosition == sampleWidth)
    {
      playBeforeButton.setEnabled(true);
      playAfterButton.setEnabled(false);
    }

    if(DEBUG)
      System.out.println("mouse click:  " + currentPixelPosition);

    updateIndexValues();
    soundPanel.repaint();
  }

  /**
   * Method to handle a mouse press
   * @param e the mouse event
   */
  public void mousePressed(MouseEvent e)
  {
    mousePressedX = e.getX();
  }

  /**
   * Method to handle a mouse release
   * @param e the mouse event
   */
  public void mouseReleased(MouseEvent e)
  {
    mouseReleasedX = e.getX();

    if(mouseDragged)
    {

      mousePressed = mousePressedX;
      mouseReleased = mouseReleasedX;

      if (mousePressed > mouseReleased)//selected right to left
      {
        int temp = mousePressed;
        mousePressed = mouseReleased;
        mouseReleased = temp;
      }

      startFrame = (int)(mousePressed * framesPerPixel);
      stopFrame = (int)(mouseReleased * framesPerPixel);

      //stopped dragging outside the window.
      if(stopFrame >= sound.getLengthInFrames())
        stopFrame = sound.getLengthInFrames();

      //stopped dragging outside the window
      if(startFrame < 0)
        startFrame = 0;

      //new values for the labels
      startIndexLabel.setText(startIndexText + (startFrame));
      stopIndexLabel.setText(stopIndexText + (stopFrame));

      //for highlighting the selection
      selectionStart = mousePressed;
      selectionStop = mouseReleased;

      soundPanel.repaint();
      playSelectionButton.setEnabled(true);
      clearSelectionButton.setEnabled(true);
      mouseDragged = false;
    }

  }

  /**
   * Method to handle a mouse entered event
   * @param e the mouse event
   */
  public void mouseEntered(MouseEvent e)
  {}

  /**
   * Method to handle a mouse exited event
   * @param e the mouse event
   */
  public void mouseExited(MouseEvent e)
  {}

  /**
   * Method to handle a mouse dragged event
   * @param e the mouse event
   */
  public void mouseDragged(MouseEvent e)
  {
    mouseDragged = true;

    //highlight the selection as we drag by pretending
    //that we're releasing the mouse at each point
    mouseReleased(e);
  }

  /**
   * Method to handle a mouse move event
   * @param e the mouse event
   */
  public void mouseMoved(MouseEvent e)
  {}

  /**
   * Method to handle the line event update
   * @param e the line event
   */
  public void update(LineEvent e)
  {
    if(e.getType().equals(LineEvent.Type.OPEN))
    {
      playEntireButton.setEnabled(false);
      playBeforeButton.setEnabled(false);
      playAfterButton.setEnabled(false);
      selectionPrevState = playSelectionButton.isEnabled();
      playSelectionButton.setEnabled(false);
      clearSelectionButton.setEnabled(false);
      stopButton.setEnabled(true);
    }
    if(e.getType().equals(LineEvent.Type.CLOSE))
    {
      playEntireButton.setEnabled(true);
      playSelectionButton.setEnabled(selectionPrevState);
      clearSelectionButton.setEnabled(selectionPrevState);
      stopButton.setEnabled(false);
      if(currentPixelPosition==0)
      {
        playBeforeButton.setEnabled(false);
        playAfterButton.setEnabled(true);
      }
      else if(currentPixelPosition < sampleWidth)
      {
        playBeforeButton.setEnabled(true);
        playAfterButton.setEnabled(true);
      }
      else if(currentPixelPosition == sampleWidth)
      {
        playBeforeButton.setEnabled(true);
        playAfterButton.setEnabled(false);
      }
    }

  }

  /**
   * Method to handle an action event
   * @param e the action event
   */
  public void actionPerformed(ActionEvent e)
  {
    if(e.getActionCommand() == "Play Entire Sound")
    {
      try
      {
        sound.play();
      }
      catch(Exception ex)
      {
        catchException(ex);
      }
    }
    else if(e.getActionCommand() == "Play Selection")
    {
      try
      {
        sound.playAtRateInRange(1, startFrame, stopFrame);
      }
      catch(Exception ex)
      {
        catchException(ex);
      }
    }
    else if(e.getActionCommand().equals("Stop"))
    {
      //stop all playback threads related to this sound
      for(int i = 0; i < sound.getPlaybacks().size(); i++)
      {
        ((Playback)sound.getPlaybacks().elementAt(i))
          .stopPlaying();
      }
    }
    else if(e.getActionCommand().equals("Zoom In"))
    {
      handleZoomIn(true);
    }
    else if (e.getActionCommand().equals("Zoom Out"))
    {
      handleZoomOut();
    }
    else if(e.getActionCommand().equals("Play Before"))
    {
      try
      {
        sound.playAtRateInRange
          (1, 0, (int)(currentPixelPosition * framesPerPixel));
      }
      catch(Exception ex)
      {
        catchException(ex);
      }
    }
    else if(e.getActionCommand().equals("Play After"))
    {
      try
      {
        sound.playAtRateInRange
          (1, (int)(currentPixelPosition*framesPerPixel),
           sound.getLengthInFrames()-1);
      }
      catch(Exception ex)
      {
        catchException(ex);
      }
    }
    else
    {
     // System.err.println("command not defined: " +
     //                    e.getActionCommand());
    }

  }

  /**
   * Method to check that the current position is in the viewing area and if
   * not scroll to center the current position if possible
   */
  public void checkScroll()
  {
    // only do this if we are not zoomed out
    if (sampleWidth != zoomOutWidth) {

      // get the rectangle that defines the current view
      JViewport viewport = scrollSound.getViewport();
      Rectangle rect = viewport.getViewRect();
      int rectMinX = (int) rect.getX();
      int rectWidth = (int) rect.getWidth();
      int rectMaxX = rectMinX + rectWidth - 1;

      // get the maximum possible index
      int maxIndex = sound.getLength() - rectWidth - 1;

      // check if current position is outside viewing area
      if (currentPixelPosition < rectMinX ||
          currentPixelPosition > rectMaxX) {

        // calculate how to position the current position in the middle of the viewing
        // area
        int barXPos = currentPixelPosition - (int) (rectWidth / 2);
        int barYPos = (int) (sampleHeight - rect.getHeight()) / 2;

        // check if the barPos is less than 0 or greater than max
        if (barXPos < 0)
          barXPos = 0;
        else if (barXPos > maxIndex)
          barXPos = maxIndex;

        // move the viewport upper left point
        viewport.setViewPosition(new Point(barXPos, barYPos));
      }
    }
  }

  /**
   * Method to handle a zoom in
   */
  private void handleZoomIn(boolean checkScrollFlag)
  {
    // change the zoom button to zoom out information
    zoomButton.setText("Zoom Out");
    zoomButton.setToolTipText("Click to zoom out (see the whole sound)");

    // get the frame index current position, selection start and stop
    currentPixelPosition = (int)(currentPixelPosition*framesPerPixel);
    selectionStart = (int)(selectionStart*framesPerPixel);
    selectionStop = (int)(selectionStop*framesPerPixel);

    if(DEBUG)
      System.out.println("Zoom In:  currentPixelPosition = " +
                         currentPixelPosition);

    sampleWidth = zoomInWidth;
    framesPerPixel = sound.getLengthInFrames() / sampleWidth;

    soundPanel.setPreferredSize(new Dimension(zoomInWidth,
                                              soundPanel.getHeight()));
    soundPanel.setSize(soundPanel.getPreferredSize());

    leftSoundPanel.setPreferredSize(new Dimension(zoomInWidth,
                                                  leftSoundPanel.getHeight()));
    leftSoundPanel.setSize(leftSoundPanel.getPreferredSize());

    leftSampleWrapper.setPreferredSize(new Dimension(zoomInWidth,
                                                     leftSampleWrapper.getHeight()));
    leftSampleWrapper.setSize(leftSampleWrapper.getPreferredSize());
    leftSamplePanel.setPreferredSize(new Dimension(sampleWidth,
                                                   sampleHeight));
    leftSamplePanel.setSize(leftSamplePanel.getPreferredSize());

    leftSamplePanel.createWaveForm(true);

    if(inStereo)
    {
      rightSoundPanel.setPreferredSize
        (new Dimension(zoomInWidth,
                       rightSoundPanel.getHeight()));
      rightSoundPanel.setSize
        (rightSoundPanel.getPreferredSize());

      rightSampleWrapper.setPreferredSize
        (new Dimension(zoomInWidth,
                       rightSampleWrapper.getHeight()));
      rightSampleWrapper.setSize
        (rightSampleWrapper.getPreferredSize());

      rightSamplePanel.setPreferredSize
        (new Dimension(zoomInWidth,
                       rightSamplePanel.getHeight()));
      rightSamplePanel.setSize
        (rightSamplePanel.getPreferredSize());

      rightSamplePanel.createWaveForm(false);
    }
    if(DEBUG)
    {
      System.out.println("ZOOM IN SIZES:");
      System.out.println("\tleftSamplePanel: " +
                         leftSamplePanel.getSize());
      System.out.println("\t\tpreferred: " +
                         leftSamplePanel.getPreferredSize());

      System.out.println("\tleftSampleWrapper: " +
                         leftSampleWrapper.getSize());
      System.out.println("\t\tpreferred: " +
                         leftSampleWrapper.getPreferredSize());

      System.out.println("\tleftSoundPanel: " +
                         leftSoundPanel.getSize());
      System.out.println("\t\tpreferred: " +
                         leftSoundPanel.getPreferredSize());

      System.out.println("\tsoundPanel: " +
                         soundPanel.getSize());
      System.out.println("\t\tpreferred: " +
                         soundPanel.getPreferredSize());
    }

    // revalidate to handle the new preferred sizes
    scrollSound.revalidate();

    // update the index values
    updateIndexValues();

    // check for the need to scroll
    if (checkScrollFlag)
       checkScroll();
  }

  /**
   * Method to handle a zoom in to view all sample values
   * @param index the index to use after the zoom in
   */
  private void handleZoomIn(int index)
  {
    if (index % framesPerPixel != 0) {
       // do normal zoom in on current position
       handleZoomIn(false);
    }

    // change current position to the passed index
    currentPixelPosition = (int) (index / framesPerPixel)-base;

    // now check the scroll
    checkScroll();

    // repaint
    soundPanel.repaint();

  }

  /**
   * Method to handle a zoom out to view the entire sound wave
   */
  private void handleZoomOut()
  {
    zoomButton.setText("Zoom In");
    zoomButton.setToolTipText(zoomInHint);

    sampleWidth = zoomOutWidth;
    framesPerPixel = sound.getLengthInFrames() / sampleWidth;

    int divisor = (sound.getLengthInFrames()/sampleWidth);
    currentPixelPosition = (int)(currentPixelPosition/divisor);
    selectionStart = (int)(selectionStart/divisor);
    selectionStop = (int)(selectionStop/divisor);

    if(DEBUG)
      System.out.println("Zoom Out:  currentPixelPosition = " +
                         currentPixelPosition);

    soundPanel.setPreferredSize
      (new Dimension(zoomOutWidth,
                     soundPanel.getHeight()));
    soundPanel.setSize(soundPanel.getPreferredSize());

    leftSoundPanel.setPreferredSize
      (new Dimension(zoomOutWidth,
                     leftSoundPanel.getHeight()));
    leftSoundPanel.setSize(leftSoundPanel.getPreferredSize());

    leftSampleWrapper.setPreferredSize
      (new Dimension(zoomOutWidth,
                     leftSampleWrapper.getHeight()));
    leftSampleWrapper.setSize
      (leftSampleWrapper.getPreferredSize());

    leftSamplePanel.setPreferredSize
      (new Dimension(sampleWidth, sampleHeight));
    leftSamplePanel.setSize(leftSamplePanel.getPreferredSize());

    leftSamplePanel.createWaveForm(true);

    if(inStereo)
    {
      rightSoundPanel.
        setPreferredSize
        (new Dimension(zoomOutWidth,
                       rightSoundPanel.getHeight()));
      rightSoundPanel.setSize
        (rightSoundPanel.getPreferredSize());

      rightSampleWrapper.setPreferredSize
        (new Dimension(zoomOutWidth,
                       rightSampleWrapper.getHeight()));
      rightSampleWrapper.setSize
        (rightSampleWrapper.getPreferredSize());

      rightSamplePanel.setPreferredSize
        (new Dimension(sampleWidth, sampleHeight));
      rightSamplePanel.setSize
        (rightSamplePanel.getPreferredSize());

      rightSamplePanel.createWaveForm(false);
    }

    updateIndexValues();

    soundPanel.repaint();
  }

  /**
   * Method to handle an entry of the desired number of frames (samples)
   * shown per pixel
   * @param numFrames (the number of samples shown in a pixel)
   */
  private void handleFramesPerPixel(int numFrames)
  {

    // get the current index from the pixel position and frames per pixel
    int currIndex = (int) (currentPixelPosition * framesPerPixel);
    sampleWidth = sound.getLengthInFrames() / numFrames;
    framesPerPixel = numFrames;

    int divisor = (sound.getLengthInFrames()/sampleWidth);
    currentPixelPosition = (int)(currIndex/divisor); // new curr pixel
    selectionStart = (int)(selectionStart/divisor);
    selectionStop = (int)(selectionStop/divisor);

    soundPanel.setPreferredSize
      (new Dimension(sampleWidth,
                     soundPanel.getHeight()));
    soundPanel.setSize(soundPanel.getPreferredSize());

    leftSoundPanel.setPreferredSize
      (new Dimension(sampleWidth,
                     leftSoundPanel.getHeight()));
    leftSoundPanel.setSize(leftSoundPanel.getPreferredSize());

    leftSampleWrapper.setPreferredSize
      (new Dimension(sampleWidth,
                     leftSampleWrapper.getHeight()));
    leftSampleWrapper.setSize
      (leftSampleWrapper.getPreferredSize());

    leftSamplePanel.setPreferredSize
      (new Dimension(sampleWidth, sampleHeight));
    leftSamplePanel.setSize(leftSamplePanel.getPreferredSize());

    leftSamplePanel.createWaveForm(true);

    if(inStereo)
    {
      rightSoundPanel.
        setPreferredSize
        (new Dimension(sampleWidth,
                       rightSoundPanel.getHeight()));
      rightSoundPanel.setSize
        (rightSoundPanel.getPreferredSize());

      rightSampleWrapper.setPreferredSize
        (new Dimension(sampleWidth,
                       rightSampleWrapper.getHeight()));
      rightSampleWrapper.setSize
        (rightSampleWrapper.getPreferredSize());

      rightSamplePanel.setPreferredSize
        (new Dimension(sampleWidth, sampleHeight));
      rightSamplePanel.setSize
        (rightSamplePanel.getPreferredSize());

      rightSamplePanel.createWaveForm(false);
    }

    // revalidate to handle the new preferred sizes
    scrollSound.revalidate();

    // update the index values
    updateIndexValues();

    // check for the need to scroll
    checkScroll();

    soundPanel.repaint();
  }

  /**
   * Method to set the base for the index.  The default is a base of 0.
   * @param base the new base to use (for example use setBase(1))
   * to use base 1 instead of 0
   */
  public void setBase(int base)
  {
    this.base = base;
  }

  /**
   * Class to display the sound wave
   */
  private class SamplingPanel extends JPanel
  {

    private boolean forLeftSample;
    private Vector<Point2D.Float> points;
    private static final long serialVersionUID = 7526471155622776147L;

    /**
     * Constructor that takes a flag to tell if for left or right sample
     * @param inputForLeftSample if true = left if false = right
     */
    public SamplingPanel(boolean inputForLeftSample)
    {
      forLeftSample = inputForLeftSample;

      if(DEBUG)
        System.out.println("creating new sampling panel: " +
                           "\n\tfor left sample: "+forLeftSample +
                           "\n\tsampleWidth: " + sampleWidth +
                           "\n\tsampleHeight: " + sampleHeight);

      setBackground(backgroundColor);
      setPreferredSize(new Dimension(sampleWidth, sampleHeight));
      setSize(getPreferredSize());
      if(DEBUG)
        System.out.println("\tSample panel preferred size: " +
                           getPreferredSize() + "\n\tSample panel size: " + getSize());

      points = new Vector<Point2D.Float>();
      createWaveForm(forLeftSample);
    }//constructor(forLeftSample)

    /**
     * Method to create the sound wave
     * @param forLeftSample if true create the left form, if false the right
     */
    public void createWaveForm(boolean forLeftSample)
    {

      //get the max y value for a sound of this sample size
      AudioFormat format = sound.getAudioFileFormat().getFormat();
      float maxValue;

      if(format.getSampleSizeInBits() == 8)
      {
        maxValue = (float)Math.pow(2,7);
      }
      else if(format.getSampleSizeInBits() == 16)
      {
        maxValue = (float)Math.pow(2, 15);
      }
      else if(format.getSampleSizeInBits() == 24)
      {
        maxValue = (float)Math.pow(2, 23);
      }
      else if(format.getSampleSizeInBits() == 32)
      {
        maxValue = (float)Math.pow(2, 31);
      }
      else
      {
        try
        {
          sound.printError("InvalidSampleSize");
        }
        catch(Exception ex)
        {
          catchException(ex);
        }
        return;
      }

      points.clear();
      //framesPerPixel = sound.getLengthInFrames() / sampleWidth;
      for(int pixel = 0; pixel<sampleWidth; pixel++)
      {
        float y;
        float sampleValue;


        if(forLeftSample)
        {
          try
          {
            sampleValue = sound.
              getLeftSample((int)(pixel*framesPerPixel));
          }
          catch(Exception ex)
          {
            catchException(ex);
            return;
          }
        }
        else
        {
          try
          {
            sampleValue = sound.
              getRightSample((int)(pixel*framesPerPixel));
          }
          catch(Exception ex)
          {
            catchException(ex);
            return;
          }
        }

        y = ((float)Math.floor(sampleHeight/2) -
             (sampleValue  * ((float)Math.floor(sampleHeight/2) /
                              maxValue)));

        points.add(new Point2D.Float(pixel, y));
      }//for - collecting points

      if(DEBUG)
        System.out.println("number of points: " + points.size());
      repaint();

    }//createWaveForm()


    /**
     * Method to draw the Sampling Panel
     * @param g the graphics context
     */
    public void paintComponent(Graphics g)
    {
      Rectangle rectToPaint = g.getClipBounds();

      if(DEBUG)
      {
        System.out.println("Repainting: " + rectToPaint);
        System.out.println("\tSampleWidth: " + sampleWidth);
        System.out.println("\tframesPerPixel: " + framesPerPixel);
        System.out.println("\tSample panel size: " + getSize());
        System.out.println("\tSamplePanel Width: " + getWidth());
        System.out.println("\tSamplePanel Height: " + getHeight());
      }

      //clear out the image
      Graphics2D g2 = (Graphics2D)g;
      g2.setBackground(backgroundColor);
      g2.clearRect((int)rectToPaint.getX(), (int)rectToPaint.getY(),
                   (int)rectToPaint.getWidth(), (int)rectToPaint.getHeight());

      //draw the selection if it exists
      if(selectionStart!=-1 && selectionStop!=-1)
      {
        g2.setBackground(selectionColor);
        g2.clearRect(selectionStart, 0,
                     selectionStop-selectionStart+1, sampleHeight);
      }

      //draw the lines
      g2.setColor(waveColor);
      for(int i = (int)rectToPaint.getX();
          i < (rectToPaint.getX() + rectToPaint.getWidth() -1); i++)
      {
        g2.draw(new
                  Line2D.Float((Point2D.Float)points.elementAt(i),
                               (Point2D.Float)points.elementAt(i+1)));
      }

      //draw the center line
      g2.setColor(barColor);
      g2.setStroke(new BasicStroke(1));
      g2.draw(new Line2D.Double(rectToPaint.getX(),
                                Math.floor(sampleHeight/2),
                                rectToPaint.getX()+rectToPaint.getWidth()-1,
                                Math.floor(sampleHeight/2)));

      //draw the current position
      if (rectToPaint.getX()<currentPixelPosition &&
          currentPixelPosition<(rectToPaint.getX()+rectToPaint.getWidth()-1))
      {
        g2.setColor(barColor);
        g2.setStroke(new BasicStroke(1));
        g2.draw(new Line2D.Double(currentPixelPosition, 0,
                                  currentPixelPosition, sampleHeight));
      }
    }//paint(g)

  }//public class SamplingPanel

  /*
  public static void main(String args[])
  {
    try{
      /*
       Sound s = new Sound("/Users/ellie/mediacomp/ellie/really_long_sound.wav");
       SoundExplorer test = new SoundExplorer(s, s.isStereo());
       */


      //Sound s2 = new Sound("/Users/ellie/mediacomp/ellie/SoundDemo/audio/22-new.aif");

      //  SoundExplorer teststereo = new SoundExplorer(s2, true);
      //SoundExplorer testmono = new SoundExplorer(s2, false);

      /*

      Sound windowsSound = new Sound("/Users/ellie/Desktop/sound2.wav");
      SoundExplorer testWin = new SoundExplorer(windowsSound, false);

      Sound shaggz =
        new Sound("/Users/ellie/Desktop/audio2/SOUND1.WAV");
      System.out.println(shaggz.getAudioFileFormat().getFormat());

      shaggz.blockingPlay();

      SoundExplorer shaggzView = new SoundExplorer(shaggz, false);

      Sound shaggz2 =
        new Sound("/Users/ellie/Desktop/audio2/SOUND1.WAV");
      for(int i = 0; i < shaggz2.getLengthInFrames(); i++)
      {
        shaggz2.setSampleValue(i, shaggz2.getSampleValue(i));
      }
      SoundExplorer shaggzView2 = new SoundExplorer(shaggz2, false);

      /*
       Sound emptySound = new Sound(5);
       SoundExplorer testempty = new SoundExplorer(emptySound, false);
       */
      /*
       Sound sStates = new Sound("Z:\\croak.wav");
       SoundExplorer testStates = new SoundExplorer(sStates, sStates.isStereo());
       */
   /* }
    catch(Exception ex)
    {
      System.out.println(ex.getMessage());
    }

  } */
}//end class SoundExplorer
