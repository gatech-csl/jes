import javax.sound.midi.*;
import java.io.*;

/**
 * Class that knows how to play notes using the midi standard
 * Copyright 2004 Georgia Institute of Technology
 * <br>
 * @author unknown Georgia Tech Students
 * @author Barbara Ericson
 */
public class MidiPlayer
{
  ////////////// fields //////////////////////////////////

  ///////////// constants ////////////////////////////////
  public static final int PIANO = 0;
  public static final int HARMONICA = 22;
  public static final int MUSIC_BOX = 10;
  public static final int XYLOPHONE = 11;
  public static final int GUITAR = 24;
  public static final int STEEL_GUITAR = 25;
  public static final int JAZZ_GUITAR = 26;
  public static final int BASS = 32;
  public static final int VIOLIN = 40;
  public static final int CELLO = 42;
  public static final int HARP = 46;
  public static final int TIMPANI = 47;
  public static final int TRUMPET = 56;
  public static final int TROMBONE = 57;
  public static final int TUBA = 58;
  public static final int FRENCH_HORN = 60;
  public static final int ALTO_SAX = 65;
  public static final int TENOR_SAX = 66;
  public static final int OBOE = 68;
  public static final int CLARINET = 71;
  public static final int PICCOLO = 72;
  public static final int FLUTE = 73;
  public static final int WHISTLE = 78;
  public static final int BIRD = 123;
  public static final int TELEPHONE = 124;
  public static final int HELICOPTER = 125;
  public static final int APPLAUSE = 126;
  public static final int ICE_CUBE = 343;

  private Synthesizer synth; // the music synthesizer
  private Soundbank soundbank; // the sound bank
  private MidiChannel[] channels; // all the channels
  private MidiChannel channel;

  //////////// Constructors //////////////////////////////

  /**
   * Constructor that takes no arguments
   */
  public MidiPlayer()
  {
    /* try to create a synthesizer and get an
     * instrument and channel
     */
    try{
      synth = MidiSystem.getSynthesizer();
      synth.open();
      soundbank = synth.getDefaultSoundbank();
      if (soundbank != null)
        synth.loadAllInstruments(soundbank);
      channels = synth.getChannels();
      channel = channels[0];
    }catch(Exception e){
      System.out.println(e);
    }
  }

  /////////////////// Methods //////////////////////////////////

  /**
   * Method to return the synthesizer
   * @return the synthesizer
   */
  public Synthesizer getSynthesizer() { return synth;}

  /**
   * Method to close the midi player
   */
  public void close(){
    synth.close();
  }

  /**
   * Method to clean up the midi player
   */
  public void cleanUp(){
    MidiChannel c = null;
    for (int i=0; i < channels.length; i++) {
      c = channels[i];
      if (c != null)
        c.allNotesOff();
    }
  }

  /**
   * Method to play a note
   * @param note the note to play (0 to 127, 60 is middle C)
   * @param duration how long to play the note in milliseconds
   * @param intensity how loud to play the note (how hard the key
   * was struck on a piano)
   */
  public void playNote(int note, int duration, int intensity)
  {
    try {
      channel.noteOn(note, intensity);
      Thread.currentThread().sleep(duration);
      channel.noteOff(note, intensity);
    } catch(InterruptedException e){}
  }

  /**
   * Method to rest for a specified number of milliseconds
   * @param duration the amount to rest in milliseconds
   */
  public void rest(int duration)
  {
    try {
      Thread.currentThread().sleep(duration);
    } catch(InterruptedException e){}
  }

  /**
   * Method to change the current channel
   * @param index the index of the channel to use
   */
  public void setChannel(int index)
  {
    channel = channels[index];
  }

  /**
   * Method to set the instrument to play
   * @param num a number from 0 to 127 that represents
   * the instruments
   */
  public void setInstrument(int num)
  {
    try {
      channel.programChange(num);
    } catch (Exception ex) {
      System.out.println("Sorry instrument number " +
                         num + " is not available");
    }
  }

  /**
   * Method to get the map of index number to instrument names
   */
  public void getInstrumentNames()
  {
    Instrument[] ia = synth.getLoadedInstruments();
    for (int i = 0; i < ia.length; i++)
      System.out.println("Index: " + i + " Name: " + ia[i].getName());
  }

  /**
   * Method to play a note
   * @param note the note to play
   * @param duration how long to play the note
   */
  public void playNote(int note, int duration){
    playNote(note, duration, 64);
  }

  /**
   * Method to play an array of notes with the given
   * durations and intensities
   * @param index the index of the channel to use
   * @param notes the array of notes to play (0-127)
   * @param durations the array of durations to
   * use for playing the notes in milliseconds
   * @param intensities the array of intensities (loudness)
   */
  public void playNotesOnChannel(int index,
                                 int [] notes,
                                 int [] durations,
                                 int [] intensities)
  {
    // set the channel based on the index
    channel = channels[index];

    // loop through the array of notes
    for ( int i = 0; i < notes.length; i++ ) {
      channel.noteOn( notes[ i ], intensities[ i ] );
      try { Thread.sleep( durations[ i ] ); } catch
        ( InterruptedException e ) { }
    }

    // turn off the notes
    for ( int i = 0; i < notes.length; i++ )
      channel.noteOff( notes[ i ] );
  }

  /**
   * Method to play the first 3 measures of Jingle Bells
   */
  private void playJingleBellsM1To3()
  {
    // measure 1
    playNote(52,250); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 2
    playNote(52,500); // e quarter note
    rest(250);        // rest
    playNote(52,125); // e sixteenth note
    playNote(52,125); // e sixteenth note

    // measure 3
    playNote(52,500); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note
  }

  /**
   * Method to play measure 5 of Jingle Bells
   */
  private void playJingleBellsM5()
  {
    // measure 5
    playNote(53,250); // f eighth note
    playNote(61,250); // d flat eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
  }

  /**
   * Method to play measure 7 of Jingle Bells
   */
  private void playJingleBellsM7()
  {
    // measure 7
    playNote(55,250); // g eighth note
    playNote(65,250); // f eighth note
    playNote(63,250); // e flat eighth note
    playNote(61,250); // d flat eighth note
  }

  /**
   * Method to play measure 9 of Jingle Bells
   */
  private void playJingleBellsM9()
  {
    // measure 9
    playNote(52,250); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note
  }

  /**
   * Method to play measure 11 of Jingle Bells
   */
  private void playJingleBellsM11()
  {
    // measure 11
    playNote(52,250); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note
  }

  /**
   * Method to play measures 13-16 of Jingle Bells
   */
  private void playJingleBellsM13To16()
  {
    // measure 13
    playNote(53,250); // f eighth note
    playNote(61,250); // d flat eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note

    // measure 14
    playNote(55,250); // g eighth note
    playNote(63,250); // e flat eighth note
    playNote(62,250); // d eighth note
    playNote(63,250); // e flat eighth note

    // measure 15
    playNote(65,250); // f eighth note
    playNote(63,250); // e flat eighth note
    playNote(61,250); // d flat eighth note
    playNote(58,250); // b flat eighth note

    // measure 16
    playNote(56,1000); // a flat half note
  }

  /**
   * Method to play the first verse of jingle bells
   * with each measure taking 1000 milliseconds (1 second)
   * It is in 2/4 time
   */
  private void playJingleBellsV1()
  {
    // measure 1
    playNote(52,250); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 2
    playNote(52,500); // e quarter note
    rest(250);        // rest
    playNote(52,125); // e sixteenth note
    playNote(52,125); // e sixteenth note

    // measure 3
    playNote(52,500); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 4
    playNote(53,1000); // f half note

    // measure 5
    playNote(53,250); // f eighth note
    playNote(61,250); // d flat eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note

    // measure 6
    playNote(55,1000); // g half note

    // measure 7
    playNote(55,250); // g eighth note
    playNote(65,250); // f eighth note
    playNote(63,250); // e flat eighth note
    playNote(61,250); // d flat eighth note

    // measure 8
    playNote(60,1000); // c half note

    // measure 9
    playNote(52,250); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 10
    playNote(52,1000); // e half note

    // measure 11
    playNote(52,250); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 12
    playNote(53,1000); // f half note

    // measure 13
    playNote(53,250); // f eighth note
    playNote(61,250); // d flat eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note

    // measure 14
    playNote(55,250); // g eighth note
    playNote(63,250); // e flat eighth note
    playNote(62,250); // d eighth note
    playNote(63,250); // e flat eighth note

    // measure 15
    playNote(65,250); // f eighth note
    playNote(63,250); // e flat eighth note
    playNote(61,250); // d flat eighth note
    playNote(58,250); // b flat eighth note

    // measure 16
    playNote(56,1000); // a flat half note

  }

   /**
   * Method to play the first verse of jingle bells
   * with each measure taking 1000 milliseconds (1 second)
   * It is in 2/4 time
   */
  public void playJingleBellsV1V2()
  {
    // play measure 1 to 3
    playJingleBellsM1To3();

    // measure 4
    playNote(53,1000); // f half note

    // measure 5
    playJingleBellsM5();

    // measure 6
    playNote(55,1000); // g half note

    // measure 7
    playJingleBellsM7();

    // measure 8
    playNote(60,1000); // c half note

    // measure 9
    playJingleBellsM9();

    // measure 10
    playNote(52,1000); // e half note

    // measure 11
    playJingleBellsM11();

    // measure 12
    playNote(53,1000); // f half note

    // measures 13 - 16
    playJingleBellsM13To16();
  }

