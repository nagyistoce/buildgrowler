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

# BGUtils
import BGUtils

class PasswordController(NibClassBuilder.AutoBaseClass):

    def __init__(self):
        self.password = None
        self.changed = False

    def initWithCoder_(self, frame):
        self = super(PasswordController, self).initWithCoder_(frame)
        if self is None: return None
        self.__init__()
        self.setDelegate_(self)
        return self

    def hasNewPassword(self):
        return not self.password is None

    def getNewPassword(self):
        return self.password

    def clearNewPassword(self):
        self.password = None

    # Whenever we get focus
    def becomeFirstResponder(self):
        self.setStringValue_('')
        return super(PasswordController, self).becomeFirstResponder()

    # Whenever a new character is typed
    def controlTextDidChange_(self, n):
          self.changed = True

    # When editing finishes, (as far as I can tell, when focus leaves the
    # control)
    def controlTextDidEndEditing_(self, n):
        if self.changed:
            self.password = BGUtils.AIWiredString.stringWithString_(self.stringValue())
            self.changed = False
            self.setStringValue_('        ')

    def youLostFocusButYouMightNotKnowIt(self):
        # I'm having problems where I do not get loss of focus messages or
        # anything else, like controlTextDidEndEditing messages when I think I
        # should. Ie user has edited in control, does not leave it, but
        # immediately presses a button. I'll use this for the really annoying
        # cases, though I'd like to fix it properly so that I get some kind of
        # message... cos other text edit fields have the same problem.
        self.controlTextDidEndEditing_(None)

# vim:ts=4:sw=4:et:
