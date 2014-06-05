/**
 * Class that represents a slide show. A SlideShow has an array of pictures
 * and a delay time between pictures and a title. The SlideShow can be viewed
 * with the show() method
 */
public class SlideShow
{
  /////////// fields ///////////////
  public Picture[] pictureArray;
  private int waitTime;
  private String title;

  ///////////// constructors //////////

  /** Constructor that takes no arguments */
  public SlideShow() {}

 /**
  * Constructor that takes an array of Pictures
  * @param pictArray the Picture array to use
  */
  public SlideShow(Picture[] pictArray)
  {
    this.pictureArray = pictArray;
  }

 /**
  * Constructor that takes an array of Pictures and a delay time between transitions
  * @param pictArray the Picture array to use
  * @param time the delay time between Pictures
  */
  public SlideShow(Picture[] pictArray,
                   int time)
  {
    this.pictureArray = pictArray;
    this.waitTime = time;
  }

  //////////// methods ///////////////

 /**
  * Method to get the title of the SlideShow
  * @return the title of the SlideShow
  */
  public String getTitle() { return this.title;}

 /**
  * Method to set the title for the SlideShow
  * @param theTitle the title to use for the SlideShow
  */
  public void setTitle(String theTitle)
  {
    this.title = theTitle;
  }

 /**
  * Method to get the delay time between transitions
  * @return the delay time between transitions
  */
  public int getWaitTime()
  {
    return this.waitTime;
  }

 /**
  * Method to get the Picture of the passed index
  * @param index the index of the Picture to return
  * @return the Picture of the passed index
  */
  public Picture getPicture(int index)
  {
    if (this.pictureArray == null)
      return null;
    if (index < 0 ||
        index >= this.pictureArray.length)
      return null;
    return this.pictureArray[index];
  }

 /**
  * Method to return a string with information about this SlideShow
  * @return a string with information about this SlideShow
  */
  public String toString()
  {
    String result = "A slide show with ";
    if (this.pictureArray != null)
      result = result + this.pictureArray.length +
       " pictures and ";
    else
      result = result + "no pictures and ";
    result = result +
      "a wait time of " + this.waitTime;
    return result;
  }

 /**
  * Method to show the title sceen for the SlideShow
  */
  private void showTitle() throws Exception
  {
    Picture titlePict = new Picture(640,480);
    titlePict.addMessage(this.title, 100,100);
    titlePict.show();
    Thread.sleep(this.waitTime);
    titlePict.hide();
  }

 /**
  * Method to show the SlideShow
  */
  public void show() throws Exception
  {
    if (pictureArray != null)
    {
      // show the title as a slide
      Picture titlePict = new Picture(640,480);
      titlePict.addMessage(this.title,100,100);
      titlePict.show();
      Thread.sleep(this.waitTime);
      titlePict.hide();

      for (Picture currPict : pictureArray)
      {
        if (currPict != null)
        {
          currPict.show();
          Thread.sleep(waitTime);
          currPict.hide();
        }
      }
    }
  }

  public static void main(String[] args) throws Exception
  {
    Picture[] pictArray = new Picture[5];
    pictArray[0] = new Picture(FileChooser.getMediaPath("beach.jpg"));
    pictArray[1] = new Picture(FileChooser.getMediaPath("blueShrub.jpg"));
    pictArray[2] = new Picture(FileChooser.getMediaPath("church.jpg"));
    pictArray[3] = new Picture(FileChooser.getMediaPath("redDoor.jpg"));
    pictArray[4] = new Picture(FileChooser.getMediaPath("butterfly.jpg"));
    SlideShow show1 = new SlideShow(pictArray,1000);
    show1.setTitle("Vacation Slides");
    show1.show();
  }
}