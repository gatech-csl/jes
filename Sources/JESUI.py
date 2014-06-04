#JES- Jython Environment for Students
#Copyright (C) 2002  Jason Ergle, Claire Bailey, David Raines, Joshua Sklare
#See JESCopyright.txt for full licensing information
# 5/16/03: Added coloring to the load button to indicate concurrency with the
#          editor document -AdamW
# 5/29/08: Added hideRight class to give the htmlBrowser and watcher
#          panels close buttons, and set their OneTouchExpandable to 1.
#          Prompt for saving changes on exit, and cancel option for
#          users at promptSave. Support for "redo" - Buck Scharfnorth
#          (hideRight for help fixed as of 7/04/08)
# 5/13/09: Changes for redesigning configuration writing from python to java -Buck

import JESConfig
import JESHomeworkTurninThread
import JESCommandWindow
import JESConstants
import JESDebugWindow
import JESEditor
import JESProgram
import JESHomeworkSubmission
import JESDBVariableWatcher
import Html_Browser
import JESGutter
from JESBugReporter import JESBugReporter
import media

import java.awt as awt
import javax.swing as swing
import java.util as util
import java.awt.Event as Event
import java.awt.event.KeyEvent as KeyEvent
import java.lang as lang
import httplib
import java.net as net
import os
import re
import string
import JESAddressFinder
from java.awt.event import ActionListener
#from pawt import swing
import javax.swing as swing
import java.awt.print as printer
import JESPrintableDocument
import java.lang.System as System
#import org.flexdock.docking
import javax.swing.UIManager as UIManager
import javax.swing.SwingUtilities as SwingUtilities
from java.lang import Thread


MENU_SEPARATOR = '-'
EXPLAIN_PREFIX = 'Explain '
COMMAND_NEW    = 'New Program'
COMMAND_OPEN   = 'Open Program'
COMMAND_SAVE   = 'Save Program'
COMMAND_SAVEAS = 'Save Program As...'
COMMAND_EXIT   = 'Exit'
COMMAND_CUT    = 'Cut'
COMMAND_COPY   = 'Copy'
COMMAND_PASTE  = 'Paste'
COMMAND_UNDO   = 'Undo'
COMMAND_REDO   = 'Redo'
COMMAND_GOTO   = 'Goto Line ...'
COMMAND_OPTIONS = 'Options'
#COMMAND_DIRECTORY = 'Change Default Directory...'
COMMAND_HELP   = 'Help'
COMMAND_ABOUT  = 'About JES'
COMMAND_BUGREPORT = 'Report a problem in JES!'
COMMAND_SEARCH = 'Search'
COMMAND_LOAD   = 'Load Program'
COMMAND_EDITOR = 'Editor'
COMMAND_COMMAND= 'Command'
COMMAND_EXPLORE= 'Explain'
COMMAND_EXPLORE_HELP = 'Explain <click>'
COMMAND_SOUND_TOOL = 'Sound Tool...'
COMMAND_PICTURE_TOOL = 'Picture Tool...'
COMMAND_FRAMESEQUENCER_TOOL = 'Movie Tool...'
TURNIN_OPTIONS = 'Register...'
TURNIN_HW = 'Assignment'
DEBUG_SHOW_DEBUGGER = 'Watcher'
DEBUG_HIDE_DEBUGGER = 'Watcher'
DEBUG_WATCH_VAR = 'add Variable...'
DEBUG_UNWATCH_VAR = 'remove Variable...'
PRINT= 'Print'
AUTOSAVE = 'Auto save code file when loading'
COMMAND_WINDOW_2 = 'Program Area + Interactions Area'
COMMAND_WINDOW_3HELP = 'Program Area + Interactions Area + Help'
COMMAND_WINDOW_3DEBUG = 'Program Area + Interactions Area + Watcher'
EXPLAIN_DEFAULT_STATUS = 'For help on a particular JES function, move the cursor over it'

FILE_TITLE = 'File'
EDIT_TITLE = 'Edit'
HELP_TITLE = 'Help'
TURNIN_TITLE = 'Turnin'
DEBUG_TITLE = 'Watcher'
PREFERENCES_TITLE = 'Preferences'
MEDIA_TOOLS_TITLE = 'MediaTools'
API_TITLE = 'Java API'
JES_API_TITLE = 'JES Functions'
WINDOW_TITLE = 'Window Layout'
SKINS_TITLE = 'Skins'
HELP_FILE_EXTENTION = '.html'


# fixme: there should be a cleaner way to do this for the api menu.
#        maybe we could look into javaimporter that is in jython2.2alpha

import AnimationPanel
# import ArraySorter
import ColorChooser
import DigitalPicture
import FileChooser
import FrameSequencer
import ImageDisplay
import JavaMusic
import MidiPlayer
import ModelDisplay
import MoviePlayer
import PathSegment
import Pen
import PictureExplorer
import PictureFrame
import Picture
import Pixel
import Playback
import SimpleInput
import SimpleOutput
import SimplePicture
import SimpleSound
import SimpleTurtle
import SlideShow
import SoundExplorer
import Sound
import SoundSample
import SoundTest
import Turtle
import World

## make sure all these are imported

API_SECTIONS = [AnimationPanel,
ColorChooser,
DigitalPicture,
FileChooser,
FrameSequencer,
ImageDisplay,
JavaMusic,
MidiPlayer,
ModelDisplay,
MoviePlayer,
PathSegment,
Pen,
PictureExplorer,
PictureFrame,
Picture,
Pixel,
Playback,
SimpleInput,
SimpleOutput,
SimplePicture,
SimpleSound,
SimpleTurtle,
SlideShow,
SoundExplorer,
Sound,
SoundSample,
SoundTest,
Turtle,
World]


JES_API_SECTIONS = [ \
('Colors', ['distance', 'makeColor', 'makeDarker', 'makeLighter', 'pickAColor', 'getColorWrapAround', 'setColorWrapAround']),
('Files', ['pickAFile', 'pickAFolder', 'setMediaPath', 'setMediaFolder',
            'getMediaPath', 'getMediaFolder', 'getShortPath', 'setLibPath']),
('Input/Output', ['requestNumber', 'requestInteger', 'requestIntegerInRange', 'requestString', \
                  'showWarning', 'showInformation', 'showError', 'printNow']),
('Turtles', ['turn', 'turnLeft', 'turnRight', 'forward', 'backward', 'moveTo', 'turnToFace', \
                'makeTurtle', 'penUp', 'penDown', 'makeWorld',
                'getTurtleList', 'drop', 'getHeading', 'getXPos', 'getYPos']),
('Movies', ['playMovie', 'makeMovie', 'makeMovieFromInitialFile', \
            'writeFramesToDirectory', 'addFrameToMovie', 'writeQuicktime', 'writeAVI', \
            'openFrameSequencerTool', 'explore']),
('Pixels', ['getColor', 'setColor', 'getRed', 'getGreen', 'getBlue', \
            'setRed', 'setGreen', 'setBlue', 'getX', 'getY']),
('Pictures', ['addArc', 'addArcFilled', 'addLine', 'addOval', 'addOvalFilled', 'addRect', \
            'addRectFilled', 'addText', 'addTextWithStyle', 'copyInto', 'duplicatePicture', 'getHeight', 'getWidth', \
              'getPixel', 'getPixels', 'getPixelAt', 'makePicture', 'makeEmptyPicture', 'makeStyle', 'show', 'repaint', \
              'writePictureTo', 'openPictureTool', 'setAllPixelsToAColor', 'explore']),
('Sound', ['blockingPlay', 'duplicateSound', 'getDuration', 'getLength', 'getNumSamples', 'getSampleObjectAt', 'getSamples', 'getSampleValue', 'getSampleValueAt', \
           'getSamplingRate', 'getSound', 'makeEmptySound', 'makeEmptySoundBySeconds', 'makeSound', 'play', 'playNote', \
#           'playInRange', 'blockingPlayInRange', 'playAtRateInRange', 'blockingPlayAtRateInRange', \
           'setSampleValue', 'setSampleValueAt', 'stopPlaying', 'writeSoundTo', 'openSoundTool', 'explore'])]

if System.getProperty('os.name').find('Mac') <> -1:  # if we are on a Mac
    CONTROL_KEY = Event.META_MASK
else:
    CONTROL_KEY = Event.CTRL_MASK

#The following is an array that is used to build the main menu bar.  The
#information stored in here is the high level menu item names, the menu bar
#option names, and the accelerator keys for those menu options.
MENU_OPTIONS = [
    [FILE_TITLE,
      [[COMMAND_NEW,    KeyEvent.VK_N,  CONTROL_KEY],
       [COMMAND_OPEN,   KeyEvent.VK_O,  CONTROL_KEY],
       [COMMAND_SAVE,   KeyEvent.VK_S,  CONTROL_KEY],
       [COMMAND_SAVEAS, KeyEvent.VK_S,  CONTROL_KEY + Event.SHIFT_MASK],
       [COMMAND_LOAD,   KeyEvent.VK_L,  CONTROL_KEY],
       [PRINT, KeyEvent.VK_P,  CONTROL_KEY],
       [MENU_SEPARATOR, 0,              0],
       [COMMAND_EXIT,   KeyEvent.VK_Q,  CONTROL_KEY]]],
    [EDIT_TITLE,
      [[COMMAND_EDITOR, KeyEvent.VK_UP, CONTROL_KEY],
       [COMMAND_COMMAND,KeyEvent.VK_DOWN,CONTROL_KEY],
       [MENU_SEPARATOR, 0,              0],
       [COMMAND_UNDO,  KeyEvent.VK_Z,  CONTROL_KEY],
       [COMMAND_REDO,  KeyEvent.VK_Y,  CONTROL_KEY],
       [COMMAND_CUT,    KeyEvent.VK_X,  CONTROL_KEY],
       [COMMAND_COPY,   KeyEvent.VK_C,  CONTROL_KEY],
       [COMMAND_PASTE,  KeyEvent.VK_V,  CONTROL_KEY],
       [MENU_SEPARATOR, 0,              0],
       [COMMAND_GOTO,  KeyEvent.VK_G,  CONTROL_KEY],
       [COMMAND_SEARCH,  KeyEvent.VK_F,  CONTROL_KEY],
       [MENU_SEPARATOR, 0,              0],
       [COMMAND_OPTIONS,   0,  0]]],
    [TURNIN_TITLE,
      [[TURNIN_HW,0,0],
       [TURNIN_OPTIONS,0,0]]],
    [DEBUG_TITLE,
      [[DEBUG_SHOW_DEBUGGER,0,0,1], # this is a checkBoxMenuItem
       #[DEBUG_BREAK,0,0],
       [DEBUG_WATCH_VAR,0,0],
       [DEBUG_UNWATCH_VAR,0,0]]],

    [MEDIA_TOOLS_TITLE,
      [[COMMAND_SOUND_TOOL, 0, 0],
       [COMMAND_PICTURE_TOOL, 0, 0],
       [COMMAND_FRAMESEQUENCER_TOOL, 0, 0]]],
    [JES_API_TITLE, []
      ],
# uncomment the following two to put the Java api menu in
#    [API_TITLE, []
#      ],
    [WINDOW_TITLE,
      [[COMMAND_WINDOW_2, KeyEvent.VK_R,  CONTROL_KEY],
       [COMMAND_WINDOW_3HELP, KeyEvent.VK_H,  CONTROL_KEY],
       [COMMAND_WINDOW_3DEBUG, 0, 0]
]],
    # [SKINS_TITLE, [] ],

    [HELP_TITLE,
      [[COMMAND_ABOUT,  0,              0],
       [COMMAND_BUGREPORT, 0, 0],
       [COMMAND_EXPLORE,KeyEvent.VK_E,  CONTROL_KEY]]]]

