import java.awt.*;
import java.awt.geom.*;

/**
 * This class represents a displayable path segment
 * it has a color, width, and a Line2D object
 * <br>
 * Copyright Georgia Institute of Technology 2005
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class PathSegment
{
  //////////////// fields /////////////////////
  private Color color;
  private int width;
  private Line2D.Float line;

  //////////////// constructors ///////////////

  /**
   * Constructor that takes the color, width,
   * and line
   * @param theColor the color of the PathSegment
   * @param theWidth the width of the PathSegment
   * @param theLine the Line2D.Float which represents this PathSegment
   */
  public PathSegment (Color theColor, int theWidth,
                      Line2D.Float theLine)
  {
    this.color = theColor;
    this.width = theWidth;
    this.line = theLine;
  }

  //////////////// methods ////////////////////

  /**
   * Method to paint this path segment
   * @param g the graphics context
   */
  public void paintComponent(Graphics g)
  {
    Graphics2D g2 = (Graphics2D) g;
    BasicStroke penStroke = new BasicStroke(this.width);
    g2.setStroke(penStroke);
    g2.setColor(this.color);
    g2.draw(this.line);
  }

} // end of class