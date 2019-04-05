public class JESVersion {
    public static final String TITLE = "JES";
    public static final String FULL_TITLE = "JES";

    public static final String HOMEPAGE_URL = "https://github.com/gatech-csl/jes";
    public static final String HOMEPAGE_HOST = "GitHub";

    public static final String ISSUES_URL = "https://github.com/gatech-csl/jes/issues";
    public static final String ISSUES_HOST = "GitHub";

    public static final String VERSION = "5.02";
    public static final String RELEASE = VERSION + "0";

    public static final String RELEASE_DATE = "May 11, 2015";

    public static final String COPYRIGHT_FIRST_YEAR = "2002";
    public static final String COPYRIGHT_LAST_YEAR = "2015";

    public static final String COPYRIGHT_YEARS =
            COPYRIGHT_FIRST_YEAR + "–" + COPYRIGHT_LAST_YEAR;

    public static final String LICENSE = "GNU General Public License";

    public static final String SCM_INFO = "Git commit 56b6799 (Mon, 11 May 2015 16:01:16 -0400)";


    private static String[] pluginDescriptions = null;

    public static void setPlugins (String[] plugins) {
        pluginDescriptions = plugins;
    }


    public static String getTitle () {
        return TITLE;
    }

    public static String getFullTitle () {
        return FULL_TITLE;
    }

    public static String getVersion () {
        return VERSION;
    }

    public static String getRelease () {
        return RELEASE;
    }

    public static String getReleaseDate () {
        return RELEASE_DATE;
    }

    public static String getCopyrightYears () {
        return COPYRIGHT_YEARS;
    }

    public static String getLicense () {
        return LICENSE;
    }

    public static String getSCMInfo () {
        return SCM_INFO;
    }

    public static String getOSVersion () {
        String name = System.getProperty("os.name");

        // Windows includes the version the user would know in os.name.
        // The os.version property doesn't include anything useful.
        // (For example, os.name is "Windows 7" and os.version is "6.1"
        // on my Windows 7 laptop.)
        // So, on Windows platforms, we only return the name.
        // It is more useful on OS X and Linux.
        if (name.startsWith("Windows ")) {
            return name;
        } else {
            return name + " " + System.getProperty("os.version");
        }
    }

    public static String getBaseMessage () {
        return String.format(
            "%s version %s\n" +
            "Release date:   %s\n" +
            "Source control: %s\n" +
            "Java version:   %s (%s/%s)\n" +
            "Jython version: %s (build %s)\n" +
            "Computer OS:    %s (%s architecture)",
            TITLE, RELEASE, RELEASE_DATE, SCM_INFO,
            System.getProperty("java.version"),
            System.getProperty("java.runtime.name"),
            System.getProperty("java.vm.name"),
            org.python.Version.PY_VERSION, org.python.Version.getBuildInfo(),
            getOSVersion(), System.getProperty("os.arch")
        );
    }

    public static String getPluginMessage () {
        if (pluginDescriptions == null) {
            return "";
        } else {
            StringBuilder builder = new StringBuilder();
            String template = "\nPlugins:        %s";

            for (int i = 0; i < pluginDescriptions.length; i++) {
                builder.append(String.format(template, pluginDescriptions[i]));
                if (i == 0) {
                    template = "\n                %s";
                }
            }

            return builder.toString();
        }
    }

    public static String getMessage () {
        return getBaseMessage() + getPluginMessage();
    }
}

