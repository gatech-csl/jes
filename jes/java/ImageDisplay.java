import javax.swing.*;
import java.awt.*;
import java.awt.image.*;

/**
 * Class to display an image and the current location with a + sign
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class ImageDisplay extends JPanel implements Scrollable
{

  /////////////////////////// fields (attributes ///////////////////////////
  private Image image;         // the image to draw
  private Dimension prefSize;  // the preferred size of the display
  private int currentX = 0;    // the current x index
  private int currentY = 0;    // the current y index

  private static final long serialVersionUID = 7526471155622776147L;

  //////////////////////////// constructors /////////////////////////////////

  /**
   * Constructor that takes the image to display
   * @param theImage the image to display
   */
  public ImageDisplay(Image theImage)
  {
    image = theImage;
    prefSize = new Dimension(image.getWidth(this),image.getHeight(this));
    setPreferredSize(prefSize);
    revalidate();
  }

  /**
   * Constructor that takes the image and current x and y
   * @param theImage the image to display
   * @param x the current x value to use
   * @param y the current y value to use
   */
  public ImageDisplay(Image theImage, int x, int y)
  {
    this(theImage);
    currentX = x;
    currentY = y;
  }

  ////////////////////// methods /////////////////////////////////////////////

  /**
   * Method to get the image
   * @return the image
   */
  public Image getImage() { return image; }

  /**
   * Method to get the current x
   * @return the current x value
   */
  public int getCurrentX() { return currentX; }

  /**
   * Method to get the current y
   * @return the current y value
   */
  public int getCurrentY() { return currentY; }

  /**
   * Method to set the current x
   * @param x the x value to use
   */
  public void setCurrentX(int x)
  {
    currentX = x;
    repaint();
  }

  /**
   * Method to set the current y
   * @param y the y value to use
   */
  public void setCurrentY(int y)
  {
    currentY = y;
    repaint();
  }

  /**
   * Method to set the image
   * @param theImage the new image to use
   */
  public void setImage(Image theImage)
  {
    image = theImage;
    setPreferredSize(new Dimension(image.getWidth(this),image.getHeight(this)));
    repaint();
  }

  /**
   * Method to return the preferred size
   * @return the preferred size of this component
   */
  public Dimension getPreferredScrollableViewportSize()
  {
    return prefSize;
  }

  /**
   * Method to return the unit increment for scrolling
   * @param visibleRect the visible rectangle
   * @param orientation vertical or horizontal
   * @param direction neg is up or left and pos is right or down
   * @return the unit increment for arrow clicks
   */
  public int getScrollableUnitIncrement(Rectangle visibleRect,
                                        int orientation,
                                        int direction)
  { return 1; }

  /**
   * Method to return the block increment for scrolling
   * @param visibleRect the visible rectangle
   * @param orientation vertical or horizontal
   * @param direction neg is up or left and pos is right or down
   * @return the block increment for clicking in scroll area
   */
  public int getScrollableBlockIncrement(Rectangle visibleRect,
                                        int orientation,
                                        int direction)
  {
    return 10;
  }

  /**
   * Method to check if the viewport width is the source width
   * @return true if viewport and source have same width
   */
  public boolean getScrollableTracksViewportWidth()
  { return false; }

  /**
   * Method to check if the viewport height is the source height
   * @return true if viewport and soure have same height
   */
  public boolean getScrollableTracksViewportHeight()
  { return false; }

  /**
   * Method to handle displaying this object
   * @param g the graphics object for drawing with
   */
  public void paintComponent(Graphics g)
  {
    super.paintComponent(g);
    int num = 3;
    int xStart = currentX - num;
    int xEnd = currentX + num;
    int yStart = currentY - num;
    int yEnd = currentY + num;
    int width = image.getWidth(this);
    int maxX = width - 1;
    int height = image.getHeight(this);
    int maxY = height - 1;

    // draw the image
    g.drawImage(image,0,0,this);

    // check if the current index is in the image
    if (currentX >= 0 && currentX < width &&
        currentY >= 0 && currentY < height)
    {

      // check that the start and end values are visible
      if (xStart < 0)
        xStart = 0;
      if (xEnd > maxX)
        xEnd = maxX;
      if (yStart < 0)
        yStart = 0;
      if (yEnd > maxY)
        yEnd = maxY;

      // draw a small cross at the current x and y in yellow
      g.setColor(Color.yellow);
      g.drawLine(xStart,currentY,xEnd,currentY);
      g.drawLine(currentX,yStart,currentX,yEnd);
      g.setColor(Color.black);

      // outline the cross in black so that it shows up better
      int leftX = currentX - 1;
      int rightX = currentX + 1;
      int upY = currentY - 1;
      int downY = currentY + 1;
      if (xStart <= leftX && upY >= 0)
        g.drawLine(xStart,upY,leftX,upY);
      if (yStart <= upY && leftX >= 0)
        g.drawLine(leftX,yStart,leftX,upY);
      if (yStart <= upY && rightX <= maxX)
        g.drawLine(rightX,yStart,rightX,upY);
      if (upY >= 0 && rightX <= xEnd)
        g.drawLine(rightX,upY,xEnd,upY);
      if (downY < height && rightX <= xEnd)
        g.drawLine(rightX,downY,xEnd,downY);
      if (downY <= yEnd && rightX < width)
        g.drawLine(rightX,downY,rightX,yEnd);
      if (xStart <= leftX && downY < height)
        g.drawLine(xStart,downY,leftX,downY);
      if (leftX >= 0 && downY <= yEnd)
        g.drawLine(leftX,downY,leftX,yEnd);

    }
  }


}