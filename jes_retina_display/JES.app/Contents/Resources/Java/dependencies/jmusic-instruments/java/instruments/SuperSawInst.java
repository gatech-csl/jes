package instruments;


import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A multiple sawtooth instrument implementation
 * which has each wave detuned.
 * @author Andrew Brown, Nick Coleman and Andrew Sorensen
 */

public final class SuperSawInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	
	/** The points to use in the construction of Envelopes */
	private EnvPoint[] pointArray = new EnvPoint[10];
	/** the same rate */
	private int sampleRate;
	/** The frequency ratio between wavefroms */
	private double detune;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial sample rate
	 * @param sampleRate 
	 */
	public SuperSawInst(int sampleRate){
		this(sampleRate, 0.001);
	}
	
	/**
	 * Basic default constructor to set an initial sample rate
	 * @param sampleRate 
	 */
	public SuperSawInst(int sampleRate, double detune){	
		this.sampleRate = sampleRate;
		this.detune = detune;
		EnvPoint[] tempArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.02, (float)1.0),
			new EnvPoint((float)0.15, (float)0.6),
			new EnvPoint((float)0.9, (float)0.3),
			new EnvPoint((float)1.0, (float)0.0)
		};
		pointArray = tempArray;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
	   
	/**
	 * Initialisation method used to build the objects that
	 * this instrument will use
	 */
	public void createChain(){
		Oscillator wt1 = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, 2);
		Oscillator wt2 = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, 2);
		wt2.setFrqRatio((float)(1.0 + detune));
		Oscillator wt3 = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, 2);
		wt3.setFrqRatio((float)(1.0 - detune * 2));
		Oscillator wt4 = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, 2);
		wt4.setFrqRatio((float)(1.0 + detune * 2));
		Oscillator wt5 = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, 2);
		wt5.setFrqRatio((float)(1.0 - detune));
		Oscillator wt6 = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, 2);
		wt6.setFrqRatio((float)(1.0 + detune * 3));
		Oscillator wt7 = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, 2);
		wt7.setFrqRatio((float)(1.0 - detune * 3));
		AudioObject[] waves = {wt1, wt2, wt3, wt4, wt5, wt6, wt7};
		Add add = new Add(waves);
		Envelope env = new Envelope(add, pointArray);
		Volume vol = new Volume(env);
		StereoPan span = new StereoPan(vol);
		SampleOut sout = new SampleOut(span);
	}	
}

