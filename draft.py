#!/usr/bin/python
# -*- coding: utf_8 -*-

###############################################################################
################################ INTRODUCTION #################################
###############################################################################
#
# Open with: "./watermark.py wholeKYUROM.pdf" while the terminal is
# opened in the workdirectory.
#
# This python script will generate a DRAFT watermark for Rapuma projects on
# A4 size background. Page dimensions are read in from the project's layout
# config file and converted to float pixel value. The watermark is centered
#  on the A4 background.
#
# A SVG file is generated based on calculated co-ordinates of the watermark
# text. With RSVG-convert the SVG is
# # The end product combined with a test pdf to a markedDRAFT pdf that can be opened
# to check the result.
#
###############################################################################
############################## SETUP ENVIRONMENT ##############################
###############################################################################

# IMPORTS
import os, sys, codecs, subprocess, tempfile

# INITIAL SETTINGS
procfile = sys.argv[1]      # wholeNT.pdf

# FUNCTION DEFINITION
def draftsvg(A4Width,A4Height,pageWidth,pageHeight):
	"This function writes the SVG code for the watermark"

	with codecs.open(backgrSVG, 'wb') as fbackgr :            # open file for writing

	#   SVG INTRODUCTION
		fbackgr.write( '''<svg xmlns="http://www.w3.org/2000/svg"
	version="1.1" width = "'''+str (round(A4Width,1))+'''" height = "'''+str (round(A4Height,1))+ '''">

	<g><text x = "'''+str (round((A4Width - pageWidth)/2 + 54,1))+ '''" y = "'''+str (round((A4Height - pageHeight)/2 + 120,1))+ '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:start;fill:#e6e6ff;fill-opacity:1">'''+str (pubProg)+'''</text>

	<text x = "'''+str (round((A4Width)/2,1))+ '''" y = "'''+str (round((A4Height - pageHeight)/2 + 194))+ '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:middle;fill:#e6e6ff;fill-opacity:1">'''+str (pubProg)+'''</text>

	<text x = "'''+str (round((A4Width + pageWidth)/2-54,1))+ '''" y = "'''+str (round((A4Height - pageHeight)/2 + 268,1))+ '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:end;fill:#e6e6ff;fill-opacity:1">'''+str (pubProg)+'''</text>

	<text x = "'''+str (round(A4Width/2,1))+ '''" y = "'''+str (round((A4Height - pageHeight)/2 + 342,1))+ '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:middle;fill:#e6e6ff;fill-opacity:1">'''+str (pubProg)+'''</text>

	<text x = "'''+str (round((A4Width - pageWidth)/2 + 54,1))+ '''" y = "'''+str (round((A4Height - pageHeight)/2 + 416,1))+ '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:start;fill:#e6e6ff;fill-opacity:1">'''+str (pubProg)+'''</text>

	<text x = "'''+str (round((A4Width + pageWidth)/2 - 10,1))+ '''" y = "'''+str (round((A4Height - pageHeight)/2 + 520 + 36,1))+ '''" style="font-family:DejaVu Sans;font-style:regular;font-weight:bold;font-size:68;text-anchor:end;fill:#e6e6ff;fill-opacity:1">'''+str (pubVers)+''' </text>

	<text x = "'''+str (round((A4Width - pageWidth)/2,1))+ '''" y = "'''+str (round((A4Height + pageHeight)/2 + 72,1))+ '''" style="font-family:DejaVu Sans;font-style:italic;font-size:10;text-anchor:start;fill:000000ff;fill-opacity:1">'''+str (addTxt)+'''</text></g></svg>''')

		fbackgr.close()        # GENERATION of background svg finished
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

factor = 72/25.4    # 1 mm = 72/25.4 pixels

aw = float(A4Width) * factor
ah = float(A4Height) * factor
pw = float(pageWidth) * factor
ph = float(pageHeight) * factor


# TEXT VARIABLES for publication program, publication version and additional
# information outside the page.
pubProg = "Rapuma"
pubVers = "DRAFT"
addTxt = "[sample text at the bottom of the page:] KYU-LATN-NT rom draft 2014-04-23"


#GENERATE A SVG of the watermark

draftsvg(aw,ah,pw,ph)


#   CONVERSION OF backgrSVG into backgrPDF with rsvg-convert
subprocess.call(["rsvg-convert", "-f", "pdf", "-o", backgrPDF, backgrSVG])

#   WATERMARKING procfile with backgrPDF
subprocess.call(["pdftk", procfile, "background", backgrPDF, "output", "markedDRAFT.pdf"])
