#!/usr/bin/python
# -*- coding: utf_8 -*-

# By Flip Wester (flip_wester@sil.org)

###############################################################################
################################ INTRODUCTION #################################
###############################################################################
#
# Open with: "./crop.py KYUtest.pdf" while the terminal is
# opened in the workdirectory.
#
# This python script will generate cropmarks for Rapuma projects on a big
# sheet(A4 size) to define a rendered NT page (A5 size) and centered on the
# big sheet background. Page dimensions are extracted directly from the pdfs
# with the pyPdf element # "pdf.getPage(0).mediaBox" and coverted to float.
#
# A SVG file is generated based on extracted sheet and page size. The SVG is
# converted to a PDF with RSVG-convert
#
# The end product is combined with a test pdf to a markedCROP pdf that may be
# opened to check the result.
# NOTE: This last bit is only to test not part of the current script
#
###############################################################################
############################## SETUP ENVIRONMENT ##############################
###############################################################################

# IMPORTS
import os, sys, codecs, subprocess, tempfile, pyPdf
from pyPdf import PdfFileReader

# INITIAL SETTINGS ./c
procfile = sys.argv[1]      # KYUtest.pdf

# Definition of CROP MARK SVG function
def cropsvg(A4Width, A4Height,pageWidth,pageHeight) :
	"This function writes the SVG code for crop lines, original co-ordinates are top left x and y"

	with codecs.open(backgrSVG, 'wb') as fbackgr :            # open file for writing

				# starting lines of SVG xml
		fbackgr.write( '''<svg xmlns="http://www.w3.org/2000/svg"
version="1.1" width = "'''+str (A4Width)+ '''" height = "'''+str(A4Height)+'''">\n''')
				# vertical top left
		fbackgr.write( '''<path d = "m'''+str ((A4Width - pageWidth)/2)+''','''+str ((A4Height - pageHeight)/2 - 32.0)+''',v27," style="stroke:#000000;stroke-width:.2"/>\n''')
				# vertical bottom left
		fbackgr.write( '''<path d = "m'''+str ((A4Width - pageWidth)/2)+''','''+str ((A4Height + pageHeight)/2 + 5.0)+''',v27" style="stroke:#000000;stroke-width:.2" />\n''')
				# vertical bottom right
		fbackgr.write( '''<path d = "m'''+str ((A4Width + pageWidth)/2)+''','''+str ((A4Height - pageHeight)/2 - 32.0)+''',v27" style="stroke:#000000;stroke-width:.2"/>\n''')
				# vertical top right
		fbackgr.write( '''<path d = "m'''+str ((A4Width + pageWidth)/2)+''','''+str ((A4Height + pageHeight)/2 + 5.0)+''',v27" style="stroke:#000000;stroke-width:.2" />\n''')
				# horzontal top left
		fbackgr.write( '''<path d =" m'''+str ((A4Width - pageWidth)/2 - 32.0)+''','''+str ((A4Height - pageHeight)/2)+''',h27" style="stroke:#000000;stroke-width:.2" />\n''')
				# horzontal top right
		fbackgr.write( '''<path d =" m'''+str ((A4Width + pageWidth)/2 + 5.0)+''','''+str ((A4Height - pageHeight)/2)+''',h27" style="stroke:#000000;stroke-width:.2" />\n''')
				# horzontal bottom right
		fbackgr.write( '''<path d =" m'''+str ((A4Width - pageWidth)/2 - 32.0)+''','''+str ((A4Height + pageHeight)/2)+''',h27" style="stroke:#000000;stroke-width:.2" />\n''')
				# horzontal bottom left
		fbackgr.write( '''<path d =" m'''+str ((A4Width + pageWidth)/2 +5.0)+''','''+str ((A4Height + pageHeight)/2)+''',h27" style="stroke:#000000;stroke-width:.2" />\n''')
		fbackgr.write( '''</svg>''')

		fbackgr.close()                                         # close file for writing
	return

# TEMPORARY FILES
backgrSVG = tempfile.NamedTemporaryFile().name  #"backgr.svg"
backgrPDF = tempfile.NamedTemporaryFile().name  #"backgr.pdf"

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

# The variable type of bgWidth and bgHeight is 'int', while smWidth and
# smHeight are <class 'decimal.Decimal'>. In order to work properly in
# the cropsvg function the variables are changed to 'float'.

aw = float (bgWidth)
ah = float (bgHeight)
pw = float (smWidth)
ph = float (smHeight)


# GENERATE A SVG of the crop marks; convert to pdf

cropsvg(aw,ah,pw,ph)

##   CONVERSION OF stamp svg into stamp pdf with rsvg-convert
subprocess.call(["rsvg-convert", "-f", "pdf", "-o", backgrPDF, backgrSVG])

##   Add cropmarks to procfile with backgrPDF
# this is only to test the result, it is not part of the crop mark generation
subprocess.call(["pdftk", procfile, "background", backgrPDF, "output", "markedCROP.pdf"])
