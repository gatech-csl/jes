package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic amplitude modulation that causes a warbing trumolo effect
 * @author Andrew Brown
 */

public final class SimpleTremoloInst extends jm.audio.Instrument{
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
	public SimpleTremoloInst(int sampleRate){
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
            Value modFreq = new Value(this, this.sampleRate, this.channels, (float)5.0);
            Oscillator modulator = new Oscillator(modFreq, Oscillator.SINE_WAVE, 
                 Oscillator.FREQUENCY);
            Volume amp = new Volume(modulator, (float)0.4);
            Oscillator carrier = new Oscillator(amp, Oscillator.SINE_WAVE, Oscillator.AMPLITUDE);
            SampleOut sout = new SampleOut(carrier);
	}	
}

