import javax.swing.JColorChooser;
import javax.swing.JFrame;
import java.awt.Color;

/**
 * A class to make working with a color chooser easier
 * for students.  It uses a JColorChooser to let the user
 * pick a color and returns the choosen color object.
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class ColorChooser
{

  /**
   * Method to let the user pick a color and return
   * the color object.
   * @return the picked color or red if no color was picked
   */
  public static Color pickAColor()
  {
    Color color = Color.white;

    // create a JFrame to be the parent of the color chooser open dialog
    // if you don't do this then you may not see the dialog.
    JFrame frame = new JFrame();

    // use the color chooser to pick the color
    color = JColorChooser.showDialog(frame,"Pick a color",color);

    return color;
  }

}