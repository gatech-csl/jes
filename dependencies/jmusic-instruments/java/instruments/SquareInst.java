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

public final class SquareInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	
	/** The points to use in the construction of Envelopes */
	private double[] envArray = {0.0, 0.0, 0.02, 1.0, 0.15, 0.6,
			0.95, 0.4, 1.0, 0.0};
	private int sampleRate;
    private int channels;
    private SampleOut sout;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	
        /**
	 * Basic default constructor using default settings.
         */
        public SquareInst() {
            this(44100);
        }
        
        /**
	 * Basic default constructor to set an initial 
	 * sampling rate.
	 * @param sampleRate 
	 */
	public SquareInst(int sampleRate){
            this(sampleRate, 2);
        }
        
        /**
	 * Basic default constructor to set an initial 
	 * sampling rate and number of channels.
	 * @param sampleRate The audio quality.
         * @param channels The number of channels.
	 */

        public SquareInst(int sampleRate, int channels){
            this.sampleRate = sampleRate;
            this.channels = channels;
        }
        
        /**
	 * Basic default constructor to set an initial 
	 * sampling rate, number of channels, and amplitude envelope.
	 * @param sampleRate The audio quality.
         * @param channels The number of channels.
         * @param double[] An array of envelope break points.
	 */

        public SquareInst(int sampleRate, int channels, double[] envArray){
		this.sampleRate = sampleRate;
                this.channels = channels;
		this.envArray = envArray;
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
                    this.sampleRate, channels);
		Envelope env = new Envelope(wt, envArray);
		Volume vol = new Volume(env);
		StereoPan span = new StereoPan(vol);
		if (output == RENDER) sout = new SampleOut(span);
	}	
}

