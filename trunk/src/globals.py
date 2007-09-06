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


##############################################################################
# Twisted
##############################################################################
# http://twistedmatrix.com/trac/changeset/18387
# http://twistedmatrix.com/trac/ticket/1833
# Use of threadselectreactor is not recommended it seems
#from twisted.internet.threadedselectreactor import install
#reactor = install()
from twisted.internet import _threadedselect 
reactor = _threadedselect.install() 
#from twisted.internet import cfreactor
#cfreactor.install()




##############################################################################
# Growl
##############################################################################
growl = None

# vim:ts=4:sw=4:et:
