#!/usr/bin/python
# -*- coding: utf_8 -*-

###############################################################################
################################ INTRODUCTION #################################
###############################################################################
#
# Open with: "./intro.py wholeNT.pdf introPages.csv" while the terminal is
# opened in the workdirectory.
#
# This python script will add pagenumbers to the introduction pages of the
# individual bible books of a New Testament or whole Bible. In addition to the
# script a pdf of the whole NT/Bible and a list of introduction pages of the
# individual books has to be supplied either in the workdirectory or with a
# full path. In this page list there is to be an indication if the introduction
# spills over to the next page.

# After setting up the environment (importing modules, defining initial
# settings, temporary file and arguments) a working copy is made of the whole
# NT/Bible pdf.

# The whole process is written as a function definition, in which a svg of the
# introduction page stamp is generated, converted and added to the appropriate
# content page. This is done for each introduction page mentioned in the list.
#
# The end product is written in the working pdf of the of the whole NT/Bible.
# After inspection this file is to be renamed to the original file name.
#
###############################################################################
############################## SETUP ENVIRONMENT ##############################
###############################################################################

# IMPORTS
import os, sys, shutil, re, codecs, subprocess, tempfile, csv, operator

# INITIAL SETTINGS
paperWidth = 483.02     # 6.71in at 72 dpi
paperHeight = 667.28    # 9.27in at 72 dpi#

# ARGUMENTS ENTERED AT THE TIME of calling the script, i.e.
# "./intro.py wholeNT.pdf introPages.csv", in which intro.py is sys.argv[0]
# (by default), wholeNT.pdf is sys.argv[1] and introPages.csv is sys.argv[2]
# More arguments may be added as needed

try :
	procfile = sys.argv[1]      # wholeNT.pdf
	other = sys.argv[2]         # introPages.csv
except Exception as e :         # Error message if either or both arguments are missing
	if str(e) == 'list index out of range' :
		sys.exit('\nMissing input file, you must provide two input files:\n 1. pdf of the NT you want a print dummy of and\n 2. text file containing a list of the start (introduction) pages of the individual bible books\n')
	else :
		sys.exit('Input file error: ' + str(e))

# The exists() command is used here to make sure that the file name given is real.

if not os.path.isfile(procfile) :
	msg = 'This file: ' + procfile + ' is no good!'
	sys.exit(msg)

if not os.path.isfile(other) :
	msg = 'This file: ' + other + ' is no good!'
	sys.exit(msg)

###############################################################################
################################## PROGRESS ###################################
###############################################################################
#                                                                             #
# The process of adding page numbers on the introduction pages of a whole     #
# Bible or NT takes some time therefore the progress is make visible by some  #
# explanatory text and a sequence of greater-than signs '>'.                  #
#                                                                             #
###############################################################################

sys.stdout.write('\n Initiating proces')
			# text to signal the progress of the program
sys.stdout.flush()
print '\n Wait, adding pagenumbers to book introduction pages \n    ',
			# forcing a blank line between last text and prompt

###############################################################################
#################### WORKING COPY AND FUNCTION DEFINITION #####################
###############################################################################
#                                                                             #
# To protect the whole text document (wholeNT.pdf) it is copied and renamed   #
# to the working file 'result.pdf'.                                           #
# The process of generating a stamp svg, converting it to a stamp pdf and     #
# implementing changes in 'result.pdf' is written a function. This enables    #
# multiple uses of the process without repeating the script.                  #
#                                                                             #
###############################################################################

# CREATING WORKING COPY of the whole text pdf
shutil.copy(procfile, 'result.pdf')

