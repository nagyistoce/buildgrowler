#!/usr/bin/python
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

import sys
import re

import objc
from AppKit import *
from Foundation import *
from PyObjCTools import NibClassBuilder, AppHelper

# Power management
#from IOKit import pwr_mgt, IOMessage

# http://twistedmatrix.com/trac/changeset/18387
# http://twistedmatrix.com/trac/ticket/1833
# Use of threadselectreactor is not recommended it seems
#from twisted.internet.threadedselectreactor import install
#reactor = install()
from twisted.internet import _threadedselect 
reactor = _threadedselect.install() 
#from twisted.internet import cfreactor
#cfreactor.install()
from twisted.application.internet import TimerService

from twisted.spread import pb 
from twisted.cred import credentials, error

import pbutil

import Growl 


NibClassBuilder.extractClasses("MainMenu")

# BuildGrowler imports
import BuildGrowlerWindow
import BuildGrowlerController
from BuildGrowlerNotifier import *


class StatusClient(pb.Referenceable):
    """To use this, call my .connected method with a RemoteReference to the
    buildmaster's StatusClientPerspective object.
    """

    def __init__(self, events):
        self.builders = {}
        self.events = events

    def connected(self, remote):
        #print "connected"
        self.remote = remote
        remote.callRemote("subscribe", self.events, 5, self)

    def remote_builderAdded(self, buildername, builder):
        #print "builderAdded", buildername, builder
        pass

    def remote_builderRemoved(self, buildername):
        #print "builderRemoved", buildername
        pass

    def remote_builderChangedState(self, buildername, state, eta):
        #print "builderChangedState", buildername, state, eta
        pass

    def remote_buildStarted(self, buildername, build):
        print "buildStarted", buildername, build
        growl.notify(growl.notifications[growl.NOTIFICATION_BUILD_START],
            "BuildBot: " + buildername,
            "Started build")

    def remote_buildFinished(self, buildername, build, results):
        print "buildFinished", buildername, build, results
        if results == 0:
            growl.notify(growl.notifications[growl.NOTIFICATION_BUILD_END],
                "BuildBot: " + buildername,
                "Finished build")
        else:
            growl.notify(growl.notifications[growl.NOTIFICATION_BUILD_ERROR],
                "BuildBot: " + buildername,
                "Build error",
                priority = Growl.growlPriority["High"],
                sticky = True)

    def remote_buildETAUpdate(self, buildername, build, eta):
        #print "ETA", buildername, eta
        pass

    def remote_stepStarted(self, buildername, build, stepname, step):
        #print "stepStarted", buildername, build, stepname, step
        pass

    def remote_stepFinished(self, buildername, build, stepname, step, results):
        #print "stepFinished", buildername, build, stepname, step, results
        pass

    def remote_stepETAUpdate(self, buildername, build, stepname, step,
                                             eta, expectations):
        #print "stepETA", buildername, stepname, eta
        pass

    def remote_logStarted(self, buildername, build, stepname, step,
                                        logname, log):
        #print "logStarted", buildername, stepname
        pass

    def remote_logFinished(self, buildername, build, stepname, step,
                                         logname, log):
        #print "logFinished", buildername, stepname
        pass

    def remote_logChunk(self, buildername, build, stepname, step, logname, log,
                                    channel, text):
        #ChunkTypes = ["STDOUT", "STDERR", "HEADER"]
        #print "logChunk[%s]: %s" % (ChunkTypes[channel], text)
        pass


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

    def run(self, host, port):
        """Start the client."""
        reactor.interleave(AppHelper.callAfter)
        self.startConnecting(host, port)
        #reactor.run()

    def setRecentHosts_(self, recentHosts):
        self.recentHosts = recentHosts

    def startConnecting(self, host, port):
        theself = self
        class MyPBClientFactory(pb.PBClientFactory):
            def clientConnectionLost(self, connector, reason, reconnecting=0):
                # FIXME: I have never seen this happen, but should we do as with
                # clientConnectionFailed???
                print "Lost connection"
            def clientConnectionFailed(self, connector, reason):    
                theself.not_connected(reason)
        cf = MyPBClientFactory()
        creds = credentials.UsernamePassword("statusClient", "clientpw")
        d = cf.login(creds)
        self.connection = reactor.connectTCP(host, port, cf)
        d.addCallbacks(self.connected, self.not_connected)
        return d

    def connected(self, ref):
        ref.notifyOnDisconnect(self.disconnected)
        self.listener.connected(ref)
        growl.notify(growl.notifications[growl.NOTIFICATION_STATUS],
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
        growl.notify(growl.notifications[growl.NOTIFICATION_STATUS],
                "BuildGrowler", str)
        self.caller.startButton.setEnabled_(True)
        self.caller.hostText.setEnabled_(True)
        self.caller.portText.setEnabled_(True)
                

    def disconnected(self, ref):    
        growl.notify(growl.notifications[growl.NOTIFICATION_STATUS],
                "BuildGrowler",
                "Disconnected")
        self.caller.startButton.setEnabled_(True)
        self.caller.stopButton.setEnabled_(False)
        self.caller.hostText.setEnabled_(True)
        self.caller.portText.setEnabled_(True)

    def start(self, caller, host, port):
        self.caller = caller
        self.run(host, port)

    def stop(self):
        self.connection.disconnect();
        #growl.notify(growl.notifications[growl.NOTIFICATION_STATUS],
        #       "BuildGrowler",
        #       "Stopped")


class RecentHosts(NSObject):
    def __init__(self, defaults):
        self.defaults = defaults

    def initWithDefaults(self, defaults):
        self = super(RecentHosts, self).init()
        if self is None: return None
        self.__init__(defaults)
        return self

    def __getRecentHosts(self):
        return self.defaults.arrayForKey_(u'RecentHosts')

    def __setRecentHosts(self, l):
        self.defaults.setObject_forKey_(l, u'RecentHosts')

    # FIXME:
    # Change this into a method which returns the index and then the user can
    # use getPortForIndex instead
    def getPortForHost(self, host):
        recentHosts = self.__getRecentHosts()
        hosts = [h[0] for h in recentHosts]
        try:
            i = hosts.index(host)
            return recentHosts[i][1]
        except ValueError:
            return None

    def getPortForIndex(self, index):
        return self.__getRecentHosts()[index][1]

    def getHostForIndex(self, index):
        return self.__getRecentHosts()[index][0]

    def getLength(self):
        return len(self.__getRecentHosts())

    def addHost_Port_(self, host, port):
        hosts = self.__getRecentHosts()
        newHosts = [(host, port)]
        for h in hosts:
            if host != h[0]:
                newHosts.append(h)
        self.__setRecentHosts(newHosts)
       
    # ComboBox datasource methods
    def comboBox_objectValueForItemAtIndex_(self, comboBox, index):
        return self.getHostForIndex(index)

    def numberOfItemsInComboBox_(self, combobox):
        return self.getLength()


def setupGrowl():
    global growl
    growl = BuildGrowlerNotifier()
    growl.register()
    growl.notify(growl.notifications[growl.NOTIFICATION_STATUS],
            "BuildGrowler",
            "Initialised")

if __name__ == "__main__":
    setupGrowl()
    AppHelper.runEventLoop()

# vim:ts=4:sw=4:et:
