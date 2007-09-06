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

import objc
from AppKit import *
from PyObjCTools import NibClassBuilder

class BuildGrowlerWindow(NibClassBuilder.AutoBaseClass):    
    def initWithContentRect_styleMask_backing_defer_(self, rect, style, backing, defer):
        self = super(BuildGrowlerWindow,
                self).initWithContentRect_styleMask_backing_defer_(rect, style,
                        backing, defer)
        if self is None: return None

        bg = NSColor.colorWithDeviceRed_green_blue_alpha_(0.7, 0.7, 0.7, 1.0)
        self.setBackgroundColor_(bg)
        return self
