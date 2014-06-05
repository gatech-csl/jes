
/**
 * Class that represents a sample
 * <br>
 * Copyright Georgia Institute of Technology 2006
 * @author Timmy Douglas timmy@cc
 */
public class Sample
{

  /**
   * the sound we point to
   */
    private Sound sound = null;

  /**
   * the sample index
   */
    private int index;



  /**
   * Constructor that takes a sound and an index
   * @param aSound the sound
   * @param index the index
   */
    public Sample(Sound aSound, int index) {
        this.index = index;
        this.sound = aSound;
    }

  /**
   * Obtains a string representation of this Sample
   * @return a String representation of this Sample
   */
  public String toString()
  {
      try {
          return ("Sample at " + (this.index + SimpleSound._SoundIndexOffset) + " with value " + this.getValue());
      } catch (Exception e) {
          return ("Sample at " + (this.index + SimpleSound._SoundIndexOffset) + " value unknown");

      }
  }

  /**
   * Method to get this sample's sound object
   * @return a sound object
   */
  public Sound getSound()
  {
      return this.sound;
  }


  /**
   * Method to get the sample value
   * @return a sample value
   */
  public int getValue() throws SoundException
  {
      return this.sound.getSampleValueAt(this.index);
  }


  /**
   * Method to set the sample value
   * @param newValue the new value to store
   */
  public void setValue(int newValue) throws SoundException
  {
      // System.out.println("setValue!!");
      this.sound.setSampleValueAt(this.index, newValue);
  }


  /**
   * Method to set the sample value
   * @param newValue the new value to store
   */
  public void setValue(double newValue) throws SoundException
  {
      this.setValue((int)newValue);
  }

}
