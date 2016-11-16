#!/bin/bash - 
#===============================================================================
#
#          FILE: create_sdist.sh
# 
#         USAGE: ./create_sdist.sh 
# 
#   DESCRIPTION: Generate source distribution from git repo.
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Dilawar Singh (), dilawars@ncbs.res.in
#  ORGANIZATION: NCBS Bangalore
#       CREATED: Saturday 12 November 2016 03:12:37  IST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
set -x
set -e
echo "Version for this realeae?"
read VERSION
(
    cd ..
    mkdir -p moose-$VERSION
    rsync --progress -azv --cvs-exclude moose-package/ moose-$VERSION/
    tar --exclude-vcs -cvfz moose-$VERSION.tar.gz moose-$VERSION
)