# FUNCTION DEFINITION.
# Temporary files are notified as comment between [] where they are used
def svg_pdf(stampSVG, stampPDF):
	"Generate a svg of the introduction page stamp; convert to pdf; stamp the appropriate introduction page (from other) and combine with contents (procfile)"

	with codecs.open(stampSVG, 'wb') as fstamp :            # open file for writing [stampSVG]

	#   SVG INTRODUCTION
		fstamp.write( '''<svg xmlns="http://www.w3.org/2000/svg"
version="1.1" width="''')

	#   PAGE DIMENSIONS
		fstamp.write(str (paperWidth))
		fstamp.write( '''" height="''')
		fstamp.write(str (paperHeight))
		fstamp.write( '''">
<g><text  x = "''')

	#   GENERATING POSITION and defining appearance of page number
		fstamp.write(str (abcissa_text))    # horizonatal position of page number
		fstamp.write( '''" y = "''')
		fstamp.write(str (ordinate_text))   # vertical position of page number
		fstamp.write( '''" style="font-family: Charis SIL;font-style:regular;font-size:10;text-anchor:middle">''')    # font and anchor

	#   ADDING THE ACTUAL PAGE number in the right position
		fstamp.write(str (actualPage))      # actual page number
		fstamp.write('''</text></g>
</svg>''')
		fstamp.close()        # GENERATION of stamp svg finished

	#   CONVERSION OF stamp svg into stamp pdf with rsvg-convert [stampPDF]
	subprocess.call(["rsvg-convert", "-f", "pdf", "-o", stampPDF, stampSVG])

	#   EXTRACTING the introduction page [intP]
	subprocess.call(["pdftk", procfile, "cat", introPage, "output", intP])

	#   STAMPING the introduction page with page number [stamped]
	subprocess.call(["pdftk", intP, "stamp", stampPDF, "output", stamped])

	#   DETERMINING page ranges before and after introduction page
	before = "1-" + str(int(introPage) - 1)  # 'before' from page 1 up to introduction page
	after = str(int(introPage) + 1) + "-end"  # 'after' from page following introduction page to end

	#   EXTRACTING page ranges before and after introduction page [firstpart, lastpart]
	subprocess.call(['pdftk', 'A=result.pdf', 'cat', before,'output', firstpart])
	subprocess.call(['pdftk', 'A=result.pdf', 'cat', after,'output', lastpart])

	#   COMBINING page ranges and introduction page back to whole
	subprocess.call(['pdftk', firstpart, stamped, lastpart, 'output', 'resultstamped.pdf'])

	#   RENAMING combined pages to working pdf. This is needed to allow defining
	#   'A=result.pdf' in the generation of [firstpart] and [lastpart] for the next
	#   introduction page.
	os.rename('resultstamped.pdf', 'result.pdf')

#---------------------------------------------------------------------------------
# PROGRESS
	sys.stdout.write('>')       # write a greater-than sign for every extract done
	sys.stdout.flush()          # stop the cursor from going to the next line
#---------------------------------------------------------------------------------

	return()                    # END OF FUNCTION

###############################################################################
################################ START PROGRAM ################################
######## DEFINING TEMPORARY FILES AND ASSIGNING VALUES TO VARIABLES  ##########
###############################################################################

# DEFINITION OF TEMPORARY FILES
stampSVG = tempfile.NamedTemporaryFile().name   # stamp image generated as svg
stampPDF = tempfile.NamedTemporaryFile().name   # stamp image converted to pdf
intP = tempfile.NamedTemporaryFile().name       # extracted introduction page pdf
stamped = tempfile.NamedTemporaryFile().name    # intP stamped with stampPDF
firstpart = tempfile.NamedTemporaryFile().name  # page range before introduction page
lastpart = tempfile.NamedTemporaryFile().name   # page range after introduction page

#Open extractfile for reading
with codecs.open(other, 'rt') as contents :
	lines = contents.read().split('\n')     # read text line by line
	for l in lines:
		locate = l.split(',')
		if locate <> [""]:
			# ASSIGNMENT OF VALUES TO VARIABLES
			count = locate[0]                   # counter
			introPage = locate[1]               # page number of introduction in whole NT
			actualPage = locate[2]              # page number as entered on the page
			abcissa_text = (paperWidth)/2       # horizontal position of page number
			ordinate_text = 615                 # vertical position of page number bottom
			secondIntroPage = locate[3]         # introduction spills to next page: yes/no
			svg_pdf(stampSVG, stampPDF)         # run function

			if secondIntroPage == 'yes':
				# CHANGING VALUES OF VARIABLES FOR TWO PAGE INTRODUCTIONS
				introPage = str (int(locate[1]) + 1)    # next page number in document
				actualPage = str (int(locate[2]) + 1)   # next page number on page
				abcissa_text = (paperWidth)/2           # horizontal position of page number
				ordinate_text = 63                      # vertical position of page number top
				svg_pdf(stampSVG, stampPDF)             # run function

#---------------------------------------------------------------------------------
# PROGRESS
sys.stdout.write('>>> numbering is done <<<')
sys.stdout.write('\n    >>> to see the result open result.pdf  <<<')
					# text to signal the end of the program
#sys.stdout.flush()
print '\n'          # forcing a blank line between last text and prompt

#---------------------------------------------------------------------------------

# FINAL RESULT
# the final result is opened for inspection

os.system('xdg-open "result.pdf"')
