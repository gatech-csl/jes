package instruments;

import jm.audio.io.*;
import jm.audio.Instrument;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;

public final class NoiseCombInst extends jm.audio.Instrument{
    private int sampleRate;
    private int channels;
    private int delay;
    private double decay;
    /**
    * Constructor
    */
    public NoiseCombInst(int sampleRate){
        this(sampleRate, 1, 0.5);
    }
    
    public NoiseCombInst(int sampleRate, int delay, double decay){
        this.sampleRate = sampleRate;
        this.delay = delay;
        this.decay = decay;
        this.channels = 1;
    }
    /**
     * This method is automatically called on startup to initialise
     * any AudioObjects used by this instrument
     */
    public void createChain() {
        Noise osc = new Noise(this, Noise.WHITE_NOISE, this.sampleRate,
            this.channels);
        Envelope env = new Envelope(osc, new double[] {0.0, 0.0, 0.1, 1.0, 0.3, 0.0});
        Comb comb = new Comb(env, delay, decay);
        SampleOut sout = new SampleOut(comb);
    }
}

