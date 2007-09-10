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

# I'mm having some issues with py2app 0.3.6 and python2.3 (I think thats the
# issue anyway). So if we are building with < 2.4 (ie the Apple supplied Python)
# use an older style of specifying the setup, by importing py2app and not
# setuptools.
# FIXME: Some of this might be true ONLY if we are using the apple supplied
# Python2.3 and doing a semi-standalone build??? and not generally for
# Python2.3?
if sys.hexversion < 0x02040000:
    setup_options=dict(setup_requires=["py2app"])
    # FIXME: Is this required for >= 2.4 as well?
    py2app_options=dict(packages='zope')
    version = sys.version[:3]
    # This is required to make the app look for _objc.so (and probably other
    # things) in the right place. From:
    # http://maba.wordpress.com/2006/08/31/ 
    # incredible-2d-images-using-nodebox-universal-binary/
    plist_options=dict(PyResourcePackages=[
        (s % version) for s in [
            u'lib/python%s', 
            u'lib/python%s/lib-dynload',
            u'lib/python%s/site-packages',
            u'lib/python%s/site-packages.zip',
            ]])
else:
    setup_options=dict(setup_requires=["py2app"])
    py2app_options=dict()
    plist_options=dict()

from setuptools import setup

#from distutils.core import setup
import distutils.cmd 
import distutils.command.build

from distutils.util import *
import distutils.spawn as d_spawn
import os
class build_frameworks(distutils.cmd.Command):
    description = "Builds OS X Frameworks"
    user_options = [
            ('frameworks', None, "A list of frameworks to build"),
            ('target', None, "The target to build (for all frameworks)")]
    def initialize_options(self):
        self.frameworks = None
        self.configuration = 'Release'
        self.target = None
        self.dist_dir = None
        self.bdist_dir = None
        self.framework_dir = None
        self.framework_temp = None
        self.temp_dir = None
        self.xcodebuild = None
        self.alias = None

    def finalize_options(self):
        # I don't know of a better way of getting this directory other than
        # copying the relevant code from py2app.build_app into here...
        py2app = self.get_finalized_command('py2app')
        py2app.create_directories()
        self.set_undefined_options('py2app', 
                ('dist_dir', 'dist_dir'),
                ('bdist_dir', 'bdist_dir'),
                ('framework_dir', 'framework_dir'),
                ('temp_dir', 'temp_dir'),
                ('alias', 'alias'))
        self.framework_temp = os.path.join(self.temp_dir, 'BuiltFrameworks')
        # I want absolute paths:
        self.framework_dir = os.path.abspath(self.framework_dir)
        self.temp_dir = os.path.abspath(self.temp_dir)
        #self.ensure_dirname(self.frameworks)
        #self.ensure_string(self.target)

    def run(self):
        # Nothing to do?
        if self.frameworks is None:
            return
        # Find xcodebuild
        self.xcodebuild = d_spawn.find_executable('xcodebuild')
        if not self.xcodebuild:
            raise DistutilsExecError('Could not find the xcodebuild command, ' \
                  'have you installed Xcode?')
        # Build things    
        self.execute(self.__build, 
                [self.frameworks], 
                'Building Framework: %s' % (self.frameworks))
        # If we are doing an alias build, we have to get py2app to link in the
        # framework
        if self.alias:
            # (At least some) py2app(s) generate bad symlinks for frameworks in
            # alias builds. Therefore we'll do it ourselves.
            py2app = self.get_finalized_command('py2app')
            app_path = os.path.join(
                    self.dist_dir,
                    py2app.get_appname() + '.app')
            app_framework_path = os.path.join(
                    app_path, 'Contents', 'Frameworks')
            from py2app.util import makedirs
            makedirs(app_framework_path)
            # FIXME: Move somewhere else, ie into a Frameworks class, like the
            # Extensions class
            framework_name = os.path.split(self.frameworks)
            if framework_name[1] == '':
                framework_name = os.path.split(framework_name[0])[1]
            else:
                framework_name = framework_name[1]
            framework_name = framework_name + '.framework'    
            src = os.path.join(self.framework_dir, framework_name)
            dst = os.path.join(app_framework_path, framework_name)
            try:
                os.remove(dst)
            except:
                pass
            os.symlink( os.path.abspath(src), dst)


    def __build(self, framework):
        # We need to change into the project directory in order for xcodebuild
        # to do its thing (ie the directory with the .xcodeproj in it)
        cwd = os.getcwd()
        os.chdir(framework)
        self.spawn([
            self.xcodebuild,
            'CONFIGURATION_BUILD_DIR=%s' % (self.framework_dir),
            'PROJECT_TEMP_DIR=%s' % (self.framework_temp)])
        # However we MUST also put the cwd back to what it was, as other
        # commands might rely on relative paths
        os.chdir(cwd)
                  

distutils.command.build.build.sub_commands.append(('build_frameworks', None))

setup(
    cmdclass={'build_frameworks': build_frameworks},
    app=['src/main.py'],
    data_files=['src/English.lproj', 'icon/BuildGrowlerIcon48x48.png'],
    options=dict(
        build_frameworks=(dict(frameworks='src/Frameworks/BGUtils/')),
        py2app=dict(
        iconfile='icon/BuildGrowler.icns',
        #frameworks='src/Frameworks/BGUtils/build/Release/BGUtils.framework',
        # For a short list of these with descriptions, see the 
        # 'Essential Application Identification Properties' section in the
        # 'Cocoa Application Tutorial' in the 'ADC Reference Library'
        plist=dict(
            CFBundleName='BuildGrowler',
            CFBundleIdentifier='org.transterpreter.BuildGrowler',
            NSHumanReadableCopyright='Copyright 2007 Christian L. Jacobsen',
            #CFBundleVersion='0.1', # build version
            CFBundleShortVersionString='0.2.0', # release-version-number
            **plist_options # Options from above
        ),
        **py2app_options # Options from above
    )),
    **setup_options # Options from above   
)

# vim:ts=4:sw=4:et:
