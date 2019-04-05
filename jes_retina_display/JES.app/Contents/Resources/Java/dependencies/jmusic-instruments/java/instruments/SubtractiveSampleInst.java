package instruments;

import jm.audio.io.*;
import jm.audio.Instrument;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

public final class SubtractiveSampleInst extends jm.audio.Instrument{
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
	/** The envelope sustain value */
	private double sustain;
	/** low pass filter cutoff */
	private int cutoff;
	/** Envelope attributes */
	private int attack, decay, release;
	/** Depth of filter modulation (0.0 - 1.0)*/
	private double modAmount = 0.9;
	/** Speed of filter modulation in Hertz*/
	private double modRate = 0.05;
	/** The volume of the squarewave sub oscillator */
	private double subAmp = 0.0;
	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Constructor
	 */
	public SubtractiveSampleInst(String fileName){
		this(fileName, 440.00, 500);
	}
	
	public SubtractiveSampleInst(String fileName, double baseFreq){
		this(fileName, baseFreq, 500);
	}
	
 	public SubtractiveSampleInst(String fileName, double baseFreq, int cutoff){
		this(fileName, baseFreq, cutoff, 2, 50, 0.4, 200);
	}
	
	public SubtractiveSampleInst(String fileName, double baseFreq, int cutoff, int attack, int decay, double sustain, int release){
		this.fileName = fileName;
		this.baseFreq = baseFreq;
		this.cutoff = cutoff;
		this.attack = attack;
		this.decay = decay;
		this.release = release;
		this.sustain = sustain;
	}

	//----------------------------------------------
	// Methods
	//----------------------------------------------
	
	public void setModAmount(double val) {
		this.modAmount = val;
	}
	
	public void setModDepth(double val) {
		this.modAmount = val;
	}
	
	public void setModRate(double val) {
		this.modRate = val;
	}
	
	public void setWholeFile(boolean val) {
		this.wholeFile = val;
	}
	
	public void setSubAmp(double val) {
		this.subAmp = val;
	}
	
	/**
	 * Create the Audio Chain for this Instrument 
	 * and assign the primary Audio Object(s). The 
	 * primary audio object(s) are the one or more
	 * objects which head up the chain(s)
	 */
	public void createChain(){
            //define the chain
            SampleIn sin = new SampleIn(this, fileName);
            sin.setWholeFile(wholeFile);
            ReSample reSample = new ReSample(sin, this.baseFreq);
            // modulate filter cutoff
            Oscillator sineMod = new Oscillator(this, Oscillator.SINE_WAVE, sin.getSampleRate(), 
			sin.getChannels(), Oscillator.FREQUENCY, (float)modRate);
            sineMod.setAmp((float) this.modAmount * this.cutoff);
            // sub
            Oscillator subOsc = new Oscillator(this, Oscillator.SQUARE_WAVE, sin.getSampleRate(), 
			sin.getChannels());
	  subOsc.setFrqRatio(0.5f);
	  subOsc.setAmp((float)subAmp);
	  Add adder = new Add(new AudioObject[] {reSample, subOsc});
	  // filter
            Filter filt = new Filter(new AudioObject[] {adder, sineMod}, this.cutoff, Filter.LOW_PASS);
            ADSR env = new ADSR(filt, attack, decay, sustain, release);
            Volume vol = new Volume(env);
            StereoPan span = new StereoPan(vol);
            SampleOut sout = new SampleOut(span);
	}
}
