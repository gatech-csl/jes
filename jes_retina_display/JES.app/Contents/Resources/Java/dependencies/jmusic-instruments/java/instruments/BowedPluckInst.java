package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

public final class BowedPluckInst extends jm.audio.Instrument{
	/** The points to use in the construction of Envelopes */
	private EnvPoint[] pointArray = new EnvPoint[10];
	/** The number of channels */
	private int channels;
	/** the sample rate passed to the instrument */
	private int sampleRate;
        /** the filter cutoff frequency in hertz */
	private int cutoff;
	/** A constructor to set an initial sampling rate */
	public BowedPluckInst(int sampleRate){
	    this(sampleRate, 1, 8000);
	}
	/** A constructor to set an initial sampling rate and number of channels.*/
	public BowedPluckInst(int sampleRate, int channels, int cutoff){
		this.sampleRate = sampleRate;
		this.channels = channels;
                this.cutoff = cutoff;
	}
	/** Initialisation method used to build the objects that this instrument will use */
	public void createChain(){
		Pluck plk = new Pluck(this,sampleRate, this.channels);
                Filter filt = new Filter(plk, this.cutoff, Filter.LOW_PASS);
                Envelope env = new Envelope(filt, new double[] {0.0, 0.0, 0.1, 0.5, 0.3, 1.0, 0.4, 0.5, 1.0, 0.0});
		Volume vol = new Volume(env);
                SampleOut sout = new SampleOut(vol);
	}	
}


