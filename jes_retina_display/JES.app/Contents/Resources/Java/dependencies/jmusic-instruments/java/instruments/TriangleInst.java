package instruments;


import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic triangle wave instrument implementation
 * which implements envelope and volume control
 * @author Andrew Brown and Andrew Sorensen
 */

public final class TriangleInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	
	/** The points to use in the construction of Envelopes */
	private EnvPoint[] pointArray = new EnvPoint[10];
	private int sampleRate;
	private int channels;
    private SampleOut sout;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate and buffersize in addition
	 * to the neccessary frequency relationships 
	 * and volumes for each frequency to be added
	 * the instrument
	 * @param sampleRate 
	 */
	public TriangleInst(int sampleRate){
		this(sampleRate, 2);
	}
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate and buffersize in addition
	 * to the neccessary frequency relationships 
	 * and volumes for each frequency to be added
	 * the instrument
	 * @param sampleRate In hertz
	 * @param channels 1 = mono, 2 = Stereo
	 */
	public TriangleInst(int sampleRate, int channels){
		this.sampleRate = sampleRate;
		this.channels = channels;
		EnvPoint[] tempArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.02, (float)1.0),
			new EnvPoint((float)0.15, (float)0.6),
			new EnvPoint((float)0.9, (float)0.3),
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
		Oscillator wt = new Oscillator(this, Oscillator.TRIANGLE_WAVE,
                    this.sampleRate, this.channels);
		Envelope env = new Envelope(wt, pointArray);
		Volume vol = new Volume(env);
		Filter filt = new Filter(vol, (float)(this.sampleRate/2.1),
			Filter.LOW_PASS);
		StereoPan span = new StereoPan(filt);
		if(output == RENDER) sout = new SampleOut(span);
	}	
}

