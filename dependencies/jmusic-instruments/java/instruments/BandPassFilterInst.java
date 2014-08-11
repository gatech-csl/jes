package instruments;

import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A sawtooth waveform instrument implementation
 * which includes low and high pass filters act in series to
 * form a band pass filter.
 * @author Andrew Brown
 */

public final class BandPassFilterInst extends Instrument{
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
	 * Basic default constructor.
	 * @param sampleRate 
	 */
	public BandPassFilterInst(int sampleRate){
		this(sampleRate, 2500, 1);
	}
        
        /**
	 *  Constructor that sets sample rate and the number of channels
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         */
     public BandPassFilterInst(int sampleRate, int filterCutoff){
		this(sampleRate, filterCutoff, 1);
	}
        
        /**
	 *  Constructor that sets sample rate and the number of channels
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         * @param channels 1 for Mono or 2 for Stereo
         */
        public BandPassFilterInst(int sampleRate, int filterCutoff, int channels){
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
          Oscillator osc = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, this.channels);
          Filter lpf = new Filter(osc, this.filterCutoff, Filter.LOW_PASS);
          Filter hpf = new Filter(lpf, this.filterCutoff, Filter.HIGH_PASS);
          Volume vol = new Volume(hpf);
          Envelope env = new Envelope(vol, 
              new double[] {0.0, 0.0, 0.05, 1.0, 0.2, 0.4, 0.8, 0.3, 1.0, 0.0});
          StereoPan span = new StereoPan(env);
          SampleOut sout = new SampleOut(span);
	}	
}


