import javax.swing.*;
import java.util.List;
import java.awt.*;
import java.awt.image.*;
import java.io.*;
import java.util.*;

/**
 * Class to show a frame-based animation.<br>
 * Copyright Georgia Institute of Technology 2007
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class AnimationPanel extends JComponent
{
  /////////////// fields /////////////////////

  /** list of image objects */
  private List<Image> imageList = new ArrayList<Image>();

  /** List of the file names */
  private List<String> nameList = new ArrayList<String>();

  /** index of currently displayed image */
  private int currIndex = 0;

  /** number of frames per second */
  private int framesPerSec = 16;


  private static final long serialVersionUID = 7526471155622776147L;

  ////////////// constructors /////////////////

  /**
   * Constructor that takes no arguments
   */
  public AnimationPanel()
  {
    this.setSize(new Dimension(100,100));
  }

  /**
   * Constructor that takes a list of pictures
   * @param pictList the list of pictures
   */
  public AnimationPanel(List<Picture> pictList)
  {
    Image image = null;
    Picture picture = null;
    for (int i = 0; i < pictList.size(); i++)
    {
      picture = pictList.get(i);
      nameList.add(picture.getFileName());
      image = picture.getImage();
      imageList.add(image);
    }

    BufferedImage bi = (BufferedImage) image;
    int width = bi.getWidth();
    int height = bi.getHeight();
    this.setSize(new Dimension(width,height));
    this.setMinimumSize(new Dimension(width,height));
    this.setPreferredSize(new Dimension(width,height));
  }

  /**
   * Constructor that takes the directory to read the frames from
   * @param directory the directory to read from
   */
  public AnimationPanel(String directory)
  {

    // get the list of files in the directory
    File dirObj = new File(directory);
    String[] fileArray = dirObj.list();
    ImageIcon imageIcon = null;
    Image image = null;

    // loop through the files
    for (int i = 0; i < fileArray.length; i++)
    {
      if (fileArray[i].indexOf(".jpg") >= 0)
      {

        imageIcon = new ImageIcon(directory + fileArray[i]);
        nameList.add(directory + fileArray[i]);
        imageList.add(imageIcon.getImage());
      }
    }

    // set size of this panel
    if (imageIcon != null)
    {
      image = (Image) imageList.get(0);
      int width = image.getWidth(null);
      int height = image.getHeight(null);
      this.setSize(new Dimension(width,
                               height));
      this.setMinimumSize(new Dimension(width,
                                      height));
      this.setPreferredSize(new Dimension(width,
                                          height));
    }
  }

  /**
   * Constructor that takes the directory to
   * read from and the number of frames per
   * second
   * @param directory the frame direcotry
   * @param theFramesPerSec the number of frames
   * per second
   */
  public AnimationPanel(String directory,
                        int theFramesPerSec)
  {
    this(directory);
    this.framesPerSec = theFramesPerSec;
  }

  ////////////// methods /////////////////////////

  /**
   * Method to get the current index
   * @return the current index
   */
  public int getCurrIndex() { return currIndex;}

  /**
   * Method to set the frames per second to show the movie
   * @param numFramesPerSec the number of frames to show per second
   */
  public void setFramesPerSec(int numFramesPerSec)
  {
    this.framesPerSec = numFramesPerSec;
  }

  /**
   * Method to get the frames per second
   * @return the number of frames per second
   */
  public int getFramesPerSec() { return this.framesPerSec;}
  /**
   * Method to add a picture
   * @param picture the picture to add
   */
  public void add(Picture picture)
  {
    Image image = picture.getImage();
    imageList.add(image);
    nameList.add(picture.getFileName());
  }

  /**
   * Method to show just the next frame
   */
  public void showNext()
  {
    this.currIndex++;
    if (this.currIndex == imageList.size())
      this.currIndex = 0;
    draw(this.getGraphics());
  }

  /**
   * Method to show the previous frame
   */
  public void showPrev()
  {
    this.currIndex--;
    if (this.currIndex < 0)
      this.currIndex = imageList.size() - 1;
    draw(this.getGraphics());
  }

  /**
   * show all frames starting at 0
   */
  public void showAll()
  {
    Graphics g = null;
    long startTime = 0;
    long endTime = 0;
    int timeToSleep =  1000 / framesPerSec;
    for (int i = 0; i < imageList.size(); i++)
    {
      startTime = System.currentTimeMillis();
      this.currIndex = i;
      g = this.getGraphics();
      draw(g);
      g.dispose();
      endTime = System.currentTimeMillis();

      // sleep
      try {
         if (endTime - startTime < timeToSleep)
            Thread.sleep(timeToSleep-(endTime-startTime));
      } catch (InterruptedException ex) {
      }
      // reset curr index
      currIndex = imageList.size() - 1;
    }
  }

   /**
   * show animation from current index
   */
  public void showAllFromCurrent()
  {
    Graphics g = null;
    int timeToSleep = (int) (1000 / framesPerSec);
    for (; currIndex < imageList.size(); currIndex++)
    {
      // draw current image
      g = this.getGraphics();
      draw(g);
      g.dispose();

      // sleep
      try {
        Thread.sleep(timeToSleep);
      } catch (InterruptedException ex) {
      }
    }
    // reset curr index
    currIndex = imageList.size() - 1;
  }

  /**
   * Method to remove all before current from
   * list
   */
  public void removeAllBefore()
  {
    File f = null;
    boolean result = false;
    for (int i = 0; i <= currIndex; i++)
    {
      f = new File(nameList.get(i));
      result = f.delete();
      if (result != true)
        System.out.println("trouble deleting " +
                           nameList.get(i));
      imageList.remove(0);
    }
  }

  /**
   * Method to remove all after the current index
   */
  public void removeAllAfter()
  {
    int i = currIndex + 1;
    int index = i;
    File f = null;
    boolean result = false;
    while (i < imageList.size())
    {
      f = new File(nameList.get(index++));
      result = f.delete();
      if (result != true)
        System.out.println("trouble deleting " +
                           nameList.get(index-1));
      imageList.remove(i);
    }
  }

  /**
   * Method to paint the frames
   * @param g the graphics context to draw to
   */
  public void draw(Graphics g)
  {
      Image image = (Image) imageList.get(this.currIndex);
      g.drawImage(image,0,0,this);
  }

  /**
   * Method to paint the component
   * @param g the graphics context to draw to
   */
  public void paintComponent(Graphics g)
  {
    if (imageList.size() == 0)
      g.drawString("No images yet!",20,20);
    else
      draw(g);
  }

  /**
   * Method to test
   */
  public static void main(String[] args)
  {
    JFrame frame = new JFrame();
    AnimationPanel panel = new AnimationPanel("c:/intro-prog-java/mediasources/fish/");
    frame.getContentPane().add(panel);
    frame.pack();
    frame.setVisible(true);
    panel.showAll();
  }

}