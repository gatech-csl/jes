package instruments;


import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic square wave instrument implementation
 * which implements envelope , pan, and volume control
 * @author Andrew Brown and Andrew Sorensen
 */

public final class SquareLPFInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	
	/** The points to use in the construction of Envelopes */
	private EnvPoint[] pointArray = new EnvPoint[10];
	
	private int sampleRate;
        private int cutoff; 

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate.
	 * @param sampleRate 
	 */
	public SquareLPFInst(int sampleRate){
            this(sampleRate, 500);
        }
        
        /**
        * Basic default constructor to set an initial 
        * sampling rate.
        * @param sampleRate
        *@param cuttoff Filter cuttoff frequency in hertz
        */
        public SquareLPFInst(int sampleRate, int cutoff){
            this.sampleRate = sampleRate;
            this.cutoff = cutoff;
            EnvPoint[] tempArray = {
                    new EnvPoint((float)0.0, (float)0.0),
                    new EnvPoint((float)0.02, (float)1.0),
                    new EnvPoint((float)0.15, (float)0.6),
                    new EnvPoint((float)0.95, (float)0.4),
                    new EnvPoint((float)1.0, (float)0.0)
            };
            pointArray = tempArray;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
	   
	/**
	 * Initialisation method used to build the objects that
	 * this instrument will use
	 */
	public void createChain(){
            Oscillator wt = new Oscillator(this, Oscillator.SQUARE_WAVE, 
                this.sampleRate, 2);
            Filter filt = new Filter(wt, cutoff, Filter.LOW_PASS);
            Envelope env = new Envelope(filt, pointArray);
            Volume vol = new Volume(env);
            StereoPan span = new StereoPan(vol);
            SampleOut sout = new SampleOut(span);
	}	
}

