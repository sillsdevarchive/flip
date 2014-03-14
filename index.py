#!/usr/bin/python
# -*- coding: utf_8 -*-

###############################################################################
################################### Intro #####################################
###############################################################################
#
# Open with: "./extract.py wholeNT.pdf TOC.csv" with terminal opened in the
# workdirectory.
#
# This python script will generate a printed thumb index on the final version
# of a New Testament or whole Bible. In addition to the script a pdf of the
# whole NT/Bible and a list of start/end pages of individual bible books has
# to be supplied either in the workdirectory or with a full path.

# After setting up the environment (importing modules, defining initial
# settings, temporary file and arguments) the front matter, individual bible
# books and back matter are extracted from the whole NT/Bible.

# Per book a SVG file is generated for the odd and even index rectangles, these
# two files are converted into PDF with RSVG and stamped on the individual pages
# of the bible books. The odd and even stamped pages are then combined to the
# original book pdf.
#
# At the end all individual book pdf-pages are combined back to the
# whole NT/Bible.
#
###############################################################################
############################## Setup Environment ##############################
###############################################################################

import os, sys, shutil, re, codecs, subprocess, tempfile, pyPdf, csv, operator


# INITIAL SETTINGS
paperWidth = 483.02     # 6.71in at 72 dpi
paperHeight = 667.28    # 9.27in at 72 dpi

# DEFINITION OF VARIABLES
M_all_extracts = []         # list of appended individual bible book pdfs

# ARGUMENTS ENTERED AT THE TIME of calling the script, i.e.
# "./extract.py wholeNT.pdf TOC.csv", in which extract.py is sys.argv[0]
# (by default), wholeNT.pdf is sys.argv[1] and TOC.csv is sys.argv[2]
# More arguments may be added as needed

try :
	procfile = sys.argv[1]
	other = sys.argv[2]
except Exception as e :
	if str(e) == 'list index out of range' :
		sys.exit('\nMissing input file, must provide two input files:\n 1. pdf of the NT you want a print dummy of and\n 2. text file containing a list of start/end pages of individual bible books\n')
	else :
		sys.exit('Input file error: ' + str(e))

# The exists() (or similar) command could be used here to make sure that the file
# name given is real. I would do something like this

if not os.path.isfile(procfile) :
	msg = 'This file: ' + procfile + ' is no good!'
	sys.exit(msg)

if not os.path.isfile(other) :
	msg = 'This file: ' + other + ' is no good!'
	sys.exit(msg)

# PROGRESS
# The process of indexing process of a whole Bible or NT takes some time
# therefore the progress is make visible by some text and a sequence of
# greater-than signs '>'.

sys.stdout.write('\n Initiating proces')  # text to signal the end of the program
sys.stdout.flush()
print '\n Wait, working on indexing  ',          # forcing a blank line between last text and prompt

###############################################################################
################################ START PROGRAM ################################
######## SETTING UP TEMPORARY FILES AND ASSIGNING VALUES TO VARIABLES  ########
###############################################################################

# Open extractfile for reading
with codecs.open(other, 'rt') as contents :
	lines = contents.read().split('\n')     # read text line by line
	for l in lines:
		locate = l.split(',')
		if locate <> [""]:

# DEFINITION OF TEMPORARY FILES
# [a] individual books
			extract = tempfile.NamedTemporaryFile().name        # all individual bible books
																# both before and after processing
# [b] SVG and PDF files used in stamp generation
			svgodd = tempfile.NamedTemporaryFile().name         # SVG generated for odd page index
			svgeven = tempfile.NamedTemporaryFile().name        # SVG generated for even page index
			pdfodd = tempfile.NamedTemporaryFile().name         # PDF with odd page index stamp
			pdfeven = tempfile.NamedTemporaryFile().name        # PDF with odd page index stamp
# [c] Odd and even stamped pdfs
			out_odd = tempfile.NamedTemporaryFile().name        # book pdf containing odd pages
			out_index_odd = tempfile.NamedTemporaryFile().name  # book pdf containing stamped odd pages
			out_even = tempfile.NamedTemporaryFile().name       # book pdf containing even pages
			out_index_even = tempfile.NamedTemporaryFile().name # book pdf containing stamped even pages