LOAD_BUTTON_CAPTION = 'Load Program'
STOP_BUTTON_CAPTION = 'Stop'
SHOW_DEBUGGER_CAPTION = 'Watcher'
HIDE_DEBUGGER_CAPTION = 'Watcher'
UNTITLED_FILE_NAME  = 'Untitled'
HELP_URL = ''
LOAD_STATUS_CURRENT = ''
LOAD_STATUS_DIFF = ' UNLOADED '
MIN_COMMAND_WINDOW_SIZE = 150
MAX_COMMAND_WINDOW_SIZE = 250
VISUAL_CONTROL_MARGIN_SIZE = 5
SPLITTER_SIZE = 10
WATCHER_HSPLITTER_LOCATION = 400
HELP_HSPLITTER_LOCATION = 600
VSPLITTER_LOCATION = 320
BUTTON_PANE_HEIGHT = 15
STATUS_BAR_HEIGHT = 30

#PROMPT_SAVE_MESSAGE = 'You should save the file that you are working\non before loading or submitting it.\n-Would you like to save now?'

# Added by Adam Poncz
PROMPT_NEW_MESSAGE = 'You are about to open a new program area\n-Would you like to save your old program area?'
PROMPT_OPEN_MESSAGE = 'You are about to open a file.\n-Would you like to save the existing program area?'
PROMPT_LOAD_MESSAGE = 'You must save the file that you are working\non before loading it.\n-Would you like to save now?'
#end add

PROMPT_SAVE_CAPTION = 'Save File?'
#5 lines added to allow saving changes before exit. - 29 May 2008 by Buck Scharfnorth
PROMPT_EXIT_MESSAGE = 'Program area has been modified.\n-Would you like to save changes?'
PROMPT_PRINT_MESSAGE = 'You should save the file that you are working\non before printing it.\n-Would you like to save now?'
PROMPT_TURNIN_MESSAGE = 'You should save the file that you are working\non before submitting it.\n-Would you like to save now?'
ERROR_SAVE_FAIL = 'The file could not been saved.'
ERROR_OP_CANCEL = 'Operation Cancelled.'

FocusOwner = None

def getMethodList(klass):
  ret = []
  for (name, val) in klass.__dict__.items():
    if type(val).__name__.endswith('Function'):
      ret.append(name)
  return ret

class JESUI(swing.JFrame):

    FocusOwner = None
################################################################################
# Function name: __init__
# Return:
#     An instance of the JESUI class.
# Description:
#     Creates a new instance of the JESUI.
################################################################################

    def __init__(self, program):
        try:
#            media.setColorWrapAround( program.wrapPixelValues )
            self.soundErrorShown = 0
            self.FocusOwner = None
            self.swing = swing
            self.program = program
            self.size = JESConstants.INITIAL_WINDOW_SIZE
            self.windowClosing = self.exit

	    self.setLocationRelativeTo(None)

            #line added to allow saving changes before exit. - 29 May 2008 by Buck Scharfnorth
            self.setDefaultCloseOperation(swing.WindowConstants.DO_NOTHING_ON_CLOSE)

            self.contentPane.setLayout(swing.BoxLayout(self.contentPane,
                                                       swing.BoxLayout.Y_AXIS))
            self.setIconImage(swing.ImageIcon("images/jesicon.gif").getImage())
            #Create the visual components that will be placed in the UI
            self.runningBar = swing.JProgressBar(0, 5, string='',
                                                 preferredSize=(50, 30))

            self.editor        = JESEditor.JESEditor(self)
            self.commandWindow = JESCommandWindow.JESCommandWindow(self)
            self.loadButton    = swing.JButton(LOAD_BUTTON_CAPTION,
                                               actionPerformed=self.actionPerformed)
            self.loadButton.enabled = 0
            self.loadStatus    = swing.JLabel()
            self.stopButton    = swing.JButton(STOP_BUTTON_CAPTION,
                                               actionPerformed=self.actionPerformed)
            self.debuggerButton = swing.JButton(SHOW_DEBUGGER_CAPTION,
                                                actionPerformed=self.actionPerformed)
            self.cursorStatusLabel = swing.JLabel()
            self.cursorStatusLabel.setBorder(swing.BorderFactory.createEmptyBorder
                                                    (0,
                                                     VISUAL_CONTROL_MARGIN_SIZE,
                                                     0,
                                                     VISUAL_CONTROL_MARGIN_SIZE))
            self.nameStatusLabel = swing.JLabel()
            self.nameStatusLabel.setBorder(swing.BorderFactory.createEmptyBorder
                                                    (0,
                                                     VISUAL_CONTROL_MARGIN_SIZE,
                                                     0,
                                                     VISUAL_CONTROL_MARGIN_SIZE))
            self.docpane = swing.JPanel()
            self.docpane.setLayout(swing.BoxLayout(self.docpane, swing.BoxLayout.X_AXIS))
            self.gutter = JESGutter(self.editor, self.editor.getFont())
            self.gutter.setPreferredSize(awt.Dimension(25,300))
            self.gutter.setBorder(swing.BorderFactory.createEtchedBorder())
            if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_GUTTER):
                self.docpane.add(self.gutter)
            self.docpane.add(self.editor)

            #Create and set up the panes that all visual components reside on
            helpDivider  = swing.JSplitPane()
            helpDivider.setOneTouchExpandable(1)
            watcherDivider  = swing.JSplitPane()
            watcherDivider.setOneTouchExpandable(1)
            splitterPane = swing.JSplitPane()
            editorPane   = swing.JScrollPane(self.docpane)
            buttonPane   = swing.JPanel()
            commandPane  = swing.JScrollPane(self.commandWindow)
            bottomPane   = swing.JPanel()
            statusbar    = swing.JPanel()
            minSize =      awt.Dimension(100, 100)


            splitterPane.setPreferredSize(awt.Dimension(400,400))

            # self.program.wrapPixelValues = 1
            self.settingsWindow= None
            self.directoryWindow= None
            self.errorWindow= None
            self.turninWindow=None
            self.namefield = None
            self.mailfield=None
            self.gtfield=None
            self.optionsWindow=None
            self.listPane=None
            self.titlefield=swing.JTextField()
            self.gotoFrame=None
            self.linefield=swing.JTextField()
            self.searchFrame=None
            self.searchfield=swing.JTextField()
            self.up=swing.JRadioButton("Search Up")
            self.down = swing.JRadioButton("Search Down",1)
            self.attachmentlist=None
            self.list = None
            self.notesToTA=swing.JTextArea()
            self.notesScrollPane = swing.JScrollPane(self.notesToTA)
            self.notesScrollPane.setVerticalScrollBarPolicy(swing.JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)

            splitterPane.orientation = swing.JSplitPane.VERTICAL_SPLIT
            splitterPane.setDividerSize(SPLITTER_SIZE)
            splitterPane.setDividerLocation(VSPLITTER_LOCATION)
            splitterPane.setResizeWeight(1.0)
            splitterPane.setLeftComponent(editorPane)
            splitterPane.setRightComponent(bottomPane)

            helpDivider.orientation = swing.JSplitPane.HORIZONTAL_SPLIT
            self.htmlBrowser = Html_Browser.Html_Browser(JESConstants.HELP_START_PAGE)
            self.htmlBrowser.setMinimumSize(minSize)
            helpDivider.setDividerSize(SPLITTER_SIZE)
            helpDivider.setDividerLocation(HELP_HSPLITTER_LOCATION)
            helpDivider.setResizeWeight(1.0)
            helpDivider.setLeftComponent(splitterPane)

            #4 lines added to add a close button to help - 29 May 2008 by Buck Scharfnorth
            self.htmlBrowserWithHide = Html_Browser_With_Hide(self.htmlBrowser)
            self.htmlBrowserWithHide.setLayout(swing.BoxLayout(self.htmlBrowserWithHide, swing.BoxLayout.Y_AXIS))
            self.htmlBrowserWithHide.add(hideRight(self.actionPerformed))
            self.htmlBrowserWithHide.add(self.htmlBrowserWithHide.htmlBrowser)
            #line modified to add a close button to help - 29 May 2008 by Buck Scharfnorth
            helpDivider.setRightComponent(self.htmlBrowserWithHide)

            watcherDivider.orientation = swing.JSplitPane.HORIZONTAL_SPLIT
            watcherDivider.leftComponent = splitterPane
            #self.htmlBrowser = Html_Browser.Html_Browser(JESConstants.HELP_START_PAGE)

            # see jesprogram.py, this is initialized later
            # watcherDivider.rightComponent = self.program.interpreter.debugger.watcher
            watcherDivider.setDividerSize(SPLITTER_SIZE)
            watcherDivider.setDividerLocation(WATCHER_HSPLITTER_LOCATION)
            watcherDivider.setResizeWeight(1.0)
            watcherDivider.setLeftComponent(splitterPane)

            #3 lines added to add a close button to debugger - 29 May 2008 by Buck Scharfnorth
            self.watcherWithHide = swing.JPanel()
            self.watcherWithHide.setLayout(swing.BoxLayout(self.watcherWithHide, swing.BoxLayout.Y_AXIS))
            self.watcherWithHide.add(hideRight(self.actionPerformed))

            editorPane.setPreferredSize(awt.Dimension(lang.Short.MAX_VALUE,
                                                      lang.Short.MAX_VALUE))
            editorPane.getVerticalScrollBar().setUnitIncrement(14)

            buttonPane.setLayout(awt.BorderLayout())
            #buttonPane.setBorder(swing.BorderFactory.createEmptyBorder
             #                                        (VISUAL_CONTROL_MARGIN_SIZE,
              #                                        VISUAL_CONTROL_MARGIN_SIZE,
               #                                       VISUAL_CONTROL_MARGIN_SIZE,
                #                                      VISUAL_CONTROL_MARGIN_SIZE))
            buttonPane.setMaximumSize(awt.Dimension(lang.Short.MAX_VALUE,
                                                    BUTTON_PANE_HEIGHT))

            commandPane.setMinimumSize(awt.Dimension(0, MIN_COMMAND_WINDOW_SIZE))

            bottomPane.setLayout(swing.BoxLayout(bottomPane,
                                                 swing.BoxLayout.Y_AXIS))

            statusbar.setMinimumSize(awt.Dimension(0, STATUS_BAR_HEIGHT))
            statusbar.setMaximumSize(awt.Dimension(lang.Short.MAX_VALUE,
                                                   STATUS_BAR_HEIGHT))
            statusbar.setLayout(awt.BorderLayout())
            statusbar.setBorder(swing.BorderFactory.createLoweredBevelBorder())

            #Add all of the components to the main frame
            #self.contentPane.add(helpDivider)
            #self.contentPane.add(statusbar)

            # export the following for window layouts
            self.statusbar = statusbar
            self.helpDivider = helpDivider
            self.watcherDivider = watcherDivider
            self.splitterPane = splitterPane
            self.editorPane = editorPane
            self.bottomPane = bottomPane

            eastBar = swing.JPanel()
            #eastBar.setMaximumSize(awt.Dimension(lang.Short.MAX_VALUE,
            #                                    BUTTON_PANE_HEIGHT))
            eastBar.add(self.debuggerButton)
            eastBar.add(self.stopButton)
            eastBar.add(self.runningBar)
            westBar = swing.JPanel()
            westBar.add(self.loadButton)
            westBar.add(self.loadStatus)

            bottomPane.add(buttonPane)
            bottomPane.add(commandPane)
            buttonPane.add(westBar, awt.BorderLayout.WEST)
            #buttonPane.add(self.loadStatus, awt.BorderLayout.CENTER)
            buttonPane.add(eastBar, awt.BorderLayout.EAST)

            self.docLabel=swing.JLabel(EXPLAIN_DEFAULT_STATUS)

            self.explainButton    = swing.JButton(COMMAND_EXPLORE_HELP,
                                                  actionPerformed=self.actionPerformed)

            cursorAndName = swing.JPanel()
            cursorAndName.add(self.explainButton)
            cursorAndName.add(self.cursorStatusLabel)
            #cursorAndName.add(self.nameStatusLabel)

