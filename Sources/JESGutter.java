import java.awt.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.text.*;
import java.io.*;
import java.awt.font.TextAttribute;
import java.text.*;
import java.util.*;
import java.util.regex.*;

/**
 * The JES Gutter
 * Created for the Jython Environment for Students
 * The JES Gutter is a side bar that shows useful contextual information
 * about the document being currently edited.  It shows line numbers, block
 * marking, and demarcates def statements.
 */
public class JESGutter extends JComponent implements DocumentListener
{
    /* Line indention levels */
    private Vector indents = new Vector();

    /* Line YLocation levels */
    private int[] ylocs;

    /* Gutter Font */
    private Font gutterFont = new Font("Monospaced", Font.PLAIN, 10);

    /* Regular expression for matching newlines */
    private Pattern newlineReg = Pattern.compile("\n");

    /* The Text Component the gutter marks lines */
    private JEditorPane text = new JEditorPane();

    /* The number of lines in the document */
    private int numLines = 0;

    /* The number of lines in the document before a change */
    private int oldLines = 0;

    /* The font used in the editor */
    private Font editorFont = new Font("Monospaced", Font.PLAIN, 12);

    /* Line Height */
    private float lineHeight = 12.0f;

    /*Line mark */
    private int lineMark = -1;

    private static final long serialVersionUID = 7526471155622776147L;

    /**
     * Creates a Gutter object with a given TextComponent and Font.
     * @param tc the TextComponent
     * @param f the Font
     */
    public JESGutter(JEditorPane tc, Font f)
    {
        text = tc;
        text.getDocument().addDocumentListener(this);
        editorFont = f;
        lineHeight = editorFont.getSize2D();
    }


    /**
     * Adds a line to the gutter.  includes indentation information and y height.
     * @param line the line number being added
     * @param indent the indentation level of the line
     * @param height the Y location information of the bottom of the line
     */
    public void setLine(int line, int indent, int height)
    {
    }

    /**
     * Sets the document for the gutter to listen for changes in.  When a change
     * occurs check to see if a newline was added or removed.
     * @param doc the document to listen to
     */
    public void setDocument(Document doc)
    {
        doc.addDocumentListener(this);
    }

    /**
     * Sets the TextComponent the gutter models itself after
     * @param tc the TextComponent
     */
    public void setTextComponent(JEditorPane tc)
    {
        text = tc;
    }

    /**
     * Sets the line do demarcate on the gutter
     * @param line the line to mark
     */
    public void setLineMark(int line)
    {
        lineMark = line;
    }

    /**
     * Removes the line demarcation from the gutter
     */
    public void removeLineMark()
    {
        lineMark = -1;
    }

    /**
     * Paints gutter information to the graphics object
     */
    public void paint(Graphics g)
    {
        Element root = text.getDocument().getDefaultRootElement();
        int count = root.getElementCount();
        Rectangle clip = g.getClipBounds();
        Point topClip = new Point(0, clip.y);
        Point bottomClip = new Point(0, clip.y + clip.height);
        g.setFont(gutterFont);
        int start;
        int bottom;
        try{
            start = text.viewToModel(topClip);
            start =  root.getElementIndex(start - 1);
        }
        catch(Exception e){
            start = 0;
        }
        try{
            bottom = text.viewToModel(bottomClip);
            bottom = root.getElementIndex(bottom + 1);
        }
        catch(Exception e){
            bottom = count;
        }
        for (int i = start; i <= bottom; i++)
        {
            try
            {
                int startChar = root.getElement(i).getStartOffset();
                if ((i + 1) == lineMark)
                    g.setColor(Color.green);
                g.drawString((new Integer(i + 1)).toString(), 3, text.modelToView(startChar).y + 10);
                if ((i + 1) == lineMark)
                    g.setColor(Color.black);
            }catch (Exception e){/*This is inelegant, oh well, it's the behavior I want.*/}
        }
        super.paint(g);
    }


    /**
     * Recounts the number of lines in the Document, and updates the lines
     * list to have the new last few lines.
     */
    public void updateLines()
    {
        numLines = text.getDocument().getDefaultRootElement().getElementCount();
        repaint();
    }

    /**
     * Gives notification that an attribute or set of attributes changed.
     * @param e The DocumentEvent describing the change
     */
    public void changedUpdate(DocumentEvent e)
    {
    }

    /**
     * Gives notification that there was text inserted into the document.
     * @param e the DocumentEvent describing the insert
     */
    public void insertUpdate(DocumentEvent e)
    {
        try
        {
            Document doc = e.getDocument();
            int offset = e.getOffset();
            int length = e.getLength();
            Matcher m = newlineReg.matcher(doc.getText(offset, length));
            if (m.find())
                updateLines();
        }catch (Exception ex){}
    }

    /**
     * Gives notifications that text was removed from the document.
     * @param e the DocumentEvent describing the removal
     */
    public void removeUpdate(DocumentEvent e)
    {
        try
        {
            Document doc = e.getDocument();
            int offset = e.getOffset();
            int length = e.getLength();
            Matcher m = newlineReg.matcher(doc.getText(offset, length));
            if (m.find())
                updateLines();
        }catch (Exception ex){}
    }

  }