# ASSIGNING VALUES TO VARIABLES
# [a] variables for extracting process
			count = float(locate[0])                    # counter as float of first content item
			firstPage = locate[1]                       # first page of bookpart - integer directly from TOC
			lastPage = locate[2]                        # last page of bookpart - integer next TOC value minus 1
			bookLen = firstPage + "-" + str (lastPage)  # number of pages of bookpart
			bookName = locate[3]                        # ParaText abbriviation to identify the book by default
														# can be replaced by language names in the sys.argv[2]

# [b] abcissas and ordinates of rectangles and text in svg generation
#           NOTE: page origin is top left corner of the page
			abcissa_odd = paperWidth -36 - 20       # distance left index rectangle in relation to page origin on odd pages
			abcissa_text_odd = abcissa_odd + 2.00   # starting point text instide index rectangle on odd pages
			abcissa_even = 36                       # distance left index rectangle in relation to page origin on even pages
			abcissa_text_even = abcissa_even + 3.00 # starting point text instide index rectangle on even pages
			ordinate = 165.00 + count*14.94         # distance top index rectangle in relation to page origin
			ordinate_text = ordinate + 7.00         # distance baseline text inside index rectangle in relation to page origin

###############################################################################
########################## EXTRACTING INDIVIDUAL BOOKS ########################
###############################################################################

# EXTRACTING THE PAGE PDF with
# subprocess call(["pdftk", "in.pdf" , "cat", "pages", "output", "out.pdf"])
# with in.pdf = procfile; pages = bookLen and out.pdf = extract

			subprocess.call(["pdftk", procfile, "cat", bookLen, "output", extract])

			M_all_extracts.append(str(extract)) # file names of extracted books are appended into
												# M_all_extracts, this list is used in the combination
												# of the individual stamped book pdfs at the end of
												# the indexing process

			if count <> 1.0:                    # Front matter will have no index and is left unchanged

#################################################################################
########################### GENERATE STAMP SVG FILEs ############################
#################################################################################
#     Open file
				with codecs.open(svgodd, 'wb') as fodd :        # for odd pages

#   Write the svg introduction and page size to the open file. This part will
#   always the same except of the paper dimensions defined in the initial
#   settings

					fodd.write( '''<?xml version="1.0" standalone="no"?>
	<!DOCTYPE svg SYSTEM "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
	<svg xmlns="http://www.w3.org/2000/svg"
		 version="1.1" width="''')
					fodd.write(str (paperWidth))
					fodd.write( '''" height="''')
					fodd.write(str (paperHeight))
					fodd.write( '''">
	  <g>
			<title>index for odd pages</title>
			<desc>
			SVG file with index rectangle on the right side of the odd page
			Position and text differ per bookName
		</desc>
		<rect
		   width = "20"
		   height = "10"
		   x = "''')
#   The x-values (abcissa) for odd and even pages are different because the index
#   rectangles in odd pages are on the right outside of the book, in even pages
#   they are on the right. The y-value (ordinate) is the same for odd and even,
#   however the values vary per individual book
					fodd.write(str (abcissa_odd))   # left side of the rectangle
					fodd.write( '''"\ny = "''')
					fodd.write(str (ordinate))      # top of the rectangle
					fodd.write('''"
		  style="fill:#000000;fill-opacity:1;stroke:#000000;stroke-width:0.31999999;stroke-linecap:square;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0" />
		   <text  x = "''')

#    The x and y-values for the text inside the index rectangles are different from
#    those of the rectangles
					fodd.write(str (abcissa_text_odd))  # start of text
					fodd.write( '''" y = "''')
					fodd.write(str (ordinate_text))     # position of text
					fodd.write('''"
		   style="font-family: Charis SIL;font-style:regular;font-size:7;fill:rgb(255,255,255)">''')
					fodd.write(str (bookName))          # ParaText or language book abbriviation
					fodd.write('''
		   </text>
	  </g>
	</svg>''')
					fodd.close()        # odd page svg closed

#     Open file
				with codecs.open(svgeven, 'wb') as feven :       # for even pages
