
/**
 * Class that represents a sample of a sound.  It knows what sound object
 * it comes from and knows what frame number this sample is in the sound
 * object.
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 */
public class SoundSample {
    /** the sound that this element belongs to */
    private SimpleSound sound = null;

    /** the frame number of this sample in the buffer */
    private int frameNumber = 0;


    ///////////////////// configuration (wraparound) //////////////////////////////////
    private static boolean wrapLevels = false;

    /**
     * Indicates whether levels outside the range (-32768, 32767) are clamped
     * or wrapped around (saturating or modular arithmetic).
     *
     * @return False to clamp levels, true to modulo them.
     */
    public static boolean getWrapLevels () {
        return wrapLevels;
    }

    /**
     * Changes Sample's behavior for dealing with levels outside the range
     * (-32768, 32767).
     *
     * @param wrap If true, values will be wrapped (modular arithmetic).
     * If false, values will be clamped (saturating arithmetic).
     */
    public static void setWrapLevels (boolean wrap) {
        wrapLevels = wrap;
    }
    
    /**
     * Round and correct a color level to be within (-32768, 32767),
     * according to the current wrapLevels setting.
     *
     * @param level The user-provided level.
     * @return A value within (-32768, 32767).
     */
    public static int correctLevel (double level) {
        return correctLevel((int) Math.round(level));
    }

    /**
     * Correct a sample level to be within (-32768, 32767),
     * according to the current wrapLevels setting.
     *
     * @param level The user-provided level.
     * @return A value within (-32768, 32767).
     */
    public static int correctLevel (int level) {
        if (wrapLevels) {
            if (level < 0) {
                return -1*((-1*level) % 32768);
            } 
            else if (level > 0) {
                return level % 32767;
            }
        } 
        else if (level < -32768) {
            return 0;
        } 
        else if (level > 32767) {
            return 32767;
        } 
        return level;
    }

    ///////////////////// Constructors //////////////////////////////////

    /**
     * Constructor that takes a sound and valueArray
     * @param sound the sound object this sample comes from
     * @param frameNumber the frameNumber of this sample in the sound
     */
    public SoundSample(SimpleSound sound, int frameNumber) {
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
    public void setValue(int value) {
        try {
            sound.setSampleValue(frameNumber, value);
        } catch (SoundException ex) {
        }
    }

    /**
     * Method to return a string with the information about
     * this object
     * @return a string with information about this object
     */
    public String toString() {
        return "Sample at index " + frameNumber + " has value " + getValue();
    }
} // end of SoundSample class