import java.awt.Color;

/**
 * Class that references a pixel in a picture. A pixel has an x and y
 * location in a picture.  A pixel knows how to get and set the red,
 * green, blue, and alpha values in the picture.  A pixel also knows
 * how to get and set the color using a Color object.
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 *
 * Modified 6 July 2007 Pam Cutter Kalamazoo College
 *    Added a field to hold the pixel's color.  Updated the get/set
 *     color methods to reflect this new field.  Commented out
 *     original code.
 *
 * Kalamazoo additional methods merged by Buck Scharfnorth 22 May 2008
 */
public class Pixel
{

  ////////////////////////// fields ///////////////////////////////////

  /** the digital picture this pixel belongs to */
  private DigitalPicture picture;

  /** the x location of this pixel in the picture (0,0) is top left */
  private int x;

  /** the y location of this pixel in the picture (0,0) is top left */
  private int y;

  /** the color of the pixel */
  private java.awt.Color pxColor;

  ////////////////////// constructors /////////////////////////////////

  /**
   * A constructor that take the x and y location for the pixel and
   * the picture the pixel is coming from
   * @param picture the picture that the pixel is in
   * @param x the x location of the pixel in the picture
   * @param y the y location of the pixel in the picture
   */
  public Pixel(DigitalPicture picture, int x, int y)
  {
    // set the picture
    this.picture = picture;

    // set the x location
    this.x = x;

    // set the y location
    this.y = y;

    // get the color of this pixel
    pxColor = new java.awt.Color(this.picture.getBasicPixel(x, y));
  }

  ///////////////////////// methods //////////////////////////////
  // Pam Cutter - modified the get methods to get the values from
  // the color field.  No shifting is necessary at this level.

  /**
   * Method to get the x location of this pixel.
   * @return the x location of the pixel in the picture
   */
  public int getX() { return x; }

  /**
   * Method to get the y location of this pixel.
   * @return the y location of the pixel in the picture
   */
  public int getY() { return y; }

  /**
   * Method to get the amount of alpha (transparency) at this pixel.
   * It will be from 0-255.
   * @return the amount of alpha (transparency)
   */
  public int getAlpha() { return pxColor.getAlpha(); }


  /**
   * Method to get the amount of red at this pixel.  It will be
   * from 0-255 with 0 being no red and 255 being as much red as
   * you can have.
   * @return the amount of red from 0 for none to 255 for max
   */
  public int getRed() { return pxColor.getRed(); }

  /**
   * Method to get the red value from a pixel represented as an int
   * @param value the color value as an int
   * @return the amount of red
   */
  public static int getRed(int value)
  {
    int red = (value >> 16) & 0xff;
    return red;
  }

  /**
   * Method to get the amount of green at this pixel.  It will be
   * from 0-255 with 0 being no green and 255 being as much green as
   * you can have.
   * @return the amount of green from 0 for none to 255 for max
   */
  public int getGreen() { return pxColor.getGreen(); }

  /**
   * Method to get the green value from a pixel represented as an int
   * @param value the color value as an int
   * @return the amount of green
   */
  public static int getGreen(int value)
  {
    int green = (value >> 8) & 0xff;
    return green;
  }

  /**
   * Method to get the amount of blue at this pixel.  It will be
   * from 0-255 with 0 being no blue and 255 being as much blue as
   * you can have.
   * @return the amount of blue from 0 for none to 255 for max
   */
  public int getBlue() { return pxColor.getBlue(); }

  /**
   * Method to get the blue value from a pixel represented as an int
   * @param value the color value as an int
   * @return the amount of blue
   */
  public static int getBlue(int value)
  {
    int blue = value & 0xff;
    return blue;
  }

  /**
   * Method to get a color object that represents the color at this pixel.
   * @return a color object that represents the pixel color
   */
  public Color getColor() { return pxColor; }

  /**
   * Method to set the pixel color to the passed in color object.
   * @param newColor the new color to use
   */
  public void setColor(Color newColor)
  {
	pxColor = newColor;
	picture.setBasicPixel(x, y, newColor.getRGB());
  }

  /**
   * Method to set the pixel color to the passed in RGB and alpha components.
   * @param red the new red component value to use
   * @param green the new green component value to use
   * @param blue the new blue component value to use
   * @param alpha the new alpha component value to use
   */
  public void setColor(int red, int green, int blue, int alpha)
  {
  	setColor(new java.awt.Color(red, green, blue, alpha));
  }

