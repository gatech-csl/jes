package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;
import jm.audio.AOException;

/**
 * A basic vibrato from FM synthesis
 * @author Andrew Brown
 */

public final class VibratoInstRT extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//---------------------------------------------
	/** The number of channels */
	private int channels;
	/** The deviation index */
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
	 */
	public VibratoInstRT(int sampleRate){
	    this(sampleRate, 1);
	}
	/**
	 * A constructor to set an initial 
	 * sampling rate and number of channels.
	 * @param sampleRate 
         * @param channels The number of channels
	 */
	public VibratoInstRT(int sampleRate, int channels){
		this.sampleRate = sampleRate;
		this.channels = channels;
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
            Value modFrequency = new Value(this, this.sampleRate, 1, (float)5.0);
            Oscillator modulator = new Oscillator(modFrequency,
                Oscillator.SINE_WAVE, Oscillator.FREQUENCY);
            modulator.setAmp((float)8.0); 
            // constant
            Value constFreq = new Value(this, this.sampleRate, this.channels, (float)260.0);
            Add add = new Add(new AudioObject[] {constFreq, modulator});
            // carrier
            Oscillator carrier = new Oscillator(add, 
                Oscillator.SINE_WAVE, Oscillator.FREQUENCY);
            Envelope env2 = new Envelope(carrier, 
                new double[] {0.0, 0.0, 0.1, 1.0, 1.0, 0.0});
            Volume amp = new Volume(env2, (float)1.0);
            //SampleOut sout = new SampleOut(amp);
	}	
}

