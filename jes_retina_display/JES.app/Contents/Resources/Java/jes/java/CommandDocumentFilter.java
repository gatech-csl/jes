// JES - Jython Environment for Students
// (C) 2014 Matthew Frazier and Mark Guzdial
// License: GNU GPL v2 or later, see jes/help/JESCopyright.txt for details

import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.DocumentFilter;
import javax.swing.text.DocumentFilter.FilterBypass;

/**
 * This class prevents text from being entered before a particular position
 * in the document. It's written in Java for speed.
 */
public class CommandDocumentFilter extends DocumentFilter {
    private boolean enabled = false;
    private int inputLimit = 0;
    private AttributeSet overrideAttr = null;

    public void enable (int limit, AttributeSet attr) {
        enabled = true;
        inputLimit = limit;
        overrideAttr = attr;
    }

    public void disable () {
        enabled = false;
        overrideAttr = null;
    }

    public void insertString (FilterBypass bypass, int offset, String string, AttributeSet attr) {
        try {
            if (!enabled) {
                bypass.insertString(offset, string, attr);
            } else if (offset >= inputLimit) {
                string = string.replace("\t", "  ");
                if (overrideAttr != null) {
                    attr = overrideAttr;
                }

                bypass.insertString(offset, string, attr);
            }
        } catch (BadLocationException exc) {
            // Ignored
        }
    }

    public void replace (FilterBypass bypass, int offset, int length, String string, AttributeSet attr) {
        try {
            if (!enabled) {
                bypass.replace(offset, length, string, attr);
            } else {
                int endOffset = offset + length;
                string = string.replace("\t", "  ");
                if (overrideAttr != null) {
                    attr = overrideAttr;
                }

                if (offset >= inputLimit && endOffset >= inputLimit) {
                    bypass.replace(offset, length, string, attr);
                } else if (offset < inputLimit && endOffset >= inputLimit) {
                    int newLength = length - (inputLimit - offset);
                    bypass.replace(inputLimit, newLength, string, attr);
                }
            }
        } catch (BadLocationException exc) {
            // Ignored
        }
    }

    public void remove (FilterBypass bypass, int offset, int length) {
        try {
            if (!enabled) {
                bypass.remove(offset, length);
            } else {
                int endOffset = offset + length;

                if (offset >= inputLimit && endOffset >= inputLimit) {
                    bypass.remove(offset, length);
                } else if (offset < inputLimit && endOffset >= inputLimit) {
                    int newLength = length - (inputLimit - offset);
                    bypass.remove(inputLimit, newLength);
                }
            }
        } catch (BadLocationException exc) {
            // Ignored
        }
    }
}

