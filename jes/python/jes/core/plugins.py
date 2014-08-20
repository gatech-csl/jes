# -*- coding: utf-8 -*-
"""
jes.core.plugins
================
This allows you to install plugins in JES.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import os
import os.path
from java.lang import System
from java.util import Scanner
from java.util.jar import JarFile
from shutil import copy
from weakref import WeakValueDictionary

class InvalidPluginError(Exception):
    pass


REQUIRED_ATTRIBUTES = ["JES-Plugin-Title", "JES-Plugin-Version"]


def javaNormpath(path):
    return os.path.normpath(os.path.join(System.getProperty("user.dir"), path))


def getClasspath():
    pathsep = System.getProperty("path.separator")
    path = System.getProperty("java.class.path")
    base = System.getProperty("user.dir")
    return [javaNormpath(e) for e in path.split(pathsep)]


def getPluginInfo(jarFilename):
    if not (os.path.isfile(jarFilename) and jarFilename.endswith(".jar")):
        raise InvalidPluginError("JES plugins must be .jar files.")

    jar = JarFile(jarFilename)
    manifest = jar.getManifest()
    if manifest is None:
        raise InvalidPluginError("JES plugins need to have a JAR manifest "
                                 "indicating that they are for JES.")

    attrs = manifest.mainAttributes
    for attr in REQUIRED_ATTRIBUTES:
        if attrs.getValue(attr) is None:
            raise InvalidPluginError("JES plugins need to define a %s "
                                     "in their JAR manifest." % attr)

    entry = jar.getEntry(".JESDescription.txt")
    if entry is None:
        raise InvalidPluginError("JES plugins need to include a description file.")

    inputStream = jar.getInputStream(entry)
    scanner = Scanner(inputStream).useDelimiter("\\A")
    description = scanner.next() if scanner.hasNext() else "(No description given.)"
    inputStream.close()

    info = {
        'filename':     jarFilename,
        'basename':     os.path.basename(jarFilename),
        'dirname':      os.path.dirname(jarFilename),
        'title':        attrs.getValue("JES-Plugin-Title"),
        'version':      attrs.getValue("JES-Plugin-Version"),
        'description':  description
    }

    info['display'] = "%s %s (%s)" % (info['title'], info['version'], info['basename'])
    info['longDescription'] = info['display'] + '\n' + description

    jar.close()
    return info


class PluginData(object):
    def __init__(self):
        self.pluginInfos = {}
        self.activePlugins = set()
        self.activePluginBasenames = set()
        self.classpath = getClasspath()

        for entry in self.classpath:
            if entry.endswith(".jar"):
                try:
                    info = self.getPluginInfo(entry)
                except InvalidPluginError:
                    continue
                else:
                    self.activePlugins.add(entry)
                    self.activePluginBasenames.add(info['basename'])

    def getPluginInfo(self, pathname):
        pathname = javaNormpath(pathname)
        if pathname in self.pluginInfos:
            return self.pluginInfos[pathname]

        info = getPluginInfo(pathname)

        info['isActive'] = info['filename'] in self.classpath
        info['status'] = 'active' if info['isActive'] else 'unknown'

        self.pluginInfos[pathname] = info
        return info

    def getMultiplePluginInfos(self, pathnames):
        return dict((name, self.getPluginInfo(name)) for name in pathnames)

    def getActivePluginInfo(self):
        return self.getMultiplePluginInfos(self.activePlugins)


class PluginInstaller(object):
    def __init__(self, data):
        self.data = data
        self.dir = System.getProperty("jes.plugindir")
        self.available = self.dir is not None
        self.toRemove = []

    def cleanUp(self):
        for jarInfo in self.toRemove:
            if jarInfo['dirname'] == self.dir:
                os.remove(jarInfo['filename'])

    def getAllPlugins(self):
        return self.data.activePlugins | self.getInstalledPlugins()

    def getInstalledPlugins(self):
        if self.dir is None or not os.path.isdir(self.dir):
            return set()

        plugins = set()
        for basename in os.listdir(self.dir):
            if not basename.endswith(".jar"):
                continue
            pathname = os.path.normpath(os.path.join(self.dir, basename))

            try:
                info = self.data.getPluginInfo(pathname)
            except InvalidPluginError:
                continue
            else:
                plugins.add(pathname)
        return plugins

    def getMultiplePluginInfos(self, names):
        plugins = self.data.getMultiplePluginInfos(names)
        for info in plugins.values():
            if os.path.dirname(info['filename']) == self.dir:
                info['isInstalled'] = True
                if info['isActive']:
                    info['status'] = 'installed'
                    info['note'] = ("(This plugin is installed in the user "
                                    "plugins directory.)")
                else:
                    info['status'] = 'to be installed'
                    info['note'] = ("(This plugin will be activated when you "
                                    "restart JES.)")
            else:
                info['isInstalled'] = False
                if info['isActive']:
                    info['status'] = 'built in'
                    info['note'] = ("(This plugin is installed with JES "
                                    "in the installation directory.)")
                else:
                    info['status'] = 'not installed'
                    info['note'] = "(This plugin is not installed yet.)"
        return plugins

    def getAllPluginInfo(self):
        return self.getMultiplePluginInfos(self.getAllPlugins())

    def getInstalledPluginInfo(self):
        return self.getMultiplePluginInfos(self.getInstalledPlugins())

    def findConflicts(self, jarInfo):
        infos = self.getAllPluginInfo()
        conflicts = []
        for compared in infos.values():
            if compared['basename'] == jarInfo['basename']:
                conflicts.append(compared)
        return conflicts

    def install(self, jarInfo, replace=False):
        conflicts = self.findConflicts(jarInfo)
        if len(conflicts) > 0:
            if not replace or len(conflicts) != 1 or not conflicts[0]['isInstalled']:
                message = ("This plugin conflicts with:\n" +
                           "\n".join(plugin['display']))
                raise InvalidPluginError(message)

        self.checkPluginDirectory()
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        copy(jarInfo['filename'], os.path.join(self.dir, jarInfo['basename']))

    def uninstall(self, jarInfo):
        self.checkPluginDirectory()
        if not jarInfo['isInstalled']:
            raise EnvironmentError("This plugin is not installed in the user "
                                   "plugins directory.")
        jarInfo['status'] = 'to be removed'
        jarInfo['note'] = ("(This plugin will be removed from the user plugins "
                           "directory when you restart JES.)")
        self.toRemove.append(jarInfo)

    def checkPluginDirectory(self):
        if not self.available:
            raise EnvironmentError("The plugin system is not configured.\n"
                                   "(Make sure your launcher is setting the "
                                   "jes.plugindir system property.)")

        if os.path.exists(self.dir) and not os.path.isdir(self.dir):
            raise EnvironmentError("The plugin directory (%s) is not a "
                                   "directory. Find out what it is and "
                                   "remove it so you can use plugins." %
                                   self.dir)

