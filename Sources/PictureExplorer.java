
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.awt.image.*;
import javax.swing.border.*;
/**
 * Displays a picture and lets you explore the picture by displaying the x, y, red,
 * green, and blue values of the pixel at the cursor when you click a mouse button or
 * press and hold a mouse button while moving the cursor.  It also lets you zoom in or
 * out.  You can also type in a x and y value to see the color at that location.
 * <br>
 * Originally created for the Jython Environment for Students (JES).
 * <br>
 * Modified to work with DrJava by Barbara Ericson
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Keith McDermottt, gte047w@cc.gatech.edu
 * @author Barb Ericson ericson@cc.gatech.edu
 *
 * Modified 19 July 2007 Pamela Cutter Kalamazoo College
 *    Set the base to be 1 instead of 0 to be consistent with
 *     pictures in JES.
 *
 * Kalamazoo update merged by Buck Scharfnorth 22 May 2008
 *
 * Changed base to use the value SimplePicture._PictureIndexOffset (29 Oct 2008) -Buck
 *
 * May 28 2009: Removed unused changeToBaseOne method. -Buck
 */
public class PictureExplorer implements MouseMotionListener, ActionListener, MouseListener
{

 // current x and y index
 private int xIndex = 0;
 private int yIndex = 0;

 //Main gui variables
 private JFrame pictureFrame;
 private JScrollPane scrollPane;

 //information bar variables
 private JLabel xLabel;
 private JButton xPrevButton;
 private JButton yPrevButton;
 private JButton xNextButton;
 private JButton yNextButton;
 private JLabel yLabel;
 private JTextField xValue;
 private JTextField yValue;
 private JLabel rValue;
 private JLabel gValue;
 private JLabel bValue;
 private JLabel colorLabel;
 private JPanel colorPanel;

 // menu components
 private JMenuBar menuBar;
 private JMenu zoomMenu;
 private JMenuItem twentyFive;
 private JMenuItem fifty;
 private JMenuItem seventyFive;
 private JMenuItem hundred;
 private JMenuItem hundredFifty;
 private JMenuItem twoHundred;
 private JMenuItem fiveHundred;

 /** The picture being explored */
 private DigitalPicture picture;

 /** The image icon used to display the picture */
 private ImageIcon scrollImageIcon;

 /** The image display */
 private ImageDisplay imageDisplay;

 /** the zoom factor (amount to zoom) */
 private double zoomFactor;

 /** the number system to use, 0 means starting at 0, 1 means starting at 1 */
 private int numberBase = SimplePicture._PictureIndexOffset;

 /**
  * Constructor that takes a picure to be explored
  * @param picture the picture to explore
  */
 public PictureExplorer(DigitalPicture picture)
 {
   // set the fields
   this.picture=picture;
   zoomFactor=1;

   // create the window and set things up
   createWindow();
 }

 /**
  * Set the title of the frame
  * @param title the title to use in the JFrame
  */
 public void setTitle(String title)
 {
   pictureFrame.setTitle(title);
 }