#            statusbar.add(self.cursorStatusLabel, awt.BorderLayout.CENTER)
#            statusbar.add(self.nameStatusLabel, awt.BorderLayout.EAST)
            statusbar.add(cursorAndName, awt.BorderLayout.EAST)
            statusbar.add(self.docLabel, awt.BorderLayout.WEST)



            self.turninstatuslabel=swing.JLabel("Creating Mail...")
            self.turninstatuswindow=swing.JFrame("Turnin Status")

            #Create the menu bar and menu items
            self.addmenu()

            # self.menu = swing.JMenuBar()
            # self.setJMenuBar(self.menu)

            # for eachMenu in MENU_OPTIONS:
            #     newMenu = swing.JMenu(eachMenu[0], actionPerformed=self.actionPerformed)
            #     self.menu.add(newMenu)
            #     #Create each menu option under the menu
            #     for eachMenuItem in eachMenu[1]:
            #         if eachMenuItem[0] == MENU_SEPARATOR:
            #             newMenu.addSeparator()
            #         else:
            #             if len(eachMenuItem) > 3 and eachMenuItem[3] == 1:
            #                 newMenuItem = swing.JCheckBoxMenuItem(eachMenuItem[0],
            #                                           actionPerformed = self.actionPerformed)
            #             else:
            #                 newMenuItem = swing.JMenuItem(eachMenuItem[0],
            #                                           actionPerformed = self.actionPerformed)
            #
            #             if eachMenuItem[1] <> 0:
            #                 newMenuItem.setAccelerator(swing.KeyStroke.getKeyStroke
            #                                                    (eachMenuItem[1],
            #                                                     eachMenuItem[2],
            #                                                     0))
            #             newMenu.add(newMenuItem)
            #     #If this is the help menu, store it in the self.helpMenu variable.
            #     if eachMenu[0] == HELP_TITLE:
            #         self.helpMenu = newMenu
            #     if eachMenu[0] == DEBUG_TITLE:
            #         self.debugMenu = newMenu
            #         #print 'length:',len(self.debugMenu.subElements)
            #         #print self.debugMenu.subElements[0].subElements
            #         self.debugMenu.subElements[0].subElements[1].setEnabled(0)
            #         self.debugMenu.subElements[0].subElements[2].setEnabled(0)
            #     if eachMenu[0] == API_TITLE:
            #         #BUILD API HELP
            #         for section in API_SECTIONS:
            #             newMenuSection = swing.JMenu(str(section),
            #                                          actionPerformed = self.apiHelp)
            #
            #             for api_function in getMethodList(section):
            #                 func_name = str(section)+'.'+api_function
            #                 newMenuItem = swing.JMenuItem(func_name,
            #                                               actionPerformed = self.apiHelp)
            #                 newMenuSection.add(newMenuItem)
            #             newMenu.add(newMenuSection)
            #     if eachMenu[0] == JES_API_TITLE:
            #         #BUILD JES API HELP
            #         for (section, api_functions) in JES_API_SECTIONS:
            #             newMenuSection = swing.JMenu(str(section),
            #                                          actionPerformed = self.apiHelp)
            #
            #             for api_function in api_functions:
            #                 newMenuItem = swing.JMenuItem(api_function,
            #                                               actionPerformed = self.apiHelp)
            #                 newMenuSection.add(newMenuItem)
            #             newMenu.add(newMenuSection)

            #     # if eachMenu[0] == SKINS_TITLE:
            #     #     #BUILD SKINS LIST
            #     #     for skin in UIManager.getInstalledLookAndFeels():
            #     #         newMenuSection = swing.JMenuItem(str(skin.getName()),
            #     #                                      actionPerformed = self.changeSkin)
            #     #         newMenu.add(newMenuSection)

            #Set remaining object variables
            self.heldText = ''
            self.setRunning(0)
            self.setFileName('')
            self.UpdateRowCol(1, 1)
            self.UpdateName()
            self.helpFiles = {}
            self.helplist = []

            editorDocument = self.editor.getDocument()
            editorDocument.changeFontSize(JESConfig.getInstance().getIntegerProperty(JESConfig.CONFIG_FONT))
            commandDocument = self.commandWindow.getDocument()
            commandDocument.changeFontSize(JESConfig.getInstance().getIntegerProperty(JESConfig.CONFIG_FONT))

        except:
            import traceback
            import sys
            a,b,c = sys.exc_info()
            print "JESUI: WEIRD EXCEPT:"
            traceback.print_exception(a,b,c)

    def addmenu(self):
        """Regenerates then installs the menu, based on the current state of
        the world; this doesn't change often, and currently we only have to
        decide whether to include the 'turnin' menu."""

        self.menu = self.buildmenu()
        self.setJMenuBar(self.menu)

    def buildmenu(self):
        """Regenerate and return an apropos menu."""

        output = swing.JMenuBar()

        for eachMenu in MENU_OPTIONS:

            if eachMenu[0] == TURNIN_TITLE and not JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_SHOWTURNIN):
                continue

            newMenu = swing.JMenu(eachMenu[0], actionPerformed=self.actionPerformed)
            output.add(newMenu)
            #Create each menu option under the menu
            for eachMenuItem in eachMenu[1]:
                if eachMenuItem[0] == MENU_SEPARATOR:
                    newMenu.addSeparator()
                else:
                    if len(eachMenuItem) > 3 and eachMenuItem[3] == 1:
                        newMenuItem = swing.JCheckBoxMenuItem(eachMenuItem[0],
                                                  actionPerformed = self.actionPerformed)
                    else:
                        newMenuItem = swing.JMenuItem(eachMenuItem[0],
                                                  actionPerformed = self.actionPerformed)

                    if eachMenuItem[1] <> 0:
                        newMenuItem.setAccelerator(swing.KeyStroke.getKeyStroke
                                                           (eachMenuItem[1],
                                                            eachMenuItem[2],
                                                            0))
                    newMenu.add(newMenuItem)
            #If this is the help menu, store it in the self.helpMenu variable.
            if eachMenu[0] == HELP_TITLE:
                self.helpMenu = newMenu
            if eachMenu[0] == DEBUG_TITLE:
                self.debugMenu = newMenu
                #print 'length:',len(self.debugMenu.subElements)
                #print self.debugMenu.subElements[0].subElements
                self.debugMenu.subElements[0].subElements[1].setEnabled(0)
                self.debugMenu.subElements[0].subElements[2].setEnabled(0)
            if eachMenu[0] == API_TITLE:
                #BUILD API HELP
                for section in API_SECTIONS:
                    newMenuSection = swing.JMenu(str(section),
                                                 actionPerformed = self.apiHelp)

                    for api_function in getMethodList(section):
                        func_name = str(section)+'.'+api_function
                        newMenuItem = swing.JMenuItem(func_name,
                                                      actionPerformed = self.apiHelp)
                        newMenuSection.add(newMenuItem)
                    newMenu.add(newMenuSection)
            if eachMenu[0] == JES_API_TITLE:
                #BUILD JES API HELP
                for (section, api_functions) in JES_API_SECTIONS:
                    newMenuSection = swing.JMenu(str(section),
                                                 actionPerformed = self.apiHelp)

                    for api_function in api_functions:
                        newMenuItem = swing.JMenuItem(api_function,
                                                      actionPerformed = self.apiHelp)
                        newMenuSection.add(newMenuItem)
                    newMenu.add(newMenuSection)

        return output

    ################################################################################
    # Function name: apiHelp
    # Parameters:
    #     -event: event object that represents action that occured
    # Description:
    #     This function is called when a menu option is selected or a button is
    #     pressed.  It calls the correct function in order to perform the action
    #     that the user wants.
    ################################################################################
    def apiHelp(self, event):
        actionCommand = event.getActionCommand()

        self.program.logBuffer.addMenuOption(actionCommand)

        html_page = ''
        section = ''
        api_function = ''
        try:
            section,api_function = actionCommand.split('.', 2)
        except:
            pass


        if actionCommand.find('.') == -1:
            #JES SECTION HELP

            focusedComponent = self.FocusOwner
            if isinstance(focusedComponent, swing.JTextPane):
                focusedComponent.replaceSelection(actionCommand+'(')

            self.openExploreWindow(actionCommand)

        else:
            #JAVA SECTION HELP
            #FIXME : jump directly to the function...difficult because javadoc puts the types in the html A NAME field
            html_page = 'file:///' + os.getcwd() + '/Sources/javadoc/' + section + '.html#method_summary'

            focusedComponent = self.FocusOwner
            if isinstance(focusedComponent, swing.JTextPane):
                focusedComponent.replaceSelection('my'+actionCommand+'(')

    def changeSkin(self, event):
        try:
            actionCommand = event.getActionCommand()
        except AttributeError, e:
            actionCommand = event

        if(actionCommand == "comboBoxChanged"):
            box = event.getSource()
            actionCommand = str(box.getSelectedItem())

        for skin in UIManager.getInstalledLookAndFeels():
            if str(skin.getName()) == actionCommand:

                UIManager.setLookAndFeel(skin.getClassName())
                SwingUtilities.updateComponentTreeUI(self);
                # self.pack()

                if(self.optionsWindow):
                    SwingUtilities.updateComponentTreeUI(self.optionsWindow);
                    self.optionsWindow.pack()

                JESConfig.getInstance().setStringProperty( JESConfig.CONFIG_SKIN, skin.getName() )
                #self.program.skin = str(skin.getName())
                # for some reason this is needed or the commandWindow will go dead