  /**
   * Method to play the second verse of jingle bells
   * with each measure taking 1000 milliseconds (1 second)
   * It is in 2/4 time
   */
  private void playJingleBellsV2()
  {

    // measure 1
    rest(750);
    playNote(52,250); // e eighth note

    // measure 2
    playNote(52,250); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 3
    playNote(52,500); // e quarter note
    rest(250);        // rest
    playNote(52,125); // e sixteenth note
    playNote(52,125); // e sixteenth note

    // measure 4
    playNote(52,500); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 5
    playNote(53,750); // f dotted quarter note
    playNote(53,250); // f eighth note

    // measure 6
    playNote(53,250); // f eighth note
    playNote(61,250); // d flat eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note

    // measure 7
    playNote(55,750); // g dotted quarter note
    playNote(55,250); // g eighth note

    // measure 8
    playNote(55,250); // g eighth note
    playNote(65,250); // f eighth note
    playNote(63,250); // e flat eighth note
    playNote(61,250); // d flat eighth note

    // measure 9
    playNote(60,750); // c dotted quarter note
    playNote(52,250); // e eighth note

    // measure 10
    playNote(52,250); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 11
    playNote(52,750); // e dotted quarter note
    playNote(52,250); // e eighth note

    // measure 12
    playNote(52,250); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 13
    playNote(53,750); // f dotted quarter note
    playNote(53,250); // f eighth note

    // measure 14
    playNote(53,250); // f eighth note
    playNote(61,250); // d flat eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note

    // measure 15
    playNote(55,250); // g eighth note
    playNote(63,250); // e flat eighth note
    playNote(62,250); // d eighth note
    playNote(63,250); // e flat eighth note

    // measure 16
    playNote(65,250); // f eighth note
    playNote(63,250); // e flat eighth note
    playNote(61,250); // d flat eighth note
    playNote(58,250); // b flat eighth note

    // measure 17
    playNote(56,1000); // a flat half note

  }

  /**
   * Method to play refrain of Jingle Bells
   */
  private void playJingleBellsRefrain()
  {
    // measure 1
    playNote(60,250); // c eighth note
    playNote(60,250); // c eighth note
    playNote(60,500); // c quarter note

    // measure 2
    playNote(63,250); // e flat eighth note
    playNote(63,250); // e flat eighth note
    playNote(63,500); // e flat quarter note

    // measure 3
    playNote(60,250); // c eighth note
    playNote(60,250); // c eighth note
    playNote(65,375); // f dotted eighth note
    playNote(65,125); // f sixteenth note

    // measure 4
    playNote(64,1000); // e half note

    // measure 5
    playNote(65,250); // f eighth note
    playNote(61,250); // d flat eighth note
    playNote(56,250); // a flat eighth note
    playNote(64,250); // f eighth note

    // measure 6
    playNote(63,250); // e flat eighth note
    playNote(60,250); // c eighth note
    playNote(56,250); // a flat eighth note
    playNote(56,125); // a flat sixteenth note
    playNote(58,125); // b flat sixteenth note

    // measure 7
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note
    playNote(58,250); // b flat eighth note

    // measure 8
    playNote(60,1000); // c half note

    // measure 9
    playNote(60,250); // c eighth note
    playNote(60,250); // c eighth note
    playNote(60,500); // c quarter note

    // measure 10
    playNote(63,250); // e flat eighth note
    playNote(63,250); // e flat eighth note
    playNote(63,500); // e flat quarter note

    // measure 11
    playNote(60,250); // c eighth note
    playNote(60,250); // c eighth note
    playNote(65,250); // f eighth note
    playNote(65,250); // f eighth note

    // measure 12
    playNote(64,1000); // e half note

    // measure 13
    playNote(53,250); // f eighth note
    playNote(61,250); // d flat eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note

    // measure 14
    playNote(56,250); // a flat eighth note
    playNote(63,250); // e flat eighth note
    playNote(62,250); // d eighth note
    playNote(63,125); // e flat sixteenth note
    playNote(63,125); // e flat sixteenth note

    // measure 16
    playNote(65,250); // f eighth note
    playNote(63,250); // e flat eighth note
    playNote(61,250); // d flat eighth note
    playNote(58,250); // b flat eighth note

    // measure 17
    playNote(56,500); // a flat quarter note
    rest(500); // rest
  }

  /**
   * Method to play Jingle Bells
   */
  public void playJingleBells()
  {
    // play verse 1
    playJingleBellsV1();

    // play refrain
    playJingleBellsRefrain();

    // play verse 2
    playJingleBellsV2();

    // play refrain
    playJingleBellsRefrain();
  }


  /**
   * Method to play the first 4 measures of jingle bells
   * with each measure taking 1000 milliseconds (1 second)
   */
  public void playJingleBells4()
  {
    // measure 1
    playNote(52,250); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 2
    playNote(52,500); // e quarter note
    rest(250);        // rest
    playNote(52,125); // e sixteenth note
    playNote(52,125); // e sixteenth note

    // measure 3
    playNote(52,500); // e eighth note
    playNote(60,250); // c eighth note
    playNote(58,250); // b flat eighth note
    playNote(56,250); // a flat eighth note

    // measure 4
    playNote(53,1000); // f half note
  }

} // end of class (do not remove and put all method before this)
