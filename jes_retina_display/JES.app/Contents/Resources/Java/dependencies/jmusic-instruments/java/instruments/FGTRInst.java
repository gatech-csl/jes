package instruments;

/**
 * File: FGTRInst.java
 * Author: Timothy Opie
 * Created: Wed Nov 12 16:59:02 EST 2003
 */

import jm.audio.io.*;
import jm.audio.Instrument;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

public final class FGTRInst extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	// the name of the sample file
	public int channels = 2, sampleRate = 44100;
	private String fileName;
	private int grainDuration,grainsPerSecond;
    private float bandwidthTop, bandwidthBottom;
	
	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	public FGTRInst(String fileName, int gDur, float bwTop, float bwBottom, int gps){
		// Use this constructor when you want to granulate an audio file.
		this.fileName = fileName; //Name of .au file
		this.grainDuration = gDur*((channels*sampleRate)/1000); //in milliseconds
		this.bandwidthBottom = bwBottom; //bottom frequency
		this.bandwidthTop = bwTop; //top frequency
		this.grainsPerSecond = gps; 
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
		Oscillator sin = new Oscillator(this, 2, 44100,2);
		//SampleIn sin = new SampleIn(this, fileName);
		//Filter lpf = new Filter(sin, bandwidthBottom, Filter.LOW_PASS);
		//Filter hpf = new Filter(lpf, bandwidthTop, Filter.HIGH_PASS);
		AllFGTR fgtr = new AllFGTR(/*hpf*/sin, grainDuration, bandwidthTop, bandwidthBottom, grainsPerSecond);
		SampleOut sout = new SampleOut(fgtr);
	}
}
