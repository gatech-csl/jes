import java.util.Vector;

/**
 * Class that represents a list of samples
 * <br>
 * Copyright Georgia Institute of Technology 2006
 * @author Timmy Douglas timmy@cc
 */
public class Samples
{

  /**
   * the sound we point to
   */
    private Sound sound = null;

  /**
   * A collection of the threads that are playing this sound.
   */
    private Sample[] samples;

  /**
   * Constructor that takes a sound
   * @param aSound the sound
   */
    public Samples(Sound aSound)
    {
        this.sound = aSound;
        this.samples = new Sample[aSound.getLength()];
        for (int i=0; i < aSound.getLength(); i++) {
            samples[i] = new Sample(aSound, i);
        }
    }

  /**
   * Method to get the array of samples from a sound
   * @param aSound the sound
   * @return the array of samples
   */
    static public Sample[] getSamples(Sound aSound)
    {
        Sample[] samples = new Sample[aSound.getLength()];
        for (int i=0; i < aSound.getLength(); i++) {
            samples[i] = new Sample(aSound, i);
        }
        return samples;
    }

  /**
   * Obtains a string representation of this array of Samples.
   * @return a String representation of this array of Samples.
   */
    public String toString()
    {
        return ("Samples, length " + this.sound.getLength());
    }

  /**
   * Method to get a specific Sample
   * @param index the index to get the sample from
   * @return the sample
   */
    public Sample getSample(int index)
    {
        return this.samples[index];
    }

  /**
   * Method to set the value of a specific Sample
   * @param index the index to get the sample
   * @param value the value to set it to
   */
    public void setSample(int index, int value) throws SoundException
    {
        this.samples[index].setValue(value);
    }

  /**
   * Method to set the value of a specific Sample
   * @param index the index to get the sample
   * @param value the value to set it to
   */
    public void setSample(int index, double value) throws SoundException
    {
        this.setSample(index, Math.round(value));
    }

  /**
   * Method to get these Samples' sound object
   * @return a sound object
   */
  public Sound getSound()
  {
      return this.sound;
  }

}
