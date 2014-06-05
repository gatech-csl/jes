import javax.swing.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Observer;
import java.awt.*;

/**
 * Class to represent a 2d world that can hold turtles and
 * display them
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class World extends JComponent implements ModelDisplay
{
  ////////////////// fields ///////////////////////

  /** should automatically repaint when model changed */
  private boolean autoRepaint = true;

  /** the background color for the world */
  private Color background = Color.white;

  /** the width of the world */
  private int width = 640;

  /** the height of the world */
  private int height = 480;

  /** the list of turtles in the world */
  private List<Turtle> turtleList = new ArrayList<Turtle>();

  /** the JFrame to show this world in */
  private JFrame frame = new JFrame("World");

  /** background picture */
  private Picture picture = null;

  private static final long serialVersionUID = 7526471155622776147L;

  ////////////////// the constructors ///////////////

  /**
   * Constructor that takes no arguments
   */
  public World()
  {
    // set up the world and make it visible
    initWorld(true);
  }

  /**
   * Constructor that takes a boolean to
   * say if this world should be visible
   * or not
   * @param visibleFlag if true will be visible
   * else if false will not be visible
   */
  public World(boolean visibleFlag)
  {
    initWorld(visibleFlag);
  }

  /**
   * Constructor that takes a width and height for this
   * world
   * @param w the width for the world
   * @param h the height for the world
   */
  public World(int w, int h)
  {
    width = w;
    height = h;

    // set up the world and make it visible
    initWorld(true);
  }

  ///////////////// methods ///////////////////////////

  /**
   * Method to initialize the world
   * @param visibleFlag the flag to make the world
   * visible or not
   */
  private void initWorld(boolean visibleFlag)
  {
    // set the preferred size
    this.setPreferredSize(new Dimension(width,height));

    // create the background picture
    picture = new Picture(width,height);

    // add this panel to the frame
    frame.getContentPane().add(this);

    // pack the frame
    frame.pack();

    // show this world
    frame.setVisible(visibleFlag);
  }

  /**
   * Method to get the graphics context for drawing on
   * @return the graphics context of the background picture
   */
  public Graphics getGraphics() { return picture.createGraphics(); }

  /**
   * Method to clear the background picture
   */
  public void clearBackground() { picture = new Picture(width,height); }

  /**
   * Method to get the background picture
   * @return the background picture
   */
  public Picture getPicture() { return picture; }

  /**
   * Method to set the background picture
   * @param pict the background picture to use
   */
  public void setPicture(Picture pict) { picture = pict; }

  /**
   * Method to paint this component
   * @param g the graphics context
   */
  public synchronized void paintComponent(Graphics g)
  {
    Turtle turtle = null;

    g.setColor(this.background);

    // draw the background image
    g.drawImage(picture.getImage(),0,0,null);

    // loop drawing each turtle on the background image
    Iterator<Turtle> iterator = turtleList.iterator();
    while (iterator.hasNext())
    {
      turtle = iterator.next();
      turtle.paintComponent(g);
    }
  }

  /**
   * Metod to get the last turtle in this world
   * @return the last turtle added to this world
   */
  public Turtle getLastTurtle()
  {
    return (Turtle) turtleList.get(turtleList.size() - 1);
  }


  /**
   * Method to add a model to this model displayer
   * @param model the model object to add
   */
  public void addModel(Object model)
  {
    turtleList.add((Turtle) model);
    if (autoRepaint)
       repaint();
  }

  /**
   * Method to check if this world contains the passed
   * turtle
   * @return true if there else false
   */
  public boolean containsTurtle(Turtle turtle)
  {
    return (turtleList.contains(turtle));
  }

  /**
   * Method to remove the passed object from the world
   * @param model the model object to remove
   */
  public void remove(Object model)
  {
    turtleList.remove(model);
  }

  /**
   * Method to get the width in pixels
   * @return the width in pixels
   */
  public int getWidth() { return width; }

  /**
   * Method to get the height in pixels
   * @return the height in pixels
   */
  public int getHeight() { return height; }

  /**
   * Method that allows the model to notify the display
   */
  public void modelChanged()
  {
    if (autoRepaint)
       repaint();
  }

  /**
   * Method to set the automatically repaint flag
   * @param value if true will auto repaint
   */
  public void setAutoRepaint(boolean value) { autoRepaint = value; }

  /**
   * Method to hide the frame
   */
  public void hideFrame()
  {
    frame.setVisible(false);
  }

  /**
   * Method to show the frame
   */
  public void showFrame()
  {
    frame.setVisible(true);
  }

  /**
   * Method to get the list of turtles in the world
   * @return a list of turtles in the world
   */
  public List getTurtleList()
  { return turtleList;}

  /**
   * Method to get an iterator on the list of turtles
   * @return an iterator for the list of turtles
   */
  public Iterator getTurtleIterator()
  { return turtleList.iterator();}

  /**
   * Method that returns information about this world
   * in the form of a string
   * @return a string of information about this world
   */
  public String toString()
  {
    return "A " + getWidth() + " by " + getHeight() +
      " world with " + turtleList.size() + " turtles in it.";
  }

  /**
   * Method that returns the background color of this world
   * @return the background color this world
   */
  public Color getBackground() {
      return this.background;
  }

} // end of World class
