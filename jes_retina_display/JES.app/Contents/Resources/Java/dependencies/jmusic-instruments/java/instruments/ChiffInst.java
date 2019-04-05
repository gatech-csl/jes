package instruments;

//==========================================================
// File:                 ChiffInst.java
// Package:              inst
// Function:             basic implementation of a white noise burst
// Author:               Andrew Brown
// Environment:          JDK1.1 / jMusic 1.1
//==========================================================
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.audio.Instrument;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic white noise synthesis implementation
 * which provides an onset burst of noise.
 * @author Andrew Brown
 */

public final class ChiffInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	
	/** The points to use in the construction of Envelopes */
	private EnvPoint[] pointArray = new EnvPoint[10];
	private int channels;
	private int sampleRate;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate.
	 * @param sampleRate 
	 */
	public ChiffInst(int sampleRate){
	    this(sampleRate, 2);
	}
	
	/**
	 * A second constructor to set an initial 
	 * sampling rate and number of channels.
	 * @param sampleRate 
	 * @param channels (i.e., 1 = mono, 2 = stereo)
	 */
	public ChiffInst(int sampleRate, int channels){
		this.sampleRate = sampleRate;
		this.channels = channels;
		EnvPoint[] tempArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.03, (float)0.6),
			new EnvPoint((float)0.1, (float)0.01),
			new EnvPoint((float)1.0, (float)0.0)
		};
		pointArray = tempArray;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
	   
	/**
	 * Initialisation method used to build a chain of the objects that
	 * this instrument will use.
	 */
	public void createChain(){
		Noise noise = new Noise(this, Noise.WHITE_NOISE, this.sampleRate, this.channels);
		Envelope env = new Envelope(noise, pointArray);
		Volume vol = new Volume(env, (float)1.0);
		StereoPan span = new StereoPan(vol);
		SampleOut sout = new SampleOut(span);
	}	
}

