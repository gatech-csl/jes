package instruments;

import jm.audio.Instrument;

import jm.audio.io.*;

import jm.audio.synth.*;

import jm.music.data.Note;

import jm.audio.AudioObject;



/**

 * A monophonic sawtooth waveform instrument implementation

 * which includes a static high pass filter.

 * @author Andrew Brown

 */



public final class SawHPFInst extends Instrument{

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

	public SawHPFInst(int sampleRate){

		this(sampleRate, 2000);

        }

        

     /**

     * Constructor that sets sample rate and the filter cutoff frequency.

     * @param sampleRate The number of samples per second (quality)

     * @param filterCutoff The frequency above which overtones are cut

     */

     public SawHPFInst(int sampleRate, int filterCutoff){

		this.sampleRate = sampleRate;

		this.filterCutoff = filterCutoff;

		this.channels = 1;

	}



	//----------------------------------------------

	// Methods 

	//----------------------------------------------   

	/**

	 * Initialisation method used to build the objects that

	 * this instrument will use and specify their interconnections.

	 */

	public void createChain(){

            Oscillator wt = new Oscillator(this, Oscillator.SAWTOOTH_WAVE, 
                                           this.sampleRate, this.channels);

            Filter filt = new Filter(wt, this.filterCutoff, Filter.HIGH_PASS);

            Envelope env = new Envelope(filt, 
                                        new double[] {0.0, 0.0, 0.05, 1.0, 0.2, 
                                                      0.4, 0.8, 0.3, 1.0, 0.0});

            Volume vol = new Volume(env);

            SampleOut sout = new SampleOut(vol);

	}	

}



