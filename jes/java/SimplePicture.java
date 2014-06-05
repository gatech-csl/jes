import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import javax.swing.ImageIcon;
import java.awt.*;
import java.io.*;
import java.awt.geom.*;

/**
 * A class that represents a simple picture.  A simple picture may have
 * an associated file name and a title.  A simple picture has pixels,
 * width, and height.  A simple picture uses a BufferedImage to
 * hold the pixels.  You can show a simple picture in a
 * PictureFrame (a JFrame).
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 *
 * Modified 6 July 2007 Pam Cutter Kalamazoo College
 *    Added 3-param constructor, and setDefaults method
 *     to allow creation of a blank picture with a specified background color
 *
 * Additional and updated methods merged by Buck Scharfnorth 22 May 2008
 *
 * _PictureIndexOffset added (29 Oct 2008) -Buck
 */
public class SimplePicture implements DigitalPicture
{

  /////////////////////// Fields /////////////////////////
  /**
   * Constant for the index base (0 or 1)
   */
  public static final int _PictureIndexOffset = 0;

  /**
   * the file name associated with the simple picture
   */
  private String fileName;

  /**
   * the title of the simple picture
   */
  private String title;

  /**
   * buffered image to hold pixels for the simple picture
   */
  private BufferedImage bufferedImage;

  /**
   * frame used to display the simple picture
   */
  private PictureFrame pictureFrame;

  /**
   * extension for this file (jpg or bmp)
   */
  private String extension;


 /////////////////////// Constructors /////////////////////////

 /**
  * Constructor that takes no arguments. All fields will be null.
  * A no-argument constructor must be given in order for a class to
  * be able to be subclassed. By default all subclasses will implicitly
  * call this in their parent's no argument constructor unless a
  * different call to super() is explicitly made as the first line
  * of code in a constructor.
  */
 public SimplePicture()
 {this(200,100);}

 /**
  * Constructor that takes a file name and uses the file to create
  * a picture
  * @param fileName the file name to use in creating the picture
  */
 public SimplePicture(String fileName) {
   // load the picture into the buffered image
   load(fileName);
 }

 /**
  * Constructor that takes the width and height desired for a picture and
  * creates a buffered image of that size. This constructor doesn't
  * show the picture.
  * @param width the desired width
  * @param height the desired height
  */
 public  SimplePicture(int width, int height)
 {
   bufferedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
   title = "None";
   fileName = "None";
   extension = "jpg";
   setAllPixelsToAColor(Color.white);
 }

 /**
  * Constructor that takes the width and height desired for a picture and
  * creates a buffered image of that size.  It also takes the
  * color to use for the background of the picture.
  * @param width the desired width
  * @param height the desired height
  * @param theColor the background color for the picture
  */
 public  SimplePicture(int width, int height, Color theColor)
 {
   this(width,height);
   setAllPixelsToAColor(theColor);
 }

 /**
  * Constructor that takes a picture to copy information from
  * @param copyPicture the picture to copy from
  */
 public SimplePicture(SimplePicture copyPicture)
 {
   if (copyPicture.fileName != null)
   {
      this.fileName = new String(copyPicture.fileName);
      this.extension = copyPicture.extension;
   }
   if (copyPicture.title != null)
      this.title = new String(copyPicture.title);
   if (copyPicture.bufferedImage != null)
   {
     this.bufferedImage = new BufferedImage(copyPicture.getWidth(),
                                            copyPicture.getHeight(),
                                            BufferedImage.TYPE_INT_RGB);
     this.copyPicture(copyPicture);
   }
 }

 /**
  * Constructor that takes a buffered image
  * @param image the buffered image
  */
 public SimplePicture(BufferedImage image)
 {
   this.bufferedImage = image;
   title = "None";
   fileName = "None";
   extension = "jpg";
 }

 ////////////////////////// Methods //////////////////////////////////

 /**
  * Method to get the extension for this picture
  * @return the extension (jpg or bmp)
  */
 public String getExtension() { return extension; }


 /**
  * Method that will copy all of the passed source picture into
  * the current picture object
  * @param sourcePicture the picture object to copy
  */
 public void copyPicture(SimplePicture sourcePicture)
 {
   Pixel sourcePixel = null;
   Pixel targetPixel = null;

   // loop through the columns
   for (int sourceX = 0, targetX = 0;
        sourceX < sourcePicture.getWidth() &&
        targetX < this.getWidth();
        sourceX++, targetX++)
   {
     // loop through the rows
     for (int sourceY = 0, targetY = 0;
          sourceY < sourcePicture.getHeight() &&
          targetY < this.getHeight();
          sourceY++, targetY++)
     {
       sourcePixel = sourcePicture.getPixel(sourceX,sourceY);
       targetPixel = this.getPixel(targetX,targetY);
       targetPixel.setColor(sourcePixel.getColor());
     }
   }
 }

