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

import Growl 

class BuildGrowlerNotifier(Growl.GrowlNotifier):
    applicationName = 'BuildGrowler'
    notifications = ['BuildGrowler Status', 'Build Started', 'Build Finished', 'Build Error']
    NOTIFICATION_STATUS      = 0
    NOTIFICATION_BUILD_START = 1
    NOTIFICATION_BUILD_END   = 2
    NOTIFICATION_BUILD_ERROR = 3
    # Why does this not work?
    #applicationIcon=Growl.Image.imageWithIconForCurrentApplication()
    applicationIcon=Growl.Image.imageFromPath("BuildGrowlerIcon48x48.png")

# vim:ts=4:sw=4:et:
