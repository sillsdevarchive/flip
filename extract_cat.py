#!/usr/bin/python
# -*- coding: utf_8 -*-

import os, sys, shutil, re, codecs, subprocess, tempfile, pyPdf

# HI DENNIS WOULD YOU PLEASE LOOK AT THIS SCRIPT? IT WILL AUTOMATICALLY GENERATE
# A DUMMY OR SIGNATURE PAGES. I WOULD LIKE TO AUTOMATICALLY ADD THE FRONT AND BACK
# MATTER, BUT COULD NOT FIND A WAY TO SORT THE LINES AFTER COMBINING THE FILES.


# Initial settings
paperWidth = 483.02     # 6.71in at 72 dpi
paperHeight = 667.28    # 9.27in at 72 dpi

# Arguments entered at the time of calling the script, i.e.
# ./extract.py extract wholeNT.pdf, in which extract.py is sys.argv[0]
# (by default) extract is sys.argv[1] and  wholeNT.pdf sys.argv[2].
# More arguments may be added as needed

extractfile = sys.argv[1]
#print sys.argv[1]
procfile = sys.argv[2]
#print sys.argv[2]

# Determine the number of pages in the procfile pdf document

from pyPdf import PdfFileReader
pdf = PdfFileReader(open(procfile))
pdf.getNumPages()
allPages = pdf.getNumPages()

#allPages = 144                # by commenting/uncommenting the value
# in this and previous line allPages can be given another value to
# try out the code below

count = 0           # number of signatures
countp = 0          # number of extracted pages
M_all_page = []     # list of appended individual stamped pages
locate = ""



###############################################################################
############################# Number of signatures ############################
###############################################################################
#                                                                             #
# NTs are bound with smyth sewing in signatures of 32 pages, as an exception  #
# it is allowed to use one 16 page signature in the NT, provided it is not    #
# the last one in the book. The total pagecount has to be a multiple of 16,   #
# if not the contents have to be extended with blank pages.                   #
# This is to test how many 32 page signatures there are and how many 16 page  #
# lots there are in a given NT.                                               #
###############################################################################

print ('\n')
num32pSign = allPages/32           # number of 32 page signatures
num16pSign = allPages/16           # number of 16 page lots, if this is
								   # an odd number there will be a 16 page
								   # signature
print "half signature? ",
if num16pSign%2 == 1:              # Modulus 2 of num16pSign will give
	print " True"                  # 1 when the integer is odd
else:
	print " False"                 # 0 when the integer is even
print ('\n')


###############################################################################
######################### Begin and end of signatures #########################
###############################################################################
#                                                                             #
# Calculate the start/end signature pages and write them in extractfile.      #
# Between begin and end of a signature are 31 pages                           #
# While count is less than the total number of signatures the calculation is  #
# countsimple addition of 31 pages between the first and last page of the     #
# signature (or 32 pages from start to start of the next)                     #
###############################################################################

with codecs.open(extractfile, 'wb') as fo :
	while count != num32pSign:
		if count <> 0:                      # count is the signature number
			page = 0 + count * 32           # end of signature
											# end signature 0 does not exist!
#            print page, count
			fo.write(page.__str__())        # write signature end page number
			fo.write(''', End of Signature ''')
			fo.write(count.__str__())       # write signature number
			fo.write('''\n''')
			page = 1 + count * 32           # start of signature
											# signature 1 is a special case!
#            print page, count + 1
			fo.write(page.__str__())        # write next signature start number
			fo.write(''', Start of Signature ''')
			fo.write((count + 1).__str__()) # write next signature number
			fo.write('''\n''')
		count += 1

# In case there is a half signature and it has signature number has the value
# num32pSign. Another 32 page signature is added following.

	while count == num32pSign and num16pSign%2 == 1:

		page = page + 15                # there are 15 pages between start and end
#        print page, count
		fo.write(page.__str__())        # end page
		fo.write(''', End of Signature ''')
		fo.write(count.__str__())       # signature num32pSign
		fo.write(''', CAUTION 16 page signature''')
		fo.write('''\n''')
		page = page + 1
#        print page, count + 1
		fo.write(page.__str__())        # last start page
		fo.write(''', Start of Signature ''')
		fo.write((count + 1).__str__()) # signature num32pSign + 1
		fo.write('''\n''')
		count += 1
		page = page + 31                # there are 31 pages between start and end
