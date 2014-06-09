
/**
 * Class that represents a sound.  This class is used by the students
 * to extend the capabilities of SimpleSound.
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barbara Ericson ericson@cc.gatech.edu
 *
 * Modified 17 July 2007 Pam Cutter Kalamazoo College
 * 	  Added a copySoundInto method which allows copying as much of
 * 	   this sound as will fit into a destination sound
 *    Added a cropSound method which returns a new sound which is a
 *     specified portion of this sound
 *
 * Kalamazoo and other additional methods merged by Buck Scharfnorth 22 May 2008
 */
public class Sound extends SimpleSound
{

  /////////////// consructors ////////////////////////////////////

  /**
   * Constructor that takes a file name
   * @param fileName the name of the file to read the sound from
   */
  public Sound(String fileName) throws SoundException
  {
    // let the parent class handle setting the file name
    super(fileName);
  }

  /**
   * Constructor that takes the number of samples in
   * the sound
   * @param numSamples the number of samples desired
   */
  public Sound (int numSamples)
  {
    // let the parent class handle this
    super(numSamples);
  }

  /**
   * Constructor that takes the number of samples that this
   * sound will have and the sample rate
   * @param numSamples the number of samples desired
   * @param sampleRate the number of samples per second
   */
  public Sound (int numSamples, int sampleRate)
  {
    // let the parent class handle this
    super(numSamples,sampleRate);
  }

  /**
   * Constructor that takes a sound to copy
   * @param copySound the Sound to copy
   */
  public Sound (Sound copySound)
  {
    // let the parent class handle this
    super(copySound);
  }

  ////////////////// methods ////////////////////////////////////

  /**
   * Method to return the string representation of this sound
   * @return a string with information about this sound
   */
  public String toString()
  {
    String output = "Sound";
    String fileName = getFileName();

    // if there is a file name then add that to the output
    if (fileName != null)
      output = output + " file: " + fileName;

    // add the length in frames
    output = output + " number of samples: " + getLengthInFrames();

    return output;
  }

  /**
   * Method to copy as much of this sound as will fit into
   * another sound.
   * @param dest the sound which gets copied into
   * @param startIndex the starting index for copying
   */
  public void copySoundInto(Sound dest, int startIndex)throws SoundException
  {
  	int numSamplesToCopy = Math.min(this.getLength(), dest.getLength()-startIndex);

  	for (int i=0; i<numSamplesToCopy; i++)
  	{
  		int value = this.getSampleValueAt(i);
  		dest.setSampleValueAt(i+startIndex,value);

  	}
  }

  /**
   * Mehtod to crop out a portion of this sound and return it
   * as a new sound
   * @param startIndex the index at which to start cropping
   * @param numSamples the number of samples to crop out
   * @return the new sound derived from this sound by cropping
   * @throws SoundException
   */
  public Sound cropSound(int startIndex, int numSamples) throws SoundException
  {
  	int numSamplesToCopy;
  	if (startIndex+numSamples < this.getLength())
		numSamplesToCopy = startIndex+numSamples;
  	else
  		numSamplesToCopy = this.getLength()-startIndex;
  	Sound newSound = new Sound(numSamplesToCopy);

  	for (int i=0; i<numSamplesToCopy; i++)
  	{
  		int value = this.getSampleValueAt(i+startIndex);
  		newSound.setSampleValueAt(i,value);
  	}
  	return newSound;
  }
} // end of class Sound, put all new methods before this