 /**
  * Method to set the color in the picture to the passed color
  * @param color the color to set to
  */
 public void setAllPixelsToAColor(Color color) {
    Graphics2D g = (Graphics2D) this.getBufferedImage().getGraphics();
    g.setColor(color);
    g.fillRect(0, 0, this.getWidth(), this.getHeight() );
 }


 /**
  * Method to get the buffered image
  * @return the buffered image
  */
 public BufferedImage getBufferedImage()
 {
    return bufferedImage;
 }

 /**
  * Method to get a graphics object for this picture to use to draw on
  * @return a graphics object to use for drawing
  */
 public Graphics getGraphics()
 {
   return bufferedImage.getGraphics();
 }

 /**
  * Method to get a Graphics2D object for this picture which can
  * be used to do 2D drawing on the picture
  * @return a Graphics2D object to use for drawing
  */
 public Graphics2D createGraphics()
 {
   return bufferedImage.createGraphics();
 }

 /**
  * Method to get the file name associated with the picture
  * @return the file name associated with the picture
  */
 public String getFileName() { return fileName; }

 /**
  * Method to set the file name
  * @param name the full pathname of the file
  */
 public void setFileName(String name)
 {
   fileName = name;
 }

 /**
  * Method to get the title of the picture
  * @return the title of the picture
  */
 public String getTitle()
 { return title; }

 /**
  * Method to set the title for the picture
  * @param title the title to use for the picture
  */
 public void setTitle(String title)
 {
   this.title = title;
   if (pictureFrame != null)
       pictureFrame.setTitle(title);
 }

 /**
  * Method to get the width of the picture in pixels
  * @return the width of the picture in pixels
  */
 public int getWidth() { return bufferedImage.getWidth(); }

 /**
  * Method to get the height of the picture in pixels
  * @return the height of the picture in pixels
  */
 public int getHeight() { return bufferedImage.getHeight(); }

 /**
  * Method to get the picture frame for the picture
  * @return the picture frame associated with this picture
  * (it may be null)
  */
 public PictureFrame getPictureFrame() { return pictureFrame; }

 /**
  * Method to set the picture frame for this picture
  * @param pictureFrame the picture frame to use
  */
 public void setPictureFrame(PictureFrame pictureFrame)
 {
   // set this picture objects' picture frame to the passed one
   this.pictureFrame = pictureFrame;
 }

 /**
  * Method to get an image from the picture
  * @return the buffered image since it is an image
  */
 public Image getImage()
 {
   return bufferedImage;
 }

 /**
  * Method to return the pixel value as an int for the given x and y location
  * @param x the x coordinate of the pixel
  * @param y the y coordinate of the pixel
  * @return the pixel value as an integer (alpha, red, green, blue)
  */
 public int getBasicPixel(int x, int y)
 {
    return bufferedImage.getRGB(x,y);
 }

 /**
  * Method to set the value of a pixel in the picture from an int
  * @param x the x coordinate of the pixel
  * @param y the y coordinate of the pixel
  * @param rgb the new rgb value of the pixel (alpha, red, green, blue)
  */
 public void setBasicPixel(int x, int y, int rgb)
 {
   bufferedImage.setRGB(x,y,rgb);
 }

 /**
  * Method to get a pixel object for the given x and y location
  * @param x the x location of the pixel in the picture
  * @param y the y location of the pixel in the picture
  * @return a Pixel object for this location
  */
 public Pixel getPixel(int x, int y)
 {
   // create the pixel object for this picture and the given x and y location
   Pixel pixel = new Pixel(this,x,y);
   return pixel;
 }

 /**
  * Method to get a one-dimensional array of Pixels for this simple picture
  * @return a one-dimensional array of Pixel objects starting with y=0
  * to y=height-1 and x=0 to x=width-1.
  */
 public Pixel[] getPixels()
 {
   int width = getWidth();
   int height = getHeight();
   Pixel[] pixelArray = new Pixel[width * height];

   // loop through height rows from top to bottom
   for (int row = 0; row < height; row++)
     for (int col = 0; col < width; col++)
       pixelArray[row * width + col] = new Pixel(this,col,row);

   return pixelArray;
 }

 /**
  * Method to load the buffered image with the passed image
  * @param image the image to use
  */
 public void load(Image image)
 {
   // get a graphics context to use to draw on the buffered image
   Graphics2D graphics2d = bufferedImage.createGraphics();

   // draw the image on the buffered image starting at 0,0
   graphics2d.drawImage(image,0,0,null);

   // show the new image
   show();
 }

