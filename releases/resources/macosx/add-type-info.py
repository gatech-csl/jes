# -*- coding: utf-8 -*-
"""
add-type-info.py
================
This script takes the path to an info.plist file, and writes in the keys
necessary to associate JES with .py files on OS X.
"""
import plistlib
import sys

# Check that we were provided a plist.

if len(sys.argv) != 2:
    print >>sys.stderr, "Usage: add-type-info.py path/to/Info.plist"
    sys.exit(1)

# Read it.

filename = sys.argv[1]
contents = plistlib.readPlist(filename)

# Add in the type information.

pyType = {
    "CFBundleTypeName":         "Python Program",
    "CFBundleTypeRole":         "Editor",
    "LSHandlerRank":            "Alternate",
    "LSItemContentTypes":       ["public.python-script"],
    "CFBundleTypeExtensions":   ["py"],
    "CFBundleTypeMIMETypes":    ["application/x-python"]
}

contents.setdefault("CFBundleDocumentTypes", []).append(pyType)

# Write it back out.

plistlib.writePlist(contents, filename)

