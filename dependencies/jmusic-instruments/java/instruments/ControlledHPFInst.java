package instruments;

import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A triangle waveform instrument implementation which includes
 * a high pass filter that is swept by a sine wave.
 * @author Andrew Brown
 */

public final class ControlledHPFInst extends Instrument{
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
	 * the instrument
	 * @param sampleRate 
	 */
	public ControlledHPFInst(int sampleRate){
		this(sampleRate, (int)(sampleRate * 0.2));
	}
        
        /**
	 * Constructor that sets sample rate and filter cutoff frequency
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency below which overtones are cut
         */
        public ControlledHPFInst(int sampleRate, int filterCutoff){
		this(sampleRate, filterCutoff, (int)(filterCutoff * 0.6));
	}
        
        /**
	 * Constructor that sets sample rate, cutoff, and modulation amount
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency below which overtones are cut
         * @param modAmount The filter devation above and below the cutoff
         */
        public ControlledHPFInst(int sampleRate, int filterCutoff, int modAmount){
		this(sampleRate, filterCutoff, modAmount, 1);
	}
        
        /**
	 *  Constructor with all attributes
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency below which overtones are cut
         * @param modAmount The filter devation above and below the cutoff
         * @param channels 1 for Mono or 2 for Stereo
         */
        public ControlledHPFInst(int sampleRate, int filterCutoff, int modAmount, int channels){
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
            // oscilator
            Oscillator osc = new Oscillator(this, Oscillator.SQUARE_WAVE, this.sampleRate, this.channels);   
           // filter mod
            Value modfreq = new Value(this, this.sampleRate, this.channels, (float)0.1);
            Oscillator sineMod = new Oscillator(modfreq, Oscillator.SINE_WAVE, Oscillator.FREQUENCY);
            sineMod.setAmp((float) this.modAmount);
            // filter
            Filter filt = new Filter(new AudioObject[] {osc, sineMod}, this.filterCutoff, Filter.HIGH_PASS);
            Envelope env = new Envelope(filt, 
              new double[] {0.0, 0.0, 0.1, 1.0, 0.3, 0.6, 0.8, 0.2, 1.0, 0.0});
            SampleOut sout = new SampleOut(env);
	}	
}



