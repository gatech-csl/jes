package instruments;


import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic triangle wave instrument implementation
 * which implements envelope and volume control
 * @author Andrew Brown and Andrew Sorensen
 */

public final class TriangleRepeatInst extends Instrument{
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
	public TriangleRepeatInst(int sampleRate){
		this.sampleRate = sampleRate;
		EnvPoint[] tempArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.02, (float)1.0),
			new EnvPoint((float)0.15, (float)0.6),
			new EnvPoint((float)0.95, (float)0.2),
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
		Oscillator wt = new Oscillator(this, Oscillator.TRIANGLE_WAVE, 
                    this.sampleRate, 1);
		Envelope env = new Envelope(wt, pointArray);
		Volume vol = new Volume(env);
		Delay delay = new Delay(vol, 4000);
		AudioObject[] sources = {vol, delay};
		Add add = new Add(sources);
		SampleOut sout = new SampleOut(add);
	}	
}

