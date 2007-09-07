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
from Foundation import *
from PyObjCTools import NibClassBuilder, AppHelper

# Twisted
from twisted.application.internet import TimerService
from twisted.spread import pb 
from twisted.cred import credentials, error

# BuildGrowler
import globals
from StatusClient import *


# class defined in MainMenu.nib
class BuildGrowler(NibClassBuilder.AutoBaseClass):
    # the actual base class is NSObject

    def __init__(self):
        self.listener = StatusClient("steps")
        self.caller = None
        self.connection = None
        
    def init(self):
        self = super(BuildGrowler, self).init()
        if self is None: return None
        self.__init__()
        return self

    def run(self, host, port, username, password):
        """Start the client."""
        globals.reactor.interleave(AppHelper.callAfter)
        self.startConnecting(host, port, username, password)
        #reactor.run()

    def setRecentHosts_(self, recentHosts):
        self.recentHosts = recentHosts

    def startConnecting(self, host, port, username, password):
        theself = self
        class MyPBClientFactory(pb.PBClientFactory):
            def clientConnectionLost(self, connector, reason, reconnecting=0):
                # FIXME: I have never seen this happen, but should we do as with
                # clientConnectionFailed???
                print "Lost connection"
            def clientConnectionFailed(self, connector, reason):    
                theself.not_connected(reason)
        cf = MyPBClientFactory()
        # I have discovered that the UsernamePassword method does not like
        # PyObjC objects, at least not the ones I was passing. We should ensure
        # that we have strings here therefore, to avoid future confusion.
        assert type(username) == str
        assert type(password) == str
        creds = credentials.UsernamePassword(username, password)
        d = cf.login(creds)
        self.connection = globals.reactor.connectTCP(host, port, cf)
        d.addCallbacks(self.connected, self.not_connected)
        return d

    def connected(self, ref):
        ref.notifyOnDisconnect(self.disconnected)
        self.listener.connected(ref)
        globals.growl.notify(globals.growl.notifications[globals.growl.NOTIFICATION_STATUS],
                "BuildGrowler",
                "Connected")
        self.caller.stopButton.setEnabled_(True)
        # Now that we have connected successfully add the host/port to the
        # recent hosts
        self.recentHosts.addHost_Port_(self.connection.host, self.connection.port)

        # This seems to make a difference in detecting dropped connections!
        class Thingy(TimerService):
            def __init__(self, ref):
                self.ref = ref
                TimerService.__init__(self, 30, self.callme)

            def callme(self):   
                self.ref.callRemote("getBuilderNames").addErrback(self.fux)

            def fux(self, thingy):
                pass


        t = Thingy(ref)
        t.startService()

    def not_connected(self, why):   
        str = "Could not connect"
        if why.check(error.UnauthorizedLogin):
            str = str + "\n(Unauthorised login(!?)"
        globals.growl.notify(globals.growl.notifications[globals.growl.NOTIFICATION_STATUS],
                "BuildGrowler", str)
        self.caller.startButton.setEnabled_(True)
        self.caller.hostText.setEnabled_(True)
        self.caller.portText.setEnabled_(True)
        self.caller.credUserName.setEnabled_(True)
        self.caller.credPassword.setEnabled_(True)
                

    def disconnected(self, ref):    
        globals.growl.notify(globals.growl.notifications[globals.growl.NOTIFICATION_STATUS],
                "BuildGrowler",
                "Disconnected")
        self.caller.startButton.setEnabled_(True)
        self.caller.stopButton.setEnabled_(False)
        self.caller.hostText.setEnabled_(True)
        self.caller.portText.setEnabled_(True)
        self.caller.credUserName.setEnabled_(True)
        self.caller.credPassword.setEnabled_(True)

    def start(self, caller, host, port, username, password):
        self.caller = caller
        self.run(host, port, username, password)

    def stop(self):
        self.connection.disconnect();
        #growl.notify(growl.notifications[growl.NOTIFICATION_STATUS],
        #       "BuildGrowler",
        #       "Stopped")

# vim:ts=4:sw=4:et:
