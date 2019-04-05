import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Properties;

/**
 * Represents a set of JES configuration information.
 * There is only one instance of this class, because the configuration
 * values are used in many places.
 *
 * The class loads and stores its data in a .properties file.
 * It also can read and write old files that stored the property values
 * one per line in a predefined order.
 */
public class JESConfig {
    // SETTING NAMES
    // Add a constant here for each new setting.

    /** Whether to wrap red/blue/green values from 0 to 255. */
    public static final String CONFIG_WRAPPIXELVALUES = "media.wraprgb";

    /** The last-used media path. */
    public static final String CONFIG_MEDIAPATH = "media.path";


    /** The selected interface mode. */
    public static final String CONFIG_MODE = "interface.mode";

    public static final String MODE_BEGINNER = "Beginner";
    public static final String MODE_EXPERT = "Expert";

    /** The Java UI skin. */
    public static final String CONFIG_SKIN = "interface.skin";

    /** The command-window color scheme. */
    public static final String CONFIG_COMMAND_WINDOW_THEME = "interface.commandwindow.theme";

    /** The interface font size. */
    public static final String CONFIG_FONT = "interface.fontsize";

    public static final int FONT_SIZE_MIN = 8;
    public static final int FONT_SIZE_MAX = 72;
    public static final int FONT_SIZE_MAXREC = 32;

    /** Whether to display line numbers. */
    public static final String CONFIG_GUTTER = "interface.gutter";

    /** Whether to help the user indent with an indentation block. */
    public static final String CONFIG_BLOCK = "interface.block";


    /** Whether to save files automatically on load. */
    public static final String CONFIG_AUTOSAVEONRUN = "save.onload";

    /** Whether to save backup files. */
    public static final String CONFIG_BACKUPSAVE = "save.backups";


    /** The list of recent files. */
    public static final String CONFIG_RECENT_FILES = "recentfiles";


    /**
     * This Properties object contains properties which are used to "fill in"
     * a Properties file after it's loaded, when properties are absent.
     */
    private static final Properties defaults = new Properties();

    static {
        defaults.setProperty(CONFIG_WRAPPIXELVALUES,        "0");
        defaults.setProperty(CONFIG_MEDIAPATH,              "");

        defaults.setProperty(CONFIG_MODE,                   MODE_BEGINNER);
        defaults.setProperty(CONFIG_SKIN,                   "");
        defaults.setProperty(CONFIG_FONT,                   "12");
        defaults.setProperty(CONFIG_COMMAND_WINDOW_THEME,   "Old JES (Yellow on Black)");
        defaults.setProperty(CONFIG_GUTTER,                 "1");
        defaults.setProperty(CONFIG_BLOCK,                  "0");

        defaults.setProperty(CONFIG_AUTOSAVEONRUN,          "0");
        defaults.setProperty(CONFIG_BACKUPSAVE,             "1");

        defaults.setProperty(CONFIG_RECENT_FILES,           "");
    };


    // CONFIGURATION FILE INFO

    /**
     * The default name of the modern JES .properties files.
     */
    public static final String DEFAULT_FILE_NAME = "JESConfig.properties";

    /**
     * The header to include in .properties files.
     */
    private static final String FILE_COMMENTS =
        "### JES configuration file. You can change these options from Edit:Options in JES.";

    /**
     * The value to substitute for true.
     */
    private static final String TRUE = "1";

    /**
     * The value to substitute for false.
     */
    private static final String FALSE = "0";

    /**
     * The default name of the legacy JESConfig.txt files.
     */
    public static final String MIGRATION_FILE_NAME = "JESConfig.txt";

    /**
     * The order in which properties appeared in legacy configuration files.
     * null is for properties which are no longer used in JES 5.
     */
    private static final String[] MIGRATION_ORDER = {
        null,
        null,
        null,
        CONFIG_MODE,
        CONFIG_FONT,
        null,
        CONFIG_GUTTER,
        CONFIG_BLOCK,
        null,
        CONFIG_AUTOSAVEONRUN,
        null,
        CONFIG_WRAPPIXELVALUES,
        CONFIG_SKIN,
        null,
        CONFIG_BACKUPSAVE,
        null,
        CONFIG_MEDIAPATH
    };


    /**
     * Returns a File pointing to the current configuration file,
     * as indicated by the jes.configfile property. If that property is
     * not set, then the default config file is used.
     */
    public static File getConfigFile () {
        String path = System.getProperty("jes.configfile");

        if (path != null) {
            return new File(path);
        } else {
            return getDefaultConfigFile();
        }
    }

    /**
     * Returns a File pointing to the default configuration file location,
     * independent of the current platform. (This is usually not ideal.)
     */
    public static File getDefaultConfigFile () {
        return new File(System.getProperty("user.home") +
                        File.separatorChar + DEFAULT_FILE_NAME);
    }

    /**
     * Returns a File pointing to the location of the configuration file
     * used before JES 5.0.
     */
    public static File getMigrationConfigFile () {
        return new File(System.getProperty("user.home") +
                        File.separatorChar + MIGRATION_FILE_NAME);
    }


    // SINGLETON

    private static JESConfig theInstance = null;

    /**
     * Returns the one instance of JESConfig, loading the configuration
     * files in the process.
     */
    public static JESConfig getInstance () {
        if (theInstance == null) {
            theInstance = new JESConfig();
            theInstance.loadConfig();
        }

        return theInstance;
    }


    // INSTANCE STATE

    private Properties properties;

    private boolean loaded = false;
    private boolean migrated = false;
    private boolean modified = false;

    private IOException loadError = null;
    private IOException writeError = null;

    /**
     * Initializes a blank JESConfig instance.
     */
    private JESConfig () {
        properties = new Properties(defaults);
    }

    private void afterLoad () {
        if (!(new File(getStringProperty(CONFIG_MEDIAPATH))).exists()) {
            setStringProperty(CONFIG_MEDIAPATH, System.getProperty("user.home"));
        }

        int fontSize = getIntegerProperty(CONFIG_FONT);
        if (fontSize == 0) {
            // Reset it to the default.
            setIntegerProperty(CONFIG_FONT, 12);
        } else if (fontSize < FONT_SIZE_MIN) {
            // Clamp it to 8 (the safe minimum).
            setIntegerProperty(CONFIG_FONT, FONT_SIZE_MIN);
        } else if (fontSize > FONT_SIZE_MAX) {
            // Clamp it to 72 (the sane maximum).
            setIntegerProperty(CONFIG_FONT, FONT_SIZE_MAX);
        }
    }

    // FILE HANDLING

    /**
     * Reads a file full of properties.
     */
    public void loadConfig () {
        Properties props = new Properties(defaults);

        // Start loading, maybe?
        File propFile = getConfigFile();
        File migrationFile = getMigrationConfigFile();

        FileInputStream stream = null;

        try {
            if (propFile.exists()) {
                FileInputStream propStream = new FileInputStream(propFile);
                props.load(propStream);

                loaded = true;
                migrated = false;
            } else if (migrationFile.exists()) {
                FileInputStream textStream = new FileInputStream(migrationFile);
                migrateOldConfigFile(props, migrationFile, textStream);

                loaded = true;
                migrated = true;
            } else {
                loaded = false;
                migrated = false;
            }

            loadError = null;
            properties = props;
            modified = migrated;
            afterLoad();
        } catch (IOException exc) {
            loadError = exc;
            exc.printStackTrace();
        } finally {
            if (stream != null) {
                try {
                    stream.close();
                } catch (IOException exc) {
                    // seriously?!
                }
            }
        }
    }

    /**
     * Method to write the current JES settings to the file user.home/JES_CONFIG_FILE_NAME
     */
    public void writeConfig () {
        if (!modified) {
            return;
        }

        File propFile = getConfigFile();
        FileOutputStream stream = null;

        try {
            stream = new FileOutputStream(propFile);
            properties.store(stream, FILE_COMMENTS);

            writeError = null;
            loaded = true;
            modified = false;
        } catch (IOException exc) {
            writeError = exc;
            exc.printStackTrace();
        } finally {
            if (stream != null) {
                try {
                    stream.close();
                } catch (IOException exc) {
                    // seriously?!
                }
            }
        }
    }


    // CONFIGURATION STATUS

    /**
     * Indicates that the configuration was loaded from a file.
     */
    public boolean wasLoaded() {
        return loaded;
    }

    /**
     * Indicates that the configuration was loaded from an configuration file
     * from before JES 5.0. It will be saved to a .properties file when
     * it's written out.
     */
    public boolean wasMigrated () {
        return migrated;
    }

    /**
     * Indicates that a property has been added to the configuration
     * since it was loaded.
     */
    public boolean isModified () {
        return modified;
    }

    /**
     * Returns the most recent load error.
     */
    public IOException getLoadError () {
        return loadError;
    }


    // READ PROPERTIES

    /**
     * Reads a property from the settings.
     *
     * @param property The name of the property.
     * You should use one of the JESConfig.CONFIG_* constants.
     * @return The string value, or "" if the value is unset.
     */
    public String getStringProperty (String property) {
        String value = properties.getProperty(property);
        return value != null ? value : "";
    }

    /**
     * Reads a property from the settings as a Boolean.
     *
     * @param property The name of the property.
     * You should use one of the JESConfig.CONFIG_* constants.
     * @return The boolean value, or false if the value is unset.
     */
    public boolean getBooleanProperty (String property) {
        String val = getStringProperty(property);
        return val.equals(TRUE) ? true : false;
    }

    /**
     * Reads a property from the settings as an integer.
     *
     * @param property The name of the property.
     * You should use one of the JESConfig.CONFIG_* constants.
     * @return The integral value, or 0 if the value is unset.
     */
    public int getIntegerProperty (String property) {
        String val = getStringProperty(property);
        if (!val.equals("")) {
            try {
                return Integer.parseInt(val);
            } catch (NumberFormatException exc) {
                return 0;
            }
        } else {
            return 0;
        }
    }


    // WRITE PROPERTIES

    /**
     * Sets a property.
     *
     * @param property The name of the property.
     * You should use one of the JESConfig.CONFIG_* constants.
     * @param value The value to set for the property.
     */
    public void setStringProperty (String property, String value) {
        properties.setProperty(property, value);
        modified = true;
    }

    /**
     * Sets a property and stores it as an integer.
     *
     * @param property The name of the property.
     * You should use one of the JESConfig.CONFIG_* constants.
     * @param value The value to set for the property.
     */
    public void setIntegerProperty (String property, int value) {
        setStringProperty(property, String.valueOf(value));
    }

    /**
     * Sets a property and stores it as a Boolean.
     *
     * @param property The name of the property.
     * You should use one of the JESConfig.CONFIG_* constants.
     * @param value The value to set for the property.
     */
    public void setBooleanProperty (String property, boolean value) {
        setStringProperty(property, value ? TRUE : FALSE);
    }


    // MIGRATION

    private void migrateOldConfigFile (Properties props, File inputFile, InputStream input)
            throws IOException {
        byte bt[] = new byte[(int) inputFile.length()];
        input.read(bt);

        String[] lines = new String(bt).split("\r\n|\r|\n");

        // For every line that has a corresponding MIGRATION_ORDER entry,
        // copy the value into props.
        for (int line = 0; line < lines.length && line < MIGRATION_ORDER.length; line++) {
            if (MIGRATION_ORDER[line] != null) {
                props.setProperty(MIGRATION_ORDER[line], lines[line]);
            }
        }
    }
}

