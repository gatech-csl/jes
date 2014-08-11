package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic amplitude modulation that causes a warbing trumolo effect
 * @author Andrew Brown
 */

public final class TremoloInst extends jm.audio.Instrument{
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
	public TremoloInst(int sampleRate){
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
		Oscillator modulator = new Oscillator(this, Oscillator.SINE_WAVE, this.sampleRate,
			this.channels, Oscillator.FREQUENCY, (float)5.0);
		Volume vol = new Volume(modulator, 10.0f);
		Oscillator carrier = new Oscillator(vol, 
			Oscillator.SINE_WAVE, Oscillator.AMPLITUDE);
		Envelope env2 = new Envelope(carrier, 
			new double[] {0.0, 0.0, 0.1, 1.0, 1.0, 0.0});
		SampleOut sout = new SampleOut(env2);
	}	
}

