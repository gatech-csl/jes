import java.awt.Graphics;

/**
 * Interface to used to communicate between a model
 * and its display
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public interface ModelDisplay
{
  /** method to notify the thing that displays that
   * the model has changed */
  public void modelChanged();

  /** method to add the model to the world
   * @param model the model object to add */
  public void addModel(Object model);

  /**
   * Method to remove the model from the world
   * @param model the model object to remove */
  public void remove(Object model);

  /**
   * Method that returns the graphics context
   * for this model display
   * @return the graphics context
   */
  public Graphics getGraphics();

  /**
   * Method to clear the background
   */
  public void clearBackground();

  /** Method to get the width of the display
   * @return the width in pixels of the display
   */
  public int getWidth();

  /** Method to get the height of the display
   * @return the height in pixels of the display
   */
  public int getHeight();
}