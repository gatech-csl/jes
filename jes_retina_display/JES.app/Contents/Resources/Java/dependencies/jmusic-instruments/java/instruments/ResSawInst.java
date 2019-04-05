package instruments;

import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A  sawtooth waveform instrument implementation
 * which iincludes a low pass filter that is swept by
 * a three filters - two forming a band pass anf
 * one as the low pass.
 * @author Andrew Brown
 */

public final class ResSawInst extends Instrument{
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
	 * sampling rate 
	 * @param sampleRate 
	 */
	public ResSawInst(int sampleRate){
		this(sampleRate, 2500, 1);
	}
        
        /**
	 *  Constructor that sets sample rate and filter cutoff
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         */
     public ResSawInst(int sampleRate, int filterCutoff){
		this(sampleRate, filterCutoff, 1);
	}
        
        /**
	 *  Constructor that sets sample rate , cutoff and channels
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         * @param channels 1 for Mono or 2 for Stereo
         */
        public ResSawInst(int sampleRate, int filterCutoff, int channels){
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
	  // filter mod source 1 
          Value modfreq = new Value(this, this.sampleRate, this.channels, (float)0.5);
          Oscillator sineMod = new Oscillator(modfreq, Oscillator.COSINE_WAVE, Oscillator.FREQUENCY);
	  Splitter lfo = new Splitter(sineMod);
          sineMod.setAmp((float) 2000.0);
          Oscillator wt = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, this.channels);
          Filter filt = new Filter(new AudioObject[] {wt, lfo}, this.filterCutoff, Filter.LOW_PASS);
          // filter mod source 2
	Filter filt2 = new Filter(new AudioObject[] {filt, lfo}, this.filterCutoff, Filter.HIGH_PASS);
          Volume vol2 = new Volume(filt2, (float)10.0); // amount of resonance
          // filter mod source 3
          Oscillator wt3 = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, this.channels);
          Filter filt3 = new Filter(new AudioObject[] {wt3, lfo}, this.filterCutoff, Filter.LOW_PASS);
          Volume vol3 = new Volume(filt3);
          // add and pocess everythning
          Add add = new Add(new AudioObject[] {vol2, vol3}); 
          Envelope env = new Envelope(add, 
              new double[] {0.0, 0.0, 0.05, 1.0, 0.2, 0.4, 0.8, 0.3, 1.0, 0.0});
		StereoPan span = new StereoPan(env);
		SampleOut sout = new SampleOut(span);
	}	
}

