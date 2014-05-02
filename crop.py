#!/usr/bin/python
# -*- coding: utf_8 -*-

###############################################################################
################################ INTRODUCTION #################################
###############################################################################
#
# Open with: "./crop.py KYUtest.pdf" while the terminal is
# opened in the workdirectory.
#
# This python script will generate cropmarks for Rapuma projects on A4 size
# background. Page dimensions are read in from the project's layout config
# file and converted to float pixel value. The watermark is will be centered
# on the A4 background.
#
# A SVG file is generated based on calculated co-ordinates of the cropmarks
# With RSVG-convert the the SVG is converted to a pdf
# The end product combined with a test pdf to a markedCROP pdf that may be
# opened to check the result.
#
###############################################################################
############################## SETUP ENVIRONMENT ##############################
###############################################################################

# IMPORTS
import os, sys, codecs, subprocess, tempfile

# INITIAL SETTINGS ./c
procfile = sys.argv[1]      # wholeNT.pdf

# Definition of CROP MARK SVG function
def cropsvg(A4Width, A4Height,pageWidth,pageHeight) :
	"This function writes the SVG code for crop lines, original co-ordinates are top left x and y"

	with codecs.open(backgrSVG, 'wb') as fbackgr :            # open file for writing

				# starting lines of SVG xml
		fbackgr.write( '''<svg xmlns="http://www.w3.org/2000/svg"
version="1.1" width = "'''+str (round(A4Width,1))+ '''" height = "'''+str(round(A4Height,1))+'''">\n''')
				# vertical top left
		fbackgr.write( '''<path d = "m'''+str (round((A4Width - pageWidth)/2,1))+''','''+str (round((A4Height - pageHeight)/2 - 32.0,1))+''',0,27" style="stroke:#000000;stroke-width:.2"/>\n''')
				# vertical bottom left
		fbackgr.write( '''<path d = "m'''+str (round((A4Width - pageWidth)/2,1))+''','''+str (round((A4Height + pageHeight)/2 + 5.0,1))+''',0,27" style="stroke:#000000;stroke-width:.2" />\n''')
				# vertical bottom right
		fbackgr.write( '''<path d = "m'''+str (round((A4Width + pageWidth)/2,1))+''','''+str (round((A4Height - pageHeight)/2 - 32.0,1))+''',0,27" style="stroke:#000000;stroke-width:.2"/>\n''')
				# vertical top right
		fbackgr.write( '''<path d = "m'''+str (round((A4Width + pageWidth)/2,1))+''','''+str (round((A4Height + pageHeight)/2 + 5.0,1))+''',0,27" style="stroke:#000000;stroke-width:.2" />\n''')
				# horzontal top left
		fbackgr.write( '''<path d =" m'''+str (round((A4Width - pageWidth)/2 - 32.0,1))+''','''+str (round((A4Height - pageHeight)/2,1))+''',27,0" style="stroke:#000000;stroke-width:.2" />\n''')
				# horzontal top right
		fbackgr.write( '''<path d =" m'''+str (round((A4Width + pageWidth)/2 + 5.0,1))+''','''+str (round((A4Height - pageHeight)/2,1))+''',27,0" style="stroke:#000000;stroke-width:.2" />\n''')
				# horzontal bottom right
		fbackgr.write( '''<path d =" m'''+str (round((A4Width - pageWidth)/2 - 32.0,1))+''','''+str (round((A4Height + pageHeight)/2,1))+''',27,0" style="stroke:#000000;stroke-width:.2" />\n''')
				# horzontal bottom left
		fbackgr.write( '''<path d =" m'''+str (round((A4Width + pageWidth)/2 +5.0,1))+''','''+str (round((A4Height + pageHeight)/2,1))+''',27,0" style="stroke:#000000;stroke-width:.2" />\n''')
		fbackgr.write( '''</svg>''')

		fbackgr.close()                                         # close file for writing
	return

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

factor = 72.0/25.4    # 1 mm = 72/25.4 pixels

aw = float(A4Width) * factor
ah = float(A4Height) * factor
pw = float(pageWidth) * factor
ph = float(pageHeight) * factor

# GENERATE A SVG of the crop marks; convert to pdf; add crop marks backgound to the procfile.

cropsvg(aw,ah,pw,ph)

#   CONVERSION OF stamp svg into stamp pdf with rsvg-convert
subprocess.call(["rsvg-convert", "-f", "pdf", "-o", backgrPDF, backgrSVG])

#   WATERMARKING wholeNT with backgrPDF
subprocess.call(["pdftk", procfile, "background", backgrPDF, "output", "markedCROP.pdf"])
