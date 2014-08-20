# -*- coding: utf-8 -*-
"""
jes.gui.plugins
===============
This allows you to install plugins in JES.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
import traceback
from javax.swing import JOptionPane
from jes.core.plugins import InvalidPluginError
from jes.gui.components.actions import methodAction
from jes.gui.components.filechooser import FileChooser

TITLE = "JES Plugin Installer"
RESTART_MESSAGE = "(You have to restart JES for the changes to take effect.)"

class PluginActions(object):
    def __init__(self, parentWindow, installer):
        self.installer = installer
        self.parentWindow = parentWindow

    @methodAction(name="Install Plugin...")
    def installPlugin(self):
        try:
            self.installer.checkPluginDirectory()

            chooser = FileChooser()
            chooser.setExtensionFilter("jar", "Java archives")
            path = chooser.chooseFileToOpen(self.parentWindow)
            if path is None:
                return

            jarInfo = self.installer.data.getPluginInfo(path)

            replace = False
            conflicts = self.installer.findConflicts(jarInfo)
            if len(conflicts) == 1 and conflicts[0]['isInstalled']:
                replace = True
                message = ("Do you want to install the plugin\n%s?\n"
                           "It will replace %s!\n\n\n%s" %
                           (jarInfo['display'], conflicts[0]['display'],
                            jarInfo['description']))
            elif len(conflicts) > 0:
                message = ("This plugin cannot be installed, because it conflicts with\n" +
                           "\n".join(p['display'] for p in conflicts))
                JOptionPane.showMessageDialog(self.parentWindow,
                    message, TITLE, JOptionPane.ERROR_MESSAGE
                )
                return
            else:
                message = ("Do you want to install the plugin\n%s?\n\n%s" %
                           (jarInfo['display'], jarInfo['description']))

            if self.confirm(message):
                self.installer.install(jarInfo)
                self.notifyDone("%s was installed!" % jarInfo['title'])
        except (EnvironmentError, InvalidPluginError), exc:
            self.showErrorMessage(exc)

    @methodAction(name="Manage Plugins...")
    def managePlugins(self):
        try:
            self.installer.checkPluginDirectory()
            plugins = self.installer.getAllPluginInfo()

            if not plugins:
                JOptionPane.showMessageDialog(self.parentWindow,
                    "No plugins are installed.\n"
                    "If you have a plugin that you wish to install, "
                    "select \"Install Plugin...\" from the \"File\" menu.",
                    TITLE, JOptionPane.ERROR_MESSAGE
                )
                return

            pluginsByDisplay = dict((info['display'] + ' - ' + info['status'], info)
                                    for info in plugins.values())
            pluginNames = pluginsByDisplay.keys()
            pluginNames.sort()

            while True:
                name = JOptionPane.showInputDialog(self.parentWindow,
                    "Here are the installed plugins.\n"
                    "Select a plugin to see its description or uninstall it.",
                    TITLE, JOptionPane.QUESTION_MESSAGE, None,
                    pluginNames, pluginNames[0]
                )

                if name is None or name not in pluginsByDisplay:
                    return
                info = pluginsByDisplay[name]
                message = info['longDescription'] + '\n' + info['note']

                if info['isInstalled']:
                    choice = JOptionPane.showOptionDialog(self.parentWindow,
                        message, TITLE, JOptionPane.YES_NO_OPTION,
                        JOptionPane.INFORMATION_MESSAGE, None,
                        ["OK", "Uninstall"], "OK"
                    )

                    if choice == JOptionPane.NO_OPTION:
                        if not self.confirm("Are you sure you want to uninstall\n%s?" % info['display']):
                            return

                        self.installer.uninstall(info)
                        self.notifyDone("%s was removed." % info['title'])
                        return
                else:
                    JOptionPane.showMessageDialog(self.parentWindow,
                        message, TITLE, JOptionPane.INFORMATION_MESSAGE
                    )
        except (EnvironmentError, InvalidPluginError), exc:
            self.showErrorMessage(exc)


    def notifyDone(self, message):
        message = message + "\n" + RESTART_MESSAGE
        JOptionPane.showMessageDialog(
            self.parentWindow, message, TITLE, JOptionPane.INFORMATION_MESSAGE
        )

    def confirm(self, message):
        confirm = JOptionPane.showConfirmDialog(
            self.parentWindow, message, TITLE, JOptionPane.YES_NO_OPTION
        )
        return confirm == JOptionPane.YES_OPTION

    def showErrorMessage(self, exc):
        traceback.print_exc()
        excMessage = getattr(exc, 'strerror', str(exc))
        JOptionPane.showMessageDialog(
            self.parentWindow, excMessage, TITLE, JOptionPane.ERROR_MESSAGE
        )