 /**
  * Method to show the picture in a picture frame
  */
 public void show()
 {
    // if there is a current picture frame then use it
   if (pictureFrame != null)
     pictureFrame.updateImageAndShowIt();

   // else create a new picture frame with this picture
   else
     pictureFrame = new PictureFrame(this);
 }

 /**
  * Method to hide the picture
  */
 public void hide()
 {
   if (pictureFrame != null)
     pictureFrame.setVisible(false);
 }

 /**
  * Method to make this picture visible or not
  * @param flag true if you want it visible else false
  */
 public void setVisible(boolean flag)
 {
   if (flag)
     this.show();
   else
     this.hide();
 }

 /**
  * Method to open a picture explorer on a copy of this simple picture
  */
 public void explore()
 {
   // create a copy of the current picture and explore it
   new PictureExplorer(new SimplePicture(this));
 }

 /**
  * Method to force the picture to redraw itself. This is very
  * useful after you have changed the pixels in a picture.
  */
 public void repaint()
 {
   // if there is a picture frame tell it to repaint
   if (pictureFrame != null)
     pictureFrame.repaint();

   // else create a new picture frame
   else
     pictureFrame = new PictureFrame(this);
 }

 /**
  * Method to load the picture from the passed file name
  * @param fileName the file name to use to load the picture from
  */
 public void loadOrFail(String fileName) throws IOException
 {
    // set the current picture's file name
   this.fileName = fileName;

   // set the extension
   int posDot = fileName.indexOf('.');
   if (posDot >= 0)
     this.extension = fileName.substring(posDot + 1);

   // if the current title is null use the file name
   if (title == null || title == "None")
     title = fileName;

   File file = new File(this.fileName);

   if (!file.canRead())
   {
     // try adding the media path
     file = new File(FileChooser.getMediaPath(this.fileName));
     if (!file.canRead())
     {
       throw new IOException(this.fileName +
                             " could not be opened. Check that you specified the path");
     }
   }

   bufferedImage = ImageIO.read(file);
 }

 /**
  * Method to load the contents of the picture to a file without throwing exceptions
  * @param fileName the name of the file to load the picture from
  * @return true if success else false
  */
 public boolean load(String fileName)
 {
     try {
         this.loadOrFail(fileName);
         return true;

     } catch (Exception ex) {
         System.out.println("There was an error trying to open " + fileName);
         System.out.println(ex);
         // ex.printStackTrace();
         bufferedImage = new BufferedImage(600,200,
                                           BufferedImage.TYPE_INT_RGB);
         addMessage("Couldn't load " + fileName,5,100);
         return false;
     }

 }

 /**
  * Method to load the picture from the passed file name
  * this just calls load(fileName) and is for name compatibility
  * @param fileName the file name to use to load the picture from
  * @return true if success else false
  */
 public boolean loadImage(String fileName)
 {
     return load(fileName);
}

 /**
  * Method to draw a message as a string on the buffered image
  * @param message the message to draw on the buffered image
  * @param xPos the leftmost point of the string in x
  * @param yPos the bottom of the string in y
  */
 public void addMessage(String message, int xPos, int yPos)
 {
   // get a graphics context to use to draw on the buffered image
   Graphics2D graphics2d = bufferedImage.createGraphics();

   // set the color to white
   graphics2d.setPaint(Color.white);

   // set the font to Helvetica bold style and size 16
   graphics2d.setFont(new Font("Helvetica",Font.BOLD,16));

   // draw the message
   graphics2d.drawString(message,xPos,yPos);

 }

 /**
  * Method to draw a string at the given location on the picture
  * @param text the text to draw
  * @param xPos the left x for the text
  * @param yPos the top y for the text
  */
 public void drawString(String text, int xPos, int yPos)
 {
   addMessage(text,xPos,yPos);
 }

 /**
   * Method to create a new picture by scaling the current
   * picture by the given x and y factors
   * @param xFactor the amount to scale in x
   * @param yFactor the amount to scale in y
   * @return the resulting picture
   */
  public Picture scale(double xFactor, double yFactor)
  {
    // set up the scale tranform
    AffineTransform scaleTransform = new AffineTransform();
    scaleTransform.scale(xFactor,yFactor);

    // create a new picture object that is the right size
    Picture result = new Picture((int) (getWidth() * xFactor),
                                 (int) (getHeight() * yFactor));

    // get the graphics 2d object to draw on the result
    Graphics graphics = result.getGraphics();
    Graphics2D g2 = (Graphics2D) graphics;

    // draw the current image onto the result image scaled
    g2.drawImage(this.getImage(),scaleTransform,null);

    return result;
  }

  /**
   * Method to create a new picture of the passed width.
   * The aspect ratio of the width and height will stay
   * the same.
   * @param width the desired width
   * @return the resulting picture
   */
  public Picture getPictureWithWidth(int width)
  {
    // set up the scale tranform
    double xFactor = (double) width / this.getWidth();
    Picture result = scale(xFactor,xFactor);
    return result;
  }

