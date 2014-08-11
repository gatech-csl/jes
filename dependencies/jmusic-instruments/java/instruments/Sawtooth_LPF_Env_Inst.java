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

public final class Sawtooth_LPF_Env_Inst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	private int sampleRate;
        private int filterCutoff;
        private int channels;
        private double[] envValues;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate and use a default cutoff.
	 * @param sampleRate 
	 */
	public Sawtooth_LPF_Env_Inst(int sampleRate){
		this(sampleRate, 1000);
	}
        
     /**
	*  Constructor that sets sample rate and the filter cutoff frequency.
     * @param sampleRate The number of samples per second (quality)
     * @param filterCutoff The frequency above which overtones are cut
     */
     public Sawtooth_LPF_Env_Inst(int sampleRate, int filterCutoff){
		this.sampleRate = sampleRate;
		this.filterCutoff = filterCutoff;
		this.channels = 1;
                this.envValues = new double[] {0.0, 0.0, 0.05, 1.0, 0.2, 0.4, 0.8, 0.3, 1.0, 0.0};
	}

        /**
            *  Constructor that sets sample rate and the filter cutoff frequency.
            * @param sampleRate The number of samples per second (quality)
            * @param filterCutoff The frequency above which overtones are cut
            * @param chan The number of channels.
            */
        public Sawtooth_LPF_Env_Inst(int sampleRate, int filterCutoff, int chan){
            this.sampleRate = sampleRate;
            this.filterCutoff = filterCutoff;
            this.channels = chan;
            this.envValues = new double[] {0.0, 0.0, 0.05, 1.0, 0.2, 0.4, 0.8, 0.3, 1.0, 0.0};
        }

        /**
            *  Constructor that sets sample rate and the filter cutoff frequency.
            * @param sampleRate The number of samples per second (quality).
            * @param filterCutoff The frequency above which overtones are cut.
            * @param chan The number of channels.
            * @param env An array of envelope break point values.
            */
        public Sawtooth_LPF_Env_Inst(int sampleRate, int filterCutoff, int chan, double[] env){
            this.sampleRate = sampleRate;
            this.filterCutoff = filterCutoff;
            this.channels = chan;
            this.envValues = env;
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
          Envelope env = new Envelope(filt, envValues);
          Volume vol = new Volume(env);
          StereoPan pan = new StereoPan(vol);
          SampleOut sout = new SampleOut(pan);
	}	
}

