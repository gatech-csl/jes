# -*- coding: utf-8 -*-
"""
jes.gui.components.actions
==========================
Utilities for creating and working with Swing actions.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from java.awt.event import KeyEvent, InputEvent
from java.lang import System
from javax.swing import Action, AbstractAction, KeyStroke

ACTION_VALUES = {
    'accelerator':      Action.ACCELERATOR_KEY,
    'actionCommand':    Action.ACTION_COMMAND_KEY,
    'longDescription':  Action.LONG_DESCRIPTION,
    'mnemonicKey':      Action.MNEMONIC_KEY,
    'name':             Action.NAME,
    'shortDescription': Action.SHORT_DESCRIPTION,
    'smallIcon':        Action.SMALL_ICON
}


if System.getProperty('os.name').startswith("Mac "):  # if we are on a Mac
    CONTROL_MASK = InputEvent.META_MASK
else:
    CONTROL_MASK = InputEvent.CTRL_MASK


def keyCode(key):
    code = getattr(KeyEvent, 'VK_' + key.upper())
    if code is None:
        raise ValueError("Invalid VK event")
    return code


def keyStroke(key):
    return KeyStroke.getKeyStroke(keyCode(key), 0)


def control(key):
    return KeyStroke.getKeyStroke(keyCode(key), CONTROL_MASK)


def controlShift(key):
    return KeyStroke.getKeyStroke(keyCode(key), CONTROL_MASK + InputEvent.SHIFT_MASK)


class PythonAction(AbstractAction):
    """
    This is a Swing action that invokes a Python callable when the action
    is performed. You can set a variety of Swing-related options as keyword
    arguments.
    """
    def __init__(self, callback, *args, **kwargs):
        self._callback = callback

        if args:
            if 'args' in kwargs:
                raise ValueError("Can't specify args two ways")
            self._args = args
        else:
            self._args = kwargs.pop('args', ())

        self._kwargs = kwargs.pop('kwargs', {})
        self._takesEvent = kwargs.pop('takesEvent', False)

        self.setEnabled(True)
        self.setProperties(kwargs)

    def actionPerformed(self, event):
        args = (event,) + self._args if self._takesEvent else self._args
        # Intentionally ignore return value
        self._callback(*args, **self._kwargs)

    def getProperty(self, name):
        if name == 'enabled':
            return self.isEnabled()
        elif name in ACTION_VALUES:
            return self.getValue(ACTION_VALUES[name])
        else:
            raise AttributeError("%r is not a property of Actions" % name)

    def setProperty(self, name, value):
        if name == 'enabled':
            self.setEnabled(value)
        elif name in ACTION_VALUES:
            self.putValue(ACTION_VALUES[name], value)
        else:
            raise AttributeError("%r is not a property of Actions" % name)

    def setProperties(self, values):
        for name, value in values.items():
            self.setProperty(name, value)

    def __getattr__(self, name):
        return self.getProperty(name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super(PythonAction, self).__setattr__(name, value)
        else:
            self.setProperty(name, value)


class DecoratedPythonAction(PythonAction):
    """
    A PythonAction that can also act as the function that it wraps.
    It passes along the __name__ and __doc__ attributes, and allows
    the function to be invoked directly using __call__.
    """
    def __init__(self, callback, *args, **kwargs):
        super(DecoratedPythonAction, self).__init__(callback, *args, **kwargs)
        self.__name__ = callback.__name__
        self.__doc__ = callback.__doc__

    def __call__(self, *args, **kwargs):
        return self._callback(*args, **kwargs)


class MethodAction(object):
    """
    A descriptor that creates a DecoratedPythonAction when the method's
    property is accessed. This means that a method can also become an action.
    """
    def __init__(self, fn, properties):
        self.fn = fn
        self.name = fn.__name__
        self.properties = properties

    def __get__(self, instance, owner):
        if instance is None:
            if hasattr(self.fn, '__get__'):
                return self.fn.__get__(instance, owner)
            else:
                return self.fn
        else:
            if hasattr(self.fn, '__get__'):
                bound = self.fn.__get__(instance, owner)
            else:
                bound = self.fn
            action = DecoratedPythonAction(bound, **self.properties)
            setattr(instance, self.name, action)
            return action


def methodAction(fn=None, **properties):
    """
    Decorate a method with this, and it will become a MethodAction.
    You can use it as

        @methodAction
        def cut(self):
            ...

        @methodAction(takesEvent=True)
        def cut(self, event):
            ...

    This means instances' versions of these methods will automatically
    function as a Swing Action, and can have the 'enabled' etc. properties
    set on them directly.
    """
    if fn is not None:
        return MethodAction(fn, properties)
    else:
        return lambda f: MethodAction(f, properties)

