#!/bin/sh
echo "Printing list of non-universal executables and bundles in 'dist':"
find  dist -type f -exec sh -c 'file {} | grep ": Mach-O \(bundle\|executable\)"' \;
