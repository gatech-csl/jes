import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * The JES Config Class
 * Created for the Jython Environment for Students
 * The JESConfig Class reads the config file information for the JES
 * config file, located at JES_CONFIG_FILE_NAME
 */
public class JESConfig
{
	// Configuration Array Location Values

	/**
	* Ease-of-use constant for JES Config file.
	* Specifies a filename to use as the JES settings file.
	*/
	public static final String JES_CONFIG_FILE_NAME = "JESConfig.txt";
	/**
	* Ease-of-use constant for the JES user's name (for turn-in purposes).
	*/
	public static final int CONFIG_NAME = 0;
	/**
	* Ease-of-use constant for the JES user's ID # (for turn-in purposes).
	*/
	public static final int CONFIG_GT = 1;
	/**
	* Ease-of-use constant for the JES user's mail server (for turn-in purposes).
	*/
	public static final int CONFIG_MAIL = 2;
	/**
	* Ease-of-use constant for the JES user's experience level ("Normal" or "Expert").
	*/
	public static final int CONFIG_MODE = 3;
	/**
	* Ease-of-use constant for the JES user's font-size (1-72).
	*/
	public static final int CONFIG_FONT = 4;
	/**
	* Ease-of-use constant for the JES user's e-mail address (for turn-in purposes).
	*/
	public static final int CONFIG_EMAIL_ADDR = 5;
	/**
	* Ease-of-use constant for the JES line number gutter (0 is off, 1 is on).
	*/
	public static final int CONFIG_GUTTER = 6;
	/**
	* Ease-of-use constant for the JES indention help (0 is on, 1 is off).
	*/
	public static final int CONFIG_BLOCK = 7;
	/**
	* Ease-of-use constant for the JES user's web-turnin server (coweb site).
	*/
	public static final int CONFIG_WEB_TURNIN = 8;
	/**
	* Ease-of-use constant for the JES auto save on load option (0 is off, 1 is on).
	*/
	public static final int CONFIG_AUTOSAVEONRUN = 9;
	/**
	* Depreciated option, retained for backward compatibility.
	*/
	public static final int CONFIG_AUTOOPENDOC = 10;
	/**
	* Ease-of-use constant for the JES wrap pixel value option (0 out of bounds colors capped, 1 colors will be (value % 256)).
	*/
	public static final int CONFIG_WRAPPIXELVALUES = 11;
	/**
	* Ease-of-use constant for the JES skin option (UIManager.getLookAndFeel().getName()).
	*/
	public static final int CONFIG_SKIN = 12;
	/**
	* Ease-of-use constant for the JES turnin menu option (0 off, 1 on).
	*/
	public static final int CONFIG_SHOWTURNIN = 13;
	/**
	* Ease-of-use constant for the JES save backup copy on save option (0 off, 1 on).
	*/
	public static final int CONFIG_BACKUPSAVE = 14;
	/**
	* Ease-of-use constant for the JES save logs option (0 off, 1 on).
	*/
	public static final int CONFIG_LOGBUFFER = 15;
	/**
	* Ease-of-use constant for the JES mediapath option (default is user.home).
	*/
	public static final int CONFIG_MEDIAPATH = 16;
	/**
	* Number of options in the current version of JES.
	*/
	public static final int CONFIG_NLINES = 17;

	// Instance for the singleton pattern
	private static JESConfig theInstance = null;

	// Other instance variables
	private ArrayList<String> properties;
	private String[] defaults = {"","","","Normal","12","","1","0","","0","","0","","0","1","1",""};
	private boolean configLoaded = true;
	private boolean sessionWrapAround = false;
  /**
   * A constructor to preload JES settings or load defaults if settings file cannot be read.
   */
	private JESConfig()
	{
		properties = readConfig();
		if ( properties == null )
		{
			configLoaded = false;
			properties = new ArrayList<String>( Arrays.asList( defaults ) );
		}

		if ( !(new File(getStringProperty(CONFIG_MEDIAPATH))).exists() )
			setStringProperty( CONFIG_MEDIAPATH, System.getProperty("user.home") );
		sessionWrapAround = getBooleanProperty(CONFIG_WRAPPIXELVALUES);
	}

  /**
   * Method to get the instance of the JESConfig singleton pattern
   * @return the instance of JESConfig
   */
	public static JESConfig getInstance()
	{
		if (theInstance == null)
			theInstance = new JESConfig();

		return theInstance;
	}

  /**
   * Method to get the current value of the pixel wrap around option.
   * getSessionWrapAround and setSessionWrapAround will ignore the value
   * in user settings.
   * @return the boolean value of the pixel wrap around
   */
	public boolean getSessionWrapAround()
	{
		return sessionWrapAround;
	}

