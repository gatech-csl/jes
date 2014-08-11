import javax.swing.*;
import java.text.*;

/**
 * A fork of SimpleInput that adds "Stop" buttons for whatever is displaying
 * the dialog boxes.
 */
public class StoppableOutput {
    private static Stoppable thingToStop;

    /**
     * Sets the thing that will be stopped by the "Stop" buttons on these
     * dialog boxes.
     *
     * @param thing The thing to stop, or null to disable the stop buttons.
     */
    public static void setThingToStop (Stoppable thing) {
        thingToStop = thing;
    }

    /**
     * Method to show a warning to a user
     * @param message the message to display
     */
    public static void showWarning(String message) {
        if (thingToStop == null) {
            SimpleOutput.showWarning(message);
            return;
        }

        message = addNewLines(message);
        safeOutputDialog(message, "Warning Display", JOptionPane.WARNING_MESSAGE);
    }

    /**
     * Method to show an error to a user
     * @param message the message to display
     */
    public static void showError(String message) {
        if (thingToStop == null) {
            SimpleOutput.showError(message);
            return;
        }

        message = addNewLines(message);
        safeOutputDialog(message, "Error Display", JOptionPane.ERROR_MESSAGE);
    }

    /**
     * Method to show information to the user
     * @param message the message to display
     */
    public static void showInformation(String message) {
        if (thingToStop == null) {
            SimpleOutput.showInformation(message);
            return;
        }

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
        Runnable promptStringRunner = new Runnable() {
            public void run() {
                Object[] choices = {"OK", "Stop"};

                int ordinal = JOptionPane.showOptionDialog(
                    /* parentComponent: */  null,
                    /* message: */          message,
                    /* title: */            null,
                    /* optionType: */       JOptionPane.YES_NO_OPTION,
                    /* messageType: */      JOptionPane.QUESTION_MESSAGE,
                    /* icon: */             null,
                    /* options: */          choices,
                    /* initialValue: */     choices[0]
                );

                if (ordinal == 1) {
                    thingToStop.stop();
                }
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
}

