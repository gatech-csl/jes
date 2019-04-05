package instruments;


import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic square wave instrument implementation
 * which implements envelope , pan, and volume control
 * It has an envelope in reverse shape to normal.
 * @author Andrew Brown and Andrew Sorensen
 */

public final class SquareBackwardsInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	
	/** The points to use in the construction of Envelopes */
	private EnvPoint[] pointArray = new EnvPoint[10];
	
	private int sampleRate;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate and buffersize in addition
	 * to the neccessary frequency relationships 
	 * and volumes for each frequency to be added
	 * the instrument
	 * @param sampleRate 
	 * @param buffersize
	 * @param frequencies the relative freqencies to use
	 * @param volumes the volumes to use for the frequencies
	 */
	public SquareBackwardsInst(int sampleRate){
		this.sampleRate = sampleRate;
		EnvPoint[] tempArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.05, (float)0.2),
			new EnvPoint((float)0.85, (float)0.6),
			new EnvPoint((float)0.98, (float)1.0),
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
		Oscillator wt = new Oscillator(this, Oscillator.SQUARE_WAVE, 
                    this.sampleRate, 2);
		Envelope env = new Envelope(wt, pointArray);
		Volume vol = new Volume(env);
		StereoPan span = new StereoPan(vol);
		SampleOut sout = new SampleOut(span);
	}	
}

