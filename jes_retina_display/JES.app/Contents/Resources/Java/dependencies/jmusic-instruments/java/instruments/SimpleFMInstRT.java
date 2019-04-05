package instruments;


import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;
import jm.audio.AOException;

/**
 * A basic FM synthesis instrument implementation
 * @author Andrew Sorensen
 */

public final class SimpleFMInstRT extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//---------------------------------------------
	/** The number of channels */
	private int channels;
	/** The modulation index */
	private int modIndex;
	/** The frequency ratio from the carrier frequency (the notes pitch) */
	private float frqRatio;
	
	private int sampleRate;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate.
	 * @param sampleRate 
         * @param modulation index
         * @param carrier/modulator pitch ratio
	 */
	public SimpleFMInstRT(int sampleRate, int modIndex, double ratio){
	    this(sampleRate, 1, modIndex, ratio);
	}
	/**
	 * A constructor to set an initial 
	 * sampling rate and number of channels.
	 * @param sampleRate 
         * @param channels The number of channels
         * @param deviation The modulation index
         * @param ratio The carrier/modulator pitch ratio
	 */
	public SimpleFMInstRT(int sampleRate, int channels, int modIndex, double ratio){
		this.sampleRate = sampleRate;
		this.channels = channels;
		this.modIndex = modIndex;
		this.frqRatio = (float)ratio;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
	   
	/**
	 * Initialisation method used to build the objects that
	 * this instrument will use
	 */
	public void createChain()throws AOException{
        // modulator
		Oscillator modulator = new Oscillator(this, Oscillator.SINE_WAVE,
                    this.sampleRate, this.channels);
		modulator.setAmp((float)this.modIndex);
		modulator.setFrqRatio(this.frqRatio);
        Envelope modEnv = new Envelope(modulator,
                    new double[] {0.0, 0.0, 0.2, 1.0, 1.0, 1.0});
                Volume modVol = new Volume(modEnv); // respond to note dynamic
                // constant
		Value offsetFrequency = new Value(this, this.sampleRate, 
			this.channels, Value.NOTE_PITCH);
		AudioObject[] grp1 = {modVol, offsetFrequency};
		Add add = new Add(grp1);
                // carrier
		Oscillator carrier = new Oscillator(add,
                    Oscillator.SINE_WAVE, Oscillator.FREQUENCY);
        Envelope env = new Envelope(carrier,
                    new double[] {0.0, 0.0, 0.5, 1.0, 1.0, 0.0});
		Volume vol = new Volume(env);
		StereoPan span = new StereoPan(vol);
		//SampleOut sout = new SampleOut(span);
	}	
}