  /**
   * Method to create a new picture of the passed height.
   * The aspect ratio of the width and height will stay
   * the same.
   * @param height the desired height
   * @return the resulting picture
   */
  public Picture getPictureWithHeight(int height)
  {
    // set up the scale tranform
    double yFactor = (double) height / this.getHeight();
    Picture result = scale(yFactor,yFactor);
    return result;
  }

 /**
  * Method to load a picture from a file name and show it in a picture frame
  * @param fileName the file name to load the picture from
  * @return true if success else false
  */
 public boolean loadPictureAndShowIt(String fileName)
 {
   boolean result = true;  // the default is that it worked

   // try to load the picture into the buffered image from the file name
   result = load(fileName);

   // show the picture in a picture frame
   show();

   return result;
 }

 /**
  * Method to write the contents of the picture to a file with
  * the passed name
  * @param fileName the name of the file to write the picture to
  */
 public void writeOrFail(String fileName) throws IOException
 {
   String extension = this.extension; // the default is current

   // create the file object
   File file = new File(fileName);
   File fileLoc = file.getParentFile();

   // canWrite is true only when the file exists already! (alexr)
   if (null != fileLoc && !fileLoc.canWrite()) {
       // System.err.println("can't write the file but trying anyway? ...");
        throw new IOException(fileName +
        " could not be opened. Check to see if you can write to the directory.");
   }

   // get the extension
   int posDot = fileName.indexOf('.');
   if (posDot >= 0)
       extension = fileName.substring(posDot + 1);

   // write the contents of the buffered image to the file as jpeg
   ImageIO.write(bufferedImage, extension, file);

 }

 /**
  * Method to write the contents of the picture to a file with
  * the passed name without throwing exceptions
  * @param fileName the name of the file to write the picture to
  * @return true if success else false
  */
 public boolean write(String fileName)
 {
     try {
         this.writeOrFail(fileName);
         return true;
     } catch (Exception ex) {
         System.out.println("There was an error trying to write " + fileName);
         ex.printStackTrace();
         return false;
     }

 }

 /**
  * Method to set the media path by setting the directory to use
  * @param directory the directory to use for the media path
  */
 public static void setMediaPath(String directory) {
   FileChooser.setMediaPath(directory);
 }

 /**
  * Method to get the directory for the media
  * @param fileName the base file name to use
  * @return the full path name by appending
  * the file name to the media directory
  */
 public static String getMediaPath(String fileName) {
   return FileChooser.getMediaPath(fileName);
 }

  /**
   * Method to get the coordinates of the enclosing rectangle after this
   * transformation is applied to the current picture
   * @return the enclosing rectangle
   */
  public Rectangle2D getTransformEnclosingRect(AffineTransform trans)
  {
    int width = getWidth();
    int height = getHeight();
    double maxX = width - 1;
    double maxY = height - 1;
    double minX, minY;
    Point2D.Double p1 = new Point2D.Double(0,0);
    Point2D.Double p2 = new Point2D.Double(maxX,0);
    Point2D.Double p3 = new Point2D.Double(maxX,maxY);
    Point2D.Double p4 = new Point2D.Double(0,maxY);
    Point2D.Double result = new Point2D.Double(0,0);
    Rectangle2D.Double rect = null;

    // get the new points and min x and y and max x and y
    trans.deltaTransform(p1,result);
    minX = result.getX();
    maxX = result.getX();
    minY = result.getY();
    maxY = result.getY();
    trans.deltaTransform(p2,result);
    minX = Math.min(minX,result.getX());
    maxX = Math.max(maxX,result.getX());
    minY = Math.min(minY,result.getY());
    maxY = Math.max(maxY,result.getY());
    trans.deltaTransform(p3,result);
    minX = Math.min(minX,result.getX());
    maxX = Math.max(maxX,result.getX());
    minY = Math.min(minY,result.getY());
    maxY = Math.max(maxY,result.getY());
    trans.deltaTransform(p4,result);
    minX = Math.min(minX,result.getX());
    maxX = Math.max(maxX,result.getX());
    minY = Math.min(minY,result.getY());
    maxY = Math.max(maxY,result.getY());

    // create the bounding rectangle to return
    rect = new Rectangle2D.Double(minX,minY,maxX - minX + 1, maxY - minY + 1);
    return rect;
  }

 /**
  * Method to return a string with information about this picture
  * @return a string with information about the picture
  */
 public String toString()
 {
   String output = "Simple Picture, filename " + fileName +
     " height " + getHeight() + " width " + getWidth();
   return output;
 }

} // end of SimplePicture class