#        print page, count
		fo.write(page.__str__())        # last end page
		fo.write(''', End of Signature ''')
		fo.write(count.__str__())
		fo.write(''', last printed page''')
		fo.write('''\n''')

# When there is no half signature the last signature counts 32 pages
# (add 31 to the last start page)

	if num16pSign%2 == 0:
		page = page + 31
#        print page, count
		fo.write(page.__str__())
		fo.write(''', End of Signature ''')
		fo.write(count.__str__())
		fo.write(''', last printed page''')
		fo.write('''\n''')

###############################################################################
######################### Extract begin and end pages #########################
###############################################################################

# Open extractfile for writing
	with codecs.open(extractfile, 'rt') as contents :
		lines = contents.read().split('\n')     # read text by text line
		for l in lines:
			locate = l.split(',')
			if locate <> [""]:
				countp += 1
				fetch = locate[0]
				stamptext = locate[1]

# Substitute filenames for stamp svg and resulting pdf
# These will to changed in tempfiles later
#                pdf = "stamp" + fetch + ".pdf"
#                svg = "stamp" + fetch + ".svg"
#                Mpage = "stamped" + fetch + ".pdf"
#                extract = "page_" + fetch + ".pdf"

# Set temporary filenames for svg, pdf, Mpage and extract

				pdf = tempfile.NamedTemporaryFile().name
				svg = tempfile.NamedTemporaryFile().name
				Mpage = tempfile.NamedTemporaryFile().name
				extract = tempfile.NamedTemporaryFile().name

# extracting the page pdf with pdftk
				subprocess.call(["pdftk", procfile, "cat", fetch, "output", extract])


################################################################################
########################## Generate stamp svg file #############################
################################################################################
		# Open file
				with codecs.open(svg, 'wb') as fo :

				# write the svg introduction and page size to the open file

					fo.write( '''<?xml version="1.0" standalone="no"?>
					<!DOCTYPE svg SYSTEM "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
					<svg xmlns="http://www.w3.org/2000/svg"
						 version="1.1" width="''')
					fo.write(str (paperWidth))
					fo.write( '''" height="''')
					fo.write(str (paperHeight))
					fo.write( '''">
					  <g>
					<title>dummy_stamp</title>
						<desc>
						  This a sheet with a few lines of text to be used as stamp for dummys.
						</desc>

					<!-- LINES OF TEXT TO BE USED AS STAMP IN dummy PAGES -->

						<text  y="19.4" style="font-family: Charis SIL;font-style:normal;font-size:12;fill:rgb(255,0,0)">''')

				# Generating the line(s) of text to be placed on the stamped page

					for txt in stamptext.split(','):
						frst=txt
						fo.write('''   <tspan  x="78.9" dy="15">''')
						fo.write(str (frst))
						fo.write('''</tspan>\n''')
					fo.write('''    </text>
					  </g>
					</svg>''')

###############################################################################
#################### Convert svg and generate stamp pages #####################
###############################################################################


			# After generating the stamp page as svg it is converted to pdf
			# with subprocess.call(["rsvg-convert", "-f", "pdf", "-o", pdf, svg])

			subprocess.call(["rsvg-convert", "-f", "pdf", "-o", pdf, svg])

			# Then the content of the dummy pages 'extract' are individually
			# stamped with the generated stamp pdf 'pdf', resulting in a
			# single dummy-page 'Mpage'

			subprocess.call(["pdftk", extract, "stamp", pdf, "output", Mpage])


			# Mpage is a temporary file containing the stamped page, the file
			# names are combined to one string by appending them to 'M_all_page

			sys.stdout.write('>')       # write a dot for every Mpage done
			sys.stdout.flush()          # stop the cursor from going to the next line


			M_all_page.append(str(Mpage))


###############################################################################
########################## Generating dummy file# #############################
###############################################################################

	# The individual dummy pages are combined in the single file 'dummy.pdf'
	# which is the end-product of this operation

	cmd = []
	cmd.extend(["pdftk"])
	cmd.extend(M_all_page)
	cmd.extend(["cat", "output", "dummy.pdf"])

	subprocess.call(cmd)


	sys.stdout.write('>>> dummy.pdf DONE <<<')  # text to signal the end of the program
	sys.stdout.flush()
	print '\n'          # forcing a blank line between last text and prompt
