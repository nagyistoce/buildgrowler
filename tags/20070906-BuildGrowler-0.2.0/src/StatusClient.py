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

# Twisted
from twisted.spread import pb 

# Growl
import Growl 

# BuildGrowler
import globals


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
        globals.growl.notify(globals.growl.notifications[globals.growl.NOTIFICATION_BUILD_START],
            "BuildBot: " + buildername,
            "Started build")

    def remote_buildFinished(self, buildername, build, results):
        print "buildFinished", buildername, build, results
        if results == 0:
            globals.growl.notify(globals.growl.notifications[globals.growl.NOTIFICATION_BUILD_END],
                "BuildBot: " + buildername,
                "Finished build")
        else:
            globals.growl.notify(globals.growl.notifications[globals.growl.NOTIFICATION_BUILD_ERROR],
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


