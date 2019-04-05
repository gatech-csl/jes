// JES - Jython Environment for Students
// (C) 2014 Matthew Frazier and Mark Guzdial
// License: GNU GPL v2 or later, see jes/help/JESCopyright.txt for details

import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.text.BadLocationException;
import javax.swing.text.Document;

/**
 * This serves as a proxy for a class extending InputBuffer.
 * Whenever an input limit is set, it slices out the text and passes it
 * to the InputBuffer whenever the document's text updates.
 */
public class CommandDocumentListener implements DocumentListener {
    public static class InputBuffer {
        private String currentInput;

        public String getCurrentInput () {
            return currentInput;
        }

        public void setCurrentInput (String text) {
            currentInput = text;
        }
    }

    private InputBuffer buffer = null;
    private boolean enabled = false;
    private int inputLimit = 0;

    public CommandDocumentListener (InputBuffer buffer) {
        this.buffer = buffer;
    }

    public void enable (int limit) {
        enabled = true;
        inputLimit = limit;
    }

    public void disable () {
        enabled = false;
    }

    public void changedUpdate (DocumentEvent event) {
        if (enabled) {
            handleUpdate(event);
        }
    }

    public void insertUpdate (DocumentEvent event) {
        if (enabled) {
            handleUpdate(event);
        }
    }

    public void removeUpdate (DocumentEvent event) {
        if (enabled) {
            handleUpdate(event);
        }
    }

    private void handleUpdate (DocumentEvent event) {
        Document doc = event.getDocument();
        int length = doc.getLength();
        try {
            String text = doc.getText(inputLimit, length - inputLimit);
            buffer.setCurrentInput(text.replaceAll("\n+$", ""));
        } catch (BadLocationException exc) {
            // Ignored
        }
    }
}

