# -*- coding: utf-8 -*-
"""
jes.gui.helpinfo
================
This has the list of stuff that the GUI's job is to provide help on.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from javax.swing import JMenu, JMenuItem

### Help with JES functions

JES_API_SECTIONS = [
    ('Colors', ['distance', 'makeColor', 'makeDarker', 'makeLighter',
                'pickAColor', 'getColorWrapAround', 'setColorWrapAround']),
    ('Files', ['pickAFile', 'pickAFolder', 'setMediaPath', 'setMediaFolder',
               'getMediaPath', 'getMediaFolder', 'getShortPath', 'setLibPath']),
    ('Input/Output', ['requestNumber', 'requestInteger', 'requestIntegerInRange', 'requestString',
                      'showWarning', 'showInformation', 'showError', 'printNow']),
    ('Turtles', ['turn', 'turnLeft', 'turnRight', 'forward', 'backward', 'moveTo', 'turnToFace',
                 'makeTurtle', 'penUp', 'penDown', 'makeWorld',
                 'getTurtleList', 'drop', 'getHeading', 'getXPos', 'getYPos']),
    ('Movies', ['playMovie', 'makeMovie', 'makeMovieFromInitialFile',
                'writeFramesToDirectory', 'addFrameToMovie', 'writeQuicktime', 'writeAVI',
                'openFrameSequencerTool', 'explore']),
    ('Pixels', ['getColor', 'setColor', 'getRed', 'getGreen', 'getBlue',
                'setRed', 'setGreen', 'setBlue', 'getX', 'getY']),
    ('Pictures', ['addArc', 'addArcFilled', 'addLine', 'addOval', 'addOvalFilled', 'addRect',
                  'addRectFilled', 'addText', 'addTextWithStyle', 'copyInto', 'duplicatePicture', 'getHeight', 'getWidth',
                  'getPixel', 'getPixels', 'getPixelAt', 'makePicture', 'makeEmptyPicture', 'makeStyle', 'show', 'repaint',
                  'writePictureTo', 'openPictureTool', 'setAllPixelsToAColor', 'explore']),
    ('Sound', ['blockingPlay', 'duplicateSound', 'getDuration', 'getLength', 'getNumSamples', 'getSampleObjectAt', 'getSamples', 'getSampleValue', 'getSampleValueAt',
               'getSamplingRate', 'getSound', 'makeEmptySound', 'makeEmptySoundBySeconds', 'makeSound', 'play', 'playNote',
               #           'playInRange', 'blockingPlayInRange', 'playAtRateInRange', 'blockingPlayAtRateInRange',
               'setSampleValue', 'setSampleValueAt', 'stopPlaying', 'writeSoundTo', 'openSoundTool', 'explore'])]


def buildJESFunctionsMenu(action):
    menuSections = []
    for (section, api_functions) in JES_API_SECTIONS:
        newMenuSection = JMenu(str(section), actionPerformed=action)

        for api_function in api_functions:
            newMenuItem = JMenuItem(api_function, actionPerformed=action)
            newMenuSection.add(newMenuItem)
        menuSections.append(newMenuSection)
    return menuSections


### Help with Java classes

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
import Turtle
import World

# make sure all these are imported

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
                Turtle,
                World]


def getMethodList(klass):
    ret = []
    for (name, val) in klass.__dict__.items():
        if type(val).__name__.endswith('Function'):
            ret.append(name)
    return ret


def buildJavaAPIMenu(action):
    menuSections = []
    for section in API_SECTIONS:
        newMenuSection = JMenu(str(section), actionPerformed=action)

        for api_function in getMethodList(section):
            func_name = str(section) + '.' + api_function
            newMenuItem = JMenuItem(func_name, actionPerformed=action)
            newMenuSection.add(newMenuItem)
        menuSections.append(newMenuSection)
    return menuSections

