import java.awt.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.text.*;
import java.io.*;
import java.util.*;
import java.util.regex.*;

/**
 * Highlights jython syntax in a Document
 * Created for the Jython Environment for Students (JES)
 * Hilghights keywords and environment words that are defined
 * for it.  It will also highlight single-line comments that start
 * with '#', and single-line strings that start with "'" or '"'.
 * @author Adam Wilson, awilson@cc.gatech.edu
 *
 * May 28 2009: Removed unused getLineStart, getLineEnd, addKeyword, addEnvironmentWord,and
 *				isEnvWord methods. -Buck
 */
 public class HighlightingStyledDocument extends DefaultStyledDocument
{
    /* Keyword text style */
    private SimpleAttributeSet keywordStyle = new SimpleAttributeSet();

    /* Environment word text style */
    private SimpleAttributeSet environmentWordStyle = new SimpleAttributeSet();

    /* Comment Style */
    private SimpleAttributeSet commentStyle = new SimpleAttributeSet();

    /* String Style */
    private SimpleAttributeSet stringStyle = new SimpleAttributeSet();

    /* Parentheses Style */
    private SimpleAttributeSet rParenStyle = new SimpleAttributeSet();
    private SimpleAttributeSet lParenStyle = new SimpleAttributeSet();

    /* Default Style */
    private SimpleAttributeSet defaultStyle = new SimpleAttributeSet();

    /* Jython keywords */
    private Vector<String> keywords = new Vector<String>();

    /* Gutters */
    private Vector gutters = new Vector();

    /* Parentheses */
    private Vector<Integer> lParens = new Vector<Integer>();

    /* Jython environment words */
    private Vector<String> environmentWords = new Vector<String>();

    /* Generated Regular expression for keywords */
    private Pattern keyReg = Pattern.compile("");

    /* Generated regular expression for environment words */
    private Pattern envReg = Pattern.compile("");

    /* Regular Expression for parentheses */
    //    private Patter extraParenReg = Pattern.compile("[\)\(]");

    // private Patter missingParenReg = Pattern.compile("\(\(+.*\)");

    /* Regular Expression for comments */
    private Pattern commentReg = Pattern.compile("#++[^\n]*");

    /* Regular Expression for double quote Strings */
    private Pattern doubleStringReg = Pattern.compile("\"[^\n\"]*\"");

    /* Regular Expression for single quote strings */
    private Pattern singleStringReg = Pattern.compile("'[^\n']*'");

    /* Regular Expression for string & comments */
    /* "\\\"" - why not?!? \p" */
    private Pattern stringComments = Pattern.compile("(#[^\n]*|\"([^\n\"\\x5c]|(\\x5c\")|(\\x5c))*\"|'([^\n'\\x5c]|(\\x5c')|(\\x5c))*')");

    /* Regular Expression to match multi-line strings */
    private Pattern mlString = Pattern.compile("\"\"\".*\"\"\"", Pattern.DOTALL);

    /* Regular Expression to match triple qoutes */
    private Pattern triQuote = Pattern.compile("\"\"\"");

	/** The system specific line separator String. */
    public static String newline = System.getProperty("line.separator");

    private static final long serialVersionUID = 7526471155622776147L;

    /**
     * Overrides the default method from DefaultStyledDocument. Calls appropriate
     * syntax highlighting code and then class super.
     * @param offs the starting offset >= 0
     * @param str the string to insert; does nothing with null/empty strings
     * @param a the attributes for the inserted content
     */
    public void insertString(int offs, String str, AttributeSet a) throws BadLocationException
    {
        super.insertString(offs, str, a);
        updateHighlightingInRange(offs, str.length());
    }

    /**
     * Overrides the default method from DefaultStyledDocument. Calls appropriate
     * syntax highlighting code and then class super.
     * @param e the DocumentEvent
     */
    protected void fireRemoveUpdate(DocumentEvent e)
    {
        int offset = e.getOffset();
        int length = e.getLength();
        updateHighlightingInRange(offset - 1, 0);
        super.fireRemoveUpdate(e);
    }


    /**
     * Looks at a given range of text in a document and highlights it
     * according to keywords, environment, strings, and comments.
     * @param offset where in the document the change started
     * @param length the length of change measured from the offset
     */
    public void updateHighlightingInRange(int offset, int length)
    {
        try
        {
            //int start = getLineStart(textAll, offset);
            //int end = getLineEnd(textAll, offset + length);

            Element defaultElement = getDefaultRootElement();
            int line = defaultElement.getElementIndex(offset);
            int lineend = defaultElement.getElementIndex(offset + length);
            int start = defaultElement.getElement(line).getStartOffset();
            int end = defaultElement.getElement(lineend).getEndOffset();
            int endPoint = getLength();


	    String fullText = getText(0, endPoint);
            String text = getText(start, end - start);
            setCharacterAttributes(start, end - start, defaultStyle, true);

            //Do Block Highlighting:

            //Find and highlight keywords:
            Matcher m = keyReg.matcher(text);
            while (m.find())
                setCharacterAttributes(start + m.start(), m.end() - m.start(), keywordStyle, true);

            //Find and highlight keywords:
            m = envReg.matcher(text);
            while (m.find())
                setCharacterAttributes(start + m.start(), m.end() - m.start(), environmentWordStyle, true);

            //Find and highlight Comments and strings:
            m = stringComments.matcher(text);
            while (m.find())
            {
                //System.out.println("Matched: " + getText(start + m.start(), m.end() - m.start()));
                if (text.charAt(m.start()) == '#')
                    setCharacterAttributes(start + m.start(), m.end() - m.start(), commentStyle, true);
                if (text.charAt(m.start()) == '\'' || text.charAt(m.start()) == '"')
                    setCharacterAttributes(start + m.start(), m.end() - m.start(), stringStyle, true);
            }

	    //Matches Multi-line strings starting with triple quotes:
            /*m = mlString.matcher(textAll);
	      while(m.find())
                setCharacterAttributes(m.start(), m.end() - m.start(), stringStyle, true);*/

	    // Build lParen Vector and find and highlight missing or extra parentheses
	    // make sure we check ENIRE document for it

	    for(int x = start; x < end; x++){
		char c = text.charAt(x-start);
		Integer indexVal = new Integer(x);

		if(c == '(' && !(isString(x) || isComment(x))) {
		    lParens.add(indexVal);
		} else if(c == ')' && !(isString(x) || isComment(x))) {
		    if(lParens.isEmpty()) {
			setCharacterAttributes(x, 1, rParenStyle, true); // color right paren
		    } else {
			lParens.remove(lParens.size() - 1); // remove the vector from the lparen vector
		    }
		}
	    }
	    for(Enumeration e = lParens.elements(); e.hasMoreElements();) {
		int index = ((Integer)e.nextElement()).intValue();
		setCharacterAttributes(index, 1, lParenStyle, true); // color left paren

	    }
	    lParens.clear();



        }
        catch( Exception e){}
    }

