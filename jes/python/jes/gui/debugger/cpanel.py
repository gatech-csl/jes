# -*- coding: utf-8 -*-
"""
jes.gui.debugger.cpanel
=======================
This is the panel of buttons, sliders, and friends that
display on the top row of the debugger. They allow you to control the
debugger's speed, and stop it if you need to.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import JESResources
from java.awt import Insets
from java.util import Hashtable
from javax.swing import JPanel, BoxLayout, JSlider, JButton, JLabel
from jes.gui.components.threading import threadsafe

class DebugControlPanel(JPanel):
    BUTTON_SIZE = (50, 50)

    def __init__(self, interpreter, debugger, debugPanel):
        self.interpreter = interpreter
        self.debugger = debugger
        self.debugPanel = debugPanel

        # Build our slider!
        self.slider = JSlider(JSlider.HORIZONTAL,
            debugger.MIN_SPEED, debugger.MAX_SPEED, debugger.speed,
            stateChanged=self._sliderSpeedChanged
        )

        # Label the slider!
        self.sliderLabels = labels = Hashtable()
        labels.put(debugger.MIN_SPEED, JLabel("Slow"))
        labels.put(debugger.MAX_SPEED, JLabel("Fast"))
        self.slider.labelTable = labels
        self.slider.paintLabels = True

        # Build some buttons!
        self.buttonInsets = Insets(0, 0, 0, 0)
        self.watchButton = self.makeDebuggerButton(
            self.debugPanel.watchVariable, 'images/plus.jpg'
        )
        self.unwatchButton = self.makeDebuggerButton(
            self.debugPanel.unwatchVariable, 'images/minus.jpg'
        )
        self.fullspeedButton = self.makeDebuggerButton(
            self.debugPanel.fullSpeed, 'images/fullspeed.jpg'
        )
        self.stopButton = self.makeDebuggerButton(
            self.interpreter.stopAction, 'images/stop.jpg'
        )

        # Display them all!
        self.setLayout(BoxLayout(self, BoxLayout.X_AXIS))
        self.add(self.slider)
        self.add(self.watchButton)
        self.add(self.unwatchButton)
        self.add(self.fullspeedButton)
        self.add(self.stopButton)

        # Connect the slider to the debugger!
        self.debugger.onSpeedSet.connect(self._showSpeedSetting)
        self.debugger.onStart.connect(self._lockControls)
        self.debugger.onStop.connect(self._unlockControls)

    def makeDebuggerButton(self, action, icon):
        imageIcon = JESResources.makeIcon(icon)
        return JButton(action, text=None, icon=imageIcon, margin=self.buttonInsets)

    @threadsafe
    def _sliderSpeedChanged(self, event):
        # These two event listeners could hypothetically go into
        # mutual recursion. To keep them from doing so, neither of them
        # trigger the other event unless the value actually changed.
        # This ensures they stop recursing after a single round.
        value = self.slider.getValue()
        if self.debugger.speed != value:
            self.debugger.setSpeed(value)

    @threadsafe
    def _showSpeedSetting(self, debugger, newSpeed, **_):
        if self.slider.getValue() != newSpeed:
            self.slider.setValue(newSpeed)

    @threadsafe
    def _lockControls(self, debugger, **_):
        self.debugPanel.watchVariable.enabled = False
        self.debugPanel.unwatchVariable.enabled = False
        self.debugPanel.fullSpeed.enabled = True

    @threadsafe
    def _unlockControls(self, debugger, **_):
        self.debugPanel.watchVariable.enabled = True
        self.debugPanel.unwatchVariable.enabled = True
        self.debugPanel.fullSpeed.enabled = False