#                self.program.interpreter.runCommand("printNow('')")
#                self.commandWindow.restoreConsole('run')
		self.commandWindow.setKeymap(self.commandWindow.my_keymap)
                return None

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

        self.program.logBuffer.addMenuOption(actionCommand)

        # print actionCommand

        if actionCommand == COMMAND_NEW:
            # MODIFIED by Adam Poncz
            if self.editor.modified:
				#modified for promptSave cancel button - Buck Scharfnorth 29 May 2008
                isSaved = self.promptSave(PROMPT_NEW_MESSAGE)
                if isSaved > -1:
                    self.editor.document.removeErrorHighlighting()
                    self.program.newFile()
           #inserted for promptSave cancel button - Buck Scharfnorth 29 May 2008
            else:
                self.program.newFile()
            # END MOD
        elif actionCommand == COMMAND_OPEN:
            # MODIFIED by Patrick Carnahan
            if self.editor.modified:
				#modified for promptSave cancel button - Buck Scharfnorth 29 May 2008
                isSaved = self.promptSave(PROMPT_OPEN_MESSAGE)
                if isSaved > -1:
                    self.editor.document.removeErrorHighlighting()
                    self.program.openFile()
            #inserted for promptSave cancel button - Buck Scharfnorth 29 May 2008
            else:
                self.program.openFile()
            # END MOD
        elif actionCommand == COMMAND_SAVE:
            self.program.saveFile()
        elif actionCommand == COMMAND_SAVEAS:
            self.program.saveAs()
        elif actionCommand == COMMAND_EXIT:
            #line modified to allow saving changes before exit. - Buck Scharfnorth 29 May 2008
            self.exit(actionCommand)
        elif actionCommand == COMMAND_CUT:
            self.cut()
        elif actionCommand == COMMAND_COPY:
            self.copy()
        elif actionCommand == PRINT:
            self.printCommand()
        elif actionCommand == COMMAND_PASTE:
            self.paste()
        elif actionCommand == COMMAND_UNDO:
            self.undo()
        elif actionCommand == COMMAND_REDO:
            self.redo()
        elif actionCommand == COMMAND_GOTO:
            self.getGoToLineNum()
        elif actionCommand == COMMAND_SEARCH:
            self.search()
        elif actionCommand == COMMAND_OPTIONS:
            self.openOptions()
        #elif actionCommand == COMMAND_DIRECTORY:
        #    self.openDirectoryChooser()
        elif actionCommand == COMMAND_HELP:
            self.openBrowser(self, HELP_URL)
            self.windowSetting(COMMAND_WINDOW_3HELP)
        elif actionCommand == TURNIN_OPTIONS:
            self.openSettings()
        elif actionCommand == TURNIN_HW:
            self.openTurnin(TURNIN_HW)
        elif actionCommand == DEBUG_SHOW_DEBUGGER or actionCommand == DEBUG_HIDE_DEBUGGER:
            self.program.interpreter.toggle_debug_mode()
        elif actionCommand == DEBUG_WATCH_VAR:
            self.watchVariable()
        elif actionCommand == DEBUG_UNWATCH_VAR:
            self.unwatchVariable()
        elif actionCommand == COMMAND_ABOUT:
            self.program.openAboutWindow()
        elif actionCommand == COMMAND_BUGREPORT:
            # self.program.openAboutWindow()
            bugreporter = JESBugReporter()
        elif (actionCommand == LOAD_BUTTON_CAPTION) or (actionCommand == COMMAND_LOAD):
            if self.editor.modified:
                if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_AUTOSAVEONRUN):
                    self.program.saveFile()
                    self.program.loadFile()
                #modified for promptSave cancel button - Buck Scharfnorth 29 May 2008
                elif self.promptSave(PROMPT_LOAD_MESSAGE) > 0:
                    self.editor.document.removeErrorHighlighting()
                    self.program.loadFile()
            else:
                self.program.loadFile()
        elif actionCommand == STOP_BUTTON_CAPTION:
            self.program.stopThread()
        elif actionCommand == SHOW_DEBUGGER_CAPTION or actionCommand == HIDE_DEBUGGER_CAPTION:
            self.program.interpreter.toggle_debug_mode()
        elif actionCommand == COMMAND_EDITOR:
            self.editor.requestFocus()
        elif actionCommand == COMMAND_COMMAND:
            self.commandWindow.requestFocus()
        elif actionCommand == COMMAND_EXPLORE:
            self.openExploreWindow(self.FocusOwner.getSelectedText())
        elif actionCommand[:len(EXPLAIN_PREFIX)] == EXPLAIN_PREFIX:
            self.openExploreWindow(actionCommand[len(EXPLAIN_PREFIX):])

        elif actionCommand == COMMAND_SOUND_TOOL:
            self.loadSoundTool()
        elif actionCommand == COMMAND_WINDOW_2 and not self.program.interpreter.debugger.running:
            self.windowSetting(COMMAND_WINDOW_2)
        elif actionCommand == COMMAND_WINDOW_3HELP:
            self.windowSetting(COMMAND_WINDOW_3HELP)
        elif actionCommand == COMMAND_WINDOW_3DEBUG and not self.program.interpreter.debug_mode:
            # this will call window setting by itself
            self.program.interpreter.toggle_debug_mode()

        elif actionCommand == AUTOSAVE:
            JESConfig.getInstance().setBooleanProperty(JESConfig.CONFIG_AUTOSAVEONRUN, not JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_AUTOSAVEONRUN) )
            #self.program.autoSaveOnRun = not self.program.autoSaveOnRun

        elif actionCommand == COMMAND_PICTURE_TOOL:
            self.loadPictureTool()
        elif actionCommand == COMMAND_FRAMESEQUENCER_TOOL:
            self.loadFrameSequencerTool()
        else:
            self.CheckIfHelpTopic(actionCommand)


###############################################################################
# Function: openExploreWindow
# Description:
#     Examines the highlighted text in the JTextArea, and searches for it in the
#     helplist.  Then it pops up a help window with an API description.
###############################################################################
    def openExploreWindow(self, search_text):
        #Find The word under the cursor
        try:
            str = string.strip(search_text)
            msg = "No entry found for '" + str + "'"
            #Search the API help for the word (method)
            for entry in self.helplist:
                if string.strip(entry[0]) == str:
                    msg = entry[1]
                    break
        except:
            msg = "No text selected.<br>To use Explore, highlight a function name or keyword you want help with."
            str = ""
            #Pop up the help window:

        #self.htmlBrowser.htmlPane.setText(msg)
        self.htmlBrowserWithHide.htmlBrowser.htmlPane.setText(msg)

        self.windowSetting(COMMAND_WINDOW_3HELP)

        #frame = swing.JFrame()
        #text = swing.JEditorPane("text/html", msg)
        #scrollpane = swing.JScrollPane(text)
        #text.setEditable(0)
        #frame.setTitle("Explain: " + str)
        #frame.setSize(450, 400)
        #frame.setContentPane(scrollpane)
        #frame.show()


###############################################################################
# Function: loadCurrent
# Description:
#     Updates the UI to reflact that the current code has been loaded
###############################################################################
    def loadCurrent(self):
        self.loadStatus.setText(LOAD_STATUS_CURRENT)


###############################################################################
# Function: loadCurrent
# Description:
#     Updates the UI to the new window setting
###############################################################################
    def disableDebugger(self):
        if self.program.interpreter.debug_mode:
            self.program.interpreter.toggle_debug_mode()


    def windowSetting(self, setting):

        self.contentPane.removeAll()
#        self.setContentPane(swing.JPanel())

        if setting == COMMAND_WINDOW_3HELP:
            self.disableDebugger()
            self.helpDivider.setLeftComponent(self.splitterPane)
            #line modified to add a close button to help - 29 May 2008 by Buck Scharfnorth
            self.helpDivider.setRightComponent(self.htmlBrowserWithHide)
            self.contentPane.add(self.helpDivider)
            self.contentPane.add(self.statusbar)
            self.splitterPane.resetToPreferredSizes()
            self.helpDivider.resetToPreferredSizes()
            self.helpDivider.setDividerLocation(HELP_HSPLITTER_LOCATION)

        # do not call this one explicitly!!
        elif setting == COMMAND_WINDOW_3DEBUG:
            #line added to add a close button to debugger - 29 May 2008 by Buck Scharfnorth
            self.watcherWithHide.add(self.program.interpreter.debugger.watcher)
            self.watcherDivider.setLeftComponent(self.splitterPane)
            #line modified to add a close button to debugger - 29 May 2008 by Buck Scharfnorth
            self.watcherDivider.setRightComponent(self.watcherWithHide)
            self.contentPane.add(self.watcherDivider)
            self.contentPane.add(self.statusbar)
            self.splitterPane.resetToPreferredSizes()
            self.watcherDivider.resetToPreferredSizes()
            self.watcherDivider.setDividerLocation(WATCHER_HSPLITTER_LOCATION)

        else: #setting == COMMAND_WINDOW_2:
            self.disableDebugger()
            self.splitterPane.setLeftComponent(self.editorPane)
            self.splitterPane.setRightComponent(self.bottomPane)
            self.contentPane.add(self.splitterPane)
            self.contentPane.add(self.statusbar)
            self.splitterPane.resetToPreferredSizes()

        self.setJMenuBar(self.menu)
        self.contentPane.validate()
#?        self.contentPane.revalidate()



###############################################################################
# Function: loadDifferent
# Description:
#     Updates the UI to reflact that the current code has not been loaded
###############################################################################
    def loadDifferent(self):
        self.loadStatus.setText(LOAD_STATUS_DIFF)

###############################################################################
# Function name: exit
# Parameters:
#     -event: event object that represents the event that occured
# Description:
#     This function, which closes the program, is called when the user closes
#     the JES program with the 'X' on the main window.
# Revisions:
#     Modified to prompt for save on exit - 29 May 2008 by Buck Scharfnorth
################################################################################
    def exit(self, event):
        if self.editor.modified:
            isSaved = self.promptSave(PROMPT_EXIT_MESSAGE)
            if isSaved > -1:
                JESConfig.getInstance().writeConfig()
                self.program.closeProgram()
        else:
            JESConfig.getInstance().writeConfig()
            self.program.closeProgram()

################################################################################
# Function name: promptSave
# Return:
#     TRUE if the file was saved successfully, FALSE if the save failed or the
#     user decided not to save the file.
# Description:
#     Prompts the user whether they want to save the currently loaded file.
# Revisions:
#     Modified to give the user an option to cancel the operation which
#     triggered promptSave. (Exit JES, New/Open/Load Program, Turnin, Print).
#     MODIFIED RETURNS 1 if save is a success and the operation will continue.
#     0 if user chooses not to save and the operation will continue using
#     the previous saved version of the file (when available & necessary).
#     -1 if user cancels or if save fails (such as on a read only drive).
################################################################################
    def promptSave(self, prompt):
        promptResult = swing.JOptionPane.showConfirmDialog(
                                           self,
                                           prompt,
                                           PROMPT_SAVE_CAPTION,
                                           swing.JOptionPane.YES_NO_CANCEL_OPTION)

        if promptResult == swing.JOptionPane.YES_OPTION:
            isSaved = self.program.saveFile()
            if isSaved != 1:
                swing.JOptionPane.showMessageDialog(self,
                                  ERROR_SAVE_FAIL+'\n-'+ERROR_OP_CANCEL,
                                  ERROR_OP_CANCEL,
                                  swing.JOptionPane.WARNING_MESSAGE)
                return -1
            else:
                return 1
        elif promptResult == swing.JOptionPane.NO_OPTION:
            return 0
        else:
            return -1

################################################################################
# Function name: openBrowser
# Parameters:
#     -url: Target URL or file name for the browser.  If a file name is given,
#           the entire path to that file must also be included.
# Description:
#     Opens a browser window to the specified location.  This is used when
#     displaying the HTML help.
################################################################################
    def openBrowser(self, target):
        try:
           #j=Html_Browser.Html_Browser(target)
           # self.htmlBrowser.field.setText(target)
            self.htmlBrowserWithHide.htmlBrowser.field.setText(target)
            self.htmlBrowserWithHide.htmlBrowser.goToUrl(None)
        except:
           print "ERROR opening broswer with file:",target

################################################################################
# Function name: setRunning
# Parameters:
#     -runBool: Boolean identifying whether the program is running.
# Description:
#     This function is called to tell the GUI whether the Jython interpreter is
#     running any code.  When running, the GUI will enable the stop button,
#     disable the load button, and change the cursor to an hourglass.
################################################################################
    def setRunning(self, runBool):
        self.running = runBool
        self.loadButton.enabled = not runBool
        self.stopButton.enabled = runBool

        if runBool:
            cursor = awt.Cursor(awt.Cursor.DEFAULT_CURSOR)
            textCursor = awt.Cursor(awt.Cursor.WAIT_CURSOR)
        else:
            cursor = awt.Cursor(awt.Cursor.DEFAULT_CURSOR)
            textCursor = awt.Cursor(awt.Cursor.TEXT_CURSOR)

        self.setCursor(cursor)
        self.editor.setCursor(textCursor)
        self.commandWindow.setCursor(textCursor)

