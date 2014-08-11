package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;


public final class RTPluckInst extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	/** The number of channels */
	private int channels;
	/** the sample rate passed to the instrument */
	private int sampleRate;
        /** The sustain value */
        private double feedback;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 */
	public RTPluckInst(int sampleRate){
	    this(sampleRate, 1);
	}
	/**
	 * A constructor to set an initial 
	 * sampling rate and number of channels.
	 * @param sampleRate 
	 */
	public RTPluckInst(int sampleRate, int channels){
		this(sampleRate, channels, 0.5);
	}
        
        /**
	 * A constructor to set an initial 
	 * sampling rate and number of channels.
	 * @param sampleRate 
         * @param channels
         * @param feedback
	 */
	public RTPluckInst(int sampleRate, int channels, double feedback){
		this.sampleRate = sampleRate;
		this.channels = channels;
		this.feedback = feedback;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
	   
	/**
	 * Initialisation method used to build the objects that
	 * this instrument will use
	 */
	public void createChain(){
		Pluck plk = new Pluck(this, sampleRate, channels, feedback);
		Volume vol = new Volume(plk);
		StereoPan pan = new StereoPan(vol);
		Envelope env = new Envelope(pan, new double[] {0.0, 1.0, 0.9, 1.0, 1.0, 0.0});
	}	
}

