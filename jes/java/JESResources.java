import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import javax.swing.ImageIcon;

/**
 * This manages JES resources which live under the jes.home directory.
 */
public class JESResources {
    private static String homePath;
    private static File homeFile;

    static {
        homePath = System.getProperty("jes.home");
        if (homePath != null) {
            homeFile = new File(homePath);
        }
    }

    /**
     * Returns the configured JES home directory.
     *
     * @return  The path to the home directory, or null if one is
     *          not configured in the jes.home property.
     */
    public static String getHomePath() {
        return homePath;
    }

    /**
     * Returns a File identifying a resource in the JES home directory,
     * and verifies that it exists.
     *
     * @param path  The path to the resource, relative to the JES home,
     *              without a leading /.
     *
     * @return      A File for the resource.
     *
     * @throws IllegalStateException    If the JES home is not configured,
     *                                  or the file is not installed.
     */
    public static File getFileFor(String path) {
        if (homeFile == null) {
            throw new IllegalStateException("The jes.home property is not set");
        }

        File file = new File(homeFile, path);
        if (!file.canRead()) {
            throw new IllegalStateException("The resource " + path + " is not installed");
        }

        return file;
    }

    /**
     * Returns the pathname for a resource in the JES home directory,
     * and verifies that it exists.
     *
     * @param path  The path to the resource, relative to the JES home,
     *              without a leading /.
     *
     * @return      An absolute path for the resource.
     *
     * @throws IllegalStateException    If the JES home is not configured,
     *                                  or the file is not installed.
     */
    public static String getPathTo(String path) {
        return getFileFor(path).getAbsolutePath();
    }

    /**
     * Returns a Swing ImageIcon using a particular resource in the JES
     * home directory.
     *
     * @param path  The path to the resource, without a leading /.
     *
     * @return      An ImageIcon using that resource as its file.
     *
     * @throws IllegalStateException    If the JES home is not configured,
     *                                  or the file is not installed.
     */
    public static ImageIcon makeIcon(String path) {
        String fullPath = getPathTo(path);
        return new ImageIcon(fullPath);
    }

    /**
     * Returns a Swing ImageIcon using a particular resource in the JES
     * home directory.
     *
     * @param path          The path to the resource, without a leading /.
     * @param description   A description for the icon.
     *
     * @return              An ImageIcon using that resource as its file.
     *
     * @throws IllegalStateException    If the JES home is not configured,
     *                                  or the file is not installed.
     */
    public static ImageIcon makeIcon(String path, String description) {
        String fullPath = getPathTo(path);
        return new ImageIcon(fullPath, description);
    }
}

