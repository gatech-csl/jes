import java.awt.*;

/**
 * Abstract class for shapes that can be represented with 2 points.<br>
 * Copyright Georgia Institute of Technology 2007
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public abstract class AbstractShape extends Object
{

  //////////////////// Public Attributes ///////////////////////////

  public static final String RECTANGLE = "RectangleShape"; // constant for rectangle
  public static final String OVAL = "OvalShape";           // constant for oval

  ///////////////// Protected Attributes /////////////////////////

  /** the color of this shape */
  protected Color color = Color.black;  // color to draw shape in
  /** the first point in the shape */
  protected Point p1 = new Point(); // first point
  /** the second point in the shape */
  protected Point p2 = new Point(); // second point

  ///////////////////// Constructors /////////////////////////////

  /** Constructor that takes no arguments */
  public AbstractShape()
  {
  }

  /**
   * Constructor that takes the first and second point
   * @param firstPoint    the first point that defines the shape
   * @param secondPoint   the second point that defines the shape
   */
  public AbstractShape (Point firstPoint, Point secondPoint)
  {
    p1.x = firstPoint.x;
    p1.y = firstPoint.y;
    p2.x = secondPoint.x;
    p2.y = secondPoint.y;
  }

  /**
   * Constructor that takes x1,y1,x2,y2
   * @param x1  x value of the first point that defines the shape
   * @param y1  y value of the first point that defines the shape
   * @param x2  x value of the second point that defines the shape
   * @param y2  y value of the second point that defines the shape
   */
  public AbstractShape (int x1, int y1, int x2, int y2)
  {
    p1.x = x1;
    p1.y = y1;
    p2.x = x2;
    p2.y = y2;

  }

  ////////////////////// Public Methods //////////////////////////////////

  /**
   * Method to get minimum x value of the bounding rectangle
   * @return  the minimum x value of the two points that define the shape
   */
  public int getMinX()
  {
    return Math.min(p1.x, p2.x);
  }

  /**
   *  Method to get the minimum y value of the bounding rectangle
   *  @return   the minimum y value of the two points that define the shape
   */
  public int getMinY()
  {
    return Math.min(p1.y,p2.y);
  }

  /**
   * Method to get the width of the bounding rectangle
   * @return    the width of the bounding rectangle
   */
  public int getWidth()
  {
    return Math.max(p1.x,p2.x) - getMinX() + 1;
  }

  /**
   * Method to get the height of the bounding rectangle
   * @return    the height of the bounding rectangle
   */
  public int getHeight()
  {
    return Math.max(p1.y,p2.y) - getMinY() + 1;
  }

  /**
   * Method to set the point values for point1 that defines the shape
   * @param newX    the new x value for point 1
   * @param newY    the new y value for point 1
   */
  public void setPoint1Values(int newX, int newY)
  {
    p1.x = newX;
    p1.y = newY;
  }

  /**
   * Method to set the point values for point2 that defines the shape
   * @param newX    the new x value for point 2
   * @param newY    the new y value for point 2
   */
  public void setPoint2Values(int newX, int newY)
  {
    p2.x = newX;
    p2.y = newY;
  }

  /** Abstract method to draw the shape given the graphics context
   * @param g   the graphics context to draw the shape on
   */
  public abstract void draw(Graphics g);

}


