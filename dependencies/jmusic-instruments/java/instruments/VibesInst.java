package instruments;


import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;
import jm.audio.Instrument;

/**
 * A basic additive synthesis instrument implementation
 * which implements envelope and volume control
 * @author Andrew Sorensen and Andrew Brown
 */
public final class VibesInst extends Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	/** the relative frequencies which make up this note */
	private float[] frequencies;
	/** the volumes to use for each frequency */
	private float[] volumes;
	/** The points to use in the construction of Envelopes */
	private EnvPoint[][] points;
	/** Pan */
	private float pan;
	/** The sample Rate to use */
	private int sampleRate;
	/** The Oscillators to use for each frequency specified */
	private Oscillator[] wt;
	/** Splitter object splits the signal into multiple outputs */
	//private Splitter split;
	/** The envelope to apply to each Oscillator's output */
	private Envelope[] env;
	/** The volume to apply to each envelopes output */
	private Volume[] vol;
	/** The object that adds it all together */
	private Add add;
	/** This is where it all gets added together */
	//public AUOut auFile;
	/** Stereo Pan Audio Object */
	private StereoPan[] span;
	/** resample */
	//private ReSample[] resample;

	private boolean header = true;
	private static int count = 0;
	private SampleOut sout;

	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	public VibesInst(int sampleRate){
		//Provide some defaults
		this.sampleRate = sampleRate;
		// how many partials in this additive synthesis isnstrument?
		int overtones = 3;
		// create an envelope for each partial
		EnvPoint[] pointArray = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.002, (float)1.0),
			new EnvPoint((float)0.3, (float)0.3),
			new EnvPoint((float)0.9, (float)0.1),
			new EnvPoint((float)1.0, (float)0.0)
		};
		
		EnvPoint[] pointArray2 = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.02, (float)1.0),
			new EnvPoint((float)0.2, (float)0.2),
			new EnvPoint((float)0.9, (float)0.0)
		};
		
		EnvPoint[] pointArray3 = {
			new EnvPoint((float)0.0, (float)0.0),
			new EnvPoint((float)0.02, (float)1.0),
			new EnvPoint((float)0.4, (float)0.3),
			new EnvPoint((float)0.8, (float)0.0)
		};
		
		this.points=new EnvPoint[overtones][4];
		this.frequencies=new float[overtones];
		this.volumes=new float[overtones];
		// Extend these parrameters for each overtone
		this.points[0]=pointArray; this.points[1]=pointArray2; this.points[2]=pointArray3;
		this.frequencies[0]=(float)1.0; this.frequencies[1]=(float)2.7; this.frequencies[2]=(float)6.75;
		this.volumes[0]=(float)1.0; this.volumes[1]=(float)0.77; this.volumes[2]=(float)0.7;
	}
	/**
	 * Basic default constructor to set an initial 
	 * sampling rate and buffersize in addition
	 * to the neccessary frequency relationships 
	 * and volumes for each frequency to be added
	 * the instrument
	 * @param sampleRate 
	 * @param frequencies the relative freqencies to use
	 * @param volumes the volumes to use for the frequencies
	 */
	public VibesInst(int sampleRate, float[] frequencies, 
						float[] volumes,EnvPoint[][] points){
		this.frequencies = frequencies;
		this.volumes = volumes;
		this.points = points;
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
		//define the audio chain(s)
		env = new Envelope[frequencies.length];
		vol = new Volume[frequencies.length];
		span = new StereoPan[frequencies.length];
		wt = new Oscillator[frequencies.length];
		for(int i=0;i<frequencies.length;i++){
			wt[i] = new Oscillator(this, Oscillator.SINE_WAVE, 
                            this.sampleRate, 2);
			wt[i].setFrqRatio(frequencies[i]); 
			env[i] = new Envelope(wt[i], points[i]);
			vol[i] = new Volume(env[i], volumes[i]);
			span[i] = new StereoPan(vol[i], this.pan);
		}
		//And now the add object brings us back to one path.
		add = new Add(span);
		sout = new SampleOut(add);
	}
}
