#!/usr/bin/python
# -*- coding: utf_8 -*-

# By Flip Wester (flip_wester@sil.org)

###############################################################################
################################ INTRODUCTION #################################
###############################################################################
#
# Open with: "./line.py Rompage.pdf" while the terminal is opened in the
# workdirectory.
#
# This python script will generate a line grid for Rapuma projects on a rendered
# NT page. Page dimensions are extracted directly from the NT page with the pyPdf
# element "pdf.getPage(0).mediaBox" and coverted to float. Margin and fontsize
# values are imported from the layout config file.

# A SVG file is generated based page, margin and font values. The SVG is then
# converted to a PDF with RSVG-convert
#
# The end product is combined with a test pdf to a markedLINES pdf that may be
# opened to check the result.
# NOTE: This last bit is only to test not part of the current script
#
###############################################################################
############################## SETUP ENVIRONMENT ##############################
###############################################################################

# IMPORTS
import os, sys, codecs, subprocess, tempfile, pyPdf, configobj

# PAGE DIMENSIONS
from pyPdf import PdfFileReader
pdf = PdfFileReader(open("Rompage.pdf",'rb'))
var2 = pdf.getPage(0).mediaBox
pageWidth = var2.getWidth()
pageHeight = var2.getHeight()

# MARGIN AND FONT
from configobj import ConfigObj

layoutConfig = ConfigObj('layout.conf', encoding='utf-8')

topMargin           = layoutConfig['PageLayout']['topMargin']
bottomMargin        = layoutConfig['PageLayout']['bottomMargin']
outsideMargin       = layoutConfig['PageLayout']['outsideMargin']
insideMargin        = layoutConfig['PageLayout']['insideMargin']
bodyFontSize        = layoutConfig['TextElements']['bodyFontSize']
bodyTextLeading     = layoutConfig['TextElements']['bodyTextLeading']

# Definition of CROP MARK SVG function
def linesvg(paperPxWidth,paperPxHeight,topPxMargin,outsidePxMargin,insidePxMargin,bottomPxMargin,textPxWidth,bodyFontPxSize,bodyTextPxLeading) :
	"This function writes the SVG code for a linegrid, based on pagedimensions, margins body font and body leading"

	with codecs.open(backgrSVG, 'wb') as fbackgr :            # open file for writing
			# starting lines of SVG xml
		fbackgr.write( '''<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width = "'''+str (paperPxWidth)+ '''" height = "'''+str(paperPxHeight)+'''">
	\n    <!--RECTANGLE OF MARGINS-->\n''')
		fbackgr.write( '''<rect x = "'''+str (outsidePxMargin)+'''" y= "'''+str (topPxMargin)+'''" height = "'''+str (paperPxHeight - topPxMargin - bottomPxMargin)+'''" width = "'''+str (textPxWidth)+'''" style = "fill:#ffffff;fill-opacity:1;stroke:#ffc800;stroke-opacity:1;stroke-width:.2"/>
	\n    <!--START OF LINEGRID-->\n''')
		fbackgr.write( '''<path d= "m '''+str (outsidePxMargin * 0.75-1)+"," +str (topPxMargin + bodyFontPxSize)+" " +str (textPxWidth + outsidePxMargin * 0.25)+ ''',0''')
			# filling the space between the top line and bottom margin, starting at distance
			# counter num = 0 up to the but not including the total of num x leading
			# equals the distance between top and bottom margin
		num = 0
		while (num < int(round(paperPxHeight - bottomPxMargin - topPxMargin )/bodyTextPxLeading)):
				# lines are drawn in zigzag pattern: RTL when num is even and LTR when odd
			if num%2 == 0:
				fbackgr.write( ''' m 0, '''+str (bodyTextPxLeading)+" -" +str (textPxWidth + outsidePxMargin * 0.25)+ ''',0''')
			else:
				fbackgr.write( ''' m 0, '''+str (bodyTextPxLeading)+" " +str (textPxWidth + outsidePxMargin * 0.25)+ ''',0''')
			num = num +1
			# draw all lines with following style
		fbackgr.write( '''" style="stroke-width:0.2px;stroke:#ffc800;stroke-opacity:1"/>
	\n    <!--LINE NUMBERS-->\n''')
			# add line number '1' to top line just left of margin
		fbackgr.write( '''<text x="'''+str (outsidePxMargin * 0.75-2)+'''" y="'''+str (topPxMargin + bodyFontPxSize-3)+'''" style="font-family: Charis SIL;font-style:italic;font-size:7;fill:#760076"> 1''')
			# add line numbers to all lines down to bottom margin, starting with line number
			# counter linecount = 2, the distance counter runs from '0' till one short of
			# the quotient (distance between top and bottom margin)/bodyTextPxLeading
		num = 0         # line counter
		linenumber = 2   # line number
		while (num < int(round(paperPxHeight - bottomPxMargin - topPxMargin)/bodyTextPxLeading)):
			fbackgr.write( '''<tspan x="'''+str (outsidePxMargin * 0.75-2)+'''" dy="'''+str (bodyTextPxLeading)+'''">'''+str (linenumber)+'''</tspan>''')
			linenumber = linenumber +1
			num = num +1
		fbackgr.write('''</text>
	\n  <!--LINEGRID CAPTION-->
	<text  x="36" y="'''+str (paperPxHeight - bottomPxMargin+10)+'''" style="font-family: Charis SIL;font-style:italic;font-size:7;fill:#ffc800">page size: '''+str (int(paperPxWidth/72*25.4+.5))+''' x '''+str (int(paperPxHeight/72*25.4+.5))+''' mm ; font size: '''+str (bodyFontSize)+''' pt; leading: '''+str (bodyTextLeading)+''' pt</text>
	\n    <!--PURPLE LINES TOP AND BOTTOM MARGINS-->
	<path d="M '''+str (outsidePxMargin)+"," +str (topPxMargin)+" " +str (textPxWidth + outsidePxMargin)+"," +str (topPxMargin)+'''" style="fill:#ffffff;fill-opacity:1;stroke-width:0.4px;stroke:#760076;stroke-opacity:1"/>
	<path d="M '''+str (outsidePxMargin)+"," +str (paperPxHeight - bottomPxMargin)+" " +str (textPxWidth + outsidePxMargin)+"," +str (paperPxHeight - bottomPxMargin)+'''" style="fill:#ffffff;fill-opacity:1;stroke-width:0.4px;stroke:#760076;stroke-opacity:1"/>
	</svg>''')
		# Close opened file
		fbackgr.close()
	return


