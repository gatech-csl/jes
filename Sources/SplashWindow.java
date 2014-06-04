import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

/**
 * A class to display the JES splash screen
 */
class SplashWindow extends JWindow
{
	/**
	 * Method to initialize the Frame and then call SplashWindow
	 * @param filename the file name of the splash window image
	 * @return the Frame to use
	 */
    public static Frame splash(String filename) {
        Frame frame = new Frame();
        SplashWindow splash = new
            SplashWindow(filename, frame);

        return frame;
    }

	/**
	 * Constructor to create and show the Splash Window that takes a filename and a Frame
	 * @param filename the file name of the splash window image
	 * @param filename the Frame to use
	 */
    public SplashWindow(String filename, Frame f)
    {
        super(f);
        JLabel l = new JLabel(new ImageIcon(filename));
        getContentPane().add(l, BorderLayout.CENTER);
        pack();
        Dimension screenSize =
          Toolkit.getDefaultToolkit().getScreenSize();
        Dimension labelSize = l.getPreferredSize();
        setLocation(screenSize.width/2 - (labelSize.width/2),
                    screenSize.height/2 - (labelSize.height/2));
        addMouseListener(new MouseAdapter()
            {
                public void mousePressed(MouseEvent e)
                {
                    setVisible(false);
                    dispose();
                }
            });
        setVisible(true);
    }
}

