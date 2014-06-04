import java.awt.*;

/**
 * Class Rectangle: inherits from Shape and draws a rectangle
 * <br>
 * Copyright Georgia Institute of Technology 2007
 * @author Barb Ericson
 */
public class RectangleShape extends AbstractShape
{

  ///////////////////// Constructors /////////////////////////////

  /** Constructor that takes no arguments */
  public RectangleShape ()
  {
    super();  // use parent's no arg constructor
  }

  /**
   * Constructor that takes two points to define the shape
   * @param firstPoint the first point used in defining the shape
   * @param lastPoint the second point used in defining the shape
   */
  public RectangleShape (Point firstPoint, Point lastPoint)
  {
    super(firstPoint,lastPoint); // use shape constructor
  }

  /**
   * Constructor that takes x1,y1,x2,y2
   * @param x1 the x value of the first point that defines the shape
   * @param y1 the y value of the first point that defines the shape
   * @param x2 the x value of the second point that defines the shape
   * @param y2 the y value of the second point that defines the shape
   */
  public RectangleShape (int x1, int y1, int x2, int y2)
  {
    super(x1,y1,x2,y2);  // use shape constructor
  }

  /////////////////////// Public Methods //////////////////////////////

  /** Draw the shape
   * @param g the graphics context on which to draw
   */
  public void draw(Graphics g)
  {
    // set the color
    g.setColor(color);

    // draw the rectangle given the top left point and width
    // and height
    g.drawRect(getMinX(),getMinY(),getWidth(),getHeight());
  }

}