# CONVERSIONS OF IMPORTS TO [PX]
# The variable type of pageWidth and pageHeight can be 'int' or
# <class 'decimal.Decimal'>. In order to work properly in the linessvg
# function the variables dimensions have to be [px], the conversion is
# done by changing the variables' type to 'float'.

# paper height [px]
paperPxHeight = round(float(pageHeight),1)
# paper width [px]
paperPxWidth = round(float(pageWidth),1)

# The page dimensions extracted from layoutConfig are in [mm] and
# must be converted to pixels [px], the conversion factor for [mm]
# to [px] is 72/25.4

mmToPx = 72 / 25.4
# top margin [px]
topPxMargin = round(mmToPx * float(topMargin),1)
# outside margin [px]
outsidePxMargin = round(mmToPx * float(outsideMargin),1)
# inside margin [px]
insidePxMargin = round(mmToPx * float(outsideMargin),1)
# bottom margin [px]
bottomPxMargin = round(mmToPx * float(bottomMargin),1)

textPxWidth = paperPxWidth - (outsidePxMargin + insidePxMargin)

# The font and leading are given in TeX point [pt] and are converted
# to pixels [px], the conversion factor for [pt] to [px] is 72/72.27
# bodyFontSize [px]
bodyFontPxSize = round(float(bodyFontSize) * 72/72.27,3)
# bodyTextLeading [px]
bodyTextPxLeading = round(float(bodyTextLeading) * 72/72.27,3)

# INITIAL SETTINGS ./c
procfile = sys.argv[1]      # Rompage.pdf

# TEMPORARY FILES
#backgrSVG = "backgr.svg" #tempfile.NamedTemporaryFile().name  #"backgr.svg"
#backgrPDF = "backgr.pdf" #tempfile.NamedTemporaryFile().name  #"backgr.pdf"
backgrSVG = tempfile.NamedTemporaryFile().name  #"backgr.svg"
backgrPDF = tempfile.NamedTemporaryFile().name  #"backgr.pdf"

linesvg(paperPxWidth,paperPxHeight,topPxMargin,outsidePxMargin,insidePxMargin,bottomPxMargin,textPxWidth,bodyFontPxSize,bodyTextPxLeading)

#
###   CONVERSION OF stamp svg into stamp pdf with rsvg-convert
subprocess.call(["rsvg-convert", "-f", "pdf", "-o", backgrPDF, backgrSVG])

subprocess.call(["pdftk", procfile, "background", backgrPDF, "output", "markedLINES.pdf"])
