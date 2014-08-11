package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * An amplitude modulation synthesis instrument
 * which uses a noise modulation source
 * @author Andrew Brown
 */

public final class AMNoiseInst extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	/** the sample rate passed to the instrument */
	private int sampleRate;
        /** the sample rate passed to the instrument */
	private int channels;
	/** the amount of noise modulation (0 - 1) */
	private float depth = (float)0.0;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate.
	 * @param sampleRate 
	 * @param depth 
	 */
	public AMNoiseInst(int sampleRate, double depth){
	    this.sampleRate = sampleRate;
	    this.channels = 1;
	    this.depth = (float)depth;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
        /**
	 * Initialisation method used to build the objects that
	 * this instrument will use.
	 */
	public void createChain(){
		// modulator
		Noise noise = new Noise(this, Noise.FRACTAL_NOISE, this.sampleRate, this.channels);
        	Envelope modEnv = new Envelope(noise,
                    new double[] {0.0, 0.0, 0.5, 1.0, 1.0, 1.0});
        	Volume modVol = new Volume(modEnv,(float)this.depth); // respond to note dynamic
        	// constant
		Value offsetAmp = new Value(this, this.sampleRate, this.channels, (float)0.5);
		AudioObject[] grp1 = {modVol, offsetAmp};
		Add add = new Add(grp1);
        	// carrier
		Oscillator carrier = new Oscillator(add,
                    Oscillator.SINE_WAVE, WaveTable.AMPLITUDE);
        	Envelope env = new Envelope(carrier,
                    new double[] {0.0, 0.0, 0.5, 1.0, 1.0, 0.0});
		Volume vol = new Volume(env,(float)1.0);
		StereoPan span = new StereoPan(vol);
		SampleOut sout = new SampleOut(span);
	}	
}

