package instruments;

import jm.audio.io.*;
import jm.audio.Instrument;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

public final class ReverseResampledInst extends jm.audio.Instrument{
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
	public ReverseResampledInst(String fileName){
		this(fileName, 440.00);
	}
	
 	public ReverseResampledInst(String fileName, double baseFreq){
		this(fileName, baseFreq, false);
	}

	public ReverseResampledInst(String fileName, double baseFreq, boolean wholeFile){
		this.fileName = fileName;
		this.baseFreq = baseFreq;
		this.wholeFile = wholeFile;
		//envelope
		EnvPoint[] tempArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.1, (float)1.0),
			new EnvPoint((float)0.4, (float)0.5),
			new EnvPoint((float)0.9, (float)0.3),
			new EnvPoint((float)1.0, (float)0.0)
		};
		pointArray = tempArray;
		
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
		NoteBufferReversed nb = new NoteBufferReversed(sin);
		ReSample reSample = new ReSample(nb, this.baseFreq);
                Volume vol = new Volume(reSample, (float)1.0);
                Envelope env = new Envelope(vol, pointArray);
		SampleOut sout = new SampleOut(env, "jmusic.tmp");
	}
}
