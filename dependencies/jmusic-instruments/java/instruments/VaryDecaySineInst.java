package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic sine instrument implementation
 * which changes the decay envelope on each instantiation.
 * @author Andrew Sorensen and Andrew Brown
 */

public final class VaryDecaySineInst extends jm.audio.Instrument{
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
	public VaryDecaySineInst(int sampleRate){
	    this(sampleRate, 2);
	}
	/**
	 * A constructor to set an initial 
	 * sampling rate and number of channels.
	 * @param sampleRate 
	 */
	public VaryDecaySineInst(int sampleRate, int channels){
		this.sampleRate = sampleRate;
		this.channels = channels;
		EnvPoint[] tempArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.001, (float)1.0),
			new EnvPoint((float)0.1, (float)0.5),
			new EnvPoint((float)(Math.random() * 0.4 + 0.3), (float)0.05),
			new EnvPoint((float)(Math.random() * 0.3 + 0.7), (float)0.0)
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
                    this.sampleRate, channels);
		Envelope env = new Envelope(wt, pointArray);
		Volume vol = new Volume(env);
		StereoPan span = new StereoPan(vol);
		SampleOut sout = new SampleOut( span);
	}	
}

