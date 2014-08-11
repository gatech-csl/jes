import java.awt.*;
import java.awt.event.*;
import java.lang.reflect.InvocationTargetException;
import javax.swing.*;

/**
 * A class to control a splash screen.
 */
public class SplashWindow {
    private Image image;
    private JWindow window;
    private Frame frame;

    /**
     * Creates and shows a SplashWindow with a particular image.
     *
     * @param image The image to include.
     */
    public SplashWindow (Image image) {
        this.image = image;

        SwingUtilities.invokeLater(new Runnable () {
            public void run () {
                show();
            }
        });
    }

    private synchronized void show () {
        frame = new Frame();
        window = new JWindow(frame);

        JLabel l = new JLabel(new ImageIcon(image));
        window.getContentPane().add(l, BorderLayout.CENTER);
        window.pack();

        Dimension screenSize =
            Toolkit.getDefaultToolkit().getScreenSize();
        Dimension labelSize = l.getPreferredSize();
        window.setLocation(screenSize.width / 2 - (labelSize.width / 2),
                           screenSize.height / 2 - (labelSize.height / 2));

        window.addMouseListener(new MouseAdapter() {
            public void mousePressed(MouseEvent e) {
                dispose();
            }
        });

        window.setVisible(true);
    }

    /**
     * Closes the SplashWindow in another thread.
     */
    public void done () {
        try {
            SwingUtilities.invokeAndWait(new Runnable () {
                public void run () {
                    dispose();
                }
            });
        } catch (InvocationTargetException exc) {
            throw new RuntimeException("SplashWindow could not be closed");
        } catch (InterruptedException exc) {
            throw new RuntimeException("SplashWindow could not be closed");
        }
    }

    private synchronized void dispose () {
        window.dispose();
        frame.dispose();
    }
}

