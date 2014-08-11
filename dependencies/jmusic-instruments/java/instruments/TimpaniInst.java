package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.Instrument;

/**
 * A basic additive synthesis instrument implementation
 * which implements envelope and volume control
 * @author Andrew Sorensen and Andrew Brown
 */
public final class TimpaniInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	private int overtones = 5;
	/** the relative frequencies which make up this note */
	private double[] freqVals = {1.0, 1.42, 1.53, 1.77, 1.94};
	/** the volumes to use for each frequency */
	private double[] volVals = {1.0, 0.8, 0.7, 0.6, 0.5};
	/** The points to use in the construction of Envelopes */
	private double[][] points = new double[overtones][8];
	private double[] pointArray1 = {0.0, 0.0, 0.002, 1.0, 0.3, 0.3, 1.0, 0.0};
	private double[] pointArray2 = {0.0, 0.0, 0.05, 1.0, 0.2, 0.4, 1.0, 0.0};
	private double[] pointArray3 = {0.0, 0.0, 0.1, 1.0, 0.4, 0.3, 1.0, 0.0};
	
	/** Pan */
	private float pan;
	/** The sample Rate to use */
	private int sampleRate;
	/** The Oscillators to use for each frequency specified */
	private Oscillator[] osc;
	/** The envelope to apply to each Oscillator's output */
	private Envelope[] env;
	/** The volume to apply to each envelopes output */
	private Volume[] vol;	

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	public TimpaniInst(int sampleRate){
		this.sampleRate = sampleRate;
		// set up envelope points
		points[0] = pointArray1;
		points[1] = pointArray2;
		points[2] = pointArray3;
		points[3] = pointArray2;
		points[4] = pointArray3;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
	/**
	 * Initialisation method is used to build the objects that
	 * this instrument will use
	 */
	public void createChain(){
		//define the audio chain(s)
		osc = new Oscillator[overtones];
		env = new Envelope[overtones];
		vol = new Volume[overtones];
		for(int i=0;i<overtones;i++){
			osc[i] = new Oscillator(this, Oscillator.SINE_WAVE,
                            this.sampleRate, 2);
			osc[i].setFrqRatio((float)freqVals[i]); 
			env[i] = new Envelope(osc[i], points[i]);
			vol[i] = new Volume(env[i], (float)volVals[i]);
		}
		//And now the add object brings us back to one path.
		Add add = new Add(vol);
		StereoPan span = new StereoPan(add);
		SampleOut sout = new SampleOut(span);
	}
}
