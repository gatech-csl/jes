import javax.swing.*;
import javax.swing.SwingUtilities;
import java.text.*;

/**
 * Class to make it easy to do output to the user
 * using JOptionPane
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 *
 * 14 May 2009:  Edited by Dorn to ensure all JOptionPane calls to show are threadsafe.
 */
public class SimpleOutput {

    /**
     * Method to show a warning to a user
     * @param message the message to display
     */
    public static void showWarning(String message) {
        message = addNewLines(message);
        safeOutputDialog(message, "Warning Display", JOptionPane.WARNING_MESSAGE);
    }

    /**
     * Method to show an error to a user
     * @param message the message to display
     */
    public static void showError(String message) {
        message = addNewLines(message);
        safeOutputDialog(message, "Error Display", JOptionPane.ERROR_MESSAGE);
    }

    /**
     * Method to show information to the user
     * @param message the message to display
     */
    public static void showInformation(String message) {
        message = addNewLines(message);
        safeOutputDialog(message, "Information Display", JOptionPane.INFORMATION_MESSAGE);
    }

    /**
     * Method to add new line character if the message
     * is too long
     * @param message the input message
     * @return the message with new lines added if needed
     */
    public static String addNewLines(String message) {
        BreakIterator boundary =
            BreakIterator.getLineInstance();
        boundary.setText(message);
        int start = boundary.first();
        String result = "";
        String currLine = "";
        String temp = null;

        // loop till no more possible line breaks
        for (int end = boundary.next();
                end != BreakIterator.DONE;
                start = end, end = boundary.next()) {
            // get string between start and end
            temp = message.substring(start, end);

            /* if adding that to the current line
             * would make it too long then add current
             * to result followed by a newline and
             * reset current
             */
            if (temp.length() + currLine.length() > 100) {
                result = result + currLine + "\n";
                currLine = temp;
            }
            // else add the segment to the current line
            else {
                currLine = currLine + temp;
            }
        }

        // if no line breaks use the original message
        if (result.length() == 0) {
            result = message;
        }
        // else add any leftover parts
        else {
            result = result + currLine;
        }

        return result;
    }

    private static void safeOutputDialog(final String message, final String title, final int messageType) {

        Runnable promptStringRunner =
        new Runnable() {
            public void run() {
                JOptionPane.showMessageDialog(null, message, title, messageType);
            }
        };

        try {
            if (SwingUtilities.isEventDispatchThread()) {
                promptStringRunner.run();
            } else {
                SwingUtilities.invokeAndWait(promptStringRunner);
            }
        } catch (Exception e) {
            //do nothing
        }

    }

} // end of SimpleOutput class
