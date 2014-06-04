/**
 * Class to use to report a sound exception
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Unknown Undergraduate
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class SoundException extends Exception
{

  private static final long serialVersionUID = 7526471155622776147L;

 /** Constructor that takes String as the message for the SoundException */
  public SoundException(String message)
  {
    super(message);
  }
} // end of SoundException class
