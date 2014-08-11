package instruments;

import jm.audio.io.*;

import jm.audio.synth.*;

import jm.music.data.Note;

import jm.audio.AudioObject;



/**

 * A basic layered synthesis instrument

 * @author Andrew Brown after Andrew Sorensen

 */





public final class BreathyFluteInst extends jm.audio.Instrument{

	//----------------------------------------------

	// Attributes

	//----------------------------------------------

	/** The points to use in the construction of Envelopes */

	private EnvPoint[] pointArray = new EnvPoint[10];

	/** The points to use in the construction of Envelopes */

	private EnvPoint[] pointArray2 = new EnvPoint[10];

	/** The number of channels */

	private int channels;

	/** the sample rate passed to the instrument */

	private int sampleRate;



	//----------------------------------------------

	// Constructor

	//----------------------------------------------

	/**

	 * Basic default constructor to set an initial 

	 * sampling rate.

	 * @param sampleRate 

	 */

	public BreathyFluteInst(int sampleRate){

	    this(sampleRate, 1);

	}

	/**

	 * A constructor to set an initial 

	 * sampling rate and number of channels.

	 * @param sampleRate 

	 */

	public BreathyFluteInst(int sampleRate, int channels){

		this.sampleRate = sampleRate;

		this.channels = channels;

		// tone env

		EnvPoint[] tempArray = {

			new EnvPoint((float)0.0, (float)0.0),

			new EnvPoint((float)0.2, (float)1.0),

			new EnvPoint((float)0.5, (float)0.7),

			new EnvPoint((float)0.8, (float)0.5),

			new EnvPoint((float)1.0, (float)0.0)

		};

		pointArray = tempArray;

		// Noise env

		EnvPoint[] tempArray2 = {

			new EnvPoint((float)0.0, (float)0.0),

			new EnvPoint((float)0.05, (float)0.7),

			new EnvPoint((float)0.2, (float)0.1),

			new EnvPoint((float)1.0, (float)0.0)

		};

		pointArray2 = tempArray2;

	}



	//----------------------------------------------

	// Methods 

	//----------------------------------------------

	   

	/**

	 * Initialisation method used to build the objects that

	 * this instrument will use

	 */

	public void createChain(){

                // main tone

		Oscillator wt = new Oscillator(this, Oscillator.SINE_WAVE, this.sampleRate, channels);

		Volume vol = new Volume(wt, (float)1.0);

		// overtone

		Oscillator wt2 = new Oscillator(this, Oscillator.SINE_WAVE, this.sampleRate, channels);

		wt2.setFrqRatio((float)2.001);

		Volume vol2 = new Volume(wt2, (float)0.5);

		// overtone

		Oscillator wt3 = new Oscillator(this, Oscillator.SINE_WAVE, this.sampleRate, channels);

		wt3.setFrqRatio((float)4.0);

		Volume vol3 = new Volume(wt3, (float)0.1);

		// breath

		Noise noise = new Noise(this, Noise.WHITE_NOISE, this.sampleRate );

		Volume vol4 = new Volume(noise, (float)0.2);

		// all together now

		AudioObject[] parts = {vol, vol2, vol3, vol4};

		Add add = new Add(parts);

		Envelope env = new Envelope(add, pointArray);

		StereoPan span = new StereoPan(env);

		SampleOut sout = new SampleOut(span);

	}	

}

