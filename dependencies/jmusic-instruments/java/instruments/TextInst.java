package instruments;



import jm.audio.io.*;
import jm.audio.Instrument;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;
import java.awt.*;

public final class TextInst extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	/** the name of the sample file */
	private String fileName;
	/** How many channels is the sound file we are using */
	private int numOfChannels;
	/** the base frequency of the sample file to be read in */
	private double baseFreq;
	/** should we play the wholeFile or just what we need for note duration */
	private boolean wholeFile;
	/** The points to use in the construction of Envelopes */
	private EnvPoint[] pointArray = new EnvPoint[10];
	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Constructor
	 */
	public TextInst(){
		this.fileName = openFile();
                this.baseFreq = 440.0;
		this.wholeFile = false;
	}
        
        public TextInst(String fileName){
		this(fileName, 440.00);
	}
	
 	public TextInst(String fileName, double baseFreq){
		this(fileName, baseFreq, false);
	}

	public TextInst(String fileName, double baseFreq, boolean wholeFile){
		this.fileName = fileName;
		this.baseFreq = baseFreq;
		this.wholeFile = wholeFile;
		
	}

	//----------------------------------------------
	// Methods
	//----------------------------------------------
	/**
	 * Create the Audio Chain for this Instrument 
	 * and assign the primary Audio Object(s). The 
	 * primary audio object(s) are the one or more
	 * objects which head up the chain(s)
	 */
	public void createChain(){
		//define the chain
		TextIn tin = new TextIn(this, fileName, 44100, 1);
		SampleOut sout = new SampleOut(tin);
	}
        
        // read a file
        private String openFile() {
            FileDialog loadFile = new FileDialog(new Frame(), 
                "Select any file to be treated as audio data.", 
                FileDialog.LOAD);
            loadFile.show();
            String fileName = loadFile.getDirectory() + loadFile.getFile();
            if (fileName == null) {
                System.out.println("jMusic TextInst error: No file was selected, exiting program.");
                System.exit(0);
            }
            return fileName;
        }
}
