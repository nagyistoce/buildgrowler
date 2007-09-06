#    BuildGrowler, a tool for being notified of BuildBot actions and 
#    failuers on Mac OS X. 
#    http://code.google.com/p/buildgrowler/
#
#    Copyright (C) 2007 Christian L. Jacobsen
#
#    This file is part of BuildGrowler.
#
#    BuildGrowler is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    BuildGrowler is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with BuildGrowler; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# PyObjC
import objc
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper

# BuildGrowler
import globals
from RecentHosts import *


# class defined in MainMenu.nib
class BuildGrowlerController(NibClassBuilder.AutoBaseClass):
    # the actual base class is NSObject
    # The following outlets are added to the class:
    # buildGrowler
    # hostText
    # portText
    # statusText

    def __init__(self):
        self.lastHostText = None
        
    def init(self):
        self = super(BuildGrowlerController, self).init()
        if self is None: return None
        self.__init__()
        return self

 
    def applicationDidFinishLaunching_(self, aNotification):
        """
        Invoked by NSApplication once the app is done launching and
        immediately before the first pass through the main event
        loop.
        """
        # Set up the application defaults
        self.defaults = NSUserDefaults.standardUserDefaults()
        self.setDefaultDefaults()
        # Set up the datasource for the combo box
        self.recentHosts = RecentHosts.alloc().initWithDefaults(self.defaults)
        self.hostText.setDataSource_(self.recentHosts)
        self.buildGrowler.setRecentHosts_(self.recentHosts)
        # Set up initial values in the UI
        if self.recentHosts.getLength() != 0:
            # If the user has some recent hosts, use the first one, otherwise we
            # leave the values as what is set in the nib
            self.hostText.setStringValue_(self.recentHosts.getHostForIndex(0))
            self.portText.setStringValue_(self.recentHosts.getPortForIndex(0))
        # Set initial sate of buttons
        self.startButton.setEnabled_(True)
        self.stopButton.setEnabled_(False)
        globals.reactor.interleave(AppHelper.callAfter)

    def setDefaultDefaults(self):
        defaults = dict()
        # RecentHosts is a list of tuples of hostname and portnumber.
        defaults[u'RecentHosts'] = []
        self.defaults.registerDefaults_(defaults)

    def applicationShouldTerminate_(self, sender):
        if globals.reactor.running:
            globals.reactor.addSystemEventTrigger(
                'after', 'shutdown', AppHelper.stopEventLoop)
            globals.reactor.stop()
            return False
        return True

    def windowWillClose_(self, aNotification):
        self.quitApp()

    def quitApp(self):
        """ Method which quits the app and does any necessary stuff """
        # Ensure that the defaults are saved
        NSUserDefaults.resetStandardUserDefaults()
        # Actually do the quitting...
        app = NSApplication.sharedApplication()
        app.terminate_(0) # FIXME: Whats the argument here?

    def quit_(self, sender):
        """ Action for the quit button """
        self.quitApp()

    def start_(self, sender):
        # Update the port text as this may not have happened, even though it
        # should. See controlTextDidEndEditing_'s comment
        # FIXME: This does not help at all, cos it makes it so that an existing
        # host can never changes the port numner. I've disabled completion of
        # the combobox for now, which is the real problem, as I get no
        # notification (that I can see) that the field has autocompleted
        # something, at which point I might want to update the port.
        #self.__updatePortFromString(self.hostText.stringValue())
        # Do normal start button stuff
        self.startButton.setEnabled_(False)
        host = self.hostText.objectValue()
        # FIXME: Error checking, alow only numbers
        port = int(self.portText.objectValue())
        self.hostText.setEnabled_(False)
        self.portText.setEnabled_(False)
        self.buildGrowler.start(self, host, port)

    def stop_(self, sender):
        self.buildGrowler.stop()

    #########################################################################
    # Combo Box updates
    #########################################################################

    def __updatePortFromString(self, s):
        port = self.recentHosts.getPortForHost(s)
        if port:
            self.portText.setStringValue_(port)

    def __updatePortFromIndex(self, s):
        port = self.recentHosts.getPortForIndex(s)
        if port:
            self.portText.setStringValue_(port)

    # Whenever a new character is typed
    def controlTextDidChange_(self, n):
        if n.object() is self.hostText:
            self.__updatePortFromString(n.object().stringValue())

    # Fired whenever a new selection is made from the dropdown in the combobox
    def comboBoxSelectionDidChange_(self, n):
        if n.object() is self.hostText:
            self.__updatePortFromIndex(n.object().indexOfSelectedItem())

    # This is fired when editing ends, mostly when the cursor leaves the
    # combobox. This catches cases where the selected autocompletion text
    # is used. However only if the user removes focus from the combobox. Ie this
    # does not catch cases where they use autocompletion and then immediately
    # hit the start button w/o first removing focus from the combobox.
    def controlTextDidEndEditing_(self, n):
        if n.object() is self.hostText:
            # If somebody enters and exits the host editor, and the text did not
            # change, do NOT update the port... the user might be in the process
            # of updating it.
            hostText = n.object().stringValue()
            if self.lastHostText == hostText:
                return
            self.__updatePortFromString(hostText)
            self.lastHostText = hostText

# vim:ts=4:sw=4:et:
