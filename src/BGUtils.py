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

"""
An interface to the BGUtils.framework, which is a collection of ObjectiveC bits
harvested from the different sources.

Keychain support
================

AIKeychain from the Adium sources have been harvested to provide easy access to
the Apple Keychain. The AIKeychain class provides various Keychain access
methods. The AIKeychain.m file documents the interface. A number of support
files are required for AIKeychain to work:

  * AIFunctions.{m,h}

  * AIStringAdditions.{m,h}

  * AIWiredData.{m,h}

  * AIWiredString.{m,h}

Please note however that some of these files depend on other files which are not
included in BGUtils. Thus not all their functionality is going to work.

This module also defines a number of constants useful for interacting with the
Apple keychain. These are all defined in the Apple Keychain Reference. The
constants defined in this file are:
  
  * *Keychain Authentication Type Constants*
    (typedef FourCharCode SecAuthenticationType;) 
    having the prefix: kSecAuthenticationType

  * *Keychain Protocol Type Constants* 
    (typedef FourCharCode SecProtocolType;) 
    having the prefix: kSecProtocolType

"""


def fourCharCode2Int(s):
    """
    Returns an integer representing the four bytes in the string `s`.

    This method is used to create certain parameters for Keychain functions
    which expects four character codes which are represented as an integer.
    Constats which have this property include those prefixed with:
    kSecAuthenticationType, kSecProtocolType, and others. The string `s` must be
    a byte string(!) and must be four characters long. Any other input will lead
    to an assertion error.
    """
    # This really only works on strings of length 4
    assert type(s) == str
    assert len(s) == 4
    i = 0
    # perhaps I should not be so lazy and just write this out :)
    for c in s:
        i = (i << 8) + ord(c)
    return i 

# FIXME: These are defined as: blahBlah = AUTH_TYPE_FIX_('blah')
# What is AUTH_TYPE_FIX and is it important :)
kSecAuthenticationTypeNTLM             = fourCharCode2Int('ntlm')
kSecAuthenticationTypeMSN              = fourCharCode2Int('msna')
kSecAuthenticationTypeDPA              = fourCharCode2Int('dpaa')
kSecAuthenticationTypeRPA              = fourCharCode2Int('rpaa')
kSecAuthenticationTypeHTTPBasic        = fourCharCode2Int('http')
kSecAuthenticationTypeHTTPDigest       = fourCharCode2Int('httd')
kSecAuthenticationTypeHTMLForm         = fourCharCode2Int('form')
kSecAuthenticationTypeDefault          = fourCharCode2Int('dflt')

kSecProtocolTypeFTP         = fourCharCode2Int('ftp ')
kSecProtocolTypeFTPAccount  = fourCharCode2Int('ftpa')
kSecProtocolTypeHTTP        = fourCharCode2Int('http')
kSecProtocolTypeIRC         = fourCharCode2Int('irc ')
kSecProtocolTypeNNTP        = fourCharCode2Int('nntp')
kSecProtocolTypePOP3        = fourCharCode2Int('pop3')
kSecProtocolTypeSMTP        = fourCharCode2Int('smtp')
kSecProtocolTypeSOCKS       = fourCharCode2Int('sox ')
kSecProtocolTypeIMAP        = fourCharCode2Int('imap')
kSecProtocolTypeLDAP        = fourCharCode2Int('ldap')
kSecProtocolTypeAppleTalk   = fourCharCode2Int('atlk')
kSecProtocolTypeAFP         = fourCharCode2Int('afp ')
kSecProtocolTypeTelnet      = fourCharCode2Int('teln')
kSecProtocolTypeSSH         = fourCharCode2Int('ssh ')
kSecProtocolTypeFTPS        = fourCharCode2Int('ftps')
kSecProtocolTypeHTTPS       = fourCharCode2Int('htps')
kSecProtocolTypeHTTPProxy   = fourCharCode2Int('htpx')
kSecProtocolTypeHTTPSProx   = fourCharCode2Int('htsx')
kSecProtocolTypeFTPProxy    = fourCharCode2Int('ftpx')
kSecProtocolTypeSMB         = fourCharCode2Int('smb ')
kSecProtocolTypeRTSP        = fourCharCode2Int('rtsp')
kSecProtocolTypeRTSPProxy   = fourCharCode2Int('rtsx')
kSecProtocolTypeDAAP        = fourCharCode2Int('daap')
kSecProtocolTypeEPPC        = fourCharCode2Int('eppc')
kSecProtocolTypeIPP         = fourCharCode2Int('ipp ')
kSecProtocolTypeNNTPS       = fourCharCode2Int('ntps')
kSecProtocolTypeLDAPS       = fourCharCode2Int('ldps')
kSecProtocolTypeTelnetS     = fourCharCode2Int('tels')
kSecProtocolTypeIMAPS       = fourCharCode2Int('imps')
kSecProtocolTypeIRCS        = fourCharCode2Int('ircs')
kSecProtocolTypePOP3S       = fourCharCode2Int('pops')

# Load the framework relative to the executable in the .app bundle
import objc
objc.loadBundle("BGUtils", globals(),
     bundle_path=objc.pathForFramework(u'@executable_path@/../../Frameworks/BGUtils.framework'))
del objc

# vim:ts=4:sw=4:et:
