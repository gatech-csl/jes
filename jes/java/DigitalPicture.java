import java.awt.Image;
import java.awt.image.BufferedImage;

/**
 * Interface to describe a digital picture.  A digital picture can have a
 * associated file name and a title.  It has pixels
 * associated with it and you can get and set the pixels.  You
 * can get an Image or a BufferedImage from a picture.  You can load
 * it from a file name or image.  You can show a picture.  You can
 * create a new image for it.
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public interface DigitalPicture
{
/**
 * Method to get the file name associated with the DigitalPicture
 * @return the file name associated with the DigitalPicture
 */
 public String getFileName(); // get the file name that the picture came from

/**
 * Method to get the title of the DigitalPicture
 * @return the title of the DigitalPicture
 */
 public String getTitle(); // get the title of the picture

/**
 * Method to set the title for the DigitalPicture
 * @param title the title to use for the DigitalPicture
 */
 public void setTitle(String title); // set the title of the picture

/**
 * Method to get the width of the DigitalPicture in pixels
 * @return the width of the DigitalPicture in pixels
 */
 public int getWidth(); // get the width of the picture in pixels

/**
 * Method to get the height of the DigitalPicture in pixels
 * @return the height of the DigitalPicture in pixels
 */
 public int getHeight(); // get the height of the picture in pixels

/**
 * Method to get an Image from the DigitalPicture
 * @return the Image object
 */
 public Image getImage(); // get the image from the picture

/**
 * Method to get a BufferedImage from the DigitalPicture
 * @return the BufferedImage object
 */
 public BufferedImage getBufferedImage(); // get the buffered image

/**
 * Returns the pixel value of a pixel in the DigitalPicture, given its coordinates.
 * @param x the x coordinate of the pixel
 * @param y the y coordinate of the pixel
 * @return the pixel value as an integer
 */
 public int getBasicPixel(int x, int y); // get the pixel information as an int

/**
 * Sets the value of a pixel in the DigitalPicture.
 * @param x the x coordinate of the pixel
 * @param y the y coordinate of the pixel
 * @param rgb the new rgb value of the pixel
 */
 public void setBasicPixel(int x, int y, int rgb); // set the pixel information

/**
 * Returns a Pixel object representing a pixel in the DigitalPicture given its coordinates
 * @param x the x coordinates of the pixel
 * @param y the y coordinates of the pixel
 * @return a Pixel object representing the requested pixel
 */
 public Pixel getPixel(int x, int y); // get the pixel information as an object

/**
 * Method to load the passed image into the DigitalPicture
 * @param image  the image to use
 */
 public void load(Image image); // load the image into the picture

/**
 * Method to load the contents of the passed filename
 * into the DigitalPicture without throwing errors
 * @param fileName the name of the file of the picture to load
 * @return true if success else false
 */
 public boolean load(String fileName); // load the picture from a file

/**
 * Method to show the picture in a picture frame
 */
 public void show(); // show the picture
}