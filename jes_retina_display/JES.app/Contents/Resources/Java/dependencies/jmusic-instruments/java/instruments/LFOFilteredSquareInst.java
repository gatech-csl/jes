package instruments;

import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A squarewave instrument implementation which includes
 * a low pass filter that is swept by a cosine wave.
 * @author Andrew Brown
 */

public final class LFOFilteredSquareInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	private int sampleRate;
        private int filterCutoff;
        private int channels;
        private int modAmount;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial sampling rate
	 * @param sampleRate Integer in Hertz
	 */
	public LFOFilteredSquareInst(int sampleRate){
		this(sampleRate, (int)(sampleRate * 0.2));
	}
        
        /**
	 * Constructor that sets sample rate and filter cutoff frequency
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency in hertz above which overtones are cut
         */
        public LFOFilteredSquareInst(int sampleRate, int filterCutoff){
		this(sampleRate, filterCutoff, (int)(filterCutoff * 0.9));
	}
        
        /**
	 * Constructor that sets sample rate, filter cutoff, and modulation amount
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         * @param modAmount The filter devation above and below the cutoff
         */
        public LFOFilteredSquareInst(int sampleRate, int filterCutoff, int modAmount){
		this(sampleRate, filterCutoff, modAmount, 1);
	}
        
        /**
	 *  Constructor that sets all attributes
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         * @param modAmount The filter devation above and below the cutoff
         * @param channels 1 for Mono or 2 for Stereo
         */
        public LFOFilteredSquareInst(int sampleRate, int filterCutoff, int modAmount, int channels){
		this.sampleRate = sampleRate;
                this.filterCutoff = filterCutoff;
                this.modAmount = modAmount;
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
            // oscilators
            Oscillator osc = new Oscillator(this, Oscillator.SQUARE_WAVE, this.sampleRate, this.channels);   
            Oscillator osc2 = new Oscillator(this, Oscillator.SQUARE_WAVE, this.sampleRate, this.channels);
            osc2.setFrqRatio((float)1.001);
            Oscillator osc3 = new Oscillator(this, Oscillator.SQUARE_WAVE, this.sampleRate, this.channels);
            osc3.setFrqRatio((float)0.999);
            Add add = new Add(new AudioObject[] {osc, osc2, osc3});
            // filter mod
            Value modfreq = new Value(this, this.sampleRate, this.channels, (float)0.3);
            Oscillator sineMod = new Oscillator(modfreq, Oscillator.COSINE_WAVE, Oscillator.FREQUENCY);
            sineMod.setAmp((float) this.modAmount);
            // Filter - try changing this to a high pass filter
            Filter filt = new Filter(new AudioObject[] {add, sineMod}, this.filterCutoff, Filter.LOW_PASS);
            Envelope env = new Envelope(filt, 
              new double[] {0.0, 0.0, 0.05, 1.0, 0.2, 0.3, 0.8, 0.2, 1.0, 0.0});
            Volume vol = new Volume(env);
            SampleOut sout = new SampleOut(vol);
	}	
}


