package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.Instrument;

/**
* An additive synthesis instrument implementation
* which cross fades two different spectra, each
* with five partials.
* @author Andrew Brown
*/

public final class AddMorphInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	private int overtones = 10;
	/** the relative frequencies which make up this note */
	private double[] freqVals = {1.0, 3.0, 5.0, 7.0, 9.0, 1.0, 2.8, 5.6, 8.4, 11.0};
	/** the volumes to use for each frequency */
	private double[] volVals = {1.0, 0.7, 0.5, 0.3, 0.2, 1.0, 0.7, 0.5, 0.3, 0.2};
	/** The points to use in the construction of Envelopes */
	private double[][] points = new double[overtones][6];
	private double[] pointArray1 = {0.0, 0.0, 0.02, 1.0, 1.0, 0.0};
	private double[] pointArray2 = {0.0, 0.0, 0.98, 1.0, 1.0, 0.0};
	
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
	public AddMorphInst(int sampleRate){
		this.sampleRate = sampleRate;
		// set up envelope points
		for (int i=0; i<5; i++) {
			points[i] = pointArray1;
		}
		for (int i=5; i<10; i++) {
			points[i] = pointArray2;
		}
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
