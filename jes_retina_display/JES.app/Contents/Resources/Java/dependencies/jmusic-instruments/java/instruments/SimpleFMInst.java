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

public final class SimpleFMInst extends jm.audio.Instrument{
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
	 * Basic default constructor to set basic values
	 * @param sampleRate The instrument's audio resolution
         * @param modIndex The modulation index, greater = more overtones
         * @param ratio The carrier/modulator pitch ratio = harmonicity of spectrum
	 */
	public SimpleFMInst(int sampleRate, int modIndex, double ratio){
	    this(sampleRate, modIndex, ratio, 1);
	}

	/**
	 * A constructor to set all values
	 * @param sampleRate The instrument's audio resolution
         * @param modIndex The modulation index, greater = more overtones
         * @param ratio The carrier/modulator pitch ratio = harmonicity of spectrum
	 * @param channels The number of channels
	 */
	public SimpleFMInst(int sampleRate, int modIndex, double ratio, int channels){
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
		Oscillator modulator = new Oscillator(this, Oscillator.SINE_WAVE, this.sampleRate, this.channels);
		modulator.setFrqRatio(frqRatio);
		modulator.setAmp((float)modIndex);
		Envelope env = new Envelope(modulator, new double[] {0.0, 1.0, 1.0, 0.0});
		
		// constant
		Value constFreq = new Value(this, this.sampleRate, this.channels, Value.NOTE_PITCH);
		Add add = new Add(new AudioObject[] {constFreq, env});
		
		// carrier
		Oscillator carrier = new Oscillator(add,  Oscillator.SINE_WAVE, Oscillator.FREQUENCY);
		Envelope ampEnv = new Envelope(carrier, new double[] {0.0, 0.0, 0.02, 1.0, 1.0, 0.0});
		Volume amp = new Volume(ampEnv);
		StereoPan pan = new StereoPan(amp);
		SampleOut sout = new SampleOut(pan);                
	}	
}

