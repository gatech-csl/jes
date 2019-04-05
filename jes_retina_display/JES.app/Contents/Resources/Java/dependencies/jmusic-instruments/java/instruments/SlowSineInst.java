package instruments;


import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic synthesis instrument implementation
 * which with a triable envelope.
 * @author Andrew Brown
 */

public final class SlowSineInst extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	/** The points to use in the construction of Envelopes */
	private EnvPoint[] pointArray = new EnvPoint[10];
	/** The number of channels */
	private int channels;
	/** the sample rate passed to the instrument */
	private int sampleRate;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate.
	 * @param sampleRate 
	 */
	public SlowSineInst(int sampleRate){
	    this(sampleRate, 2);
	}
	/**
	 * A constructor to set an initial 
	 * sampling rate and number of channels.
	 * @param sampleRate 
	 */
	public SlowSineInst(int sampleRate, int channels){
		this.sampleRate = sampleRate;
		this.channels = channels;
		EnvPoint[] tempArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.5, (float)1.0),
			new EnvPoint((float)1.0, (float)0.0)
		};
		pointArray = tempArray;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
	   
	/**
	 * Initialisation method used to build the objects that
	 * this instrument will use
	 */
	public void createChain(){
		Oscillator wt = new Oscillator(this, Oscillator.SINE_WAVE, 
                    this.sampleRate, this.channels);
		Envelope env = new Envelope(wt, pointArray);
		Volume vol = new Volume(env);
		StereoPan span = new StereoPan(vol);
		SampleOut sout = new SampleOut(span);
	}	
}