################################################################################
# Function name: setFileName
# Parameters:
#     -filename: name of the currenly open file
# Description:
#     Sets the file name that is displayed in the program caption.  If the
#     filename parameter is set to '', then the file name will be shown as
#     'Untitled'.
################################################################################
    def setFileName(self, filename):
        if filename == '':
            filename = UNTITLED_FILE_NAME

        self.title = JESConstants.APPLICATION_TITLE % filename

################################################################################
# Function name: callTextEditFunction
# Description:
#     Performs the cut operation on the either the editor or command window,
#     depending on which one has the focus.
################################################################################
    def callTextEditFunction(self, function):
        #global FocusOwner
        focusedComponent = self.FocusOwner #self.getFocusOwner()

        if isinstance(focusedComponent, swing.JTextPane):
            focusedComponent.function()

################################################################################
# Function name: cut
# Description:
#     Performs the cut operation on the either the editor or command window,
#     depending on which one has the focus.
################################################################################
    def cut(self):
        #global FocusOwner
        #focusedComponent = self.getFocusOwner()
        focusedComponent = self.FocusOwner
        if isinstance(focusedComponent, swing.JTextPane):
            focusedComponent.cut()

################################################################################
# Function name: copy
# Description:
#     Performs the copy operation on the either the editor or command window,
#     depending on which one has the focus.
################################################################################
    def copy(self):
        #global FocusOwner
        focusedComponent = self.FocusOwner #self.getFocusOwner()

        if isinstance(focusedComponent, swing.JTextPane):
            focusedComponent.copy()

################################################################################
# Function name: paste
# Description:
#     Performs the paste operation on the either the editor or command window,
#     depending on which one has the focus.
################################################################################
    def paste(self):
        #global FocusOwner
        focusedComponent = self.FocusOwner #self.getFocusOwner()
        if isinstance(focusedComponent, swing.JTextPane):
            focusedComponent.paste()

################################################################################
# Function name: undo
# Description:
#     Performs the undo operation on the either the editor or command window,
#     depending on which one has the focus.
################################################################################
    def undo(self):
        #global FocusOwner
        focusedComponent = self.FocusOwner #self.getFocusOwner()

        if isinstance(focusedComponent, swing.JTextPane):
            focusedComponent.undo()

################################################################################
# Function name: redo
# Description:
#     Performs the redo operation on the either the editor or command window,
#     depending on which one has the focus.
################################################################################
    def redo(self):
        #global FocusOwner
        focusedComponent = self.FocusOwner #self.getFocusOwner()

        if isinstance(focusedComponent, swing.JTextPane):
            focusedComponent.redo()

################################################################################
# Function name: print
# Description:
#     Prints the current Document contained in JES
################################################################################
    def printCommand(self):
        name = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_NAME)
#        try:
#            #Sets up local variables according to an existing config file.
#            array=self.program.readFromConfigFile()
#            name=array[JESConstants.CONFIG_NAME]
#        except:
#            #If we have a problem, just set them all to the empty string
#            name='Unknown'
        isSaved=1
        if self.editor.modified:
            #modified for promptSave cancel button - Buck Scharfnorth 29 May 2008
            isSaved=self.promptSave(PROMPT_PRINT_MESSAGE)
        if isSaved > -1:
            printerJob = printer.PrinterJob.getPrinterJob()
            printerJob.setPrintable( JESPrintableDocument.JESPrintableDocument(self.program.filename,name) )
            doPrint = printerJob.printDialog()
            if (doPrint):
                try:
                    printerJob.print()
                except:
                    print "Printing error"

################################################################################
# Function name: UpdateRowCol
# Parameters:
#     -row: current row that the cursor is on
#     -col: current column that the cursor is on
# Description:
#     Updates the status bar with the given row and column.
################################################################################
    def UpdateRowCol(self, row, col):
        self.cursorStatusLabel.text ='Line Number:' + str(col) + ' Position: ' + str(row)
        self.cursorStatusLabel.setForeground(awt.Color.black)

    def UpdateToolbarHelp(self, keyword):
        search_str = string.strip(keyword)
        msg = ''
        for entry in self.helplist:
            if string.strip(entry[0]) == search_str:
                msg = (entry[1])[:(entry[1].find('\n'))]
                break

        if not msg == '':
            msg = re.sub('<(?!(?:a\s|/a|!))[^>]*>', '', msg)
            if msg.find(':') == -1:
                self.docLabel.text = str(msg)
            else:
                self.docLabel.text = str(msg[:msg.find(':')])
            self.cursorStatusLabel.setForeground(awt.Color.black)
            self.explainButton.text = 'Explain ' + search_str

        else:
            self.docLabel.text = str(EXPLAIN_DEFAULT_STATUS)
            self.cursorStatusLabel.setForeground(awt.Color.black)
            self.explainButton.text = COMMAND_EXPLORE_HELP



    def UpdateName(self):
        self.nameStatusLabel.text = 'Current User: ' + JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_NAME)
        self.nameStatusLabel.setForeground(awt.Color.black)
#        try:
#            array=self.program.readFromConfigFile()
#            name=array[JESConstants.CONFIG_NAME]
#            name='Current User: '+ name + '   '
#            self.nameStatusLabel.text =name
#            self.nameStatusLabel.setForeground(awt.Color.black)
#        except:
#            self.nameStatusLabel.text ='Not Registered   '

################################################################################
# Function name: SetHelpFiles
# Parameters:
#     -helpFiles: array of file names (including entire path) for all help files
#                 that will be added to help menu.
# Description:
#     Adds the help files specified in the helpFiles parameter to the help menu.
################################################################################
    def SetHelpFiles(self, helpFiles):
        self.helpFiles = {}
        self.helpMenu.addSeparator()
        for eachHelpFilePath in helpFiles:
            fileName = os.path.basename(eachHelpFilePath)
            fileName = fileName.replace(HELP_FILE_EXTENTION, '')
            fileName = fileName.replace('_', ' ')
            self.helpFiles[fileName] = eachHelpFilePath
            newMenuItem = swing.JMenuItem(fileName,
                                          actionPerformed = self.actionPerformed)
            self.helpMenu.add(newMenuItem)
        #Set up contextual help list
        helpfile = open(JESConstants.JES_API_HELP_FILE, 'r')
        helpcontents = helpfile.read()
        helpl = helpcontents.split("_")
        for entry in helpl:
            self.helplist.append(entry.split("|"))
        helpfile.close()

################################################################################
# Function name: CheckIfHelpTopic
# Parameters:
#     -helpTopic: string containing the name of the menu option to be checked
# Return:
#     Returns true if the helpTopic variable was the name of a help topic, or
#     false if it was not.
# Description:
#     Checks to see if the given string (specified in the helpTopic parameter)
#     is the name of a help topic.  If it is, the openBrowser function is called
#     to open up that help file.
################################################################################
    def CheckIfHelpTopic(self, helpTopic):
        if self.helpFiles.has_key(helpTopic):
            self.openBrowser(self.helpFiles[helpTopic])
            self.windowSetting(COMMAND_WINDOW_3HELP)
            return 1
        else:
            return 0

################################################################################
# Function name: openSettings
# Description:
#     Opens up a JES settings dialog.  If the window has not been created, it is
#     created.  If the config file does not exist, the string in it are set to
#     empty strings.  Once everything is created, it is made visible.  If the
#     window already exists, but it is hidden, it is just made visible.
################################################################################
    def openSettings(self):
        if self.settingsWindow== None:
#            try:
#                #Sets up local variables according to an existing config file.
#                array=self.program.readFromConfigFile()
#                name=array[JESConstants.CONFIG_NAME]
#                gt=array[JESConstants.CONFIG_GT]
#
#                if(array[JESConstants.CONFIG_MAIL] == ''):
#                    mail=JESConstants.MAIL_SERVER #default to mail.gatech.edu
#                else:
#                    mail=array[JESConstants.CONFIG_MAIL]
#
#                mailaddr = array[JESConstants.CONFIG_EMAIL_ADDR]
#                webDefs = array[JESConstants.CONFIG_WEB_TURNIN]
#            except:
#                #If we have a problem, just set them all to the empty string
#                name=''
#                gt=''
#                mailaddr = ''
#                mail = JESConstants.MAIL_SERVER
#                webDefs = JESConstants.WEB_DEFINITIONS
            #Creating the window
            self.settingsWindow=swing.JFrame("JES Settings")
            self.settingsWindow.contentPane.layout = awt.GridLayout(0,2)
            self.settingsWindow.size = (250,150)
            savebutton = swing.JButton("Save Changes",preferredSize=(100,20),
                    actionPerformed=self.settingsButtonPressed)
            cancelbutton= swing.JButton("Cancel",preferredSize=(100,20),
                    actionPerformed=self.settingsButtonPressed)
            self.namefield= swing.JTextField(JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_NAME),preferredSize=(200,20))
            namelabel=swing.JLabel("Name:")
            self.gtfield= swing.JTextField(JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_GT),preferredSize=(200,20))
            gtlabel=swing.JLabel("Student #:")
            self.mailaddrfield= swing.JTextField(JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_EMAIL_ADDR),preferredSize=(200,20))
            mailaddrlabel=swing.JLabel("Email Address:")
            self.mailfield= swing.JTextField(JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MAIL),preferredSize=(200,20))
            maillabel=swing.JLabel("Mail Server:")
            self.webDefsField = swing.JTextField(JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_WEB_TURNIN), preferredSize=(200,20))
            webDefslabel = swing.JLabel("Turnin Definitions:")
            self.settingsWindow.contentPane.add(namelabel)
            self.settingsWindow.contentPane.add(self.namefield)
            self.settingsWindow.contentPane.add(gtlabel)
            self.settingsWindow.contentPane.add(self.gtfield)
            #RJC - always display if using coweb dynamic turnin type table
            if JESConstants.EMAIL_TURNIN or JESConstants.TURNIN_TYPE_TABLE:
                self.settingsWindow.contentPane.add(mailaddrlabel)
                self.settingsWindow.contentPane.add(self.mailaddrfield)
                self.settingsWindow.contentPane.add(maillabel)
                self.settingsWindow.contentPane.add(self.mailfield)
            if JESConstants.COWEB_TURNIN:
                pass
                #self.settingsWindow.contentPane.add(webDefslabel)
                #self.settingsWindow.contentPane.add(self.webDefsField)
            self.settingsWindow.contentPane.add(cancelbutton)
            self.settingsWindow.contentPane.add(savebutton)
            self.settingsWindow.pack()
	    self.settingsWindow.setLocationRelativeTo(None)
            self.settingsWindow.show()
        else:
            self.settingsWindow.show()


################################################################################
# Function name: openDirectoryChooser
# Description:
#     Opens up a JES directory dialog.  If the window has not been created, it is
#     created.  If the config file does not exist, the string in it are set to
#     empty strings.  Once everything is created, it is made visible.  If the
#     window already exists, but it is hidden, it is just made visible.
################################################################################

