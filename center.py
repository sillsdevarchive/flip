#!/usr/bin/python
# -*- coding: utf_8 -*-

###############################################################################
################################### Intro #####################################
###############################################################################
#
# This python script is using Ghostscript to manipulate PDFs so that a smaller
# pdf is placed in the center of a larger pdf.
#
# The page dimension of the smaller pdf, called the MEDIA, is to be read from
# the project's layoutconfig file. The papersize of the substraat on which the
# media is placed, the SHEET, is A4 by default, however, ghostscript 'knows' a
# lot more sizes. The dimension are in mm and converted to points at 72dpi.
#
# Ghostscript coordinates are measured from the left bottom corner, the
# ORIGIN. When combining a media with ghostscript on the sheet the origins of
# these documents co-incide. The media is centered on the sheet by moving it
# horizontally half the difference in width of sheet and media and vertically
# half the difference in height of sheet and media.
#
# The input file is called the string variable "media" and can be either a one
# or many pages. The output is called the string variable "centered". These
# variables are designated during the running of the script.
###############################################################################
############################## Setup Environment ##############################
###############################################################################

import os, sys, shutil, re,  subprocess, codecs

# INITIAL SETTINGS

def center(media, centered):
	"Ghostscript formula placing media in center of sheet"
	subprocess.call(["gs",  "-o", centered,  "-sDEVICE=pdfwrite",  "-dQUIET", "-sPAPERSIZE=a4",  "-dFIXEDMEDIA" , "-c", "<</PageOffset ["+pageoffset+"]>>", "setpagedevice", "-f", media])

# Size of media
mediaWidth = 148             # in mm, pageWidth from project layoutconfig
mediaHeight = 210            # in mm, pageHeight from project layoutconfig

# Sheet size A4 default
A4Width = 210           # in mm
A4Height = 297          # in mm

# Conversion factor mm to points
factor = 72/25.4

# Determining pageoffset
pagexoffset = ((A4Width - mediaWidth)/2) * factor
pageyoffset = ((A4Height - mediaHeight)/2) * factor

pageoffset = str(pagexoffset)+" "+str(pageyoffset)

centered = "output.pdf"
media = "MALpage.pdf"
center(media, centered)
