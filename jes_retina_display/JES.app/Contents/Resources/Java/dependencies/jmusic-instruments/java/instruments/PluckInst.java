package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

public final class PluckInst extends jm.audio.Instrument{
	/** The number of channels */
	private int channels;
	/** the sample rate passed to the instrument */
	private int sampleRate;
    /** The amount of sustein in the pluck algorithm */
    private double feedback;
	
	/** A constructor to set an initial sampling rate */
	public PluckInst(int sampleRate){
		this(sampleRate, 2);
	}

	/** A constructor to set an initial sampling rate andchannels*/
	public PluckInst(int sampleRate, int channels){
		this(sampleRate,channels, RENDER);
	}
        
    /** A constructor to set a sampling rate, channels, and real-time/render output*/
	public PluckInst(int sampleRate, int channels, int output){
		this(sampleRate,channels, output, 0.5);
	}
	
	/** A constructor to set sampling rate, channels, real-time/render output and feedback.*/
	public PluckInst(int sampleRate, int channels,int output, double feedback){
		this.sampleRate = sampleRate;
		this.channels = channels;
        this.output = output;	
		this.feedback = feedback;
	}
	
	/** 
    * Initialisation method used to build the objects that this instrument uses.
    */
	public void createChain(){
        Pluck plk = new Pluck(this, this.sampleRate, this.channels, this.feedback);
		Volume vol = new Volume(plk);
		StereoPan span = new StereoPan(vol);
        Envelope env = new Envelope(span, new double[] {0.0, 1.0, 0.9, 1.0, 1.0, 0.0});
		SampleOut sout;
        if(output == RENDER) sout = new SampleOut(env);
	}
	
	public void actionEvent(Object obj, int intValue) {
            // add real time changes here as required
	}
}