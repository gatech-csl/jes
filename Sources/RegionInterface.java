import java.awt.image.BufferedImage;

/** Interface for working with getting a region of an image
  * <br>
  * Copyright Georgia Institute of Technology 2007
  * @author Barb Ericson ericson@cc.gatech.edu
  */
public interface RegionInterface
{
  /** Method to set the background image to select the region from
   * @param image the image to use
   */
  public void setBackgroundImage(Picture image);

  /**
   * Method to clear the picked region (a shape)
   */
  public void clearShapes();
}