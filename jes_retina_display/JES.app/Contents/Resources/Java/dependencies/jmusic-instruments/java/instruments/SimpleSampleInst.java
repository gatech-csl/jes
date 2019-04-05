package instruments;

import jm.audio.io.*;
import jm.audio.Instrument;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

public final class SimpleSampleInst extends jm.audio.Instrument{
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
	/** The points for the break point envelope */
	private double[] points;
    private SampleOut sout;
	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Constructor
	 */
	public SimpleSampleInst(String fileName){
		this(fileName, 440.00);
	}
	
 	public SimpleSampleInst(String fileName, double baseFreq){
		this(fileName, baseFreq, false);
	}
	
	public SimpleSampleInst(String fileName, double baseFreq, double[] points){
		this(fileName, baseFreq, false, points);
	}

	public SimpleSampleInst(String fileName, double baseFreq, boolean wholeFile){
		this(fileName, baseFreq, wholeFile, 
			new double[] {0.0, 0.0, 0.01, 1.0, 0.99, 1.0, 1.0, 0.0});
	}
	
	public SimpleSampleInst(String fileName, double baseFreq, boolean wholeFile, double[] points){
		this.fileName = fileName;
		this.baseFreq = baseFreq;
		this.wholeFile = wholeFile;
		this.points = points;
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
            SampleIn sin = new SampleIn(this, fileName);
            
            ReSample reSample = new ReSample(sin, this.baseFreq);
            Volume vol = new Volume(reSample);
            StereoPan span = new StereoPan(vol);
            if (wholeFile) {
                sin.setWholeFile(wholeFile);	
                if(output == RENDER) sout = new SampleOut(span);
            } 
            else {
                Envelope env = new Envelope(span, points);
                if(output == RENDER) sout = new SampleOut(env);
            }
	}
}
