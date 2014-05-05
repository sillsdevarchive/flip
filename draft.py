#!/usr/bin/python
# -*- coding: utf_8 -*-

# By Flip Wester (flip_wester@sil.org)

###############################################################################
################################ INTRODUCTION #################################
###############################################################################
#
# Open with: "./draft.py KYUtest.py" while the terminal is
# opened in the workdirectory.
#
# This python script will generate a DRAFT watermark for Rapuma projects ona big
# sheet(A4 size) to define a rendered NT page (A5 size) and centered on the
# big sheet background. Page dimensions are extracted directly from the pdfs
# with the pyPdf element # "pdf.getPage(0).mediaBox" and coverted to float
#
# A SVG file is generated based on extracted sheet and page size. The SVG is
# converted to a PDF with RSVG-convert
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
import os, sys, codecs, subprocess, tempfile, pyPdf
from pyPdf import PdfFileReader

# INITIAL SETTINGS
procfile = sys.argv[1]      # wholeNT.pdf

# TEXT VARIABLES for publication program, publication version and additional
# information outside the page.
pubProg = "Rapuma"
pubVers = "DRAFT"
addTxt = "[sample text at the bottom of the page:] KYU-LATN-NT rom draft 2014-04-23"

# FUNCTION DEFINITION
def draftsvg(A4Width,A4Height,pageWidth,pageHeight):
	"This function writes the SVG code for the watermark"

	with codecs.open(backgrSVG, 'wb') as fbackgr :            # open file for writing

	#   SVG INTRODUCTION
		fbackgr.write( '''<svg xmlns="http://www.w3.org/2000/svg"
	version="1.1" width = "'''+str (A4Width)+'''" height = "'''+str (A4Height)+ '''">
	<g><text x = "'''+str ((A4Width - pageWidth)/2 + 54)+ '''" y = "'''+str ((A4Height - pageHeight)/2 + 120)+ '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:start;fill:#e6e6ff;fill-opacity:1">'''+str (pubProg)+'''
	<tspan x = "'''+str ((A4Width)/2)+ '''" y = "'''+str ((A4Height - pageHeight)/2 + 194)+ '''" style="text-anchor:middle">'''+str (pubProg)+'''</tspan>
	<tspan x = "'''+str ((A4Width + pageWidth)/2-54)+ '''" y = "'''+str ((A4Height - pageHeight)/2 + 268)+ '''" style="text-anchor:end">'''+str (pubProg)+'''</tspan>
	<tspan x = "'''+str (A4Width/2)+ '''" y = "'''+str ((A4Height - pageHeight)/2 + 342)+ '''" style="text-anchor:middle">'''+str (pubProg)+'''</tspan>
	<tspan x = "'''+str ((A4Width - pageWidth)/2 + 54)+ '''" y = "'''+str ((A4Height - pageHeight)/2 + 416)+ '''" style="text-anchor:start">'''+str (pubProg)+'''</tspan>
	<tspan x = "'''+str ((A4Width + pageWidth)/2 - 36)+ '''" y = "'''+str ((A4Height - pageHeight)/2 + 520 + 36)+ '''" style="font-weight:bold;font-size:68;text-anchor:end">'''+str (pubVers)+''' </tspan>
	<tspan x = "'''+str ((A4Width - pageWidth)/2)+ '''" y = "'''+str ((A4Height + pageHeight)/2 + 72)+ '''" style="font-style:italic;font-size:10;text-anchor:start;fill:#000000">'''+str (addTxt)+'''</tspan>
	</text></g></svg>''')

		fbackgr.close()        # GENERATION of background svg finished
	return

# TEMPORARY FILES
backgrSVG = "backgr.svg" #tempfile.NamedTemporaryFile().name  #"backgr.svg"
backgrPDF = "backgr.pdf" #tempfile.NamedTemporaryFile().name  #"backgr.pdf"

## DETERMINING PAGE DIMENSIONS

# Page dimensions can be determined with the pyPdf element "pdf.getPage(0).mediaBox",
# which results in a RectangleObject([0, 0, Width, Height])
# PDFs of a blank A4 and a rendered NT page (Rom of the KYU-LATN-NTCAT project) are
# used to determine the page dimensions in this script.

pdf = PdfFileReader(open("blankA4.pdf",'rb'))
var1 = pdf.getPage(0).mediaBox
bgWidth = var1.getWidth()
bgHeight = var1.getHeight().real

pdf = PdfFileReader(open("Rompage.pdf",'rb'))
var2 = pdf.getPage(0).mediaBox
smWidth = var2.getWidth()
smHeight = var2.getHeight()

# The variable type of bgWidth and bgHeight is: <type 'int'>, while smWidth
# and smHeight give <class 'decimal.Decimal'>. In order to work properly in
# the draftsvg function the variables have to be <type 'float'>:

aw = float (bgWidth)
ah = float (bgHeight)
pw = float (smWidth)
ph = float (smHeight)


#GENERATE A SVG of the watermark

draftsvg(aw,ah,pw,ph)


#   CONVERSION OF backgrSVG into backgrPDF with rsvg-convert
subprocess.call(["rsvg-convert", "-f", "pdf", "-o", backgrPDF, backgrSVG])

#   WATERMARKING procfile with backgrPDF
# this is only to test the result, it is not part of the watermark generation
subprocess.call(["pdftk", procfile, "background", backgrPDF, "output", "markedDRAFT.pdf"])











