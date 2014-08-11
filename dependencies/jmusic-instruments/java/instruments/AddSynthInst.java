package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;
import jm.audio.Instrument;

/**
 * A basic additive synthesis instrument implementation
 * which implements an envelope and allows specification
 * of the overtone frequency ratios and volume levels.
 * @author Andrew Brown and Andrew Sorensen
 */
public final class AddSynthInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	/** the relative overtoneRatios which make up this note */
	private double[] overtoneRatios;
	/** the overtoneVolumes to use for each frequency */
	private double[] overtoneVolumes;
	/** The points to use in the construction of Envelopes */
	private double[][] allEnvPoints;
	/** Default Envelope Values */
	private double[] envPoints = {0.0, 0.0, 0.05, 1.0, 0.15, 0.4, 0.9, 0.3, 1.0, 0.0};
	/** The sample rate to use */
	private int sampleRate;

	//----------------------------------------------
	// Constructors
	//----------------------------------------------
	/**
	* Basic default constructor to set an initial sampling rat.
	* @param sampleRate
	*/
	public AddSynthInst(int sampleRate){
		//Provide some defaults
		this.sampleRate = sampleRate;
		
		double[][] tempPoints = new double[5][];
		for (int i=0; i<5; i++) {
			tempPoints[i] = envPoints;
		}
		allEnvPoints = tempPoints;
		
		double[] temp1 = {1.0f, 3.0f, 5.0f, 7.0f, 9.0f};
		this.overtoneRatios = temp1;
		double[] temp2 = {1.0f, 0.5f, 0.35f, 0.25f, 0.15f};
		this.overtoneVolumes = temp2;
	}
	/**
	* Basic default constructor to set an initial 
	* sampling rate and buffersize in addition
	* to the neccessary frequency relationships 
	* and overtoneVolumes for each frequency to be added
	* the instrument
	* @param sampleRate 
	* @param overtoneRatios the relative freqencies to use
	* @param overtoneVolumes the overtoneVolumes to use for the overtoneRatios
	* @param EnvPointArray A two dimensional array of doubles as break point values between 0.0 and 1.0
	*/
	public AddSynthInst(int sampleRate, double[] overtoneRatios, 
                            double[] overtoneVolumes, double[][] envPointArray){
		this.overtoneRatios = overtoneRatios;
		this.overtoneVolumes = overtoneVolumes;
		// add envelopes for each harmonic
		//double[][] tempPoints = new double[envPointArray.length][];
		//for (int i=0; i<envPointArray.length; i++) {
		//	tempPoints[i] = envPoints;
		//}
		allEnvPoints = envPointArray; //tempPoints;
		
		this.sampleRate = sampleRate;
	}

	//----------------------------------------------
	// Methods 
	//----------------------------------------------
	/**
	 * Initialisation method is used to build the objects that
	 * this instrument will use
	 */
	public void createChain(){
		Envelope[] env = new Envelope[overtoneRatios.length];
		Volume[] vol = new Volume[overtoneRatios.length];
		Oscillator[] osc = new Oscillator[overtoneRatios.length];
		for(int i=0;i<overtoneRatios.length;i++){
			osc[i] = new Oscillator(this, Oscillator.SINE_WAVE, 
                            this.sampleRate,2);
			osc[i].setFrqRatio((float)overtoneRatios[i]);
			env[i] = new Envelope(osc[i], allEnvPoints[i]);
			vol[i] = new Volume(env[i], (float)overtoneVolumes[i]);
		}
		//And now the add object brings us back to one path.
		Add add = new Add(vol);
                StereoPan span = new StereoPan(add);
		SampleOut sout = new SampleOut(span);
	}
}
