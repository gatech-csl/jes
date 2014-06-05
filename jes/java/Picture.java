import java.awt.*;
import java.awt.font.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import java.text.*;

/**
 * A class that represents a picture.  This class inherits from
 * SimplePicture and allows the student to add functionality to
 * the Picture class. In JES, many "extra" features are already present,
 * available through OO-notation for the advanced media computation
 * students.
 * <br>
 * Copyright Georgia Institute of Technology 2004-2005
 * @author Barbara Ericson ericson@cc.gatech.edu
 *
 * Modified 6 July 2007 Pam Cutter Kalamazoo College
 * 	  Added a 3-param constructor to allow the construction of
 * 		pictures of different colors
 * 	  Added a copyInto method which allows copying as much of
 * 		this picture as will fit into a destination picture
 *    Added a crop method which returns a new picture which is a
 * 		specified portion of this picture
 *
 * Kalamazoo additional methods and improved comments merged by Buck Scharfnorth 22 May 2008
 */

public class Picture extends SimplePicture
{
  ///////////////////// constructors //////////////////////////////////

  /**
   * Constructor that takes no arguments
   */
  public Picture ()
  {
    /* not needed but use it to show students the implicit call to super()
     * child constructors always call a parent constructor
     */
    super();
  }

  /**
   * Constructor that takes a file name and creates the picture
   * @param fileName the name of the file to create the picture from
   */
  public Picture(String fileName)
  {
    // let the parent class handle this fileName
    super(fileName);
  }

  /**
   * Constructor that takes the width and height
   * @param width the width of the desired picture
   * @param height the height of the desired picture
   */
  public Picture(int width, int height)
  {
    // let the parent class handle this width and height
    super(width,height);
  }

/**
   * Constructor that takes the width and height, and a color
   * @param width the width of the desired picture
   * @param height the height of the desired picture
   * @param color the color of the desired picture
   */
  public Picture(int width, int height, Color color)
  {
    // let the parent class handle this width and height
    super(width,height,color);
  }

  /**
   * Constructor that takes a picture and creates a
   * copy of that picture.
   * @param copyPicture the picture to be copied
   */
  public Picture(Picture copyPicture)
  {
    // let the parent class do the copy
    super(copyPicture);
  }

  /**
   * Constructor that takes a buffered image
   * @param image the buffered image to use
   */
  public Picture(BufferedImage image)
  {
    super(image);
  }
  ////////////////////// methods ///////////////////////////////////////

  /**
   * Method to return a string with information about this picture.
   * @return a string with information about the picture such as fileName,
   * height and width.
   */
  public String toString()
  {
    String output = "Picture, filename " + getFileName() +
      " height " + getHeight()
      + " width " + getWidth();
    return output;
  }

/* adding graphics to pictures, for use in JES. (added by alexr, Oct 2006) */

    /**
     * Method to draw a line between two points on a picture
     * @param acolor the color of the line
     * @param x1 the x-coordinate of the first point
     * @param y1 the y-coordinate of the first point
     * @param x2 the x-coordinate of the second point
     * @param y2 the y-coordinate of the second point
     */
    public void addLine(Color acolor, int x1, int y1, int x2, int y2) {
        Graphics g = this.getBufferedImage().getGraphics();
        g.setColor(acolor);
        g.drawLine(x1 - SimplePicture._PictureIndexOffset,y1 - SimplePicture._PictureIndexOffset,x2 - SimplePicture._PictureIndexOffset,y2 - SimplePicture._PictureIndexOffset);
    }

    /**
     * Method to add a line of text to a picture
     *    @param acolor the color of the text
     *    @param x the x-coordinate of the bottom left corner of the text
     *    @param y the y-coordinate of the bottom left corner of the text
     *    @param string the text to be added to the picture
     */
    public void addText(Color acolor, int x, int y, String string) {
        Graphics g = this.getBufferedImage().getGraphics();
        g.setColor(acolor);
        g.drawString(string, x - SimplePicture._PictureIndexOffset, y - SimplePicture._PictureIndexOffset);
    }

    /**
     * Method to add text to a picture withe a particular font style
     *    @param acolor the color of the text
     *    @param x the x-coordinate of the bottom left corner of the text
     *    @param y the y-coordinate of the bottom left corner of the text
     *    @param string the text to be added to the picture
     *    @param style the font style to be used
     */
    public void addTextWithStyle(Color acolor, int x, int y, String string, Font style) {
        Graphics g = this.getBufferedImage().getGraphics();
        g.setColor(acolor);
        g.setFont(style);
        g.drawString(string, x - SimplePicture._PictureIndexOffset, y - SimplePicture._PictureIndexOffset);
    }

    /**
     * Method to draw the outline of a rectangle on a picture.
     *    @param acolor the color of the rectangle
     *    @param x the x-coordinate of the upper-left corner of the rectangle
     *    @param y the y-coordinate of the upper-left corner of the rectangle
     *    @param w the width of the rectangle
     *    @param h the height of the rectangle
     */
    public void addRect(Color acolor, int x, int y, int w, int h) {
        Graphics g = this.getBufferedImage().getGraphics();
        g.setColor(acolor);
        g.drawRect(x - SimplePicture._PictureIndexOffset,y - SimplePicture._PictureIndexOffset,w,h);
    }

    /**
     * Method to draw a solid rectangle on a picture.
     *    @param acolor the color of the rectangle
     *    @param x the x-coordinate of the upper-left corner of the rectangle
     *    @param y the y-coordinate of the upper-left corner of the rectangle
     *    @param w the width of the rectangle
     *    @param h the height of the rectangle
     */
    public void addRectFilled(Color acolor, int x, int y, int w, int h) {
        Graphics g = this.getBufferedImage().getGraphics();
        g.setColor(acolor);
        g.fillRect(x - SimplePicture._PictureIndexOffset,y - SimplePicture._PictureIndexOffset,w,h);
    }

