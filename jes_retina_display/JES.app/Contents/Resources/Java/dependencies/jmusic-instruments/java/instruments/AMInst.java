package instruments;


import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic amplitude modulation synthesis instrument
 * which implements envelope and volume control
 * @author Andrew Brown
 */

public class AMInst extends jm.audio.Instrument{
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
	public AMInst(int sampleRate){
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
		Oscillator mod = new Oscillator(this, Oscillator.SINE_WAVE, 
                    this.sampleRate, this.channels);
		mod.setFrqRatio((float)7.5);
                Envelope env = new Envelope(mod, 
                    new double[] {0.0, 0.0, 0.4, 1.0, 1.0, 0.8});
                Value offsetAmp = new Value(this, this.sampleRate, 
                    this.channels, (float)0.7);
                 Add add = new Add(new AudioObject[] {env, offsetAmp});
		Oscillator carr = new Oscillator(add, 
                    Oscillator.SINE_WAVE, WaveTable.AMPLITUDE);
		Envelope env2 = new Envelope(carr,
                    new double[] {0.0, 0.0, 0.5, 1.0, 1.0, 0.0});
		SampleOut sout = new SampleOut(env2);
	}	
}
