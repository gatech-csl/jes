package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic amplitude modulation creating a complex timbre
 * @author Andrew Brown
 */

public final class SimpleAMInst extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	/** the sample rate passed to the instrument */
	private int sampleRate;
        /** the sample rate passed to the instrument */
	private int channels;
	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate.
	 * @param sampleRate 
	 */
	public SimpleAMInst(int sampleRate){
	    this.sampleRate = sampleRate;
	    this.channels = 1;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
	/**
	 * Initialisation method used to build the objects that
	 * this instrument will use.
	 */
	public void createChain(){
            Oscillator modulator = new Oscillator(this, Oscillator.SINE_WAVE, 
                this.sampleRate, 1);
            modulator.setFrqRatio((float) 7.23);
            Volume wtAmp = new Volume(modulator);
            Value offsetAmp = new Value(this, this.sampleRate, 1, (float)0.5);
            Add add = new Add(new AudioObject[] {wtAmp, offsetAmp});
            Oscillator carrier = new Oscillator(add, 
                Oscillator.SINE_WAVE, Oscillator.AMPLITUDE);
            SampleOut sout = new SampleOut(carrier);
	}	
}

