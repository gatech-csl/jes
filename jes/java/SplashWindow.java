import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

/**
 * A class to display the JES splash screen
 */
class SplashWindow extends JWindow {
    /**
     * Creates and shows a SplashWindow with a particular image.
     *
     * @param image The image to include.
     * @param frame The Frame to use.
     */
    public SplashWindow (Image image, Frame f) {
        super(f);

        JLabel l = new JLabel(new ImageIcon(image));
        getContentPane().add(l, BorderLayout.CENTER);
        pack();

        Dimension screenSize =
            Toolkit.getDefaultToolkit().getScreenSize();
        Dimension labelSize = l.getPreferredSize();
        setLocation(screenSize.width / 2 - (labelSize.width / 2),
                    screenSize.height / 2 - (labelSize.height / 2));

        addMouseListener(new MouseAdapter() {
            public void mousePressed(MouseEvent e) {
                setVisible(false);
                dispose();
            }
        });

        setVisible(true);
    }
}

