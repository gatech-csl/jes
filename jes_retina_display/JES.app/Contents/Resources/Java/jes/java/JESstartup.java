import java.awt.AWTEvent;
import java.awt.event.AWTEventListener;
import java.awt.Toolkit;
import java.io.File;
import java.util.Arrays;
import java.util.Properties;
import javax.swing.RepaintManager;
import org.python.util.jython;

/**
 * The main launcher class for JES
 */
public class JESstartup {
    /*synthetic*/ static Class class$JESstartup;
    /*synthetic*/ static Class array$Ljava$lang$String;

    public static void showHelp () {
        System.out.printf("%s %s Launcher\n", JESVersion.getTitle(), JESVersion.getRelease());
        System.out.println("- Pass no arguments to open a new file in the editor");
        System.out.println("- Pass a filename to open that file in the editor");
        System.out.println();
        System.out.println("Available options:");
        System.out.println();
        System.out.println("--version:          Print JES version information");
        System.out.println("--properties:       Print Java system properties");
        System.out.println("--jython [args]:    Run JES's copy of Jython with all provided arguments");
        System.out.println("                    (use --jython --help for details)");
        System.out.println();
        System.out.println("Additional debugging options are available.");
        System.out.println("View the source of JESstartup.java for details.");
    }

    /**
    * The main method which launches JES
    */
    public static void main(String[] strings) {
        System.setProperty("jes.starttimens", String.valueOf(System.nanoTime()));

        String home = JESResources.getHomePath();
        if (home == null) {
            System.err.println("Your launcher did not set jes.home properly.");
            System.exit(1);
        }

        boolean showSplash = true;
        int optIndex = 0;

        for (optIndex = 0; optIndex < strings.length; optIndex++) {
            String option = strings[optIndex];

            if (option.equals("--help")) {
                showHelp();
                System.exit(0);
            } else if (option.equals("--version")) {
                System.out.println(JESVersion.getBaseMessage());
                jython.main(new String[] {"-m", "jes.core.plugins"});
                System.exit(0);
            } else if (option.equals("--properties")) {
                // Print all the properties, and exit
                Properties props = System.getProperties();

                // Sort the list of properties
                String[] blank = new String[0];
                String[] propNames = props.stringPropertyNames().toArray(blank);
                Arrays.sort(propNames);

                for (String name : propNames) {
                    System.out.printf("%s = %s\n", name, props.getProperty(name));
                }

                System.exit(0);
            } else if (option.equals("--jython")) {
                // Interpret everything else on the command line
                // as a Jython option
                int firstArg = optIndex + 1;
                int argCount = strings.length - firstArg;

                String[] args = new String[argCount];
                System.arraycopy(strings, firstArg, args, 0, argCount);

                jython.main(args);
                System.exit(0);
            } else if (option.equals("--debug-keys")) {
                // Install an AWT event handler
                Toolkit.getDefaultToolkit().addAWTEventListener(new AWTEventListener() {
                    public void eventDispatched(AWTEvent event) {
                        System.err.println(event.paramString());
                    }
                }, AWTEvent.KEY_EVENT_MASK);
            } else if (option.equals("--check-threads")) {
                // Install a thread-checking repaint manager
                RepaintManager.setCurrentManager(new ThreadCheckingRepaintManager());
            } else if (option.startsWith("--python-verbose=")) {
                // Set the Python verbosity level
                System.setProperty("python.verbose", option.substring(17));
            } else if (option.startsWith("-psn")) {
                // Apple passes every process a Process Serial Number
                // We don't really need it for anything, but if we don't
                // recognize it _somehow_, the main code will think it's
                // a filename and try to open it
                System.setProperty("apple.psn", option);
            } else {
                // All remaining arguments should get copied into the
                // Jython arguments array for jes.__main__
                if (option.equals("--run") || option.equals("--shell")) {
                    showSplash = false;
                }
                break;
            }
        }

        // Okay...we're actually going to boot the JES Python code
        // Figure out what arguments to pass it
        int firstArg = optIndex;
        int argCount = strings.length - firstArg;

        String[] args = new String[2 + argCount];
        args[0] = "-m";
        args[1] = "jes.__main__";
        System.arraycopy(strings, firstArg, args, 2, argCount);

        // Show the splash window
        SplashWindow splashWindow = null;

        if (showSplash) {
            splashWindow = JESSplashWindow.splash();
        }

        // Force reading the config file now, before we start threading
        JESConfig.getInstance();

        // Actually boot Jython, and have it run jes/python/jes/__main__.py
        try {
            jython.main(args);
        } catch (Throwable throwable) {
            System.err.println("Oh noes! Couldn't start up Jython!!");
            throwable.printStackTrace();
            System.err.flush();
            System.exit(1);
        }

        // Once the UI finishes building, give some time to settle,
        // then close the splash window
        if (splashWindow != null) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException ie) {
                System.err.println("timeout exception, eep?");
            }

            splashWindow.done();
        }
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
}

