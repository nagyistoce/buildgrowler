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

# PyObjC
import objc
from PyObjCTools import NibClassBuilder, AppHelper
# Must be done before we start importing NibClassBuilder.AutoBaseClass classes
NibClassBuilder.extractClasses("MainMenu")

# BuildGrowler imports
import globals
import BuildGrowlerWindow
import BuildGrowlerController
from BuildGrowlerNotifier import *
from BuildGrowler import *
from PasswordController import *


def setupGrowl():
    globals.growl = BuildGrowlerNotifier()
    globals.growl.register()
    globals.growl.notify(globals.growl.notifications[globals.growl.NOTIFICATION_STATUS],
            "BuildGrowler",
            "Initialised")

if __name__ == "__main__":
    setupGrowl()
    AppHelper.runEventLoop()

# vim:ts=4:sw=4:et:
