import java.awt.Frame;
import java.awt.Toolkit;
import java.net.URL;
import org.python.util.jython;
import java.io.File;

/**
 * The main launcher class for JES
 */
public class JESstartup
{
    /*synthetic*/ static Class class$JESstartup;
    /*synthetic*/ static Class array$Ljava$lang$String;

	/**
 	* The main method which launches JES
 	*/
    public static void main(String[] strings) {
        Frame frame = null;

        frame = SplashWindow.splash("images/JESsplash-v43.png");

        String [] args = {"Sources/JESProgram.py"};

        File insources = new File("Sources/JESProgram.py");
        if(! insources.exists()) {
            args[0] = "JESProgram.py";
        }

    	try {
            jython.main( args );
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

        if (frame != null) frame.dispose();
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

