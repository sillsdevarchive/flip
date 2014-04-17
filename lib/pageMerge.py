#!/usr/bin/python
# -*- coding: utf_8 -*-


# Import only the Python modules we need
import subprocess

# Define the module class name
class PageMerge (object) :

	# Initialize the module when it is instantiated
	def __init__(self) :

		self.fgWidth    = 0
		self.fgHeight   = 0
		self.bgWidth    = 0
		self.bgHeight   = 0
		self.pageoffset = 0


	def center (self, inputFile, outputFile) :
		'''Main function of the module that runs a Ghostscript formula
		that places the media (forground) in center of sheet (background).'''

		subprocess.call(["gs",  "-o", outputFile,  "-sDEVICE=pdfwrite",  "-dQUIET", "-sPAPERSIZE=a4",  "-dFIXEDMEDIA" , "-c", "<</PageOffset [" + self.pageoffset + "]>>", "setpagedevice", "-f", inputFile])


	def calculate (self, fgWidth, fgHeight, bgWidth, bgHeight) :
		'''This will calculate offsets with the page dimensions given.'''

		# Conversion factor mm to points
		factor = 72/25.4

		# Determining pageoffset
		pagexoffset = ((bgWidth - fgWidth)/2) * factor
		pageyoffset = ((bgHeight - fgHeight)/2) * factor

		self.pageoffset = str(pagexoffset) + " " + str(pageyoffset)
