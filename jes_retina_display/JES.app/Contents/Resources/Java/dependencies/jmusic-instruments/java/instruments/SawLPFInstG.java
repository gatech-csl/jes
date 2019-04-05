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
 * the filter envelope depth. A second oscillator is added
 * and detuned slightly to give a fat chorused effect.
 * @author Andrew Brown
 */

public final class SawLPFInstG extends Instrument{
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
	public SawLPFInstG(int sampleRate){
		this(sampleRate, 1000, 1);
	}
        
        /**
	 *  Constructor that sets sample rate and the number of channels
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         */
     public SawLPFInstG(int sampleRate, int filterCutoff){
		this(sampleRate, filterCutoff, 1);
	}
        
        /**
	 *  Constructor that sets sample rate and the number of channels
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         * @param channels 1 for Mono or 2 for Stereo
         */
        public SawLPFInstG(int sampleRate, int filterCutoff, int channels){
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
          // modulating LFO
          Value freq = new Value(this, this.sampleRate, this.channels, (float)6.0);
          Oscillator LFO = new Oscillator(freq, Oscillator.SINE_WAVE, Oscillator.FREQUENCY);
          LFO.setAmp((float)3.0);
          Envelope LFOenv = new Envelope(LFO, 
              new double[] {0.0, 0.0, 0.2, 0.4, 0.4, 1.0, 0.8, 1.0, 1.0, 0.0});
          // constant
		Value offsetFrequency = new Value(this, this.sampleRate, this.channels, Value.NOTE_PITCH);
		AudioObject[] grp1 = {LFOenv, offsetFrequency};
		Add add = new Add(grp1);
          // Filter cutoff envelope control
          Envelope filtEnv = new Envelope(this, this.sampleRate, this.channels,
              new double[] {0.0, 0.0, 0.5, 1.0, 1.0, 0.0});
          Value scalefactor = new Value(this, this.sampleRate, this.channels, (float)2000.0);
          Multiply mult = new Multiply(new AudioObject[] {filtEnv, scalefactor});
          // Waveform 1
          Oscillator wave = new Oscillator(add, Oscillator.SAWTOOTH_WAVE, Oscillator.FREQUENCY);
          // Filter
          Filter filt = new Filter(new AudioObject[] {wave, mult}, this.filterCutoff, Filter.LOW_PASS);
          // Envelope gnerator
          Envelope env = new Envelope(filt, 
              new double[] {0.0, 0.0, 0.05, 1.0, 0.2, 0.4, 0.8, 0.3, 1.0, 0.0});
          // respond to note dynamics
		Volume vol = new Volume(env);
		// save to a file
		SampleOut sout = new SampleOut(vol);
	}	
}

