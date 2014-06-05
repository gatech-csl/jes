
/**
 * Class that represents a sample of a sound.  It knows what sound object
 * it comes from and knows what frame number this sample is in the sound
 * object.
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class SoundSample
{
  /** the sound that this element belongs to */
  private SimpleSound sound = null;

  /** the frame number of this sample in the buffer */
  private int frameNumber = 0;

  ///////////////////// Constructors //////////////////////////////////

  /**
   * Constructor that takes a sound and valueArray
   * @param sound the sound object this sample comes from
   * @param frameNumber the frameNumber of this sample in the sound
   */
  public SoundSample(SimpleSound sound, int frameNumber)
  {
    this.sound = sound;
    this.frameNumber = frameNumber;
  }

  /////////////////// Methods /////////////////////////////////////////

  /**
   * Method to get the value of this sample as in int
   * and handle the possible sound exception
   * @return the value of this sample as an int
   */
  public int getValue() {
    int value = 0;
    try {
      value = sound.getSampleValue(frameNumber);
    } catch (SoundException ex) {
    }
    return value;
  }

  /**
   * Method to set the value of this sample and
   * handle the sound exception
   * @param value the value to use
   */
  public void setValue(int value)
  {
    try {
      sound.setSampleValue(frameNumber,value);
    } catch (SoundException ex) {
    }
  }

  /**
   * Method to return a string with the information about
   * this object
   * @return a string with information about this object
   */
  public String toString()
  {
    return "Sample at index " + frameNumber + " has value " + getValue();
  }
} // end of SoundSample class