#    Introduction same as odd
					feven.write( '''<?xml version="1.0" standalone="no"?>
	<!DOCTYPE svg SYSTEM "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
	<svg xmlns="http://www.w3.org/2000/svg"
		 version="1.1" width="''')
					feven.write(str (paperWidth))
					feven.write( '''" height="''')
					feven.write(str (paperHeight))
					feven.write( '''">
	  <g>
		<title>index  for even pages</title>
		<desc>
		  SVG file with index rectangle on the left side of the even page
		  Position and text differ per bookName
		</desc>
			this is for even pages
		<rect
		   width = "20"
		   height = "10"
		   x = "''')
					feven.write(str (abcissa_even))
					feven.write( '''"\ny = "''')
					feven.write(str (ordinate))
					feven.write('''"
		   style="fill:#000000;fill-opacity:1;stroke:#000000;stroke-width:0.31999999;stroke-linecap:square;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0" />
		   <text  x = "''')
					feven.write(str (abcissa_text_even))
					feven.write( '''" y = "''')
					feven.write(str (ordinate_text))
					feven.write('''"
					 style="font-family: Charis SIL;font-style:regular;font-size:7;fill:rgb(255,255,255)">''')
					feven.write(str (bookName))
					feven.write('''
		   </text>
	  </g>
	</svg>''')
					feven.close()        # even page svg closed

#################################################################################
######################### CONVERSION OF SVG TO STAMP PDF ########################
#################################################################################

# convert svgodd to pdfodd for odd pages of MAT thru REV
					subprocess.call(["rsvg-convert", "-f", "pdf", "-o", pdfodd, svgodd])

# convert svgeven to pdfeven for even pages of MAT thru REV
					subprocess.call(["rsvg-convert", "-f", "pdf", "-o", pdfeven, svgeven])

#################################################################################
#################### SPLITTING INDIVIDUAL BOOK PDF IN ODD/EVEN ##################
############################# AND ADDING INDEXSTAMPS  ###########################
#################################################################################
#                                                                               #
# The firstPage of individual bible books is not always an odd number, but can  #
# be even as well. Thumb indexes are positioned left on odd and right on even   #
# pages following the numbering of the original document. The odd/even property #
# of the extracted files has to be reversed in order to get a correct placement #
# of the thumb indexes in the final result.                                     #
#                                                                               #
#################################################################################

#    Generate a pdf with only odd pages
					if int(firstPage)%2 == 1:       # allowing for reversing odd to even
						subprocess.call(["pdftk", "A=" + extract, "cat", "Aodd", "output", out_odd])
						# if the firstPage value is odd and splitting is straightforward odd=odd
					else:
						subprocess.call(["pdftk", "A=" + extract, "cat", "Aeven", "output", out_odd])
						# if the firstPage value is even the splitting has to be reversed odd=even

#   Stamp odd pages with indexOdd.pdf
					subprocess.call(["pdftk", out_odd, "stamp", pdfodd, "output", out_index_odd])

#################################################################################

#   Generate a pdf with only even pages
					if int(firstPage)%2 == 1:       # allowing for reversing even to odd
						subprocess.call(["pdftk", "A=" + extract, "cat", "Aeven", "output", out_even])
						# if the firstPage value is odd splitting is straightforward even=even
					else:
						subprocess.call(["pdftk", "A=" + extract, "cat", "Aodd", "output", out_even])
						# in case the firsPage value is even the splitting has to reversed even=odd

#   Stamp even pages with indexEven.pdf
					subprocess.call(["pdftk", out_even, "stamp", pdfeven, "output", out_index_even])

#################################################################################
##################### COMBINING ODD/EVEN BACK TO ORIGINAL FILE ##################
#################################################################################

#   Combine odd and even pages to the original pdf now with indexes
					if int(firstPage)%2 == 1:       # to undo the earlier odd/even reversal
						subprocess.call(["pdftk", "A=" + out_index_odd, "B=" + out_index_even, "shuffle", "A", "B", "output", extract])
					else:
						subprocess.call(["pdftk", "A=" + out_index_even, "B=" + out_index_odd, "shuffle", "A", "B", "output", extract])

# PROGRESS
					sys.stdout.write('>')       # write a greater-than sign for every extract done
					sys.stdout.flush()          # stop the cursor from going to the next line

################################################################################
######################## GENERATING INDEXED BOOK FILE ##########################
################################################################################
#
#     The individual book files are combined in the single file 'whole_book_indexed.pdf'
#     which is the end-product of this operation

cmd = []
cmd.extend(["pdftk"])
cmd.extend(M_all_extracts)
cmd.extend(["cat", "output", "whole_book_indexed.pdf"])
#
subprocess.call(cmd)

# PROGRESS
sys.stdout.write('>>> indexing is done <<<')
sys.stdout.write('\n    >>> to see the result open whole_book_indexed.pdf  <<<')
					# text to signal the end of the program
#sys.stdout.flush()
print '\n'          # forcing a blank line between last text and prompt

# the final result is opened for inspection

os.system('xdg-open "whole_book_indexed.pdf"')
