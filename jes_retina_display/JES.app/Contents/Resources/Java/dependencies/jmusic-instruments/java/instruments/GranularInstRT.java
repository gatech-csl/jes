package instruments;

/**
 * GranularInstRT.java
 * Author: Timothy Opie
 * Last Modified: 04/08/2002
 * Designed to function with jMusic
 * by Andrew Brown and Andrew Sorenson
 * This class is identical to GranularInst.java 
 * except that the line:
 * SampleOut sout = new SampleOut(pan);
 * has been commented out.
 * Please keep these two files identical 
 * except for that one difference!
 */

import jm.audio.io.*;
import jm.audio.Instrument;
import jm.audio.synth.*;
import jm.music.data.Note;
import jm.audio.AudioObject;
import jm.audio.io.RTIn;

public final class GranularInstRT extends jm.audio.Instrument{
	//----------------------------------------------
	// Attributes
	//----------------------------------------------
	// the name of the sample file
	private String fileName;
	// How many channels is the sound file we are using
	private int channels;
	private int sampleRate;
	// the base frequency of the sample file to be read in
	//private double baseFreq;
	// should we play the wholeFile or just what we need for note duration
	//private boolean wholeFile;
	// The points to use in the construction of Envelopes
	private EnvPoint[] pointArray = new EnvPoint[10];

	private Granulator grain;
        private Volume vol;
	private StereoPan pan;
	// used to define the audio input type
	private int sounds;
	
	//----------------------------------------------
	// Constructor
	//----------------------------------------------
	public GranularInstRT(String fileName){
		// Use this constructor when you want to granulate an audio file.
		// Only the name of the audio file is required
		this.fileName = fileName;
		this.sounds = 7;
	}

	public GranularInstRT(String fileName, int sampleRate, int channels){
                // Use this constructor when you want to granulate an audio file.
                // Only the name of the audio file is required
                this.fileName = fileName;
                this.sounds = 7;
		this.sampleRate=sampleRate;
		this.channels=channels;
        }

	public GranularInstRT(int sounds){
		/**
    		 * The variable sounds is an integer used to select 
		 * which sound source type will be used.
		 * It will be defined as such:
		 * SINE WAVE = 0
		 * COSINE WAVE = 1
		 * TRIANGLE WAVE = 2
		 * SQUARE WAVE = 3
		 * SAWTOOTH WAVE = 4
		 * SAWDOWN WAVE = 5
		 * SABERSAW WAVE = 6
		 * AUDIO FILE = 7
		 * MICROPHONE = 11
		 *
		 * Use this constructor when you want to granulate internally
		 * produced audio. Note: you can still granulate audio files
		 * if you use this constructor, but it will assume the audio 
		 * file has the name song1.au.
		 */
		this.sounds = sounds;
		this.fileName = "song1.au";
	}

        public GranularInstRT(int sounds, int sampleRate, int channels){
        	this.sounds = sounds;
                this.fileName = "song1.au";
                this.sampleRate=sampleRate;
                this.channels=channels;
        }
	
	//----------------------------------------------
	// Methods
	//----------------------------------------------
	/**
	 * Create the Audio Chain for this Instrument 
	 * and assign the primary Audio Object(s). The 
	 * primary audio object(s) are the one or more
	 * objects which head up the chain(s)
	 */
	public void createChain(){
	    // define the chain
	    if (sounds<0 || sounds>6){
		if (sounds>10){
		    // if sounds is > 10 then the microphone is the input
		    // source. Default is 11, but this way it doesn't matter
		    // if a wrong number gets inputed 
		    // (8820 = buffer length of 1/5 of a second)
		    RTIn grin = new RTIn(this, sampleRate, channels, 8820);
		    grain = new Granulator(grin, sampleRate, channels, 50,100); 
		    vol = new Volume(grain,0.95f);
        	    //Volume vol2 = new Volume(vol,0.1f);
        	    pan = new StereoPan(vol);
	          //SampleOut sout = new SampleOut(pan);
		} else {
		    // if sounds is < 0 or > 6 and < 11 then it will
		    // process an audio file. Default is 7.  Again it is 
		    // very open ended to accommodate wrong input numbers. 
        	    SampleIn grin = new SampleIn(this, this.fileName);
		    grain = new Granulator(grin,sampleRate, channels, 50,100); 
		    vol = new Volume(grain, 0.95f);
        	    //Volume vol2 = new Volume(vol,0.1f);
        	    pan = new StereoPan(vol);
                    //SampleOut sout = new SampleOut(pan);
		}
    	    } else {
		// At this stage the only values left are between 0-6
		// These correspond directly to the oscillator input
		// values, so can be added directly.
        	Oscillator grin = new Oscillator(this, sounds, sampleRate, channels);
		grain = new Granulator(grin,sampleRate, channels, 50,100); 
		vol = new Volume(grain, 0.95f);
        	//Volume vol2 = new Volume(vol,0.1f);
        	pan = new StereoPan(vol);
            //SampleOut sout = new SampleOut(pan);
    	    }
	}

	public void setGrainsPerSecond(int sp){
		grain.setGrainsPerSecond(sp);
	}

	public void setGrainDuration(int gdur){
		grain.setGrainDuration(gdur);
	}

        public void setEnvelopeType(int et){
                grain.setEnvelopeType(et);
        }  
	
	public void setFreqMod(float fmod){
		grain.setFreqMod(fmod);
	}
	public void setRandomIndex(boolean b){
		grain.setRandomIndex(b);
	}
	public void setRandomGrainDuration(boolean b){
		grain.setRandomGrainDuration(b);
	}
	
	public void setRandomGrainTop(int top){
		grain.setRandomGrainTop(top);
	}
	public void setRandomGrainBottom(int b){
		grain.setRandomGrainBottom(b);
	}
	public void setRandomFreq(boolean bool){
		grain.setRandomFreq(bool);
	}
	public void setRandomDist(int rdist){
		grain.setRandomDist(rdist);
	}
	public void setRandomFreqBottom(float fbot){
		grain.setRandomFreqBottom(fbot);
	}
	public void setRandomFreqTop(float ftop){
		grain.setRandomFreqTop(ftop);
	}
        public void setVolume(float d){
		vol.setVolume(d);
	}
      	public void setPan(float p){
		pan.setPan(p);
	}
}
