import javax.swing.*;
import javax.swing.SwingUtilities;

/**
 * Class to make it easy to get input
 * from a user using JOptionPane
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 *
 * 30 June 2008: Edited by Brian so that all number methods return Doubles and Integers
 * so that it is possible to return null/None
 *
 * 14 May 2009: Edited by Dorn to ensure all JOptionPane calls to show are threadsafe.
 *
 */
public class SimpleInput {
    /**
     * Method to allow the user to input a number.
     * the dialog will keep appearing till a valid
     * number is input.
     * @param message the message to display to the user in the dialog
     * @return the number as a double
     */
    public static Double getNumber(String message) {
        boolean okay = true; // start out okay
        String answerString = null; // answer as a string
        Double answer = new Double(0.0);

        // Try to get a number using an input dialog
        do {
            // get the user's answer as a string
            answerString = safeInputDialog(message);

            // try to convert to a number
            try {
                answer = new Double(answerString);
                okay = true;
            } catch (Exception ex) {
                /* not a number so set flag to false and
                 * change message
                 */
                okay = false;
                message = "Try again.  That wasn't a number!";
                if (answerString == null) {
                    return null;
                }
            }
        } while (!okay);

        // return the answer as a number
        return answer;
    }

    /**
     * Method to allow the user to input an integer.
     * The dialog will keep appearing till a valid
     * number is input.
     * @param message the message to display to the user in the dialog
     * @return the number as an integer
     */
    public static Integer getIntNumber(String message) {
        boolean okay = true; // start out okay
        String answerString = null; // answer as a string
        Integer answer = new Integer(0);

        // Try to get a number using an input dialog
        do {
            // get the user's answer as a string
            answerString = safeInputDialog(message);

            // try to convert to a number
            try {
                answer = new Integer(answerString);
                okay = true;
            } catch (Exception ex) {
                /* not a number so set flag to false and
                 * change message
                 */
                okay = false;
                message = "Try again.  That wasn't an integer!";
                if (answerString == null) {
                    return null;
                }
            }
        } while (!okay);

        // return the answer as a number
        return answer;
    }


    /**
     * Method to get an integer between a minimum
     * and maximum (inclusive)
     * @param message the message to display to the user in the dialog
     * @param min the minimum number
     * @param max the maximum number
     * @return the user entered integer
     */
    public static Integer getIntNumber(String message,
                                       int min,
                                       int max) {
        boolean okay = true; // start out okay
        String answerString = null; // answer as a string
        String failMessage = "Try again.  That wasn't an " +
                             "integer between " + min +
                             " and " + max + "!";
        Integer answer = new Integer(0);

        // Try to get a number using an input dialog
        do {
            // get the user's answer as a string
            answerString = safeInputDialog(message);

            // try to convert to a number
            try {
                answer = new Integer(answerString);

                /* check that the answer is in the
                 * allowed range
                 */
                if (answer >= min && answer <= max) {
                    okay = true;
                } else {
                    okay = false;
                    message = failMessage;
                }
            } catch (Exception ex) {
                /* not a number so set flag to false and
                 * change message
                 */
                okay = false;
                message = failMessage;
                if (answerString == null) {
                    return null;
                }
            }
        } while (!okay);

        // return the answer as a number
        return answer;
    }

    /**
     * Method to get the name of a directory
     * @param message the message to display to the user
     * @return the pathname for a directory
     */
    public static String getDirectory(String message) {
        String name = getString(message);
        return name;
    }

    /**
     * Method to get a string input by the user.
     * The dialog will keep appearing till a
     * string is entered.
     * @param message the message to display to the user
     * @return the input string
     */
    public static String getString(String message) {
        boolean okay = true;
        String answer = null;

        do {
            answer = safeInputDialog(message);
            okay = true;

            // if null try again
            if (answer == null) {
                return null;
            }
        } while (!okay);

        // return the answer
        return answer;
    }

    /**
     * Method to prompt for a string by the user in a
     * threadsafe manner.
     * @param message the message to display to the user
     * @return the input string
     */
    private static String safeInputDialog(final String message) {
        final String[] answer = new String[1];

        Runnable promptStringRunner =
        new Runnable() {
            public void run() {
                answer[0] = JOptionPane.showInputDialog(message);
            }
        };

        try {
            if (SwingUtilities.isEventDispatchThread()) {
                promptStringRunner.run();
            } else {
                SwingUtilities.invokeAndWait(promptStringRunner);
            }
            return answer[0];
        } catch (Exception e) {
            return null;
        }

    }

} // end of SimpleInput class
