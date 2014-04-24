#!/usr/bin/python
# -*- coding: utf_8 -*-

###############################################################################
################################ INTRODUCTION #################################
###############################################################################
#
# Open with: "./box.py KYUtest.pdf" while the terminal is
# opened in the workdirectory.
#
# This python script will generate a page border for Rapuma projects on
# A4 size background. Page dimensions are read in from the project's layout
# config file and converted to float pixel value. The box is centered
# on the A4 background.
#
# A SVG file is generated based on calculated co-ordinates of the box rectangle
# With RSVG-convert the SVG is
# The end product combined with a test pdf to a markedBOX pdf that can be opened
# to check the result.
#
###############################################################################
############################## SETUP ENVIRONMENT ##############################
###############################################################################

# IMPORTS
import os, sys, codecs, subprocess, tempfile

# INITIAL SETTINGS
procfile = sys.argv[1]      # wholeNT.pdf

# TEMPORARY FILES
backgrSVG = tempfile.NamedTemporaryFile().name  #"backgr.svg"
backgrPDF = tempfile.NamedTemporaryFile().name  #"backgr.pdf"

# IMPORTING PAGE DIMENSIONS
from configobj import ConfigObj

layoutConfig = ConfigObj('layout.conf', encoding='utf-8')

A4Width = layoutConfig['PageLayout']['A4Width']
A4Height = layoutConfig['PageLayout']['A4Height']
pageWidth = layoutConfig['PageLayout']['pageWidth']
pageHeight = layoutConfig['PageLayout']['pageHeight']

# The values stored in the config are strings and in mm. To convert them to
# pixels the need to be changed to float().

factor = 72/25.4    # 1 mm = 72/25.4 pixels

aw = float(A4Width) * factor
ah = float(A4Height) * factor
pw = float(pageWidth) * factor
ph = float(pageHeight) * factor

#   GENERATE A SVG of the watermark; convert to pdf; add watermark backgound to the wholeNT"

with codecs.open(backgrSVG, 'wb') as fbackgr :            # open file for writing

#   SVG INTRODUCTION
	fbackgr.write( '''<svg xmlns="http://www.w3.org/2000/svg"
version="1.1" width = "''')

#   PAGE DIMENSIONS
	fbackgr.write(str (aw))
	fbackgr.write( '''" height = "''')
	fbackgr.write(str (ah))
	fbackgr.write( '''">
<rect x = "''')
	fbackgr.write(str ((aw - pw)/2))
	fbackgr.write( '''" y= "''')
	fbackgr.write(str ((ah - ph)/2))
	fbackgr.write( '''" height = "''')
	fbackgr.write(str (ph))
	fbackgr.write( '''" width = "''')
	fbackgr.write(str (pw))
	fbackgr.write('''"
style = "fill:#ffffff;fill-opacity:1;stroke:#000000;stroke-opacity:1;stroke-width:.1"/>
</svg>''')

	fbackgr.close()        # GENERATION of background svg finished

#   CONVERSION OF stamp svg into stamp pdf with rsvg-convert
subprocess.call(["rsvg-convert", "-f", "pdf", "-o", backgrPDF, backgrSVG])

#   WATERMARKING wholeNT with backgrPDF
subprocess.call(["pdftk", procfile, "background", backgrPDF, "output", "markedBOX.pdf"])
