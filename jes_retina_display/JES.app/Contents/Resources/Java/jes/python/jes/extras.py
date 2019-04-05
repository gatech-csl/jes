# -*- coding: utf-8 -*-
"""
jes.extras
==========
Fun stuff to use in JES programs, that isn't part of the core JES media.py
functions.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import sys
from java.lang import System

def callAndTime(function, *args, **kwargs):
    if not callable(function):
        print "callAndTime(function[, arguments...]): Input is not a function"

    name = getattr(function, '__name__', 'The function')
    def showElapsedTime(start, end):
        return "%d.%06d milliseconds" % divmod(end - start, 1000000)

    startTime = System.nanoTime()
    try:
        rv = function(*args, **kwargs)
    except:
        endTime = System.nanoTime()

        print >>sys.stderr, "%s ran for %s and crashed" % (
            name, showElapsedTime(startTime, endTime)
        )
        raise
    else:
        endTime = System.nanoTime()

        print >>sys.stderr, "%s ran in %s" % (
            name, showElapsedTime(startTime, endTime)
        )
        return rv