#    def openDirectoryChooser(self):
#        #print "In openDirectoryChooser"
#	if self.directoryWindow == None:
#            #print "No directory window yet"
#            self.directoryWindow=swing.JFrame("JES Directory Chooser")
#            self.directoryWindow.contentPane.layout = awt.GridLayout(0,3)
#            self.directoryWindow.size = (350,150)
#            savebutton = swing.JButton("Save Changes",preferredSize=(100,20),
#                    actionPerformed=self.directoryButtonPressed)
#            cancelbutton = swing.JButton("Cancel",preferredSize=(100,20),
#                    actionPerformed=self.directoryButtonPressed)
#            changedirbutton = swing.JButton("Change Directory",preferredSize=(100,20),
#                    actionPerformed=self.directoryButtonPressed)
#            self.dirfield = swing.JTextField(self.program.defaultPath,preferredSize=(200,20))
#            self.dirfield.setEditable(0)
#	     dirlabel=swing.JLabel("Directory:")
#            self.directoryWindow.contentPane.add(dirlabel)
#            self.directoryWindow.contentPane.add(self.dirfield)
#            self.directoryWindow.contentPane.add(changedirbutton)
#            self.directoryWindow.contentPane.add(cancelbutton)
#            self.directoryWindow.contentPane.add(savebutton)
#            #print "Everything added"
#            self.directoryWindow.pack()
#            self.directoryWindow.show()
#        else:
#            self.directoryWindow.show()


    ################################################################################
    # Function name: settingsButtonPressed
    # Parameters: event
    # Description:
    #     Handles events thrown from the settings dialog window.
    ################################################################################

    def settingsButtonPressed(self,event):
        if event.source.text=='Cancel':
            pass
            self.settingsWindow.hide()
        else:
            JESConfig.getInstance().writeConfig()
#            list = []
#            if self.namefield.text != None:
#                list.append([JESConstants.CONFIG_NAME, self.namefield.text])
#            if self.gtfield.text != None:
#                list.append([JESConstants.CONFIG_GT, self.gtfield.text])
#            if self.mailfield.text != None:
#                list.append([JESConstants.CONFIG_MAIL, self.mailfield.text])
#            if self.mailaddrfield.text != None:
#                list.append([JESConstants.CONFIG_EMAIL_ADDR, self.mailaddrfield.text])
#            if self.webDefsField.text != None:
#                list.append([JESConstants.CONFIG_WEB_TURNIN, self.webDefsField.text])
#            self.program.writeConfigListToFile(list)
            self.UpdateName()
            self.settingsWindow.hide()


    ################################################################################
    # Function name: directoryButtonPressed
    # Parameters: event
    # Description:
    #     Handles events thrown from the directory dialog window.
    ################################################################################

#    def directoryButtonPressed(self,event):
#        if event.source.text=='Cancel':
#	    pass
#            self.directoryWindow.hide()
#	elif event.source.text=='Change Directory':
#	    self.dirChooser = swing.JFileChooser(self.program.defaultPath)
#	    self.dirChooser.setFileSelectionMode(swing.JFileChooser.DIRECTORIES_ONLY)
#	    self.dirChooser.setApproveButtonText("Use this Directory")
#	    returnval = self.dirChooser.showOpenDialog(self.program.gui)
#	    if returnval == swing.JFileChooser.APPROVE_OPTION:
#	        self.dirfield.setText(self.dirChooser.getSelectedFile().getAbsolutePath())
#	    self.directoryWindow.toFront()
#	    #print 'ChangeDir'
#	else:
#           self.program.defaultPath = self.dirfield.getText()
#	    self.program.saveOptions()
#	    self.directoryWindow.hide()
#	    #print 'save'

    ################################################################################
    # Function name: openTurnin
    # Description:
    #     Opens up a JES Turnin dialog.
    ################################################################################
    def openTurnin(self,toTurnin):
            #decides what you are turning in.
            self.turninWindow=swing.JFrame('Assignment Submission')
            self.turninWindow.contentPane.layout = awt.GridLayout(3,1)
            self.turninWindow.size = (300,400)
            self.notesToTA.setText('')
            self.notesToTA.setLineWrap(1)
            self.notesToTA.setWrapStyleWord(1)
            notesLabel=swing.JLabel("Notes to TA:")
            self.notesScrollPane.size = (240, 200)
            toSubmitLabel=swing.JLabel("Submitting file:")
            fileNameLabel=swing.JLabel(os.path.basename(self.program.filename))
            titlelabel = swing.JLabel('Assignment to submit:   ')
            turninbutton = swing.JButton("Turnin",preferredSize=(100,20), actionPerformed=self.turninButtonPressed)
            cancelbutton= swing.JButton("Cancel",preferredSize=(100,20), actionPerformed=self.turninButtonPressed)
            addbutton = swing.JButton("Add File",preferredSize=(120,20), actionPerformed=self.turninButtonPressed)
            removebutton= swing.JButton("Remove File",preferredSize=(120,20), actionPerformed=self.turninButtonPressed)
            assignmentStrings=self.grabAssignmentList()
            self.titlefield=swing.JComboBox(assignmentStrings)
            self.attachmentlist=util.Vector()
            self.list=swing.JList(self.attachmentlist)
            self.listPane=swing.JScrollPane(self.list)
            self.listPane.preferredSize=(100,100)
            try:
#                array=self.program.readFromConfigFile()
#                name=array[JESConstants.CONFIG_NAME]
#                gt=array[JESConstants.CONFIG_GT]
#                mail=array[JESConstants.CONFIG_MAIL]
                namelabel=swing.JLabel("Name: "+JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_NAME))
                maillabel=swing.JLabel("Media Files Attached: ")
                gtlabel=swing.JLabel("Student ID#: "+JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_GT))
                blanklabel=swing.JLabel("")

                #Layout the components
                turninProperties = swing.JPanel()
                turninProperties.size = (150,50)
                turninProperties.layout = awt.GridLayout(4, 2)
                turninProperties.add(namelabel)
                turninProperties.add(gtlabel)
                turninProperties.add(toSubmitLabel)
                turninProperties.add(fileNameLabel)
                turninProperties.add(titlelabel)
                turninProperties.add(self.titlefield)
                turninProperties.add(blanklabel)
                self.turninWindow.contentPane.add(turninProperties, awt.BorderLayout.NORTH)

                attachPane = swing.JPanel()
                attachPane.layout = awt.BorderLayout()
                attachPane.add(maillabel, awt.BorderLayout.NORTH)
                attachPane.add(self.listPane, awt.BorderLayout.CENTER)
                buttonPane = swing.JPanel()
                buttonPane.layout = awt.GridLayout(1,2)
                buttonPane.add(removebutton)
                buttonPane.add(addbutton)
                attachPane.add(buttonPane, awt.BorderLayout.SOUTH)
                self.turninWindow.contentPane.add(attachPane, awt.BorderLayout.CENTER)

                notesPane = swing.JPanel()
                notesPane.layout = awt.BorderLayout()
                notesPane.add(notesLabel, awt.BorderLayout.NORTH)
                notesPane.add(self.notesScrollPane, awt.BorderLayout.CENTER)
                sendPane = swing.JPanel()
                sendPane.layout = awt.GridLayout(1,2)
                sendPane.add(cancelbutton)
                sendPane.add(turninbutton)
                notesPane.add(sendPane, awt.BorderLayout.SOUTH)
                notesPane.size = (200, 300)
                self.turninWindow.contentPane.add(notesPane, awt.BorderLayout.SOUTH)

                #self.turninWindow.contentPane.add(toSubmitLabel)
                #self.turninWindow.contentPane.add(fileNameLabel)
                #self.turninWindow.contentPane.add(titlelabel)
                #self.turninWindow.contentPane.add(self.titlefield)
                #self.turninWindow.contentPane.add(namelabel)
                #self.turninWindow.contentPane.add(gtlabel)
                #self.turninWindow.contentPane.add(maillabel)
                #self.turninWindow.contentPane.add(self.listPane)
                #self.turninWindow.contentPane.add(removebutton)
                #self.turninWindow.contentPane.add(addbutton)
                #self.turninWindow.contentPane.add(notesLabel)
                #self.turninWindow.contentPane.add(self.notesScrollPane)
                #self.turninWindow.contentPane.add(cancelbutton)
                #self.turninWindow.contentPane.add(turninbutton)
                self.turninWindow.pack()
		self.turninWindow.setLocationRelativeTo(None)
                self.turninWindow.show()
            except:
                a="JES needs to know who you are to turn in something.  \n"
                b="Please choose Register from the Turnin menu to set JES's\n preferences.  "
                c="When you are done you can try to turn this \nassignment in again."
                self.errorWindow=swing.JFrame()
                swing.JOptionPane.showMessageDialog(self.errorWindow,
                      a+b+c,
                    "Error - JES properties have not been set",
                    swing.JOptionPane.WARNING_MESSAGE)

    ################################################################################
    # Function name: turninButtonPressed
    # Description:
    #     Handles events from turnin dialog
    ################################################################################
    def turninButtonPressed(self,event):
        if event.source.text=='Turnin':
            try:
                isSaved=1
#                array=self.program.readFromConfigFile()

                title= self.titlefield.getSelectedItem()
                if self.editor.modified:
                #modified for promptSave cancel button - Buck Scharfnorth 29 May 2008
                    isSaved=self.promptSave(PROMPT_TURNIN_MESSAGE)
                if not os.path.isfile(self.program.filename):
                    isSaved=0
                #modified for promptSave cancel button - Buck Scharfnorth 29 May 2008
                if isSaved > 0:
                    if JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_GT) == '':
                        self.turninWindow.dispose()
                        self.errorWindow=swing.JFrame()
                        swing.JOptionPane.showMessageDialog(self,
                                                            'You must have a student your student number.',
                                                            'Turnin cannot complete.',
                                                            swing.JOptionPane.WARNING_MESSAGE)
                        self.openSettings()
                    elif JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_EMAIL_ADDR) == '':
                        self.turninWindow.dispose()
                        self.errorWindow=swing.JFrame()
                        swing.JOptionPane.showMessageDialog(self,
                                                            'You must enter an e-mail address.',
                                                            'Turnin cannot complete.',
                                                            swing.JOptionPane.WARNING_MESSAGE)
                        self.openSettings()
                    elif JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_NAME) == '':
                        self.turninWindow.dispose()
                        self.errorWindow=swing.JFrame()
                        swing.JOptionPane.showMessageDialog(self,
                                                 'You must enter a name.',
                                                 'Turnin cannot complete.',
                                                 swing.JOptionPane.WARNING_MESSAGE)
                        self.openSettings()
                    else:
                        if title !='Assignments':
                            filename=self.program.filename
