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

public class SawLPFInst extends Instrument{
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
	 * sampling rate and use a default cutoff.
	 * @param sampleRate 
	 */
	public SawLPFInst(int sampleRate){
		this(sampleRate, 1000);
	}
        
        /**
        *  Constructor that sets sample rate and the filter cutoff frequency.
        * @param sampleRate The number of samples per second (quality)
        * @param filterCutoff The frequency above which overtones are cut
        */
        public SawLPFInst(int sampleRate, int filterCutoff){
		this.sampleRate = sampleRate;
		this.filterCutoff = filterCutoff;
		this.channels = 1;
	}

	/**
		*  Constructor that sets sample rate and the filter cutoff frequency.
		* @param sampleRate The number of samples per second (quality)
		* @param filterCutoff The frequency above which overtones are cut
		* @param channels The numbers of channels, 1 = mono, 2 = stereo
		*/
	public SawLPFInst(int sampleRate, int filterCutoff, int channels){
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
		Filter filt = new Filter(osc, this.filterCutoff, Filter.LOW_PASS);
		//Envelope env = new Envelope(filt, 
		//new double[] {0.0, 0.0, 0.1, 1.0, 0.2, 0.6, 0.8, 0.4, 1.0, 0.0});
		ADSR env = new ADSR(filt, 20, 100, 0.6, 400);
		Volume vol = new Volume(env);
		StereoPan span = new StereoPan(vol);
		SampleOut sout = new SampleOut(span);
	}	
}

