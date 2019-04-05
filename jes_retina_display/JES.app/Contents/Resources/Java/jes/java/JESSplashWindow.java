import java.awt.Color;
import java.awt.Font;
import java.awt.Frame;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import javax.swing.SwingUtilities;

public class JESSplashWindow {
    private static final String SPLASH_FILE = "images/JESsplash.png";
    private static final int SPLASH_TEXT_X = 30;
    private static final int SPLASH_TEXT_Y = 222;

    private static final String SPLASH_FONT = "Sans";
    private static final int SPLASH_FONT_SIZE = 12;
    private static final int SPLASH_FONT_LINE_HEIGHT = 17;
    private static final int SPLASH_FONT_STYLE = Font.PLAIN;

    public static SplashWindow splash () {
        BufferedImage image = null;
        File splashFile = JESResources.getFileFor("images/JESsplash.png");

        try {
            image = ImageIO.read(splashFile);
        } catch (IOException exc) {
            throw new RuntimeException("Could not load splash screen.");
        }

        Graphics2D g = image.createGraphics();

        g.setColor(Color.BLACK);
        g.setFont(new Font(SPLASH_FONT, SPLASH_FONT_STYLE, SPLASH_FONT_SIZE));

        g.setRenderingHint(
            RenderingHints.KEY_TEXT_ANTIALIASING,
            RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

        String[] lines = {
            JESVersion.getTitle() + " version " + JESVersion.getRelease() +
                " – " + JESVersion.getReleaseDate(),
            "© " + JESVersion.getCopyrightYears() + " various authors.",
            "JES is Free Software (" + JESVersion.getLicense() + ").",
            "See Help:About to meet the JES development team!"
        };

        int x = SPLASH_TEXT_X;
        int y = SPLASH_TEXT_Y;

        for (String line : lines) {
            g.drawString(line, x, y);
            y += SPLASH_FONT_LINE_HEIGHT;
        }

        return new SplashWindow(image);
    }
}

