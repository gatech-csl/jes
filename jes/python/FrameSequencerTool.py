# A tool for interfacing with FrameSequencer for JES
#
# Timmy Douglas 2006


import java.awt.Font
import java.awt as awt
import javax.swing as swing
import java.util
import FrameSequencer
import Picture
import SimpleInput
import SimpleOutput
import os
import sys
import fnmatch
import media

COMMAND_CLEAR_IMG = "Clear image list"
COMMAND_ADD_IMG = "Add image to list"
COMMAND_ADD_DIR = "Add images in directory to list"
COMMAND_DELETE_IMG = "Delete selected image from list"
COMMAND_PLAY_MOVIE = "Play movie"
COMMAND_MOVE_UP = "Move image up"
COMMAND_MOVE_DOWN = "Move image down"
COMMAND_CHANGE_FPS = "Change Frames Per Second"
SPLITTER_SIZE = 10
VSPLITTER_LOCATION = 300


class FrameSequencerTool(swing.JFrame):

    FocusOwner = None

    def __init__(self, movie):
        try:       
            self.FocusOwner = None
            self.size = (600, 400)
            self.movie = movie
            self.fps = 30

            ## The buttons on the right side

            self.clearButton    = swing.JButton(COMMAND_CLEAR_IMG, actionPerformed=self.actionPerformed)
            self.addButton    = swing.JButton(COMMAND_ADD_IMG, actionPerformed=self.actionPerformed)
            self.addDirectoryButton    = swing.JButton(COMMAND_ADD_DIR, actionPerformed=self.actionPerformed)
            self.deleteButton    = swing.JButton(COMMAND_DELETE_IMG, actionPerformed=self.actionPerformed)
            self.playButton    = swing.JButton(COMMAND_PLAY_MOVIE, actionPerformed=self.actionPerformed)
            self.moveUpButton    = swing.JButton(COMMAND_MOVE_UP, actionPerformed=self.actionPerformed)
            self.moveDownButton    = swing.JButton(COMMAND_MOVE_DOWN, actionPerformed=self.actionPerformed)
            self.changeFPSButton    = swing.JButton(COMMAND_CHANGE_FPS, actionPerformed=self.actionPerformed)

            self.buttonpane = swing.JPanel()
            self.buttonpane.setLayout(swing.BoxLayout(self.buttonpane, swing.BoxLayout.Y_AXIS))

            self.buttonpane.add(self.clearButton)
            self.buttonpane.add(self.deleteButton)
            self.buttonpane.add(self.addDirectoryButton)
            self.buttonpane.add(self.addButton)
            self.buttonpane.add(self.playButton)
            self.buttonpane.add(self.moveUpButton)
            self.buttonpane.add(self.moveDownButton)
            self.buttonpane.add(self.changeFPSButton)


            ## The images on the left side

            self.listModel = swing.DefaultListModel()
            self.list = swing.JList(self.listModel)


            self.listpane = swing.JScrollPane(self.list)
            #self.listpane.setLayout(swing.BoxLayout(self.listpane, swing.BoxLayout.X_AXIS))
            #self.listpane.add(self.list)

            ## The splitter pane

            splitterPane = swing.JSplitPane()
            splitterPane.orientation = swing.JSplitPane.HORIZONTAL_SPLIT
            splitterPane.leftComponent = self.listpane
            splitterPane.rightComponent = self.buttonpane
            splitterPane.setDividerSize(SPLITTER_SIZE)
            splitterPane.setDividerLocation(VSPLITTER_LOCATION)
            splitterPane.setResizeWeight(1.0)

            self.add(splitterPane)
            self.addFramesIntoListModel(self.movie)
            self.show()

        except:
            import traceback
            import sys
            a,b,c = sys.exc_info()
            print "FrameSequencerTool exception:"
            traceback.print_exception(a,b,c)



    def addFramesIntoListModel(self, movie):
        for file in movie:
            self.listModel.addElement(file)

    def updateMovie(self):
        #update the movie object from the listbox
        self.movie.frames = []
        for item in self.listModel.toArray():
            self.movie.addFrame(item)



    def addImagesFromDirectoryIntoListModel(self, directory):
        patterns = ["*.gif", "*.jpg", "*.png"]
        for f in os.listdir(directory):
            file = directory+os.sep+f
            if os.path.isfile(file):
                for pattern in patterns:
                    if fnmatch.fnmatch(file, pattern):
                        self.listModel.addElement(file)

 
    ################################################################################
    # Function name: actionPerformed
    # Parameters:
    #     -event: event object that represents action that occured
    # Description:
    #     This function is called when a menu option is selected or a button is
    #     pressed.  It calls the correct function in order to perform the action
    #     that the user wants.
    ################################################################################
    def actionPerformed(self, event):
        actionCommand = event.getActionCommand()
        selection = self.list.getSelectedIndex()

        if actionCommand == COMMAND_PLAY_MOVIE:
            self.movie.play()

        elif actionCommand == COMMAND_ADD_IMG:
            self.listModel.addElement(media.pickAFile())
            self.updateMovie()

        elif actionCommand == COMMAND_ADD_DIR:
            self.addImagesFromDirectoryIntoListModel(media.pickAFolder())
            self.updateMovie()

        elif actionCommand == COMMAND_DELETE_IMG:
            if selection >= 0:
                self.listModel.remove(selection)
                self.updateMovie()

        elif actionCommand == COMMAND_CLEAR_IMG:
            self.listModel.clear()
            self.updateMovie()

        elif actionCommand == COMMAND_MOVE_UP:
            if selection > 0:
                itemAbove = self.listModel.get(selection-1)
                itemBelow = self.listModel.get(selection)
                self.listModel.set(selection-1, itemBelow)
                self.listModel.set(selection, itemAbove)
                self.list.setSelectedIndex(selection-1)
                self.updateMovie()

        elif actionCommand == COMMAND_MOVE_DOWN:
            if selection >= 0 and selection < self.listModel.size()-1:
                itemAbove = self.listModel.get(selection)
                itemBelow = self.listModel.get(selection+1)
                self.listModel.set(selection, itemBelow)
                self.listModel.set(selection+1, itemAbove)
                self.list.setSelectedIndex(selection+1)
                self.updateMovie()

        elif actionCommand == COMMAND_CHANGE_FPS:
            self.fps = SimpleInput.getIntNumber("Enter the number of frames per second")

        else:
            pass


