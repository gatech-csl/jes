package instruments;

import jm.audio.io.*;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;
/** An all pass filter is not unlike a comb filter in that it delays
 * the signal and recombines a scalled version. But it is more complex
 * in having both a fee back and feed forward adding of the delayed signal
 */
public final class SimpleAllPassInst extends jm.audio.Instrument{
	/** The points to use in the construction of Envelopes */
	private EnvPoint[] pointArray = new EnvPoint[10];
	/** The number of channels */
	private int channels;
	/** the sample rate passed to the instrument */
	private int sampleRate;
        /** the number of samples to delay the signal in the filter */
	private int delay;
	/** A constructor to set an initial sampling rate */
	public SimpleAllPassInst(int sampleRate){
	    this(sampleRate, 1, 10);
	}
	/** A constructor to set an initial sampling rate and number of channels.*/
	public SimpleAllPassInst(int sampleRate, int channels, int delay){
		this.sampleRate = sampleRate;
		this.channels = channels;
                this.delay = delay;
	}
	/** Initialisation method used to build the objects that this instrument will use */
	public void createChain(){
		Oscillator osc = new Oscillator(this, Oscillator.TRIANGLE_WAVE, this.sampleRate, this.channels);
		AllPass ap = new AllPass(osc, this.delay);
                SampleOut sout = new SampleOut(ap);
	}	
}