 /**
  * Method to create and initialize the picture frame
  */
 private void createAndInitPictureFrame()
 {
   pictureFrame = new JFrame(); // create the JFrame
   pictureFrame.setResizable(true);  // allow the user to resize it
   pictureFrame.getContentPane().setLayout(new BorderLayout()); // use border layout
   pictureFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE); // when close stop
   pictureFrame.setTitle(picture.getTitle());
   PictureExplorerFocusTraversalPolicy newPolicy = new PictureExplorerFocusTraversalPolicy();
   pictureFrame.setFocusTraversalPolicy(newPolicy);

 }

 /**
  * Method to create the menu bar, menus, and menu items
  */
 private void setUpMenuBar()
 {
   //create menu
   menuBar = new JMenuBar();
   zoomMenu = new JMenu("Zoom");
   twentyFive = new JMenuItem("25%");
   fifty = new JMenuItem("50%");
   seventyFive = new JMenuItem("75%");
   hundred = new JMenuItem("100%");
   hundred.setEnabled(false);
   hundredFifty = new JMenuItem("150%");
   twoHundred = new JMenuItem("200%");
   fiveHundred = new JMenuItem("500%");

   // add the action listeners
   twentyFive.addActionListener(this);
   fifty.addActionListener(this);
   seventyFive.addActionListener(this);
   hundred.addActionListener(this);
   hundredFifty.addActionListener(this);
   twoHundred.addActionListener(this);
   fiveHundred.addActionListener(this);

   // add the menu items to the menus
   zoomMenu.add(twentyFive);
   zoomMenu.add(fifty);
   zoomMenu.add(seventyFive);
   zoomMenu.add(hundred);
   zoomMenu.add(hundredFifty);
   zoomMenu.add(twoHundred);
   zoomMenu.add(fiveHundred);
   menuBar.add(zoomMenu);

   // set the menu bar to this menu
   pictureFrame.setJMenuBar(menuBar);
 }

 /**
  * Create and initialize the scrolling image
  */
 private void createAndInitScrollingImage()
 {
   scrollPane = new JScrollPane();

   BufferedImage bimg = picture.getBufferedImage();
   imageDisplay = new ImageDisplay(bimg);
   imageDisplay.addMouseMotionListener(this);
   imageDisplay.addMouseListener(this);
   imageDisplay.setToolTipText("Click a mouse button on a pixel to see the pixel information");
   scrollPane.setViewportView(imageDisplay);
   pictureFrame.getContentPane().add(scrollPane, BorderLayout.CENTER);
 }

 /**
  * Creates the JFrame and sets everything up
  */
 private void createWindow()
 {
   // create the picture frame and initialize it
   createAndInitPictureFrame();

   // set up the menu bar
   setUpMenuBar();

   //create the information panel
   createInfoPanel();

   //creates the scrollpane for the picture
   createAndInitScrollingImage();

   // show the picture in the frame at the size it needs to be
   pictureFrame.pack();
   pictureFrame.setVisible(true);
 }

 /**
  * Method to set up the next and previous buttons for the
  * pixel location information
  */
 private void setUpNextAndPreviousButtons()
 {
   // create the image icons for the buttons
   Icon prevIcon = new ImageIcon(SoundExplorer.class.getResource("leftArrow.gif"),
                                 "previous index");
   Icon nextIcon = new ImageIcon(SoundExplorer.class.getResource("rightArrow.gif"),
                                 "next index");
   // create the arrow buttons
   xPrevButton = new JButton(prevIcon);
   xNextButton = new JButton(nextIcon);
   yPrevButton = new JButton(prevIcon);
   yNextButton = new JButton(nextIcon);

   // set the tool tip text
   xNextButton.setToolTipText("Click to go to the next x value");
   xPrevButton.setToolTipText("Click to go to the previous x value");
   yNextButton.setToolTipText("Click to go to the next y value");
   yPrevButton.setToolTipText("Click to go to the previous y value");

   // set the sizes of the buttons
   int prevWidth = prevIcon.getIconWidth() + 2;
   int nextWidth = nextIcon.getIconWidth() + 2;
   int prevHeight = prevIcon.getIconHeight() + 2;
   int nextHeight = nextIcon.getIconHeight() + 2;
   Dimension prevDimension = new Dimension(prevWidth,prevHeight);
   Dimension nextDimension = new Dimension(nextWidth, nextHeight);
   xPrevButton.setPreferredSize(prevDimension);
   yPrevButton.setPreferredSize(prevDimension);
   xNextButton.setPreferredSize(nextDimension);
   yNextButton.setPreferredSize(nextDimension);

   // handle previous x button press
   xPrevButton.addActionListener(new ActionListener() {
     public void actionPerformed(ActionEvent evt) {
       xIndex--;
       if (xIndex < 0)
         xIndex = 0;
       displayPixelInformation(xIndex,yIndex);
     }
   });

   // handle previous y button press
   yPrevButton.addActionListener(new ActionListener() {
     public void actionPerformed(ActionEvent evt) {
       yIndex--;
       if (yIndex < 0)
         yIndex = 0;
       displayPixelInformation(xIndex,yIndex);
     }
   });

   // handle next x button press
   xNextButton.addActionListener(new ActionListener() {
     public void actionPerformed(ActionEvent evt) {
       xIndex++;
       if (xIndex >= picture.getWidth())
         xIndex = picture.getWidth() - 1;
       displayPixelInformation(xIndex,yIndex);
     }
   });

   // handle next y button press
   yNextButton.addActionListener(new ActionListener() {
     public void actionPerformed(ActionEvent evt) {
       yIndex++;
       if (yIndex >= picture.getHeight())
         yIndex = picture.getHeight() - 1;
       displayPixelInformation(xIndex,yIndex);
     }
   });
 }

 /**
  * Create the pixel location panel
  * @param labelFont the font for the labels
  * @return the location panel
  */
 public JPanel createLocationPanel(Font labelFont) {

   // create a location panel
   JPanel locationPanel = new JPanel();
   locationPanel.setLayout(new FlowLayout());
   Box hBox = Box.createHorizontalBox();

   // create the labels
   xLabel = new JLabel("X:");
   yLabel = new JLabel("Y:");

   // create the text fields
   xValue = new JTextField(Integer.toString(xIndex + numberBase),6);
   xValue.addActionListener(new ActionListener() {
     public void actionPerformed(ActionEvent e) {
       displayPixelInformation(xValue.getText(),yValue.getText());
     }
   });
   yValue = new JTextField(Integer.toString(yIndex + numberBase),6);
   yValue.addActionListener(new ActionListener() {
     public void actionPerformed(ActionEvent e) {
      displayPixelInformation(xValue.getText(),yValue.getText());
     }
   });

   // set up the next and previous buttons
   setUpNextAndPreviousButtons();

   // set up the font for the labels
   xLabel.setFont(labelFont);
   yLabel.setFont(labelFont);
   xValue.setFont(labelFont);
   yValue.setFont(labelFont);

   // add the items to the vertical box and the box to the panel
   hBox.add(Box.createHorizontalGlue());
   hBox.add(xLabel);
   hBox.add(xPrevButton);
   hBox.add(xValue);
   hBox.add(xNextButton);
   hBox.add(Box.createHorizontalStrut(10));
   hBox.add(yLabel);
   hBox.add(yPrevButton);
   hBox.add(yValue);
   hBox.add(yNextButton);
   locationPanel.add(hBox);
   hBox.add(Box.createHorizontalGlue());

   return locationPanel;
 }

 /**
  * Create the color information panel
  * @param labelFont the font to use for labels
  * @return the color information panel
  */
 private JPanel createColorInfoPanel(Font labelFont)
 {
   // create a color info panel
   JPanel colorInfoPanel = new JPanel();
   colorInfoPanel.setLayout(new FlowLayout());

   // get the pixel at the x and y
   Pixel pixel = new Pixel(picture,xIndex,yIndex);

   // create the labels
   rValue = new JLabel("R: " + pixel.getRed());
   gValue = new JLabel("G: " + pixel.getGreen());
   bValue = new JLabel("B: " + pixel.getBlue());

   // create the sample color panel and label
   colorLabel = new JLabel("Color at location: ");
   colorPanel = new JPanel();
   colorPanel.setBorder(new LineBorder(Color.black,1));

   // set the color sample to the pixel color
   colorPanel.setBackground(pixel.getColor());

   // set the font
   rValue.setFont(labelFont);
   gValue.setFont(labelFont);
   bValue.setFont(labelFont);
   colorLabel.setFont(labelFont);
   colorPanel.setPreferredSize(new Dimension(25,25));

   // add items to the color information panel
   colorInfoPanel.add(rValue);
   colorInfoPanel.add(gValue);
   colorInfoPanel.add(bValue);
   colorInfoPanel.add(colorLabel);
   colorInfoPanel.add(colorPanel);

   return colorInfoPanel;
 }

 /**
  * Creates the North JPanel with all the pixel location
  * and color information
  */
 private void createInfoPanel()
 {
   // create the info panel and set the layout
   JPanel infoPanel = new JPanel();
   infoPanel.setLayout(new BorderLayout());

   // create the font
   Font largerFont = new Font(infoPanel.getFont().getName(),
                              infoPanel.getFont().getStyle(),14);

   // create the pixel location panel
   JPanel locationPanel = createLocationPanel(largerFont);

   // create the color informaiton panel
   JPanel colorInfoPanel = createColorInfoPanel(largerFont);

   // add the panels to the info panel
   infoPanel.add(BorderLayout.NORTH,locationPanel);
   infoPanel.add(BorderLayout.SOUTH,colorInfoPanel);

   // add the info panel
   pictureFrame.getContentPane().add(BorderLayout.NORTH,infoPanel);
 }

 /**
  * Method to check that the current position is in the viewing area and if
  * not scroll to center the current position if possible
  */
 public void checkScroll()
 {
   // get the x and y position in pixels
   int xPos = (int) (xIndex * zoomFactor);
   int yPos = (int) (yIndex * zoomFactor);

   // only do this if the image is larger than normal
   if (zoomFactor > 1) {

     // get the rectangle that defines the current view
     JViewport viewport = scrollPane.getViewport();
     Rectangle rect = viewport.getViewRect();
     int rectMinX = (int) rect.getX();
     int rectWidth = (int) rect.getWidth();
     int rectMaxX = rectMinX + rectWidth - 1;
     int rectMinY = (int) rect.getY();
     int rectHeight = (int) rect.getHeight();
     int rectMaxY = rectMinY + rectHeight - 1;

     // get the maximum possible x and y index
     int maxIndexX = (int) (picture.getWidth() * zoomFactor) - rectWidth - 1;
     int maxIndexY = (int) (picture.getHeight() * zoomFactor) - rectHeight - 1;

     // calculate how to position the current position in the middle of the viewing
     // area
     int viewX = xPos - (int) (rectWidth / 2);
     int viewY = yPos - (int) (rectHeight / 2);

     // reposition the viewX and viewY if outside allowed values
     if (viewX < 0)
       viewX = 0;
     else if (viewX > maxIndexX)
       viewX = maxIndexX;
     if (viewY < 0)
       viewY = 0;
     else if (viewY > maxIndexY)
       viewY = maxIndexY;

     // move the viewport upper left point
     viewport.scrollRectToVisible(new Rectangle(viewX,viewY,rectWidth,rectHeight));
   }
 }

 /**
  * Zooms in the on picture by scaling the image.
  * It is extremely memory intensive.
  * @param factor the amount to zoom by
  */
 public void zoom(double factor)
 {
   // save the current zoom factor
   zoomFactor = factor;

   // calculate the new width and height and get an image that size
   int width = (int) (picture.getWidth()*zoomFactor);
   int height = (int) (picture.getHeight()*zoomFactor);
   BufferedImage bimg = picture.getBufferedImage();

   // set the scroll image icon to the new image
   imageDisplay.setImage(bimg.getScaledInstance(width, height, Image.SCALE_DEFAULT));
   imageDisplay.setCurrentX((int) (xIndex * zoomFactor));
   imageDisplay.setCurrentY((int) (yIndex * zoomFactor));
   imageDisplay.revalidate();
   checkScroll();  // check if need to reposition scroll
 }

 /**
  * Repaints the image on the scrollpane.
  */
 public void repaint()
 {
   pictureFrame.repaint();
 }

 //****************************************//
 //               Event Listeners          //
 //****************************************//

 /**
  * Called when the mouse is dragged (button held down and moved)
  * @param e the mouse event
  */
 public void mouseDragged(MouseEvent e)
 {
   displayPixelInformation(e);
 }

 /**
  * Method to check if the given x and y are in the picture
  * @param x the horiztonal value
  * @param y the vertical value
  * @return true if the x and y are in the picture and false otherwise
  */
 private boolean isLocationInPicture(int x, int y)
 {
   boolean result = false; // the default is false
   if (x >= 0 && x < picture.getWidth() &&
       y >= 0 && y < picture.getHeight())
     result = true;

   return result;
 }

 /**
  * Method to display the pixel information from the passed x and y but
  * also converts x and y from strings
  * @param xString the x value as a string from the user
  * @param yString the y value as a string from the user
  */
 public void displayPixelInformation(String xString, String yString)
 {
   int x = -1;
   int y = -1;
   try {
     x = Integer.parseInt(xString);
     x = x - numberBase;
     y = Integer.parseInt(yString);
     y = y - numberBase;
   } catch (Exception ex) {
   }

   if (x >= 0 && y >= 0) {
     displayPixelInformation(x,y);
   }
 }

 /**
  * Method to display pixel information for the passed x and y
  * @param pictureX the x value in the picture
  * @param pictureY the y value in the picture
  */
 private void displayPixelInformation(int pictureX, int pictureY)
 {
   // check that this x and y is in range
   if (isLocationInPicture(pictureX, pictureY))
   {
     // save the current x and y index
     xIndex = pictureX;
     yIndex = pictureY;

     // get the pixel at the x and y
     Pixel pixel = new Pixel(picture,xIndex,yIndex);

     // set the values based on the pixel
     xValue.setText(Integer.toString(xIndex  + numberBase));
     yValue.setText(Integer.toString(yIndex + numberBase));
     rValue.setText("R: " + pixel.getRed());
     gValue.setText("G: " + pixel.getGreen());
     bValue.setText("B: " + pixel.getBlue());
     colorPanel.setBackground(new Color(pixel.getRed(), pixel.getGreen(), pixel.getBlue()));

   }
   else
   {
     clearInformation();
   }

   // notify the image display of the current x and y
   imageDisplay.setCurrentX((int) (xIndex * zoomFactor));
   imageDisplay.setCurrentY((int) (yIndex * zoomFactor));
 }

 /**
  * Method to display pixel information based on a mouse event
  * @param e a mouse event
  */
 private void displayPixelInformation(MouseEvent e)
 {

   // get the cursor x and y
   int cursorX = e.getX();
   int cursorY = e.getY();

   // get the x and y in the original (not scaled image)
   int pictureX = (int) (cursorX / zoomFactor + numberBase);
   int pictureY = (int) (cursorY / zoomFactor + numberBase);

   // display the information for this x and y
   displayPixelInformation(pictureX,pictureY);

 }

 /**
  * Method to clear the labels and current color and reset the
  * current index to -1
  */
 private void clearInformation()
 {
   xValue.setText("N/A");
   yValue.setText("N/A");
   rValue.setText("R: N/A");
   gValue.setText("G: N/A");
   bValue.setText("B: N/A");
   colorPanel.setBackground(Color.black);
   xIndex = -1;
   yIndex = -1;
 }

 /**
  * Method called when the mouse is moved with no buttons down
  * @param e the mouse event
  */
 public void mouseMoved(MouseEvent e)
 {}

 /**
  * Method called when the mouse is clicked
  * @param e the mouse event
  */
 public void mouseClicked(MouseEvent e)
 {
   displayPixelInformation(e);
 }

 /**
  * Method called when the mouse button is pushed down
  * @param e the mouse event
  */
 public void mousePressed(MouseEvent e)
 {
   displayPixelInformation(e);
 }

 /**
  * Method called when the mouse button is released
  * @param e the mouse event
  */
 public void mouseReleased(MouseEvent e)
 {
 }

 /**
  * Method called when the component is entered (mouse moves over it)
  * @param e the mouse event
  */
 public void mouseEntered(MouseEvent e)
 {
 }

 /**
  * Method called when the mouse moves over the component
  * @param e the mouse event
  */
 public void mouseExited(MouseEvent e)
 {
 }

 /**
  * Method to enable all menu commands
  */
 private void enableZoomItems()
 {
   twentyFive.setEnabled(true);
   fifty.setEnabled(true);
   seventyFive.setEnabled(true);
   hundred.setEnabled(true);
   hundredFifty.setEnabled(true);
   twoHundred.setEnabled(true);
   fiveHundred.setEnabled(true);
 }

 /**
  * Controls the zoom menu bar
  *
  * @param a the ActionEvent
  */
 public void actionPerformed(ActionEvent a)
 {

   if(a.getActionCommand().equals("Update"))
   {
     this.repaint();
   }

   if(a.getActionCommand().equals("25%"))
   {
     this.zoom(.25);
     enableZoomItems();
     twentyFive.setEnabled(false);
   }

   if(a.getActionCommand().equals("50%"))
   {
     this.zoom(.50);
     enableZoomItems();
     fifty.setEnabled(false);
   }

   if(a.getActionCommand().equals("75%"))
   {
     this.zoom(.75);
     enableZoomItems();
     seventyFive.setEnabled(false);
   }

   if(a.getActionCommand().equals("100%"))
   {
     this.zoom(1.0);
     enableZoomItems();
     hundred.setEnabled(false);
   }

   if(a.getActionCommand().equals("150%"))
   {
     this.zoom(1.5);
     enableZoomItems();
     hundredFifty.setEnabled(false);
   }

   if(a.getActionCommand().equals("200%"))
   {
     this.zoom(2.0);
     enableZoomItems();
     twoHundred.setEnabled(false);
   }

   if(a.getActionCommand().equals("500%"))
   {
     this.zoom(5.0);
     enableZoomItems();
     fiveHundred.setEnabled(false);
   }
 }

 /**
  * Test Main.  It will ask you to pick a file and then show it
  */
 public static void main( String args[])
 {
   Picture p = new Picture(FileChooser.pickAFile());
   PictureExplorer test = new PictureExplorer(p);

 }

 /**
  * Class for establishing the focus for the textfields
  */
 private class PictureExplorerFocusTraversalPolicy
                 extends FocusTraversalPolicy {

        /**
         * Method to get the next component for focus
         */
        public Component getComponentAfter(Container focusCycleRoot,
                                           Component aComponent) {
            if (aComponent.equals(xValue))
              return yValue;
            else
              return xValue;
        }

        /**
         * Method to get the previous component for focus
         */
         public Component getComponentBefore(Container focusCycleRoot,
                                       Component aComponent) {
            if (aComponent.equals(xValue))
              return yValue;
            else
              return xValue;
         }

         public Component getDefaultComponent(Container focusCycleRoot) {
            return xValue;
        }

        public Component getLastComponent(Container focusCycleRoot) {
            return yValue;
        }

        public Component getFirstComponent(Container focusCycleRoot) {
            return xValue;
        }
    }

}