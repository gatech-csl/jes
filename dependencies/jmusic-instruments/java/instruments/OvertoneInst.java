package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;
/**
* A basic additive synthesis instrument implementation
* which includes sine waves as overtones.
* @author Andrew Brown
*/
public final class OvertoneInst extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	/** The number of channels */
	private int channels;
	/** the sample rate passed to the instrument */
	private int sampleRate;
	
	/**
	* A constructor to set an initial
	* sampling rate and number of channels.
	* @param sampleRate
	*/
	public OvertoneInst(int sampleRate){
		this.sampleRate = sampleRate;
		this.channels = 2;
	}
	//----------------------------------------------
	// Methods
	//----------------------------------------------
	/**
	* Initialisation method used to build the objects that
	* this instrument will use
	*/
	public void createChain(){
		// fundamental
		Oscillator osc0 = new Oscillator(this, Oscillator.SINE_WAVE, 
                        this.sampleRate, this.channels);
		Volume vol0 = new Volume(osc0,(float)1.0);
		// 1st harmonic
		Oscillator osc1 = new Oscillator(this, Oscillator.SINE_WAVE, 
                        this.sampleRate, this.channels);
		osc1.setFrqRatio((float)2.0);
		Volume vol1 = new Volume(osc1,(float)0.5);
		// 2nd harmonic
		Oscillator osc2 = new Oscillator(this, Oscillator.SINE_WAVE, 
                        this.sampleRate, this.channels);
		osc2.setFrqRatio((float)3.0);
		Volume vol2 = new Volume(osc2,(float)0.25);
		// 3nd harmonic
		Oscillator osc3 = new Oscillator(this, Oscillator.SINE_WAVE, 
                        this.sampleRate, this.channels);
		osc3.setFrqRatio((float)3.0);
		Volume vol3 = new Volume(osc3,(float)0.025);
		// add them together
		AudioObject[] overtones = {vol0, vol1, vol2, vol3};
		Add adder = new Add(overtones);
		Envelope env = new Envelope(adder, new double[] {0.0, 0.0, 0.1,
                                                    1.0, 1.0, 0.0});
		StereoPan span = new StereoPan(env);
		SampleOut sout = new SampleOut(span);
	}
}