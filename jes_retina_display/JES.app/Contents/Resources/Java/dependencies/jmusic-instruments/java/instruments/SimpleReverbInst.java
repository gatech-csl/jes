package instruments;



import jm.audio.io.*;
import jm.audio.Instrument;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

public final class SimpleReverbInst extends jm.audio.Instrument{
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
	public SimpleReverbInst(String fileName){
		this(fileName, 440.00);
	}
	
 	public SimpleReverbInst(String fileName, double baseFreq){
		this(fileName, baseFreq, false);
	}

	public SimpleReverbInst(String fileName, double baseFreq, boolean wholeFile){
		this.fileName = fileName;
		this.baseFreq = baseFreq;
		this.wholeFile = wholeFile;
		//envelope
		EnvPoint[] tempArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.1, (float)1.0),
			new EnvPoint((float)0.4, (float)0.5),
			new EnvPoint((float)0.95, (float)0.4),
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
		SampleIn sin = new SampleIn(this,fileName);
		SampleIn sin2 = new SampleIn(this,fileName);
		SampleIn sin3 = new SampleIn(this,fileName);
		SampleIn sin4 = new SampleIn(this,fileName);

		
		Comb comb = new Comb(sin,20,0.5);
		Comb comb2 = new Comb(sin2,100,0.4);
		Comb comb3 = new Comb(sin3,70,0.6);
		Comb comb4 = new Comb(sin4,50,0.5);
		AudioObject[] array = {comb,comb2,comb3,comb4};
		Add add = new Add(array);
		//AllPass ap = new AllPass(add,50,0.9);
		Filter filter = new Filter(add,2000.0, Filter.LOW_PASS);
		Filter filter2 = new Filter(filter,2000.0,Filter.HIGH_PASS);
		ReSample reSample = new ReSample(filter2, this.baseFreq);
	    	Volume vol = new Volume(reSample);
	    	Envelope env = new Envelope(vol, pointArray);
		StereoPan span = new StereoPan(env);
		SampleOut sout = new SampleOut(span);
	}
}