    /**
     * Method to draw a solid oval on a picture.
     *    @param acolor the color of the oval
     *    @param x the x-coordinate of the upper-left corner of the bounding rectangle for the oval
     *    @param y the y-coordinate of the upper-left corner of the bounding rectangle for the oval
     *    @param w the width of the oval
     *    @param h the height of the oval
     */
    public void addOvalFilled(Color acolor, int x, int y, int w, int h) {
        Graphics g = this.getBufferedImage().getGraphics();
        g.setColor(acolor);
        g.fillOval(x - SimplePicture._PictureIndexOffset,y - SimplePicture._PictureIndexOffset,w,h);
    }

    /**
     * Method to draw the outline of an oval on a picture.
     *    @param acolor the color of the oval
     *    @param x the x-coordinate of the upper-left corner of the bounding rectangle for the oval
     *    @param y the y-coordinate of the upper-left corner of the bounding rectangle for the oval
     *    @param w the width of the oval
     *    @param h the height of the oval
     */
    public void addOval(Color acolor, int x, int y, int w, int h) {
        Graphics g = this.getBufferedImage().getGraphics();
        g.setColor(acolor);
        g.drawOval(x - SimplePicture._PictureIndexOffset,y - SimplePicture._PictureIndexOffset,w,h);
    }

    /**
     * Method to draw a solid arc on a picture
     *    @param acolor the color of the arc
     *    @param x the x-coordinate of the center of the arc
     *    @param y the y-coordinate of the center of the arc
     *    @param w the width of the arc
     *    @param h the height of the arc
     *    @param start the starting angle at which to draw the arc
     *    @param angle the angle of the arc, relative to the start angle
     */
    public void addArcFilled(Color acolor, int x, int y,
    int w, int h, int start, int angle) {

        Graphics g = this.getBufferedImage().getGraphics();
        g.setColor(acolor);
        g.fillArc(x - SimplePicture._PictureIndexOffset,y - SimplePicture._PictureIndexOffset,w,h,start,angle);
    }

    /**
     * Method to draw the outline of an arc on a picture
     *    @param acolor the color of the arc
     *    @param x the x-coordinate of the center of the arc
     *    @param y the y-coordinate of the center of the arc
     *    @param w the width of the arc
     *    @param h the height of the arc
     *    @param start the starting angle at which to draw the arc
     *    @param angle the angle of the arc, relative to the start angle
     */
    public void addArc(Color acolor,int x, int y, int w, int h, int start, int angle) {
        Graphics g = this.getBufferedImage().getGraphics();
        g.setColor(acolor);
        g.drawArc(x - SimplePicture._PictureIndexOffset,y - SimplePicture._PictureIndexOffset,w,h,start,angle);
    }

    /**
     * Copies all the pixels from this picture to the destination picture,
     * starting with the specified upper-left corner.  If this picture
     * will not fit in the destination starting at the upper-left corner,
     * then only the pixels that will fit are copied.  If the specified
     * upper-left corner is not in the bounds of the destination picture,
     * no pixels are copied.
     * @param dest the picture which to copy into
     * @param upperLeftX the x-coord for the upper-left corner
     * @param upperLeftY the y-coord for the upper-left corner
     */
    public void copyInto(Picture dest, int upperLeftX, int upperLeftY)
    {
    	// Determine the actual dimensions to copy; might be less than
    	// dimensions of this picture if there is not enough space in the
    	// destination picture.
    	int width = this.getWidth();
    	int widthAvailable = dest.getWidth()-upperLeftX;
    	if (widthAvailable < width)
    		width = widthAvailable;
    	int height = this.getHeight();
    	int heightAvailable = dest.getHeight()-upperLeftY;
    	if (heightAvailable < height)
    		height = heightAvailable;

    	// Copy pixel values from this picture to the destination
    	//  (Should have been implemented with the 7-parameter
    	//   getRGB/setRGB methods from BufferedImage?)
    	for (int x = 0; x < width; x++)
    		for (int y = 0; y < height; y++)
    			dest.setBasicPixel(upperLeftX + x, upperLeftY + y, this.getBasicPixel(x, y));

    }

    /**
     * Returns a cropped version of this picture: copies the pixels in
     * it starting at the specified upper-left corner and taking as
     * many pixels as specified by <code>width</code> and <code>height</code>.
     * The final cropped picture may be smaller than indicated by the
     * parameters if the cropping area as specified would go beyond the
     * bounds of this picture.  The cropping area will be <code>0 x 0</code>
     * if the specified upper-left corner is not in the bounds of the
     * destination picture.
     * @param upperLeftX the x-coord of the upper-left corner
     * @param upperLeftY the y-coord of the upper-left corner
     * @param width the desired width of the cropped area
     * @param height the desired height of the cropped area
     * @return the new cropped picture
     */
    public Picture crop(int upperLeftX, int upperLeftY, int width, int height)
    {
    	int widthAvailable = getWidth()-upperLeftX;
   		if (widthAvailable < width)
   			width = widthAvailable;
   		int heightAvailable = getHeight()-upperLeftY;
   		if (heightAvailable < height)
   			height = heightAvailable;

   		Picture newPic = new Picture(width, height);
   		for (int sourceX = upperLeftX, destX = 0; destX < width; sourceX++, destX++)
   			for (int sourceY = upperLeftY, destY = 0; destY < height; sourceY++, destY++)
   				newPic.setBasicPixel(destX, destY, this.getBasicPixel(sourceX, sourceY));
   		return newPic;

    }
} // end of class Picture, put all new methods before this