#                            gt=array[JESConstants.CONFIG_GT]
                            zip=self.buildFileArchive(gt,title,filename)
                            j = JESHomeworkSubmission.JESHomeworkSubmission(title,filename,zip)
                            thread = JESHomeworkTurninThread.JESHomeworkTurninThread(j,self,zip)
                            self.turninstatuswindow=swing.JFrame("Turnin Status")
                            self.turninstatuswindow.contentPane.layout=awt.GridLayout(1,2)
                            self.turninstatuswindow.contentPane.add(swing.JLabel(swing.ImageIcon("images/Thinking.gif")))
                            self.turninstatuswindow.contentPane.add(self.turninstatuslabel)
                            self.turninstatuswindow.setSize(400,150)
                            self.turninstatuswindow.show()
                            thread.start()
                            self.turninWindow.dispose()
                        else:
                            self.turninWindow.dispose()
                            self.errorWindow=swing.JFrame()
                            swing.JOptionPane.showMessageDialog(self,
                                                                'You must select an assignment from the list to submit.',
                                                                'Turnin cannot complete.',
                                                                swing.JOptionPane.WARNING_MESSAGE)
                #modified for promptSave cancel button - Buck Scharfnorth 29 May 2008
                elif isSaved==0:
                    self.turninWindow.dispose()
                    self.errorWindow=swing.JFrame()
                    swing.JOptionPane.showMessageDialog(self,
                                  'There is no file open to submit, or the current file has not been saved.',
                                  'Turnin cannot complete.',
                                  swing.JOptionPane.WARNING_MESSAGE)
                #modified for promptSave cancel button - Buck Scharfnorth 29 May 2008
                else:
                    self.turninWindow.dispose()

            except Exception, string:
                self.turninWindow.dispose()
                a="An error has occurred in the turnin process. "
                b="It is likely\nthat the program turnin has failed.  Please "
                c="check JES's settings and\nresubmit the assignment."
                try:
                    d="\n   Error:  " + str(string)
                except:
                    d=""
                self.errorWindow=swing.JFrame()
                swing.JOptionPane.showMessageDialog(self,
                                                a+b+c+d,
                                                "Error - Turnin has failed",
                                                swing.JOptionPane.WARNING_MESSAGE)
        elif event.source.text == "Add File":
            chooser = swing.JFileChooser()
            chooser.setApproveButtonText("Attach File")
            returnVal = chooser.showOpenDialog(self.turninWindow)
            if returnVal ==  0: #User has chosen a file, so now it can be opened
                self.attachmentlist.add(chooser.getSelectedFile().getPath())
                self.list.setListData(self.attachmentlist)
        elif event.source.text == "Remove File":
             self.attachmentlist.remove(self.list.getSelectedValue())
             self.list.setListData(self.attachmentlist)

        else:
            self.turninWindow.dispose()


########################################################################
# Method: buildFileArchive
# Parameters:
#     -gt: The GT number of the student
#     -title: The title of the homework
#     -The working file to zip up.  Is actually the contents of the Editor
# Description:
#     Constructs a zip file of all the submission materials for a CS1315
#     assigment.  The file title will be of the form: gtXXXX-<ASSGN
#     Title>.zip.  Will also include any added files and notes from the
#     turnin dialog.
########################################################################
    def buildFileArchive(self,gt,title,fileToSend):
        import zipfile
        import user
        filenames=self.attachmentlist
        writename = gt+'-'+title+'.zip'
        writename=writename.strip()
        writename=string.replace(writename," ","_")
        if System.getProperty('os.name').find('Mac') <> -1:  # if we are on a Mac
            writename = user.home + os.sep + writename
        #open the zipfile for writing
        file = zipfile.ZipFile(writename, "w")
        for name in filenames:
            if name.strip() != fileToSend.strip():
               file.write(name,os.path.basename(name),zipfile.ZIP_DEFLATED)
        file.write(fileToSend,os.path.basename(fileToSend),zipfile.ZIP_DEFLATED)
        if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_LOGBUFFER):
            file.write(fileToSend+'log',os.path.basename(fileToSend+'log'),zipfile.ZIP_DEFLATED)
        #Create and add a text file with the notes to the TA:
        notesTA = open(".notesTA.txt", "w")
        notesTA.write(self.notesToTA.getText())
        notesTA.close()
        file.write(".notesTA.txt", "notesTA.txt", zipfile.ZIP_DEFLATED)
        file.close()
        return writename



########################################################################
    def grabAssignmentList(self):
        try:
            ret=['Assignments']
            url = net.URL(JESConstants.ASSIGNMENT_URL)
            h = httplib.HTTP(url.getHost())
            h.putrequest('GET', url.getFile())
            h.putheader('Accept', 'text/html')
            h.putheader('Accept', 'text/plain')
            h.endheaders()
            errcode, errmsg, headers = h.getreply()
            f = h.getfile()
            data = f.read() # Get the raw HTML
            f.close()
            #Remove #BEGIN and #END from file
            tempArr=string.split(data,'#BEGIN')
            data=tempArr[1]
            tempArr=string.split(data,'#END')
            data=tempArr[0]
            data=data.split("|")
            for x in data:
                arr=x.strip()
                ret.append(arr)
            return ret
        except:
            print "Error reading assignment list from network"
            return ['Assignments']

    ################################################################################
    # Function name: openOptions
    # Description:
    #     Opens up the options frame
    ################################################################################
    def openOptions(self):
        self.optionsWindow=swing.JFrame('JES Options')
	
        self.optionsWindow.contentPane.layout = awt.GridLayout(11,2)
        #self.optionsWindow.size = (350,550)

        donebutton = swing.JButton("Done",preferredSize=(100,20),
                    actionPerformed=self.optionsButtonPressed)
        cancelbutton= swing.JButton("Cancel",preferredSize=(100,20),
                    actionPerformed=self.optionsButtonPressed)

        modelabel=swing.JLabel("Mode:")
        fontlabel=swing.JLabel("Font Size (1-"+str(JESConstants.HIGH_FONT)+"):")
        gutterlabel=swing.JLabel("Line Numbers:")
        blocklabel=swing.JLabel("Show Indentation Help:")
        logginglabel=swing.JLabel("Logging:")
        autosavelabel=swing.JLabel("Auto save on load:")
        backupsavelabel=swing.JLabel("Save a backup copy on save:")
        wrappixellabel=swing.JLabel("<html>Modulo pixel color values by 256<br><center>(356 mod 256 = 100)</center></html>")
        skinlabel = swing.JLabel("Skin:")
        showturninlabel = swing.JLabel("Show Turnin Menu")

        self.autosaveBox = swing.JCheckBox( "", JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_AUTOSAVEONRUN) )
        self.backupSaveBox = swing.JCheckBox( "", JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BACKUPSAVE) )
        self.wrappixelBox = swing.JCheckBox( "", JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_WRAPPIXELVALUES) )
        self.gutterBox = swing.JCheckBox( "", JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_GUTTER) )
        self.showTurninBox = swing.JCheckBox( "", JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_SHOWTURNIN) )
        ## alexr flopped the sense of this checkbox
        self.blockBox = swing.JCheckBox( "", not JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BLOCK) )
        self.loggerBox = swing.JCheckBox( "", JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_LOGBUFFER) )

        if JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MODE) ==  JESConstants.BEGINNER_MODE:
            self.userExperienceField = swing.JComboBox( JESConstants.USER_MODES)
        else:
            self.userExperienceField = swing.JComboBox( JESConstants.USER_MODES_2)

#        if int(self.program.userFont) ==  int(JESConstants.LOW_FONT):
#            self.userFontField = swing.JComboBox( JESConstants.FONT_MODE_LOW)
#        elif int(self.program.userFont) ==  int(JESConstants.MID_FONT):
#            self.userFontField = swing.JComboBox( JESConstants.FONT_MODE_MID)
#        else:
#            self.userFontField = swing.JComboBox( JESConstants.FONT_MODE_HIGH)
        fontSizes = range(JESConstants.LOW_FONT, JESConstants.MID_FONT + 1, 2)
        userFont = int(JESConfig.getInstance().getIntegerProperty(JESConfig.CONFIG_FONT))
        self.userFontField = swing.JComboBox( fontSizes )
        self.userFontField.setEditable(1)
        if userFont in fontSizes:
            self.userFontField.setSelectedItem( userFont )
        else:
            self.userFontField.insertItemAt( userFont, 0 )
            self.userFontField.setSelectedItem( userFont )
        
        self.skinField = swing.JComboBox( listskins(), actionListener=skinActionListener(self) )

        cur = currentskin()
        for i in range(self.skinField.getItemCount()):
            item = self.skinField.getItemAt(i)

            # there's a reason for the "startswith". On the Mac, "Mac OS X"
            # and "Mac OS X Aqua" look the same but have different names!
            if( str(item).startswith(cur) or cur.startswith(str(item))):
                self.skinField.setSelectedItem( item)

        self.optionsWindow.contentPane.add(modelabel)
        self.optionsWindow.contentPane.add(self.userExperienceField)
        self.optionsWindow.contentPane.add(fontlabel)
        self.optionsWindow.contentPane.add(self.userFontField)
        self.optionsWindow.contentPane.add(gutterlabel)
        self.optionsWindow.contentPane.add(self.gutterBox)
        self.optionsWindow.contentPane.add(blocklabel)
        self.optionsWindow.contentPane.add(self.blockBox)

        self.optionsWindow.contentPane.add(showturninlabel)
        self.optionsWindow.contentPane.add(self.showTurninBox)

        self.optionsWindow.contentPane.add(logginglabel)
        self.optionsWindow.contentPane.add(self.loggerBox)

        self.optionsWindow.contentPane.add(autosavelabel)
        self.optionsWindow.contentPane.add(self.autosaveBox)

        self.optionsWindow.contentPane.add(backupsavelabel)
        self.optionsWindow.contentPane.add(self.backupSaveBox)
        # self.optionsWindow.contentPane.add(self.autoopenBox)

        self.optionsWindow.contentPane.add(wrappixellabel)
        self.optionsWindow.contentPane.add(self.wrappixelBox)

        self.optionsWindow.contentPane.add(skinlabel)
        self.optionsWindow.contentPane.add(self.skinField)

        self.optionsWindow.contentPane.add(cancelbutton)
        self.optionsWindow.contentPane.add(donebutton)

        #self.optionsWindow.size = (400,400)
        self.optionsWindow.pack()
        self.optionsWindow.setLocationRelativeTo(None)

        self.optionsWindow.show()

    def optionsButtonPressed(self,event):
        if event.source.text=='Done':
            JESConfig.getInstance().setStringProperty( JESConfig.CONFIG_MODE, self.userExperienceField.getSelectedItem() )

            chosenFontSize = self.userFontField.getSelectedItem()
            if ( not str(chosenFontSize).isdigit() or chosenFontSize < 1 or chosenFontSize > JESConstants.HIGH_FONT ):
                chosenFontSize = JESConfig.getInstance().getIntegerProperty(JESConfig.CONFIG_FONT);
		swing.JOptionPane.showMessageDialog(self, "Invalid Font Size.  Please try again using a number between 1 and " + str(JESConstants.HIGH_FONT), "Invalid Font Size", swing.JOptionPane.ERROR_MESSAGE)
                
            JESConfig.getInstance().setIntegerProperty( JESConfig.CONFIG_FONT, chosenFontSize )
            JESConfig.getInstance().setBooleanProperty( JESConfig.CONFIG_BLOCK, not self.blockBox.isSelected() )
            JESConfig.getInstance().setBooleanProperty( JESConfig.CONFIG_GUTTER, self.gutterBox.isSelected() )
            JESConfig.getInstance().setBooleanProperty( JESConfig.CONFIG_LOGBUFFER, self.loggerBox.isSelected() )
            JESConfig.getInstance().setBooleanProperty( JESConfig.CONFIG_AUTOSAVEONRUN, self.autosaveBox.isSelected() )
            JESConfig.getInstance().setBooleanProperty( JESConfig.CONFIG_BACKUPSAVE, self.backupSaveBox.isSelected() )
            JESConfig.getInstance().setBooleanProperty( JESConfig.CONFIG_WRAPPIXELVALUES, self.wrappixelBox.isSelected() )
            JESConfig.getInstance().setBooleanProperty( JESConfig.CONFIG_WRAPPIXELVALUES, self.wrappixelBox.isSelected() )
            JESConfig.getInstance().setSessionWrapAround( self.wrappixelBox.isSelected() )
            if( JESConfig.getInstance().getBooleanProperty( JESConfig.CONFIG_SHOWTURNIN ) != self.showTurninBox.isSelected() ):
                JESConfig.getInstance().setBooleanProperty( JESConfig.CONFIG_SHOWTURNIN, self.showTurninBox.isSelected() )
                self.addmenu()
                self.pack()
                ## self.update(self.getGraphics())

            JESConfig.getInstance().writeConfig()

            self.optionsWindow.dispose()
            # change fonts on the fly.
            editorDocument = self.editor.getDocument()
            editorDocument.changeFontSize(chosenFontSize)
            commandDocument = self.commandWindow.getDocument()
            commandDocument.changeFontSize(chosenFontSize)

            if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BLOCK):
                self.editor.removeBox()
            else:
                self.editor.addBox()

            if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_GUTTER):
                self.turnOnGutter()
            else:
                self.turnOffGutter()

        else:
            self.optionsWindow.dispose()

