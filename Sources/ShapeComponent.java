import java.awt.*;
import java.awt.event.*;
import java.util.*;
import javax.swing.*;
import java.awt.image.BufferedImage;

/**
 * Class ShapeCanvas:  holds shapes in a custom drawn area and
 * handles a region selection
 * <br>
 * Copyright Georgia Institute of Technology 2007
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class ShapeComponent extends JComponent implements RegionInterface
{


  ///////////////// Private Attributes /////////////////////////////

  private java.util.List<AbstractShape> shapes = new ArrayList<AbstractShape>(); // a vector of shapes
  private AbstractShape currentShape = null; // current shape being dragged
  private String currShapeType = AbstractShape.RECTANGLE; // default shape type
  private int width = 800;
  private int height = 600;
  private Color backgroundColor = Color.WHITE;
  private Picture backgroundImage = null;
  //private Image backgroundBuffer = null;        // background image for double buffering
  private Graphics backgroundG = null;    // graphics context of background image
  private VideoCapturer videoHandler = null;

  /////////////////// Constructors //////////////////////////////////

  /** Constructor that takes no arguments */
  public ShapeComponent ()
  {
    init();
  }

  /**
   * Constructor that takes the width and height
   * @param width the width of the canvas
   * @param height the height of the canvas
   */
  public ShapeComponent(int width, int height)
  {
    // set the local variables
    this.width = width;
    this.height = height;

    init();
  }

  /**
   * Constructor that takes a buffered image for the background
   * @param image the image to use
   */
  public ShapeComponent(Picture image)
  {
    this.backgroundImage = image;
    this.width = image.getWidth();
    this.height = image.getHeight();
    init();
  }

  ////////////////////// Private Methods ////////////////////////////////

  /* Method to initialize the shape component size and set the mouse listeners*/
  private void init()
  {
    // set the size of the component to the current width and height
    setSize(new Dimension(width,height));
    setMinimumSize(new Dimension(width,height));
    setPreferredSize(new Dimension(width,height));

    // add the mouse listener and mouse motion listener
    addMouseListener(new MyMouseAdapter());
    addMouseMotionListener(new MyMouseMotionAdapter());

    // add a component listener
    addComponentListener(new ComponentAdapter() {
      public void componentResized(ComponentEvent e)
      {
        //backgroundBuffer = null;
      }
    });

    // set the background color
    //setBackground(backgroundColor);
  }

  ///////////////////////// Public Methods ///////////////////////////////

  /**
   * Method to set the VideoCapturer for this ShapeComponent
   * @param handler the VideoCapturer to use
   */
  public void setVideoCapture(VideoCapturer handler)
  {
    this.videoHandler = handler;
  }

  /** Method to set the background image to select the region from
   * @param image the image to use
   */
  public void setBackgroundImage(Picture image)
  {
    Picture p = new Picture(image);
    Picture p2 = p.scale(0.5,0.5);
    backgroundImage = p2;
    width = backgroundImage.getWidth();
    height = backgroundImage.getHeight();
    setSize(new Dimension(width,height));
    setMinimumSize(new Dimension(width,height));
    setPreferredSize(new Dimension(width,height));
    repaint();
  }

  /**
   * Method to add a shape to the shape vector
   * @param shape the shape to add
   */
  public void add(AbstractShape shape)
  {
    // add the shape to the vector of shapes
    shapes.add(shape);

    // force a repaint to show the new shape
    repaint();
  }

  /**
   * Method to remove a shape from the shape vector
   * @param shape the shape to remove
   */
  public void remove(Shape shape)
  {
    // remove the shape from the vector of shapes
    shapes.remove(shape); // removes first one

    // force a repaint to show that it is gone
    repaint();
  }

  /**
   * Method to remove a shape given the index
   * @param index the index of the shape in the shape vector that you wish to remove
   */
  public void remove(int index)
  {
    // remove the shape at the given index
    shapes.remove(index);

    // force a repaint to show it is gone
    repaint();
  }

  /**
   * Update normally clears the background and calls paint
   * override it here to just call paint
   * @param g the graphics context on which to draw
   */
  public void update(Graphics g)
  {
    paint(g);
  }

  /**
   * Method to paint the shape canvas and all objects in it
   * @param g the graphic context on which to paint
   */
  public void paintComponent (Graphics g)
  {
    AbstractShape currShape;
    height = this.getHeight();
    int width = this.getWidth();

    if (backgroundImage == null)
    {
      g.setColor(backgroundColor);
      g.clearRect(0, 0, width, height);
    }
    else
      g.drawImage(backgroundImage.getImage(),0,0,this);

    // loop through the shape objects and draw each one
    for (int i=0; i<shapes.size(); i++)
    {
      currShape = (AbstractShape) shapes.get(i);
      currShape.draw(g);
    }

    // when drawing to background is done display background
    // image
    //g.drawImage(backgroundBuffer,0,0,this);
  }

  /**
   * Set the type of the shape that will be created when the user
   * clicks in the shape canvas.
   * @param shapeType the name of the shape
   */
  public void setShape(String shapeType)
  {
    currShapeType = shapeType;
  }

  /**
   * Clear all shapes out of the shape vector
   */
  public void clearShapes()
  {
    // remove all shapes from the shape vector
    shapes.clear();

    // repaint to show that they are gone
    repaint();
  }

  /////////////////// Main Method for Testing ///////////////////////////
  public static void main (String argv[])
  {
    // create a frame
    JFrame frame = new JFrame();

    // create a ShapeComponent
    ShapeComponent shapeComponent = new ShapeComponent(500,500);

    // create a rectangle shape
    AbstractShape shape = new RectangleShape(50,50,60,60);

    // add the shape to the shape canvas
    shapeComponent.add(shape);

    // add the shape canvas to the frame
    frame.getContentPane().add(shapeComponent);
    frame.pack(); // shrink to fit preferred size
    frame.setVisible(true); // show the frame
  }

  /** An inner class for handling the mouse listener interface */
  class MyMouseAdapter extends MouseAdapter
  {
    /** Method to handle when the user presses down the button */
    public void mousePressed(MouseEvent e)
    {
      int currX = e.getX();
      int currY = e.getY();

      // create an object of the current shape type
      try {
        Class shapeClass = Class.forName(currShapeType);
        currentShape = (AbstractShape) shapeClass.newInstance();
      } catch (Exception ex)
      {
        System.err.println("Problem in creating a shape");
        ex.printStackTrace();
        System.exit(1);

      }

      // fill in point1 and point2 in the new shape
      currentShape.setPoint1Values(currX,currY);
      currentShape.setPoint2Values(currX + 1, currY + 1);

      // add the shape to the vector of shapes
      add(currentShape);

      // repaint all
      repaint();

    }

    /** Method to handle when the user releases the mouse */
    public void mouseReleased(MouseEvent e)
    {
      int currX = e.getX();
      int currY = e.getY();

      // update the the point 2 values
      currentShape.setPoint2Values(currX,currY);

      if (videoHandler != null)
        videoHandler.setRegion(new java.awt.Rectangle(currentShape.getMinX()*2,
                                                      currentShape.getMinY()*2,
                                                      currentShape.getWidth()*2,
                                                      currentShape.getHeight()*2));

      // no current shape being dragged
      currentShape = null;

      // repaint
      repaint();

    }
  }

  /** Inner class for handling the mouse motion listener */
  class MyMouseMotionAdapter extends MouseMotionAdapter
  {
    /** Method to handle the drag of a mouse */
    public void mouseDragged(MouseEvent e)
    {
      int currX = e.getX();
      int currY = e.getY();

      // set the point 2 values
      currentShape.setPoint2Values(currX, currY);

      // repaint
      repaint();
    }
  }

}