    /**
     * Looks at a location in the given document and determines if
     * that location is inside a string.  Supports """ for multi-line
     * strings.
     * PRE: Strings have been colorized
     * @param offset The location to check for string-ness
     * @return True for is a string, false for is not a string
     */
    private boolean isString(int offset)
    {
	return getCharacterElement(offset).getAttributes().isEqual(stringStyle);
    }

    /**
     * Looks at a location inside a document and determines if it is
     * a comment.
     * PRE: Comments have been colorized
     * @param offset the location to check for comment-ness
     * @return true for is a comment, false for is not a comment
     */
    private boolean isComment(int offset)
    {
	return getCharacterElement(offset).getAttributes().isEqual(commentStyle);
    }

    /**
     * Sets a collection of keywords to highlight.
     * @param words an array of all the words
     */
    public void setKeywords(String[] words)
    {
        keywords.clear();
        for(int i = 0; i < words.length; i++)
        {
            keywords.add(words[i]);
        }
        compileKeywords();
    }

    /**
     * Sets a collection of environment words to highlight.
     * @param words an array of all the words
     */
    public void setEnvironmentWords(String[] words)
    {
        environmentWords.clear();
        for(int i = 0; i < words.length; i++)
        {
            environmentWords.add(words[i]);
        }
        compileEnvironmentWords();
    }

    /**
     * Sets the style of text to use for keywords
     * @param style the new text style
     */
    public void setKeywordStyle(SimpleAttributeSet style)
    {
        keywordStyle = style;
    }

    /**
     * Sets the style of text to use for environment words
     * @param style the new text style
     */
    public void setEnvironmentWordStyle(SimpleAttributeSet style)
    {
        environmentWordStyle = style;
    }

    /**
     * Sets the style of text to use for comments
     * @param style the new text style
     */
    public void setCommentStyle(SimpleAttributeSet style)
    {
        commentStyle = style;
    }

    /**
     * Sets the style of text to use for strings
     * @param style the new text style
     */
    public void setStringStyle(SimpleAttributeSet style)
    {
        stringStyle = style;
    }

    /**
     * Sets the style of text to use for invalid Left Parens
     * @param style the new text style
     */
    public void setLParenStyle(SimpleAttributeSet style)
    {
        lParenStyle = style;
    }

    /**
     * Sets the style of text to use for invalid Right Parens
     * @param style the new text style
     */
    public void setRParenStyle(SimpleAttributeSet style)
    {
        rParenStyle = style;
    }

    /**
     * Sets the default style of text to use
     * @param style the new text style
     */
    public void setDefaultStyle(SimpleAttributeSet style)
    {
        defaultStyle = style;
    }

    /**
     * Recompiles the regular expression used for matching key words.
     * Takes the collection of keywords and generates a regular expression
     * string.  It then compiles that string into the Pattern class and
     * stores it in keyReg.
     * Example: if the keywords were "if" and "for", the regular expression
     * would be: "\W(if|for)\W".  The \W isolate the keywords by non-word
     * characters.
     */
    private void compileKeywords()
    {
        String exp = new String();
        exp = "\\b("; 	//Start the expression to match non-word characters,
                        //i.e. [^a-zA-Z0-9], and then start the OR block.
        for (int i = 0; i < keywords.size(); i++)
        {
            if (i == 0)
                exp = exp + ((String)keywords.elementAt(i)).trim();
            exp = exp + "|" + ((String)keywords.elementAt(i)).trim();
        }
        exp = exp + ")\\b";
        keyReg = Pattern.compile(exp);
    }

    /**
     * Recompiles the regular expression used for matching environment words.
     * Takes the collection of environment words and generates a regular expression
     * string.  It then compiles that string into the Pattern class and
     * stores it in envReg.
     * Example: if the envwords were "if" and "for", the regular expression
     * would be: "\W(if|for)\W".  The \W isolate the envwords by non-word
     * characters.
     */
    private void compileEnvironmentWords()
    {
        String exp = new String();
        exp = "\\b("; 	//Start the expression to match non-word characters,
                        //i.e. [^a-zA-Z0-9], and then start the OR block.
        for (int i = 0; i < environmentWords.size(); i++)
        {
            if (i == 0)
                exp = exp + ((String)environmentWords.elementAt(i)).trim();
            exp = exp + "|" + ((String)environmentWords.elementAt(i)).trim();
        }
        exp = exp + ")\\b";
        envReg = Pattern.compile(exp);
    }


}//END OF HighlightingStyledDocument Class
