import java.io.*;
import java.util.*;
import java.net.*;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;

import ch.randelshofer.media.avi.AVIOutputStream;

/**
 * Class to write out an AVI or Quicktime movie from
 * a series of JPEG (jpg) frames in a directory
 * @author Barb Ericson ericson@cc.gatech.edu
 *
 * Depreciated File.toURL() replaced with File.toURI().toURL()
 * by Buck Scharfnorth 22 May 2008
 *
 * Modified writeQuicktime() and writeAVI() to check
 * for appropriate endings (".mov" and ".avi") before
 * appending them to the destination path. Also modified
 * getOutputURL to check for "%20" in destination path.
 * by Brian O'Neill 11 Aug 2008
 *
 */
public class MovieWriter {
    ///////////////// fields ///////////////////////////

    /** the directory to read the frames from */
    private String framesDir = null;
    /** the number of frames per second */
    private int frameRate = 16;
    /** the name of the movie file */
    private String movieName = null;
    /** the output url for the movie */
    private String outputURL = null;

    ////////////////// constructors //////////////////////

    /**
     * Constructor that takes no arguments
     */
    public MovieWriter() {
        framesDir = FileChooser.pickADirectory();
        movieName = getMovieName();
        outputURL = getOutputURL();
    }

    /**
     * Constructor that takes the directory that
     * has the frames
     * @param dirPath the full path for the directory
     * that has the movie frames
     */
    public MovieWriter(String dirPath) {
        framesDir = dirPath;
        if (!framesDir.endsWith(File.separator) && !framesDir.endsWith("/")) { //Makes sure framesDir ends with the file separator
            framesDir += File.separator;
        }
        movieName = getMovieName();
        outputURL = getOutputURL();
    }

    /**
     * Constructor that takes the frame rate
     * @param theFrameRate the number of frames per second
     */
    public MovieWriter(int theFrameRate) {
        framesDir = FileChooser.pickADirectory();
        frameRate = theFrameRate;
        movieName = getMovieName();
        outputURL = getOutputURL();
    }

    /**
     * Constructor that takes the frame rate and the
     * directory that the frames are stored in
     * @param theFrameRate the number of frames per second
     * @param theFramesDir the directory where the frames are
     */
    public MovieWriter(int theFrameRate,
                       String theFramesDir) {
        this.framesDir = theFramesDir;
        if (!framesDir.endsWith(File.separator) && !framesDir.endsWith("/")) { //Makes sure framesDir ends with the file separator
            framesDir += File.separator;
        }
        this.frameRate = theFrameRate;
        movieName = getMovieName();
        outputURL = getOutputURL();
    }

    /**
     * Constructor that takes the directory with the frames
     * the frame rate, and the output url (dir,name,
     * and extendsion)
     * @param theFramesDir the directory that holds the frame
     * @param theFrameRate the number of frames per second
     * @param theOutputURL the complete path name for the output
     * movie
     */
    public MovieWriter(String theFramesDir,
                       int theFrameRate,
                       String theOutputURL) {
        this.framesDir = theFramesDir;
        if (!framesDir.endsWith(File.separator) && !framesDir.endsWith("/")) { //Makes sure framesDir ends with the file separator
            framesDir += File.separator;
        }
        this.frameRate = theFrameRate;
        this.outputURL = theOutputURL;
    }


    /////////////////// methods //////////////////////////

    /**
     * Method to get the movie name from the directory
     * where the frames are stored
     * @return the name of the movie (like movie1)
     */
    private String getMovieName() {
        File dir = new File(framesDir);
        return dir.getName();
    }

    /**
     * Method to create the output URL from the directory
     * the frames are stored in.
     * @return the URL for the output movie file
     */
    private String getOutputURL() {
        File dir = null;
        URL myURL = null;
        if (framesDir != null) {
            try {
                dir = new File(framesDir + movieName);
                myURL = dir.toURI().toURL();
            } catch (Exception ex) {
            }
        }
        //return myURL.toString();
        return myURL.toString().replace("%20", " ");
    }

    /**
     * Method to get the list of jpeg frames
     * @return a list of full path names for the frames
     * of the movie
     */
    public List<String> getFrameNames() {
        File dir = new File(framesDir);
        String[] filesArray = dir.list();
        List<String> files = new ArrayList<String>();
        long lenFirst = 0;
        for (String fileName : filesArray) {
            // only continue if jpg picture
            if (fileName.indexOf(".jpg") >= 0) {
                File f = new File(framesDir + fileName);
                // check for imcomplete image
                if (lenFirst == 0 ||
                        f.length() > (lenFirst / 2)) {
                    // image okay so far
                    try {
                        BufferedImage i = ImageIO.read(f);
                        files.add(framesDir + fileName);
                    } catch (Exception ex) {
                        // if problem reading don't add it
                    }
                }
                if (lenFirst == 0) {
                    lenFirst = f.length();
                }
            }
        }
        return files;
    }

    /**
     * Method to write the movie frames in AVI format
     */
    public void writeAVI() {
        /*  JMF Code no longer functioned for writing AVIs.
         *  Commented out and code below was written to use a
         *  different AVI writing library.
         *  BJD: 11-9-09
         *
            JpegImagesToMovie imageToMovie = new JpegImagesToMovie();
            List<String> frameNames = getFrameNames();
            Picture p = new Picture((String) frameNames.get(0));
            if(!outputURL.endsWith(".avi"))
            outputURL = outputURL + ".avi";
            imageToMovie.doItAVI(p.getWidth(),p.getHeight(),
                                 frameRate,frameNames,outputURL);
        */

        // The code below utilizes Werner Randelshofer's AVIOutputStream
        // object to write an AVI movie from the list of frames.  His code
        // is shared under the Creative Commons Attribution License
        // (see http://creativecommons.org/licenses/by/3.0/).  More
        // information about that code can be found in the AVIDemo.jar
        // archive in the jars folder or at http://www.randelshofer.ch

        List<String> frameNames = getFrameNames();
        if (!outputURL.endsWith(".avi")) {
            outputURL = outputURL + ".avi";
        }
        Picture p = new Picture((String) frameNames.get(0));

        try {
            //Convert the URL into a filename
            String filename = (new URL(outputURL)).getFile();

            //Setup the output stream
            AVIOutputStream AVIout = new AVIOutputStream(new File(filename), AVIOutputStream.VideoFormat.JPG);
            AVIout.setVideoCompressionQuality(1);
            AVIout.setFrameRate(frameRate);
            AVIout.setVideoDimension(p.getWidth(), p.getHeight());

            //Write each frame
            for (int i = 0; i < frameNames.size(); i++) {
                AVIout.writeFrame(new File(frameNames.get(i)));
            }

            //Close the output stream so the AVI has proper format
            AVIout.close();
        } catch (Exception e) {    }

    }

    /**
     * Method to write the movie frames as quicktime
     */
    public void writeQuicktime() {
        JpegImagesToMovie imageToMovie = new JpegImagesToMovie();
        List<String> frameNames = getFrameNames();
        Picture p = new Picture((String) frameNames.get(0));
        if (!outputURL.endsWith(".mov")) {
            outputURL = outputURL + ".mov";
        }
        imageToMovie.doItQuicktime(p.getWidth(), p.getHeight(),
                                   frameRate, frameNames, outputURL);
    }

    public static void main(String[] args) {
        MovieWriter writer =
            new MovieWriter("c:/Temp/testmovie/");
        writer.writeQuicktime();
        writer.writeAVI();
    }
}
