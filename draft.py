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
topMargin = layoutConfig['PageLayout']['topMargin']
bottomMargin = layoutConfig['PageLayout']['bottomMargin']
outsideMargin = layoutConfig['PageLayout']['outsideMargin']
insideMargin = layoutConfig['PageLayout']['insideMargin']

# The values stored in the config are strings and in mm. To convert them to
# pixels the need to be changed to float().

factor = 72/25.4    # 1 mm = 72/25.4 pixels

aw = float(A4Width) * factor
ah = float(A4Height) * factor
pw = float(pageWidth) * factor
ph = float(pageHeight) * factor
tm = float(topMargin) * factor
bm = float(bottomMargin) * factor
om = float(outsideMargin) * factor
im = float(insideMargin) * factor

# CALCULATION OF CO-ORDINATES. The page size of the publication is in
# the range of A5. To center this page on a A4 bacground all items of
# the page have to be moved half the difference of sheet and page
# horizontally and vertically.

# HORIZONTAL (ABCISSA)
x1 = (aw - pw)/2 + 54               # 1st pubProg text ('Rapuma') about 20 mm
									# from left page border
x2 = (aw - pw)/2 +pw/2              # 2nd pubProg text centered on page
x3 = (aw - pw)/2 +pw -54            # 3rd pubProg text 20 mm from right page border
x4 = (aw - pw)/2 +pw/2              # 4th pubProg text centered on page
x5 = (aw - pw)/2 + 54               # 5th pubProg text 20 mm from left page border
x6 = (aw - pw)/2 +pw - (im+om)/2    # pubVers text flush with right margin
x7 = (aw - pw)/2                    # addTxt text flush with left page border

# VERTICAL (ORDINATE) pubProg and pubVers text are repeatedly positioned on 1/6
# of the text area. The pubVers text ('DRAFT') is positioned on the bottom margin.
# The addTxt is 25 mm below the lower page border.
y1 = (ah - ph)/2 + (ph - tm - bm)/6
y2 = (ah - ph)/2 + 2*(ph - tm - bm)/6
y3 = (ah - ph)/2 + 3*(ph - tm - bm)/6
y4 = (ah - ph)/2 + 4*(ph - tm - bm)/6
y5 = (ah - ph)/2 + 5*(ph - tm - bm)/6
y6 = (ah - ph)/2 + 6*(ph- bm)/6
y7 = (ah - ph)/2 + ph + 72

# TEXT VARIABLES for publication program, publication version and additional
# information outside the page.
pubProg = "Rapuma"
pubVers = "DRAFT"
addTxt = "[sample text at the bottom of the page:] KYU-LATN-NT rom draft 2014-04-23"


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

<g><text x = "''')
	fbackgr.write(str (x1))
	fbackgr.write( '''" y = "''')
	fbackgr.write(str (y1))
	fbackgr.write( '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:start;fill:#e6e6ff;fill-opacity:1">''')
	fbackgr.write(str (pubProg))    #Rapuma 1
	fbackgr.write('''</text>

<text x = "''')
	fbackgr.write(str (x2))
	fbackgr.write( '''" y = "''')
	fbackgr.write(str (y2))
	fbackgr.write( '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:middle;fill:#e6e6ff;fill-opacity:1">''')
	fbackgr.write(str (pubProg))   #Rapuma 2
	fbackgr.write('''</text>

<text x = "''')
	fbackgr.write(str (x3))
	fbackgr.write( '''" y = "''')
	fbackgr.write(str (y3))
	fbackgr.write( '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:end;fill:#e6e6ff;fill-opacity:1">''')
	fbackgr.write(str (pubProg))   #Rapuma 3
	fbackgr.write('''</text>

<text x = "''')
	fbackgr.write(str (x4))
	fbackgr.write( '''" y = "''')
	fbackgr.write(str (y4))
	fbackgr.write( '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:middle;fill:#e6e6ff;fill-opacity:1">''')
	fbackgr.write(str (pubProg))   #Rapuma 4
	fbackgr.write('''</text>

<text x = "''')
	fbackgr.write(str (x5))
	fbackgr.write( '''" y = "''')
	fbackgr.write(str (y5))
	fbackgr.write( '''" style="font-family:DejaVu Sans;font-style:regular;font-size:32;text-anchor:start;fill:#e6e6ff;fill-opacity:1">''')
	fbackgr.write(str (pubProg))   #Rapuma 5
	fbackgr.write('''</text>

<text x = "''')
	fbackgr.write(str (x6))
	fbackgr.write( '''" y = "''')
	fbackgr.write(str (y6))
	fbackgr.write( '''"
 style="font-family:DejaVu Sans;font-style:regular;font-weight:bold;font-size:68;text-anchor:end;fill:#e6e6ff;fill-opacity:1">''')
	fbackgr.write(str (pubVers))    # DRAFT
	fbackgr.write(''' </text>

<text x = "''')
	fbackgr.write(str (x7))
	fbackgr.write( '''" y = "''')
	fbackgr.write(str (y7))
	fbackgr.write( '''" style="font-family:DejaVu Sans;font-style:italic;font-size:10;text-anchor:start;fill:000000ff;fill-opacity:1">''')
	fbackgr.write(str (addTxt))     # [sample text at the bottom of the page:] KYU-LATN-NT rom draft 2014-04-23
	fbackgr.write('''</text></g></svg>''')

	fbackgr.close()        # GENERATION of background svg finished


#   CONVERSION OF stamp svg into stamp pdf with rsvg-convert
subprocess.call(["rsvg-convert", "-f", "pdf", "-o", backgrPDF, backgrSVG])

#   WATERMARKING wholeNT with backgrPDF
subprocess.call(["pdftk", procfile, "background", backgrPDF, "output", "markedDRAFT.pdf"])
