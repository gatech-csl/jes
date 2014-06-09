import javax.swing.JFileChooser;
import javax.swing.SwingUtilities;
import javax.swing.JFrame;

import java.io.*;
import java.net.*;

/**
 * A class to make working with a file chooser easier
 * for students.  It uses a JFileChooser to let the user
 * pick a file and returns the chosen file name.
 * <br>
 * Copyright Georgia Institute of Technology 2004
 * @author Barb Ericson ericson@cc.gatech.edu
 *
 * rewritten 05/08/09 by Dorn to make it thread safe and
 * to clean up code by refactoring
 */
public class FileChooser
{

  ///////////////////////////// class fields ///////////////////

  private static String latestPath = null;

  /////////////////////// methods /////////////////////////////

  /**
   * Method to pick an item using the file chooser.
   * NOTE: This method is written to be threadsafe in the event
   * it is called from a thread other than the GUI event-dispatch thread.
   * @param fileChooser the file Chooser to use
   * @return the path name
   */
  private static String pickPath(final int selectionMode, final String caption)
  {
	//Create a place to store the return value from the JFileChooser in the other thread
	final String[] path = new String[1];

	Runnable pickAFileRunner =
		new Runnable() {
			public void run() {
				JFileChooser fileChooser = new JFileChooser();
				fileChooser.setDialogTitle(caption);
				fileChooser.setFileSelectionMode(selectionMode);

				/* create a JFrame to be the parent of the file
			         * chooser open dialog if you don't do this then
				 * you may not see the dialog.
    				 */
				JFrame frame = new JFrame();
				frame.setAlwaysOnTop(true);
				frame.getContentPane().add(fileChooser);

				String startPath;

				// Decide which path to start from, either latest path or the media dir
				if ( latestPath != null )
					startPath = latestPath;
				else
					startPath = getMediaDirectory();

				// Check to make sure path exists, if it doesn't, use home directory
				File testFile = new File(startPath);
				if (testFile.exists())
					fileChooser.setCurrentDirectory( testFile );
				else
					fileChooser.setCurrentDirectory( new File(System.getProperty("user.home")) );

				// get the return value from choosing a file
				int dialogReturn = fileChooser.showOpenDialog(frame);

				// if the return value says the user picked a file, save path and update latest path
				if (dialogReturn == JFileChooser.APPROVE_OPTION)
				{
					path[0] = fileChooser.getSelectedFile().getPath();
					latestPath = path[0];
				}
				else
				{
					path[0] = null;
				}
			}
		};

	try
	{
		// Run the code now to get the dialog on the GUI thread and then wait for a response
		if (SwingUtilities.isEventDispatchThread())
		{
			pickAFileRunner.run();
		}
		else
		{
			SwingUtilities.invokeAndWait(pickAFileRunner);
		}
		return path[0];
	}
	catch(Exception e)
	{
		return null;
	}
  }

  /**
   * Method to let the user pick a file and return
   * the full file name as a string.  If the user didn't
   * pick a file then the file name will be null.
   * @return the full file name of the picked file or null
   */
  public static String pickAFile()
  {
  	return pickPath(JFileChooser.FILES_ONLY, "Pick A File");
  }

  /**
   * Method to let the user pick a directory and return
   * the full path name as a string.
   * @return the full directory path
   */
  public static String pickADirectory()
  {
  	return pickPath(JFileChooser.DIRECTORIES_ONLY, "Pick A Folder");
  }

 /**
  * Method to get the full path for the passed file name
  * @param fileName the name of a file
  * @return the full path for the file
  */
 public static String getMediaPath(String fileName)
 {
	return getMediaDirectory() + fileName;
 }

 /**
  * Method to get the directory for the media
  * @return the media directory
  */
 private static String getMediaDirectory()
 {
	return JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MEDIAPATH);
 }


 /**
  * Method to set the media path by setting the directory to use
  * @param directory the directory to use for the media path
  */
 public static void setMediaPath(String directory)
 {
   // check if the directory exists
   File file = null;

   if ( directory != null )
     file = new File( directory );

   if ( ( file == null ) || ( !file.exists() ) )
   {
     System.out.println("Sorry but " + directory + " doesn't exist, try a different directory.");
   }
   else
   {
	if ( !directory.endsWith( File.separator ) )
		directory += File.separator;
     	JESConfig.getInstance().setStringProperty(JESConfig.CONFIG_MEDIAPATH, directory);
   }
 }

 /**
  * Method to pick a media path using
  * the file chooser and set it
  */
 public static void pickMediaPath()
 {
 	setMediaPath( pickPath(JFileChooser.DIRECTORIES_ONLY, "Choose Media Path") );
 }

}
