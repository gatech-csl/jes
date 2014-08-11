package instruments;

import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A monophonic sawtooth waveform instrument implementation
 * which includes a static low pass filter.
 * @author Andrew Brown
 */

public final class SawLPFInstRT extends Instrument{
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
	 * Basic default constructor
	 */
	public SawLPFInstRT(){
		this(44100, 1000);
	}
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate and use a default cutoff.
	 * @param sampleRate 
	 */
	public SawLPFInstRT(int sampleRate){
		this(sampleRate, 1000);
	}
        
     /**
	*  Constructor that sets sample rate and the filter cutoff frequency.
     * @param sampleRate The number of samples per second (quality)
     * @param filterCutoff The frequency above which overtones are cut
     */
     public SawLPFInstRT(int sampleRate, int filterCutoff){
		this.sampleRate = sampleRate;
		this.filterCutoff = filterCutoff;
		this.channels = 1;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------   
	/**
	 * Initialisation method used to build the objects that
	 * this instrument will use and specify thier interconnections.
	 */
	public void createChain(){
          Oscillator wt = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, this.channels);
          Filter filt = new Filter(wt, this.filterCutoff, Filter.LOW_PASS);
          Envelope env = new Envelope(filt, 
              new double[] {0.0, 0.0, 0.05, 1.0, 0.3, 0.4, 1.0, 0.0});
		Volume vol = new Volume(env);
//		SampleOut sout = new SampleOut(vol);
	}	
}

