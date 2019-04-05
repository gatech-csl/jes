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

public final class FMNoiseInst extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	/** the sample rate passed to the instrument */
	private int sampleRate;
        /** the sample rate passed to the instrument */
	private int channels;
	private int modIndex;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate.
	 * @param sampleRate 
	 */
	public FMNoiseInst(int sampleRate, int modIndex, int channels){
		this.sampleRate = sampleRate;
		this.channels = channels;
		this.modIndex = modIndex;
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
		Noise modulator = new Noise(this, Noise.STEP_NOISE, this.sampleRate, this.channels);
		//modulator.setFrqRatio(frqRatio);
		modulator.setAmp((float)modIndex);
		Envelope env = new Envelope(modulator, new double[] {0.0, 1.0, 1.0, 0.0});

		// constant
		Value constFreq = new Value(this, this.sampleRate, this.channels, Value.NOTE_PITCH);
		Add add = new Add(new AudioObject[] {constFreq, env});

		// carrier
		Oscillator carrier = new Oscillator(add,  Oscillator.SINE_WAVE, Oscillator.FREQUENCY);
		Envelope env2 = new Envelope(carrier, new double[] {0.0, 0.0, 0.02, 1.0, 1.0, 0.0});
		Volume amp = new Volume(env2);
		StereoPan pan = new StereoPan(amp);
		SampleOut sout = new SampleOut(pan);         
	}	
}

