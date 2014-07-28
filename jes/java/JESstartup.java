import java.awt.AWTEvent;
import java.awt.event.AWTEventListener;
import java.awt.Frame;
import java.awt.Image;
import java.awt.Toolkit;
import java.io.File;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.URL;
import java.util.Arrays;
import java.util.Properties;
import javax.swing.RepaintManager;
import javax.swing.SwingUtilities;
import org.python.util.jython;

/**
 * The main launcher class for JES
 */
public class JESstartup {
    /*synthetic*/ static Class class$JESstartup;
    /*synthetic*/ static Class array$Ljava$lang$String;

    /**
    * The main method which launches JES
    */
    public static void main(String[] strings) {
        String home = JESResources.getHomePath();
        if (home == null) {
            System.err.println("Your launcher did not set jes.home properly.");
            System.exit(1);
        }

        for (String option : strings) {
            if (option.equals("--properties")) {
                Properties props = System.getProperties();

                // Sort the list of properties
                String[] blank = new String[0];
                String[] propNames = props.stringPropertyNames().toArray(blank);
                Arrays.sort(propNames);

                for (String name : propNames) {
                    System.out.printf("%s = %s\n", name, props.getProperty(name));
                }

                System.exit(0);
            } else if (option.equals("--shell")) {
                String[] args = new String[] {};
                jython.main(args);
                System.exit(0);
            } else if (option.equals("--debug-keys")) {
                Toolkit.getDefaultToolkit().addAWTEventListener(new AWTEventListener() {
                    public void eventDispatched(AWTEvent event) {
                        System.err.println(event.paramString());
                    }
                }, AWTEvent.KEY_EVENT_MASK);
            } else if (option.equals("--check-threads")) {
                RepaintManager.setCurrentManager(new ThreadCheckingRepaintManager());
            } else if (option.startsWith("--python-verbose=")) {
                System.setProperty("python.verbose", option.substring(17));
            }
        }

        // Set the dock icon and show the splash window
        setOSXDockIcon();
        SplashWindow splashWindow = JESSplashWindow.splash();

        // Force reading the config file now, before we start threading
        JESConfig.getInstance();

        // Actually boot Jython, and have it run jes/python/jes/__main__.py
        String[] args = {"-m", "jes.__main__"};
        try {
            jython.main(args);
        } catch (Throwable throwable) {
            System.err.println("Oh noes! Couldn't start up Jython!!");
            throwable.printStackTrace();
            System.err.flush();
            System.exit(1);
        }

        try {
            Thread.sleep(1000);
        } catch (InterruptedException ie) {
            System.err.println("timeout exception, eep?");
        }

        splashWindow.done();
    }

    static Class class$(String string) {
        Class var_class;
        try {
            var_class = Class.forName(string);
        } catch (ClassNotFoundException classnotfoundexception) {
            throw new NoClassDefFoundError(classnotfoundexception
                                           .getMessage());
        }
        return var_class;
    }

    private static void setOSXDockIcon () {
        // This attempts to access the Apple eAWT toolkit using reflection.
        // This means we don't need to get a stub JAR and worry about
        // compiling it.
        // https://gist.github.com/bchapuis/1562406
        try {
            // Get the class.
            Class util = Class.forName("com.apple.eawt.Application");
            Method getApplication = util.getMethod("getApplication", new Class[0]);
            Object application = getApplication.invoke(util);

            // Get the setDockIconImage method.
            Class params[] = new Class[1];
            params[0] = Image.class;
            Method setDockIconImage = util.getMethod("setDockIconImage", params);

            // Actually set the image.
            // I don't know _why_ passing null here works.
            // My guess is that Apple somehow elects an image based on the
            // first window created, and setting it to null means
            // "use the default." Then the -Xdock:icon JVM option sets
            // the default.
            setDockIconImage.invoke(application, (Object) null);
        } catch (ClassNotFoundException e) {
            // Probably not on Apple.
        } catch (NoSuchMethodException e) {
            // Whatever...
        } catch (InvocationTargetException e) {
            // Whatever...
        } catch (IllegalAccessException e) {
            // Whatever...
        }
    }
}