  /**
   * Method to set the current value of the pixel wrap around option.
   * getSessionWrapAround and setSessionWrapAround will ignore the value
   * in user settings.
   * @param value the new value for the pixel wrap around
   */
	public void setSessionWrapAround( boolean value )
	{
		sessionWrapAround = value;
	}

  /**
   * Method to determine if the JES_CONFIG_FILE was read and previous settings restored
   * @return true if the JES_CONFIG_FILE was succesfully loaded
   */
	public boolean isConfigLoaded()
	{
			return configLoaded;
	}

  /**
   * Method to get a JES String property
   * @param property the JESConfig.CONFIG_* constant for the desired property
   * @return the value of the specified property as a String
   */
	public String getStringProperty( int property )
	{
		if ( ( property >= 0 ) && ( property < CONFIG_NLINES ) )
			return properties.get( property );
		else
			return "";
	}

  /**
   * Method to get a JES boolean property
   * @param property the JESConfig.CONFIG_* constant for the desired property
   * @return the value of the specified property as a boolean
   */
	public boolean getBooleanProperty( int property )
	{
		String val = getStringProperty(property);
		return val.equals("1") ? true : false;
	}

  /**
   * Method to get a JES Integer property
   * @param property the JESConfig.CONFIG_* constant for the desired property
   * @return the value of the specified property as an Integer
   */
	public int getIntegerProperty( int property )
	{

		String val = getStringProperty(property);
		if (!val.equals(""))
			return Integer.parseInt(val);
		else
			//TODO:  default value?  But this shouldn't happen says Buck
			return 0;
	}

  /**
   * Method to set a JES String property
   * @param property the JESConfig.CONFIG_* constant for the desired property
   * @param value the new String value for the specified property
   */
	public void setStringProperty( int property, String value )
	{
		if ( ( property >= 0 ) && ( property < CONFIG_NLINES ) )
			properties.set( property, value );
	}

  /**
   * Method to set a JES Integer property
   * @param property the JESConfig.CONFIG_* constant for the desired property
   * @param value the new Integer value for the specified property
   */
	public void setIntegerProperty( int property, int value )
	{
		setStringProperty(property, value + "");
	}

  /**
   * Method to set a JES Boolean property
   * @param property the JESConfig.CONFIG_* constant for the desired property
   * @param value the new Boolean value for the specified property
   */
	public void setBooleanProperty( int property, boolean value )
	{
		setStringProperty(property, value ? "1" : "0");
	}

  /**
   * Method to read the JES settings file from user.home/JES_CONFIG_FILE_NAME
   * @return an ArrayList of settings values
   */
	private ArrayList<String> readConfig()
	{
		ArrayList<String> properties = null;
		try
		{
			String inputFileName =
			System.getProperty("user.home") +
			File.separatorChar + JES_CONFIG_FILE_NAME;
			File inputFile = new File(inputFileName);
			FileInputStream in = new
			FileInputStream(inputFile);

			byte bt[] = new
			byte[(int)inputFile.length()];
			in.read(bt);
			String s = new String(bt);
			in.close();
			properties = new ArrayList<String>(Arrays.asList(s.split("\r\n|\r|\n")));
			//you must be upgrading; adding blanks...
			while ( properties.size() < CONFIG_NLINES )
				properties.add("");
		}
		catch(java.io.IOException e)
		{
		        System.out.println( "Cannot access JESConfig file," + JES_CONFIG_FILE_NAME );
				  System.out.println(e);
		}
		return properties;
	}

  /**
   * Method to write the current JES settings to the file user.home/JES_CONFIG_FILE_NAME
   */
	public void writeConfig()
	{
		try
		{
			String inputFileName = System.getProperty("user.home") + File.separatorChar + JES_CONFIG_FILE_NAME;
			File outputFile = new File(inputFileName);
			FileOutputStream fos = new FileOutputStream( outputFile );
			OutputStreamWriter out = new OutputStreamWriter( fos );
			for (int i = 0; i < properties.size(); i++)
			{
				out.write( properties.get(i) );
				out.write("\r\n");
			}
			out.close();
		}
		catch(java.io.IOException e)
		{
		        System.out.println( "Cannot access JESConfig file," + JES_CONFIG_FILE_NAME );
				  System.out.println(e);
		}
	}

	// Main for testing
	public static void main( String[] args )
	{
		JESConfig jConfig = JESConfig.getInstance();
		for( int i = 0; i < CONFIG_NLINES; i++ )
		{
			System.out.println( jConfig.getStringProperty( i ) );
		}
		jConfig.writeConfig();
		System.out.println("MEDIAPATH: " + JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MEDIAPATH));
	}


}
