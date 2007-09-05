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
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from distutils.core import setup
#import py2app
from setuptools import setup

setup(
    app=['src/BuildGrowler.py'],
    setup_requires=["py2app"],
    data_files=['src/English.lproj', 'icon/BuildGrowlerIcon48x48.png'],
    options=dict(py2app=dict(
        iconfile="icon/BuildGrowler.icns",
        # For a short list of these with descriptions, see the 
        # 'Essential Application Identification Properties' section in the
        # 'Cocoa Application Tutorial' in the 'ADC Reference Library'
        plist=dict(
            CFBundleName='BuildGrowler',
            NSHumanReadableCopyright='Copyright 2007 Christian L. Jacobsen',
            #CFBundleVersion='0.1', # build version
            CFBundleShortVersionString='0.1' # release-version-number
        ),

    ))
)

# vim:ts=4:sw=4:et:
