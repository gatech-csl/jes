package instruments;

import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A  sawtooth waveform instrument implementation
 * which iincludes a comb filter
 * @author Andrew Brown
 */

public final class SawCombInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	private int sampleRate;
        private int delay;
        private double decay;
        private int channels;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate and buffersize in addition
	 * to the neccessary frequency relationships 
	 * and volumes for each frequency to be added
	 * the instrument
	 * @param sampleRate 
	 */
	public SawCombInst(int sampleRate){
		this(sampleRate, 300, 0.5);
	}
        
        /**
	 *  Constructor that sets sample rate and the number of channels
         * @param sampleRate The number of samples per second (quality)
         * @param delay The duration of combing in milliseconds
         */
        public SawCombInst(int sampleRate, int delay){
		this(sampleRate, delay, 0.5);
	}
        
        /**
	 *  Constructor that sets sample rate and the number of channels
         * @param sampleRate The number of samples per second (quality)
         * @param delay The duration of combing in milliseconds
         * @param decay The rate of feedback for the comb filter
         */
        public SawCombInst(int sampleRate, int delay, double decay){
		this(sampleRate, delay, decay, 2);
	}
        
        /**
	 *  Constructor that sets sample rate and the number of channels
         * @param sampleRate The number of samples per second (quality)
         * @param delay The duration of combing in milliseconds
         * @param decay The rate of feedback for the comb filter
         * @param channels 1 for Mono or 2 for Stereo
         */
        public SawCombInst(int sampleRate, int delay, double decay, int channels){
		this.sampleRate = sampleRate;
                this.delay = delay;
                this.decay = decay;
                this.channels = channels;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
	   
	/**
	 * Initialisation method used to build the objects that
	 * this instrument will use and specify thier interconnections.
	 */
	public void createChain(){
		Oscillator wt = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, 
                    this.sampleRate, this.channels);
		Comb filt = new Comb(wt, delay, decay);
                Envelope env = new Envelope(filt, 
                    new double[] {0.0, 0.0, 0.05, 1.0, 0.2, 0.4, 0.8, 0.3, 1.0, 0.0});
		Volume vol = new Volume(env);
		StereoPan span = new StereoPan(vol);
		SampleOut sout = new SampleOut(span);
	}	
}

