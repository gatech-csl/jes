import java.awt.Graphics;
import java.awt.print.PageFormat;
import java.awt.print.Printable;

/**
 * This is a simple wrapper for java.awt.print.Printable that passes on
 * the print() call to a printPage() method. This must be done because
 * Jython 2.5 doesn't let you define a method named print.
 */
abstract public class JESPrintable implements Printable {
    abstract public int printPage (Graphics graphics, PageFormat pageFormat, int pageIndex);

    public int print (Graphics graphics, PageFormat pageFormat, int pageIndex) {
        return printPage(graphics, pageFormat, pageIndex);
    }
}

