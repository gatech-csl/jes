package instruments;

import jm.audio.Instrument;
import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

/**
 * A basic subtractive synthesizer that allows specification of
 * waveform, low pass filter cutoff, and amplitude envelope.
 * @author Andrew Brown
 */

public final class SubtractiveSynthInst extends Instrument{
    //----------------------------------------------
    // Attributes
    //----------------------------------------------
    private int sampleRate;
    private int filterCutoff;
    private int channels = 2;
    private double[] envValues;
    /** Which waveform to use for the instrument - check the Oscillator class for choices */
    private int waveform;
    /** The number of milliseconds in the attack phrase of
    * the amplitude envelope */
    private int attack;
      /** The number of milliseconds in the decay phrase of
    * the amplitude envelope */
    private int decay;
      /** The level of the sustain phrase of
    * the amplitude envelope, normally between 0.0 and 1.0 */
    private double sustain;
      /** The number of milliseconds in the release phrase of
    * the amplitude envelope */
    private int release;
    /** The number of detuned oscillators to run in parralell */
    private int numbOfOsc;
    /** transpose the second oscillator down one octave? */
    private boolean subOsc;

    //----------------------------------------------
    // Constructor
    //----------------------------------------------
    /**
    * Basic default constructor to set an initial 
    * sampling rate and otherwise uses default values.
    * @param sampleRate 
    */
    public SubtractiveSynthInst(int sampleRate){
            this(sampleRate, Oscillator.SAWTOOTH_WAVE);
    }
    
     /**
     * Constructor that sets sample rate and waveform,
    * See the jm.audio.synth.Oscillator class for valid waveform values.
     * @param sampleRate The number of samples per second (quality)
     * @param waveform The oscillator shape to use.
     */
     public SubtractiveSynthInst(int sampleRate, int waveform){
         this(sampleRate, waveform, 500);
    }

    /**
    *  Constructor that sets sample rate, waveform, and low pass filter cutoff.
    * @param sampleRate The number of samples per second (quality)
    * @param waveform The oscillator shape to use
    * @param filterCutoff The frequency above which overtones are cut
    */
    public SubtractiveSynthInst(int sampleRate, int waveform, int filterCutoff){
        this(sampleRate, waveform, filterCutoff, 10, 10, 0.6, 100);
    }

    /**
    * Constructor that sets sample rate, waveform, filter cutoff, and envelope.
    * @param sampleRate The number of samples per second (quality).
    * @param waveform The oscillator shape to use
    * @param filterCutoff The frequency above which overtones are cut.
    * @param attack An envelope value in milliseconds.
    * @param decay An envelope value in milliseconds.
    * @param sustain An envelope value for volume, from 0.0 - 1.0.
    * @param release An envelope value in milliseconds.
    */
    public SubtractiveSynthInst(int sampleRate, int waveform, int filterCutoff,
				int attack, int decay, double sustain, int release){
	this(sampleRate, waveform, filterCutoff, attack, decay, sustain, release, 1);
    }
	/**
	* Constructor that sets sample rate, waveform, filter cutoff, and envelope.
	* @param sampleRate The number of samples per second (quality).
	* @param waveform The oscillator shape to use
	* @param filterCutoff The frequency above which overtones are cut.
	* @param attack An envelope value in milliseconds.
	* @param decay An envelope value in milliseconds.
	* @param sustain An envelope value for volume, from 0.0 - 1.0.
	* @param release An envelope value in milliseconds.
	* @param numbOfOsc The number of parallel oscillators to use.
	*/
	public SubtractiveSynthInst(int sampleRate, int waveform, int filterCutoff,
			     int attack, int decay, double sustain, int release, int numbOfOsc){
	    this(sampleRate, waveform, filterCutoff, attack, decay, sustain, release, numbOfOsc, false);
    }

	/**
	* Constructor that sets sample rate, waveform, filter cutoff, and envelope.
	    * @param sampleRate The number of samples per second (quality).
	    * @param waveform The oscillator shape to use
	    * @param filterCutoff The frequency above which overtones are cut.
	    * @param attack An envelope value in milliseconds.
	    * @param decay An envelope value in milliseconds.
	    * @param sustain An envelope value for volume, from 0.0 - 1.0.
	    * @param release An envelope value in milliseconds.
	    * @param numbOfOsc The number of parallel oscillators to use.
	* @param subOsc A choice about lowering the second osc one octave.
	    */
	public SubtractiveSynthInst(int sampleRate, int waveform, int filterCutoff,
				int attack, int decay, double sustain, int release, int numbOfOsc, boolean subOsc){
	    this.sampleRate = sampleRate;
	    this.waveform = waveform;
	    this.filterCutoff = filterCutoff;
	    this.envValues = envValues;
	    this.attack = attack;
	    this.decay = decay;
	    this.sustain = sustain;
	    this.release = release;
	    this.numbOfOsc = numbOfOsc;
	    this.subOsc = subOsc;
	}

    //----------------------------------------------
    // Methods 
    //----------------------------------------------   
    /**
    * Initialisation method used to build the objects that
    * this instrument will use and specify thier interconnections.
    */
    public void createChain(){
	// LFO modulator
	Value modFrequency[] = new Value[numbOfOsc];
	Oscillator modulator[] = new Oscillator[numbOfOsc];
	Oscillator[] oscArray = new Oscillator[numbOfOsc];
	Value constFreq[] = new Value[numbOfOsc];
	Add add[] = new Add[numbOfOsc];
	// volume balance
	Volume[] volArray = new Volume[numbOfOsc];
	// fill
	for(int i=0;i<numbOfOsc;i++){
	    // modulator
	    modFrequency[i] = new Value(this, this.sampleRate, this.channels, (float)(Math.random() * 0.2));
	    modulator[i] = new Oscillator(modFrequency[i], Oscillator.SINE_WAVE, Oscillator.FREQUENCY);
            modulator[i].setAmp((float)0.3);
            // constant
	    constFreq[i] = new Value(this, this.sampleRate, this.channels, Value.NOTE_PITCH);
            add[i] = new Add(new AudioObject[] {constFreq[i], modulator[i]});
	    // carrier
	    oscArray[i] = new Oscillator(add[i], this.waveform, Oscillator.FREQUENCY);
	    //oscArray[i] = new Oscillator(this, this.waveform, this.sampleRate, this.channels);
	    if (i%2 == 0 && i > 0) {
		oscArray[i].setFrqRatio((float)(1.0 + 0.001 * (i - 1)));
	    } else {
		if (this.subOsc && i == 1) {
		    oscArray[i].setFrqRatio((float)(0.5 - 0.001 * i));
		} else oscArray[i].setFrqRatio((float)(1.0 - 0.001 * i));
	    }
	    // volume difference between main and other oscillators
	    if (i == 0) volArray[i] = new Volume(oscArray[i], 1.0);
	    else volArray[i] = new Volume(oscArray[i], 0.3);
	    
	}
	Add add2 = new Add(volArray);
        Filter filt = new Filter(add2, this.filterCutoff, Filter.LOW_PASS);
        ADSR env = new ADSR(filt, attack, decay, sustain, release);
        //Envelope env = new Envelope(filt, new double[] {0.0, 0.0, 0.1, 1.0, 1.0, 0.0});
        Volume vol = new Volume(env);
        StereoPan pan = new StereoPan(vol);
        SampleOut sout = new SampleOut(pan);
    }	
}

