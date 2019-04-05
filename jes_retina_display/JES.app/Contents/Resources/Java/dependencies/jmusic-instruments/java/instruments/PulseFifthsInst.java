package instruments;


import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic pulsewave waveform instrument implementation
 * which has two tones a perfect fifth apart
 * @author Andrew Brown
 */

public final class PulseFifthsInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	
	/** The points to use in the construction of Envelopes */
	private EnvPoint[] pointArray = new EnvPoint[10];
	
	private int sampleRate;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate
	 * @param sampleRate 
	 */
	public PulseFifthsInst(int sampleRate){
		this.sampleRate = sampleRate;
		EnvPoint[] tempArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.02, (float)1.0),
			new EnvPoint((float)0.15, (float)0.6),
			new EnvPoint((float)0.9, (float)0.4),
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
		// tonic
		Oscillator wt = new Oscillator(this, Oscillator.PULSE_WAVE, 
                    this.sampleRate, 2);
                wt.setPulseWidth(0.15);
		StereoPan span = new StereoPan(wt, (float)0.2);
		// fifth
		Oscillator wt2 = new Oscillator(this, Oscillator.PULSE_WAVE, 
                    this.sampleRate, 2);
                wt2.setPulseWidth(0.15);
		wt2.setFrqRatio((float)(3.0/2.0));
		StereoPan span2 = new StereoPan(wt2, (float)0.8);
		// add together
		AudioObject[] waves = {span, span2};
		Add add = new Add(waves);
		// continue to process
		Envelope env = new Envelope(add, pointArray);
		Volume vol = new Volume(env);
		SampleOut sout = new SampleOut(vol);
	}	
}

