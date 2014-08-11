package instruments;

import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A sawtooth waveform instrument implementation
 * which iincludes a low pass filter that is swept by
 * an envelope and uses the multiply object to scale
 * the filter envelope depth..
 * @author Andrew Brown
 */

public class SawLPFInstE extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	private int sampleRate;
        private int filterCutoff;
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
	public SawLPFInstE(int sampleRate){
		this(sampleRate, 1000, 1);
	}
        
        /**
	 *  Constructor that sets sample rate and the number of channels
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         */
     public SawLPFInstE(int sampleRate, int filterCutoff){
		this(sampleRate, filterCutoff, 1);
	}
        
        /**
	 *  Constructor that sets sample rate and the number of channels
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         * @param channels 1 for Mono or 2 for Stereo
         */
        public SawLPFInstE(int sampleRate, int filterCutoff, int channels){
		this.sampleRate = sampleRate;
                this.filterCutoff = filterCutoff;
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
          Envelope filtEnv = new Envelope(this, this.sampleRate, this.channels,
              new double[] {0.0, 0.0, 0.5, 1.0, 1.0, 0.0});
          Value scalefactor = new Value(this, this.sampleRate, this.channels, (float)2000.0);
          Multiply mult = new Multiply(new AudioObject[] {filtEnv, scalefactor});
          Oscillator wave = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, this.channels);
          Filter filt = new Filter(new AudioObject[] {wave, mult}, this.filterCutoff, Filter.LOW_PASS);
          Envelope env = new Envelope(filt, 
              new double[] {0.0, 0.0, 0.05, 1.0, 0.2, 0.4, 0.8, 0.3, 1.0, 0.0});
		Volume vol = new Volume(env);
		SampleOut sout = new SampleOut(vol);
	}	
}

