#!/bin/sh

# This is a wrapper script which calls a SED regex script to do some conversion
# work.

# Call the SED script
bin/convert.sed $1 > $2
