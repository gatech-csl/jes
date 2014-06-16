import java.awt.Frame;
import java.awt.Toolkit;
import java.net.URL;
import java.util.Arrays;
import java.util.Properties;
import org.python.util.jython;
import java.io.File;

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

        if (strings.length > 0) {
            if (strings[0].equals("--properties")) {
                Properties props = System.getProperties();

                // Sort the list of properties
                String[] blank = new String[0];
                String[] propNames = props.stringPropertyNames().toArray(blank);
                Arrays.sort(propNames);

                for (String name : propNames) {
                    System.out.printf("%s = %s\n", name, props.getProperty(name));
                }

                System.exit(0);
            } else if (strings[0].equals("--shell")) {
                String[] args = new String[] {};
                jython.main(args);
                System.exit(0);
            }
        }

        String[] args = {"-c", "import JESProgram; mainJESProgram = JESProgram.JESProgram()"};
        Frame frame = SplashWindow.splash(JESResources.getPathTo("images/JESsplash-v43.png"));

        try {
            jython.main(args);
        } catch (Throwable throwable) {
            System.err.println("Oh noes! Couldn't start up Jython!!");
            throwable.printStackTrace();
            System.err.flush();
            System.exit(1);
        }

        // Force reading the config file now
        JESConfig.getInstance();

        try {
            Thread.sleep(1000);
        } catch (InterruptedException ie) {
            System.err.println("timeout exception, eep?");
        }

        if (frame != null) {
            frame.dispose();
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

