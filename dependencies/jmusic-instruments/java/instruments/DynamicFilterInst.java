package instruments;

import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A sawtooth waveform instrument implementation
 * which includes a low pass filter that is changed by
 * the note's velocity.
 * @author Andrew Brown
 */

public final class DynamicFilterInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	private int sampleRate;
        private int filterCutoff;
        private int channels;
        private double dynScale;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate.
	 * @param sampleRate 
	 */
	public DynamicFilterInst(int sampleRate){
		this(sampleRate, 200);
	}
	
	 /**
	 *  Constructor that sets sample rate and cutoff frequency in hertz
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         */
	public DynamicFilterInst(int sampleRate, int filterCutoff){
		this(sampleRate, filterCutoff, 300, 1);
	}
        
        /**
	 *  Constructor that sets sample rate, cutoff and scaling factor for mod source
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         * @param dynScale The amount to multiply the dynamic value by in
         *				order for it change the filter cutoff
         */
     public DynamicFilterInst(int sampleRate, int filterCutoff, double dynScale){
		this(sampleRate, filterCutoff, dynScale, 1);
	}
        
        /**
	 *  Constructor that sets all attributes
         * @param sampleRate The number of samples per second (quality)
         * @param filterCutoff The frequency above which overtones are cut
         * @param channels 1 for Mono or 2 for Stereo
         */
        public DynamicFilterInst(int sampleRate, int filterCutoff, double dynScale, int channels){
		this.sampleRate = sampleRate;
                this.filterCutoff = filterCutoff;
                this.dynScale = dynScale;
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
            Value modSource = new Value(this, this.sampleRate, 1, Value.NOTE_DYNAMIC);
            Value modAmount = new Value(this, this.sampleRate, 1, (float)this.dynScale);
            Multiply filterControl = new Multiply(new AudioObject[] {modSource, modAmount});
            Oscillator wave = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, this.sampleRate, this.channels);
            Filter filt = new Filter(new AudioObject[] {wave, filterControl}, this.filterCutoff, Filter.LOW_PASS);
            Envelope env = new Envelope(filt, 
              new double[] {0.0, 0.0, 0.05, 1.0, 0.2, 0.4, 0.8, 0.3, 1.0, 0.0});
            SampleOut sout = new SampleOut(env);
	}	
}


