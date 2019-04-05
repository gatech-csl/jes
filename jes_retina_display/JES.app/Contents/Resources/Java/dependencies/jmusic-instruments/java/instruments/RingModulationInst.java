package instruments;


import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic ring modulation synthesis instrument
 * which is pure Amplitude Modulation
 * @author Andrew Brown
 */

public final class RingModulationInst extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	/** the sample rate passed to the instrument */
	private int sampleRate;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate.
	 * @param sampleRate 
	 */
	public RingModulationInst(int sampleRate){
	    this.sampleRate = sampleRate;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
     /**
	 * Initialisation method used to build the objects that
	 * this instrument will use.
	 */
	public void createChain(){
		Oscillator wt1 = new Oscillator(this, Oscillator.SINE_WAVE, 
                    this.sampleRate, Oscillator.MONO);
		wt1.setFrqRatio((float)2.2);
                Envelope env = new Envelope(wt1, 
                    new double[] {0.0, 1.0, 1.0, 0.0});
		Oscillator wt2 = new Oscillator(env,
                    Oscillator.SINE_WAVE, Oscillator.AMPLITUDE);
		Envelope env2 = new Envelope(wt2,
                    new double[] {0.0, 0.0, 0.05, 1.0, 1.0, 0.0});
		SampleOut sout = new SampleOut(env2);
	}	
}

