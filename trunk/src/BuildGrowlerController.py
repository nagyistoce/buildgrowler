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
import BGUtils
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

    def awakeFromNib(self):
        # A few menu items that we are not using at the moment, but might be
        # using in the future.
        self.menuitem_help.setEnabled_(False)
        self.menuitem_preferences.setEnabled_(False)
        # Set a number formatter for the port field, so users can't type text or
        # out of range ports.
        class PortNumberFormatter(NSNumberFormatter):
            def init(self):
                self = super(PortNumberFormatter, self).init()
                if self is None: return None
                self.setMinimum_(1)
                self.setMaximum_(65535)
                self.setFormat_(u'0')
                self.setHasThousandSeparators_(False)
                return self

            def isPartialStringValid_newEditingString_errorDescription_(self, partialString):
                # Allow an empty string:
                if partialString == '':
                    return (True, None, None)
                # Check if the thing coming in is a number
                i = None
                try:
                    i = int(partialString)
                except ValueError:
                    return (False, None, u'The entered value is not a number')
                # Check if it is in the valid range
                if i < self.minimum() or i > self.maximum():
                    return (False, None, u'Invalid port range')
                return (True, None, None)

        portFormatter = PortNumberFormatter.alloc().init()
        self.portText.cell().setFormatter_(portFormatter)


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
            # FIXME: Perhaps we should check if it really is an int value coming
            # in, in case the defaults database has got confused about
            # something.
            self.portText.setIntValue_(self.recentHosts.getPortForIndex(0))
            username = self.recentHosts.getUserNameForIndex(0)
            if username:
                self.credUserName.setStringValue_(self.recentHosts.getUserNameForIndex(0))
                # We don't store an actual password, just some spaces to indicate to
                # the user that there actually is a password.
                self.credPassword.setStringValue_('        ')
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
        # The portText field ensures that the user can ONLY enter numbers (in
        # the valid port range even)
        port = int(self.portText.intValue())
        # Some Twisted bits do not like it when I pass in the PyObjC unicode
        # type object which comes out of here. Instead turn it into an str for
        # all round glorious happiness
        # FIXME: Do we support unicode usernames and passwords, well not at the
        # moment, but should they be supported
        username = str(self.credUserName.objectValue())
        # Check if the user entered a new password, if so store in keychain, i
        # then use it, else fetch password from keychain and use that
        password = ''
        if username: # If there is a username
            keychain = self.__getKeychain()
            if self.credPassword.hasNewPassword():
                # FIXME: We only store a username if the connection was went ok,
                # however the password always gets updated in the keychain
                # regardless of whether we successfully connected.
                result = keychain.\
                    setInternetPassword_forServer_securityDomain_account_path_port_protocol_authenticationType_keychainItem_error_(
                        self.credPassword.getNewPassword(),
                        host,
                        None,
                        username,
                        None,
                        port,
                        BGUtils.fourCharCode2Int('BBoT'),
                        BGUtils.kSecAuthenticationTypeDefault)
                password = self.credPassword.getNewPassword()
                # If there was an error leave the new password intact, otherwise
                # clear it
                if result[1] == None:
                    # No error occured.
                    self.credPassword.clearNewPassword()
            else:
                result = keychain.\
                    findInternetPasswordForServer_securityDomain_account_path_port_protocol_authenticationType_keychainItem_error_(
                        host,
                        None,
                        username,
                        None,
                        port,
                        BGUtils.fourCharCode2Int('BBoT'),
                        BGUtils.kSecAuthenticationTypeDefault)
                password = result[0]

        self.hostText.setEnabled_(False)
        self.portText.setEnabled_(False)
        self.credUserName.setEnabled_(False)
        self.credPassword.setEnabled_(False)
        self.buildGrowler.start(self, host, port, username, password)

    def stop_(self, sender):
        self.buildGrowler.stop()

    def __getKeychain(self):
        try:
            return self.keychain
        except AttributeError:    
            # Make a new default keychain if there was none already
            self.keychain = BGUtils.AIKeychain.keychainWithKeychainRef_(None)
            return self.keychain

    #########################################################################
    # Combo Box updates
    #########################################################################

    def __updatePortFromString(self, s):
        port = self.recentHosts.getPortForHost(s)
        if port:
            self.portText.setIntValue_(port)

    def __updatePortFromIndex(self, s):
        port = self.recentHosts.getPortForIndex(s)
        if port:
            self.portText.setIntValue_(port)

    def __updateCredentials(self, x):
        i = None
        if type(x) is int:
            i = x
        elif type(x) is objc.pyobjc_unicode:
            i = self.recentHosts.getIndexForHost(x)
        else:
            raise Exception('I didn\'t like what you passed into __updateCredentials (%s %s)' % (type(x), x))
        u = None
        if i != None:
            u = self.recentHosts.getUserNameForIndex(i)
        if u:
            self.credUserName.setStringValue_(u)
            self.credPassword.setStringValue_('        ')
        else:
            self.credUserName.setStringValue_('')
            self.credPassword.setStringValue_('')

    # Whenever a new character is typed
    def controlTextDidChange_(self, n):
        if n.object() is self.hostText:
            hostText = n.object().stringValue()
            #if self.lastHostText == hostText:
            #    return
            self.__updatePortFromString(n.object().stringValue())
            self.__updateCredentials(n.object().stringValue())
            self.lastHostText = hostText

    # Fired whenever a new selection is made from the dropdown in the combobox
    def comboBoxSelectionDidChange_(self, n):
        if n.object() is self.hostText:
            hostText = n.object().stringValue()
            #if self.lastHostText == hostText:
            #    return
            self.__updatePortFromIndex(n.object().indexOfSelectedItem())
            self.__updateCredentials(n.object().indexOfSelectedItem())
            self.lastHostText = hostText

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
            self.__updateCredentials(n.object().stringValue())
            self.lastHostText = hostText

# vim:ts=4:sw=4:et:
