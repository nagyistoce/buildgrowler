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
from Foundation import *


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

    def getIndexForHost(self, host):
        recentHosts = self.__getRecentHosts()
        hosts = [h[0] for h in recentHosts]
        try:
            i = hosts.index(host)
            return i
        except ValueError:
            return None

    def getPortForHost(self, host):
        index = self.getIndexForHost(host)
        if index:
            return self.getHostForIndex(index)
        return None

    def getPortForIndex(self, index):
        return self.__getRecentHosts()[index][1]

    def getHostForIndex(self, index):
        return self.__getRecentHosts()[index][0]

    def getUserNameForIndex(self, index):
        try:
            return self.__getRecentHosts()[index][2]
        except IndexError:
            return None

    def getHasPasswordForIndex(self, index):
        try:
            return self.__getRecentHosts()[index][3]
        except IndexError:
            return False

    def getLength(self):
        return len(self.__getRecentHosts())

    def add(self, host, port, username = None, password = False):
        hosts = self.__getRecentHosts()
        newHosts = [(host, port, username, password)]
        for h in hosts:
            if host != h[0]:
                newHosts.append(h)
        self.__setRecentHosts(newHosts)
       
    # ComboBox datasource methods
    def comboBox_objectValueForItemAtIndex_(self, comboBox, index):
        return self.getHostForIndex(index)

    def numberOfItemsInComboBox_(self, combobox):
        return self.getLength()


# vim:ts=4:sw=4:et:
