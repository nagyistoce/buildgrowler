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
from PyObjCTools import NibClassBuilder


class BuildGrowlerWindow(NibClassBuilder.AutoBaseClass):    
    bg = NSColor.colorWithDeviceRed_green_blue_alpha_(0.7, 0.7, 0.7, 1.0)
    credentialsAdditions  = 120

    def initWithContentRect_styleMask_backing_defer_(self, rect, style, backing, defer):
        self = super(BuildGrowlerWindow,
                self).initWithContentRect_styleMask_backing_defer_(rect, style,
                        backing, defer)
        if self is None: return None

        self.setBackgroundColor_(self.bg)
        return self

    def awakeFromNib(self):
        # Size the frame to not display the credentials box
        frame = self.frame()
        frame.size.height -= self.credentialsAdditions
        frame.origin.y += self.credentialsAdditions
        self.setFrame_display_animate_(frame, True, False)
        self.credentialsView.setHidden_(True)
        self.hiding = True             # We've just hidden it
        self.wasAnimatedResize = False # Nope, it wasn't
        # We want resizing notifications
        #[[NSNotificationCenter defaultCenter] addObserver:self
        #            selector:@selector(objectAddedToConverterList:)
        #                name:@"ConverterAdded" object:nil];
        NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(self,
                self.windowDidResize_, 'NSWindowDidResizeNotification', self)

    def showHideCredentials_(self, sender):
        frame = self.frame()
        if self.hiding:
            frame.size.height += self.credentialsAdditions
            frame.origin.y -= self.credentialsAdditions
            # We only want to show the window when the animation has completed. 
            # This might be a bit overcomplicated at the moment, but I want to
            # use widnowDidResize_ to see if I can do some cliping on the
            # drawing of the credentials box eventually.
            self.wasAnimatedResize = frame.size
        else:
            frame.size.height -= self.credentialsAdditions
            frame.origin.y += self.credentialsAdditions
            # Currently we want to hide this BEFORE we commence the hiding of
            # the window, otherwise it looks bad. This might change if I can get
            # some nice clipping to work.
            self.credentialsView.setHidden_(True)
        # This call only comes back after the animated resize has been concluded    
        self.setFrame_display_animate_(frame, True, True)
        self.hiding = not self.hiding

    def windowDidResize_(self, n):
        if self.wasAnimatedResize and self.wasAnimatedResize.height == self.frame().size.height:
            self.credentialsView.setHidden_(not self.credentialsView.isHidden())
            self.wasAnimagedResize = False


# vim:ts=4:sw=4:et:
