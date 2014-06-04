import javax.sound.midi.*;
import java.io.*;

/**
 * A class with wrapper methods for JavaMusic (specifically playNote)
 */
public class JavaMusic {

    private static Synthesizer synthr;
    private static MidiChannel channel;

	/**
	 * Obtains the MIDI channel to use from the default synthesizer.
	 */
	public static void open(){
	//Sequencer seqr = MidiSystem
		try{
		    synthr = MidiSystem.getSynthesizer();
		    synthr.open();
		    //Instrument[] instruments = sb.getInstruments();
		    //Instrument instr = instruments[0];
		    MidiChannel[] channels = synthr.getChannels();
		    channel = channels[0];
		}catch(Exception e){}
    }

	/**
	 * Closes the default synthesizer.
	 */
    public static void close(){
	synthr.close();
    }

	/**
	 * Obtains the MIDI channel to use from the default synthesizer.
	 */
    public static void cleanUp(){
		getChannel().allNotesOff();
    }

   	/**
	 * Returns the MIDI channel to use from the default synthesizer.
	 * @return the MIDI channel
	 */
    public static MidiChannel getChannel(){
		if (channel == null){
		    open();
	}
	return channel;
    }

	/**
	 * Plays a note with the passed note, duration, and intensity.
	 * @param note the note (a number > 0) you want to be played.
	 * @param duration the duration you want the note to be played in milliseconds.
	 * @param intensity the intensity (a number between 0 and 127) you want the note to be played.
	 */
    public static void playNote(int note, int duration, int intensity){
		try{
		    getChannel().noteOn(note, intensity);
		    Thread.currentThread().sleep(duration);
		    getChannel().noteOff(note, intensity);
		}catch(InterruptedException e){}
    }

	/**
	 * Plays a note with the passed note, duration, and the default intensity (64).
	 * @param note the note (a number > 0) you want to be played.
	 * @param duration the duration you want the note to be played in milliseconds.
	 */
    public static void playNote(int note, int duration){
		playNote(note, duration, 64);
    }

    public static void main(String[] argv){
        playNote(66, 1000);
		playNote(68, 1000);
		playNote(70, 1000);
		playNote(71, 1000);
		playNote(73, 1000);
		playNote(75, 1000);
		playNote(77, 1000);
		playNote(78, 1000);
		close();
		System.exit(0);
    }
}