######################################################################
# Function name: turnOffGutter
# Description:
#     Turns the gutter off, removes it from the scrollpane
######################################################################
    def turnOffGutter(self):
        self.docpane.remove(self.gutter)
        self.docpane.repaint()

######################################################################
# Function name: turnOnGutter
# Description:
#     Turns the gutter on, adds it to the scrollpane
######################################################################
    def turnOnGutter(self):
        self.docpane.remove(self.gutter)
        self.docpane.remove(self.editor)
        self.docpane.add(self.gutter)
        self.docpane.add(self.editor)
        self.docpane.repaint()

    def getGoToLineNum(self):
        self.gotoFrame=swing.JFrame("Goto Line Number")
        self.gotoFrame.contentPane.layout = awt.GridLayout(2,2)
        self.gotoFrame.size=(200,75)
        gotobutton = swing.JButton("Goto",preferredSize=(100,20),
                    actionPerformed=self.gotoButtonPressed)
        cancelbutton= swing.JButton("Cancel",preferredSize=(100,20),
                    actionPerformed=self.gotoButtonPressed)
        linelabel=swing.JLabel("Line #:")
        self.gotoFrame.contentPane.add(linelabel)
        self.gotoFrame.contentPane.add(self.linefield)
        self.gotoFrame.contentPane.add(cancelbutton)
        self.gotoFrame.contentPane.add(gotobutton)
        self.gotoFrame.show()

    def gotoButtonPressed(self,event):
        if event.source.text=='Goto':
            try:
                a=int(self.linefield.text)
                self.editor.document.gotoLine(a)
                self.linefield.text=''
                self.gotoFrame.dispose()
            except:
                self.linefield.text=''
                self.gotoFrame.dispose()
        else:
            self.linefield.text=''
            self.gotoFrame.dispose()

    def search(self):
        if self.searchFrame == None:
            self.searchFrame=swing.JFrame("Search for Text")
            self.searchFrame.contentPane.layout = awt.GridLayout(3,2)
            self.searchFrame.size=(200,100)
            findbutton = swing.JButton("Find",preferredSize=(100,20),
                    actionPerformed=self.searchButtonPressed)
            donebutton= swing.JButton("Cancel",preferredSize=(100,20),
                    actionPerformed=self.searchButtonPressed)
            group = swing.ButtonGroup()
            group.add(self.up)
            group.add(self.down)
            buttonpanel = swing.JPanel()
            buttonpanel.layout = awt.GridLayout(0,1)
            buttonpanel.add(self.up)
            buttonpanel.add(self.down)
            searchlabel=swing.JLabel("Text to Find:")
            self.searchFrame.contentPane.add(searchlabel)
            self.searchFrame.contentPane.add(self.searchfield)
            self.searchFrame.contentPane.add(buttonpanel)
            self.searchFrame.contentPane.add(swing.JLabel())
            self.searchFrame.contentPane.add(donebutton)
            self.searchFrame.contentPane.add(findbutton)
            self.searchFrame.show()
        else:
            self.searchFrame.show()

    def searchButtonPressed(self,event):
        if event.source.text=='Find':
            try:
                toFind=self.searchfield.text
                if self.up.isSelected():
                    self.editor.document.searchBackward(toFind)
                else:
                    self.editor.document.searchForward(toFind)
            except:
                self.searchfield.text=''
                self.searchFrame.hide()
        else:
            self.searchfield.text=''
            self.searchFrame.hide()

    def errorWindowClose(self,event):
        self.errorWindow.dispose()

    def startWork(self):
        self.runningBar.indeterminate = 1

    def stopWork(self):
        self.runningBar.indeterminate = 0

    def addBreakPoint(self):
        lineno = self.editor.getLineNo()
        self.program.interpreter.debugger.set_break(self.program.filename, lineno)
        # should contact the gutter here

    def watchVariable(self):
        var = JESDBVariableWatcher.variableDialog(self)
        if var:
            self.program.interpreter.debugger.addVariable(var)

    def unwatchVariable(self):
        var = JESDBVariableWatcher.pickVariable(self,
                                                self.program.interpreter.debugger.watcher.getVariables())
        if var:
            self.program.interpreter.debugger.removeVariable(var)

######################################################################
# Function name: editorChanged()
# Description:
#     Called whenever the editor document is changed, so the UI can
#     update accordingly.  Right now, only used for coloring the
#     LOAD button
######################################################################
    def editorChanged(self):
        self.loadDifferent()

    def refreshDebugState(self):
        enabled = self.program.interpreter.debug_mode# and self.program.editorLoaded()
        #print self.program.interpreter.debug_mode , self.program.editorLoaded()
        self.debugMenu.subElements[0].subElements[0].setSelected(enabled)
        self.debugMenu.subElements[0].subElements[1].setEnabled(enabled)
        self.debugMenu.subElements[0].subElements[2].setEnabled(enabled)
        self.program.interpreter.debugger.watcher.setVisible(enabled)
        if not enabled:
            self.debuggerButton.text = SHOW_DEBUGGER_CAPTION
            self.debugMenu.subElements[0].subElements[0].text = DEBUG_SHOW_DEBUGGER
            #line added to add a close button to debugger - 29 May 2008 by Buck Scharfnorth
            self.windowSetting(COMMAND_WINDOW_2)
        else:
            self.windowSetting(COMMAND_WINDOW_3DEBUG)
            self.debuggerButton.text = HIDE_DEBUGGER_CAPTION
            self.debugMenu.subElements[0].subElements[0].text = DEBUG_HIDE_DEBUGGER



######################################################################
# Function name: loadSoundTool()
# Description:
#     Examines the namespace for all instances of sound, and presents
#     a list for the user to pick from.  The chosen sound is then opened
#     in the sound tool.
######################################################################
    def loadSoundTool(self):
        #l = globals()
        l = self.program.interpreter.contextForExecution
        sounds = []
        soundsdict = {}
        for i in l.items():
            try:
                if i[1].__class__.__name__ == 'Sound':
                    sounds.append(i[0])
                    soundsdict.setdefault(i[0], i[1])
            except Exception, e:
                pass
        if len(sounds) > 0:
            sound = swing.JOptionPane.showInputDialog(self, "Choose a sound to examine:",
                                                      "Open Sound Tool",
                                                      swing.JOptionPane.INFORMATION_MESSAGE,
                                                      None,
                                                      sounds,
                                                      sounds[0])
            if sound != None:
                media.openSoundTool(soundsdict[sound])
        else:
            swing.JOptionPane.showMessageDialog(self, "There are no sounds to examine.",
                                                "No sounds",
                                                swing.JOptionPane.ERROR_MESSAGE)

######################################################################
# Function name: loadPictureTool()
# Description:
#     Examines the namespace for all instances of picture, and presents
#     a list for the user to pick from.  The chosen picture is then opened
#     in the picture tool.
######################################################################
    def loadPictureTool(self):
        #l = globals()
        l = self.program.interpreter.contextForExecution
        pictures = []
        picturesdict = {}
        for i in l.items():
            try:
                if i[1].__class__.__name__ == 'Picture':
                    pictures.append(i[0])
                    picturesdict.setdefault(i[0], i[1])
            except Exception, e:
                pass
        if len(pictures) > 0:
            picture = swing.JOptionPane.showInputDialog(self, "Choose a picture to examine:",
                                                      "Open Picture Tool",
                                                      swing.JOptionPane.INFORMATION_MESSAGE,
                                                      None,
                                                      pictures,
                                                      pictures[0])
            if picture != None:
                media.openPictureTool(picturesdict[picture])
        else:
            swing.JOptionPane.showMessageDialog(self, "There are no pictures to examine.",
                                                "No pictures",
                                                swing.JOptionPane.ERROR_MESSAGE)


######################################################################
# Function name: loadFrameSequencerTool()
# Description:
#     Examines the namespace for all instances of picture, and presents
#     a list for the user to pick from.  The chosen picture is then opened
#     in the picture tool.
######################################################################
    def loadFrameSequencerTool(self):
#        media.showInformation('You will be asked to pick a folder. Temporary files will be stored here')
#        media.openFrameSequencerTool(media.pickAFolder())
        #l = globals()
        l = self.program.interpreter.contextForExecution
        sounds = []
        soundsdict = {}
        for i in l.items():
            try:
                if i[1].__class__.__name__ == 'Movie':
                    sounds.append(i[0])
                    soundsdict.setdefault(i[0], i[1])
            except Exception, e:
                pass
        if len(sounds) > 0:
            sound = swing.JOptionPane.showInputDialog(self, "Choose a Movie to examine:",
                                                      "Open Movie Tool",
                                                      swing.JOptionPane.INFORMATION_MESSAGE,
                                                      None,
                                                      sounds,
                                                      sounds[0])
            if sound != None:
                media.openFrameSequencerTool(soundsdict[sound])
        else:
            swing.JOptionPane.showMessageDialog(self, "There are no movies to examine.",
                                                "No movies",
                                                swing.JOptionPane.ERROR_MESSAGE)


## little utility bits added for making skin changing easier.

# this tells us about all the available Swing look 'n' feels
def listskins():
    return [ str(skin.getName()) for skin in UIManager.getInstalledLookAndFeels()]

def currentskin():
    return str(UIManager.getLookAndFeel().getName())

class skinActionListener(awt.event.ActionListener):
    def __init__(self, ui):
        self.ui = ui

    def actionPerformed(self, e):
        self.ui.changeSkin(e)

####################################################################
####################################################################
# Class: hideRight
# Parameters:
#     -actionPerformed: The actionPerformed for the button.
# Description:
#     Creates a JPanel containing a right-aligned close button.
#     Lets the user close the right panel (Help and Debugger).
####################################################################
class hideRight(swing.JPanel):
    #Create and set up button panel for hiding the right content pane (help/debugger)
    def __init__(self, actionPerformed):
        swing.JPanel.__init__(self)
        hideRight = swing.JButton(swing.plaf.metal.MetalIconFactory.getInternalFrameCloseIcon(16))
        hideRight.setBorderPainted(0)
        hideRight.setContentAreaFilled(0)
        hideRight.setAlignmentX(swing.JButton.RIGHT_ALIGNMENT)
        hideRight.setHorizontalAlignment(swing.SwingConstants.RIGHT)
        hideRight.setActionCommand(COMMAND_WINDOW_2)
        hideRight.actionPerformed = actionPerformed
        self.setLayout(awt.FlowLayout(awt.FlowLayout.TRAILING, 1, 1))
        self.add(hideRight)

####################################################################
####################################################################
# Class: Html_Browser_With_Hide
# Parameters:
#     -htmlBrowser: The htmlBrowser used by this panel.
# Description:
#     Creates a subclass of a JPanel in order to use arbitrary property
#     htmlBrowser (the instance of Html_Browser which is doing the actual work).
####################################################################
class Html_Browser_With_Hide(swing.JPanel):
    def __init__(self, htmlBrowser):
        swing.JPanel.__init__(self)
        self.htmlBrowser = htmlBrowser
