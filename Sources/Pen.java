import java.awt.*;
import java.awt.geom.*;
import javax.swing.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

/**
 * Class to represent a pen which has a color, width,
 * and a list of path segments that it should draw.
 * A pen also knows if it is up or down
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class Pen
{
  ////////////////// fields //////////////////////

  /** track if up or down */
  private boolean penDown = true;

  /** color of ink */
  private Color color = Color.green;

  /** width of stroke */
  private int width = 1;

  /** list of path segment objects to draw */
  private List<PathSegment> pathSegmentList = new ArrayList<PathSegment>();

  //////////////// constructors ///////////////////

  /**
   * Constructor that takes no arguments
   */
  public Pen() { }

  /**
   * Constructor that takes the ink color and width
   * @param color the ink color
   * @param width the width in pixels
   */
  public Pen(Color color, int width)
  {
    this.color = color;
    this.width = width;
  }

  /**
   * Constructor that takes the ink color, width, and penDown flag
   * @param color the ink color
   * @param width the width in pixels
   * @param penDown the flag if the pen is down
   */
  public Pen(Color color, int width, boolean penDown)
  {
    // use the other constructor to set these
    this(color,width);

    // set the pen down flag
    this.penDown = penDown;
  }

  ////////////////// methods ///////////////////////

  /**
   * Method to get pen down status
   * @return true if the pen is down else false
   */
  public boolean isPenDown() { return penDown; }

  /**
   * Method to set the pen down value
   * @param value the new value to use
   */
  public void setPenDown(boolean value) { penDown = value; }

  /**
   * Method to get the pen (ink) color
   * @return the ink color
   */
  public Color getColor() { return color; }

  /**
   * Method to set the pen (ink) color
   * @param color the color to use
   */
  public void setColor(Color color) { this.color = color;}

  /**
   * Method to get the width of the pen
   * @return the width in pixels
   */
  public int getWidth() { return width; }

  /**
   * Method to set the width of the pen
   * @param width the width to use in pixels
   */
  public void setWidth(int width) { this.width = width; }

  /**
   * Method to add a path segment if the pen is down
   * @param x1 the first x
   * @param y1 the first y
   * @param x2 the second x
   * @param y2 the second y
   */
  public synchronized void addMove(int x1, int y1, int x2, int y2)
  {
    if (penDown)
    {
      PathSegment pathSeg =
        new PathSegment(this.color,this.width,
                        new Line2D.Float(x1,y1,x2,y2));
      pathSegmentList.add(pathSeg);
    }
  }

  /**
   * Method to clear the path stored for this pen
   */
  public void clearPath()
  {
    pathSegmentList.clear();
  }

  /**
   * Metod to paint the pen path
   * @param g the graphics context
   */
  public synchronized void paintComponent(Graphics g)
  {

    Color oldcolor = g.getColor();

    // loop through path segment list and
    Iterator iterator = pathSegmentList.iterator();
    PathSegment pathSeg = null;

    // loop through path segments
    while (iterator.hasNext())
    {
      pathSeg = (PathSegment) iterator.next();
      pathSeg.paintComponent(g);
    }

    g.setColor(oldcolor);
  }

} // end of class
