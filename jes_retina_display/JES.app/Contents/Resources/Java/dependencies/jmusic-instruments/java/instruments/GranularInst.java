package instruments;

/**
 * GranularInst.java
 * Author: Timothy Opie
 * Last Modified: 04/08/2002
 * Designed to function with jMusic
 * by Andrew Brown and Andrew Sorenson
 */

import jm.audio.io.*;
import jm.audio.Instrument;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;
import jm.audio.io.RTIn;

public final class GranularInst extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	// the name of the sample file
	private String fileName;
	// How many channels is the sound file we are using
	private int numOfChannels;
	// the base frequency of the sample file to be read in
	//private double baseFreq;
	// should we play the wholeFile or just what we need for note duration
	//private boolean wholeFile;
	// The points to use in the construction of Envelopes
	private float[] envelopeArray;
	private float[] durationArray; 
	private float[] gpsArray;
	private float[] freqArray;
	private boolean premapped = false;
	private boolean ri = false;
	private boolean rgd = false;
	private boolean rf = false;	
	private Granulator grain;
        private Volume vol;
        private StereoPan pan;
	// used to define the audio input type
	private int sounds;
	public static final int SINE_WAVE = 0;
	public static final int COSINE_WAVE = 1;
	public static final int TRIANGLE_WAVE = 2;
	public static final int SQUARE_WAVE = 3;
	public static final int SAWTOOTH_WAVE = 4;
        public static final int SAWDOWN_WAVE = 5;
	public static final int SABERSAW_WAVE = 6;
	public static final int MICROPHONE = 13;
	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	public GranularInst(String fileName){
		// Use this constructor when you want to granulate an audio file.
		// Only the name of the audio file is required
		this.fileName = fileName;
                this.numOfChannels = 2;
		this.sounds = 7;
	}
	
	public GranularInst(int sounds){
		/**
    		 * The variable sounds is an integer used to select 
		 * which sound source type will be used.
		 * It will be defined as such:
		 * SINE WAVE = 0
		 * COSINE WAVE = 1
		 * TRIANGLE WAVE = 2
		 * SQUARE WAVE = 3
		 * SAWTOOTH WAVE = 4
		 * SAWDOWN WAVE = 5
		 * SABERSAW WAVE = 6
		 * AUDIO FILE = 7
		 * MICROPHONE = 13
		 *
		 * Use this constructor when you want to granulate internally
		 * produced audio. Note: you can still granulate audio files
		 * if you use this constructor, but it will assume the audio 
		 * file has the name song1.au.
		 */
		this.sounds = sounds;
                this.numOfChannels = 2;
		this.fileName = "song1.au";
	}
	
	public GranularInst(int sounds, float[] durArr, float[] gpsArr, float[] freqArr){
		/**
		 * This lets you define envelopes as control parameters for
		 * the Granulator.
		 *
    		 * The variable sounds is an integer used to select 
		 * which sound source type will be used.
		 * Like previous constructor 
		 *
		 * Use this constructor when you want to granulate internally
		 * produced audio. Note: you can still granulate audio files
		 * if you use this constructor, but it will assume the audio 
		 * file has the name song1.au.
		 */
		this.sounds = sounds;
		this.durationArray = durArr;
		this.gpsArray = gpsArr;
		this.freqArray = freqArr;
                this.numOfChannels = 2;
		this.fileName = "song1.au";
		this.premapped = true;
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
	    // define the chain
	    if (sounds<0 || sounds>6){
		if (sounds>10){
		    // if sounds is > 10 then the microphone is the input
		    // source. Default is 11, but this way it doesn't matter
		    // if a wrong number gets inputed 
		    // (8820 = buffer length of 1/5 of a second)
		    RTIn grin = new RTIn(this,44100,2,8820);
		    //if (premapped) {
//			grain = new Granulator(grin,durationArray,gpsArray,freqArray,ri,rgd,rf);
//		    } else {
			grain = new Granulator(grin, 44100, 2, 50,100);
		   // } 
		    vol = new Volume(grain,0.5f);
        	    Volume vol2 = new Volume(vol,0.1f);
        	    pan = new StereoPan(vol2);
	            SampleOut sout = new SampleOut(pan);
		} else {
		    // if sounds is < 0 or > 6 and < 11 then it will
		    // process an audio file. Default is 7.  Again it is 
		    // very open ended to accommodate wrong input numbers. 
        	    SampleIn grin = new SampleIn(this, this.fileName);
		    //if (premapped) {
//			grain = new Granulator(grin,durationArray,gpsArray,freqArray,ri,rgd,rf);
//		    } else {
			grain = new Granulator(grin,44100, 2, 50,100);
		    //} 
		    vol = new Volume(grain,0.5f);
        	    Volume vol2 = new Volume(vol,0.1f);
        	    pan = new StereoPan(vol2);
                    SampleOut sout = new SampleOut(pan);
		}
    	    } else {
		// At this stage the only values left are between 0-6
		// These correspond directly to the oscillator input
		// values, so can be added directly.
        	Oscillator grin = new Oscillator(this, sounds, 44100,2);
		//if (premapped) {
//		    grain = new Granulator(grin,durationArray,gpsArray,freqArray,ri,rgd,rf);
//		} else {
		    grain = new Granulator(grin,44100, 2,50,100);
		//} 
		vol = new Volume(grain,0.5f);
        	Volume vol2 = new Volume(vol,0.1f);
        	pan = new StereoPan(vol2);
                SampleOut sout = new SampleOut(pan);
    	    }
	}
}