  /**
   * Method to update the picture based on the passed color
   * values for this pixel
   * @param alpha the alpha (transparency) at this pixel
   * @param red the red value for the color at this pixel
   * @param green the green value for the color at this pixel
   * @param blue the blue value for the color at this pixel
   */
  public void updatePicture(int alpha, int red, int green, int blue)
  {
    // create a 32 bit int with alpha, red, green blue from left to right
    int value = (alpha << 24) + (red << 16) + (green << 8) + blue;

    // update the picture with the int value
    picture.setBasicPixel(x,y,value);
  }

  /**
   * Method to correct a color value to be within 0 and 255
   * @param the value to use
   * @return a value within 0 and 255
   */
  private static int correctValue(int value)
  {
	if ( JESConfig.getInstance().getSessionWrapAround() )
		value = (value % 256);
	else
	{
		if (value < 0)
			value = 0;
		if (value > 255)
			value = 255;
	}
	return value;
  }

  /**
   * Method to set the red to a new red value
   * @param value the new value to use
   */
  public void setRed(int value)
  {
    // set the red value to the corrected value
    int red = correctValue(value);

    
    // update the pixel value in the picture
    //updatePicture(getAlpha(), red, getGreen(), getBlue());
    setColor(red, pxColor.getGreen(), pxColor.getBlue(), pxColor.getAlpha());
  }

  /**
   * Method to set the green to a new green value
   * @param value the value to use
   */
  public void setGreen(int value)
  {
    // set the green value to the corrected value
    int green = correctValue(value);

    // update the pixel value in the picture
    //updatePicture(getAlpha(), getRed(), green, getBlue());
    setColor(pxColor.getRed(), green, pxColor.getBlue(), pxColor.getAlpha());
  }

  /**
   * Method to set the blue to a new blue value
   * @param value the new value to use
   */
  public void setBlue(int value)
  {
    // set the blue value to the corrected value
    int blue = correctValue(value);

    // update the pixel value in the picture
    //updatePicture(getAlpha(), getRed(), getGreen(), blue);
    setColor(pxColor.getRed(), pxColor.getGreen(), blue, pxColor.getAlpha());
  }

  /**
   * Method to set the alpha (transparency) to a new alpha value
   * @param value the new value to use
   */
  public void setAlpha(int value)
  {
    // make sure that the alpha is from 0 to 255
    int alpha = correctValue(value);

    // update the associated picture
    //updatePicture(alpha, getRed(), getGreen(), getBlue());
    setColor(pxColor.getRed(), pxColor.getGreen(), pxColor.getBlue(), value);
  }

  /**
   * Sets the color of this pixel from the color value of
   * <code>otherPixel</code>.
   * @param otherPixel a pixel that may be in the same picture
   * 				   or a different picture.
   * <br>
   * Added by Alyce Brady/Pam Cutter
   */
  public void setColorFrom(Pixel otherPixel)
  {
  	setColor(otherPixel.getColor());
  }

 /**
  * Method to get the distance between this pixel's color and the passed color
  * @param testColor the color to compare to
  * @return the distance between this pixel's color and the passed color
  */
 public double colorDistance(Color testColor)
 {
   double redDistance = this.getRed() - testColor.getRed();
   double greenDistance = this.getGreen() - testColor.getGreen();
   double blueDistance = this.getBlue() - testColor.getBlue();
   double distance = Math.sqrt(redDistance * redDistance +
                               greenDistance * greenDistance +
                               blueDistance * blueDistance);
   return distance;
 }

 /**
  * Method to compute the color distances between two color objects
  * @param color1 a color object
  * @param color2 a color object
  * @return the distance between the two colors
  */
 public static double colorDistance(Color color1,Color color2)
 {
   double redDistance = color1.getRed() - color2.getRed();
   double greenDistance = color1.getGreen() - color2.getGreen();
   double blueDistance = color1.getBlue() - color2.getBlue();
   double distance = Math.sqrt(redDistance * redDistance +
                               greenDistance * greenDistance +
                               blueDistance * blueDistance);
   return distance;
 }

 /**
  * Method to get the average of the colors of this pixel
  * @return the average of the red, green, and blue values
  */
 public double getAverage()
 {
   double average = (getRed() + getGreen() + getBlue()) / 3.0;
   return average;
 }

  /**
   * Method to return a string with information about this pixel
   * @return a string with information about this pixel
   */
  public String toString()
  {
    return "Pixel red=" + getRed() + " green=" + getGreen() +
      " blue=" + getBlue();
  }

}
