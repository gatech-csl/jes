package instruments;

import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A triangle waveform instrument implementation
 * which iincludes a low pass filter that is swept by
 * an envelope.
 * @author Andrew Brown
 */

public final class LPFilterEnvInst extends Instrument{
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
	 * @param sampleRate 
	 */
	public LPFilterEnvInst(int sampleRate){
		this(sampleRate, (int)(sampleRate * 0.02), 1);
	}
        
        /**
	 *  Constructor that sets sample rate and filter cutoff centre frequency
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         */
        public LPFilterEnvInst(int sampleRate, int filterCutoff){
		this(sampleRate, filterCutoff, 1);
	}
        
        /**
	 *  Constructor that sets all attributes
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         * @param channels 1 for Mono or 2 for Stereo
         */
        public LPFilterEnvInst(int sampleRate, int filterCutoff, int channels){
		this.sampleRate = sampleRate;
                this.filterCutoff = filterCutoff;
                this.channels = channels;
	}

	/**
	 * Initialisation method used to build the objects that
	 * this instrument will use and specify thier interconnections.
	 */
	public void createChain(){
            // filter envelope
            Envelope filtEnv = new Envelope(this, this.sampleRate, this.channels,
                new double[] {0.0, 0.0, 0.2, (this.sampleRate * 0.4), 0.4, 0.0, 0.6, (this.sampleRate * 0.3), 1.0, 
                    (this.filterCutoff * 0.1)});
            // oscilator
            Oscillator osc = new Oscillator(this, Oscillator.TRIANGLE_WAVE, this.sampleRate, this.channels);   
            // filter
            Filter filt = new Filter(new AudioObject[] {osc, filtEnv}, this.filterCutoff, Filter.LOW_PASS);
            Envelope env = new Envelope(filt, 
              new double[] {0.0, 0.0, 0.05, 1.0, 1.0, 0.0});
            Volume vol = new Volume(env);
            StereoPan pan = new StereoPan(vol);
            SampleOut sout = new SampleOut(pan);
	}	
}

