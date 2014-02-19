#!/usr/bin/python
# -*- coding: utf_8 -*-

###############################################################################
################################### Intro #####################################
###############################################################################

# This python script will generate a SVG-file of a page with some explanatory
# text for print dummies of New Testaments.

# This SVG file is converted into a PDF-file with RSVG, which is then used
# to stamp the corresponding NT content page of the dummy.

# After all dummy pages have been stamped individually they are combined to a
# single document that can be sent to printshops as sample file.

# Paper dimensions are derived from the NT page and entered with 72 dpi

# The individual NT pages are generated with pdftk burst and saved in a
# sub folder of the python working folder.

# A list of dummy pages and stamptext has to be generated as csv file without
# quote marks, because the stamptext is read as string, later in in the process
# stamptext is changed into a list with split(',').

###############################################################################
############################## Setup Environment ##############################
###############################################################################

import os, sys, shutil, re, codecs, subprocess, tempfile

# Initial settings
paperWidth = 483.02     # 6.71in at 72 dpi
paperHeight = 667.28    # 9.27in at 72 dpi

stampfile = sys.argv[1]     # defines the input file at script command level
							# like "./stamp_sh.py dummyID_stamps_trunc"
							# in which "./stamp_sh.py" is sys.argv[0] and
							# "dummyID_stamps_trunc" is sys.argv[1]
#procfile = sys.argv[2]      # defines the process file like some whole NT pdf
							# used to extract individual dummy pages

# Sub folder containing the result of ptftk burst of the NT
burst = os.path.join(os.getcwd(), 'burst-docs')

# Variable settings
counter=0           # integer
M_all_page = []     # list of appended individual stamped pages
stamptext = ""

# Showing the progress of the script
print '\n'
sys.stdout.write('Reading stampfile and generating dummy.pdf   ')
sys.stdout.flush()
#print '\n'

#with codecs.open(stampfile, 'rt', 'utf_8_sig') as contents :
with codecs.open(stampfile, 'rt') as contents :
	lines = contents.read().split('\n')     # read stamp text by text line
	for l in lines:                         # loop through all stamp texts
		stamptext = l.split(',')            # stamptext string changed to list
		if stamptext <> [""] :              # this is to avoid that an empty
											# string is added at the end of
											# reading the lines of stampfile
			counter += 1

	# Set temporary filenames for svg, pdf, page and Mpage

			svg = tempfile.NamedTemporaryFile().name    # stamped page svg
			pdf = tempfile.NamedTemporaryFile().name    # stamped page pdf
			page = tempfile.NamedTemporaryFile().name   # individual NT page (dummy page)
			Mpage = tempfile.NamedTemporaryFile().name  # same with stamp

#            print pdf, svg, page, Mpage

	# The dummy page ID is the first item in the stamptext list. The dummy pages are in
	# the sub folder 'burst-docs' of the working folder, the content of the dummy pages
	# is copied and pasted into the temporary file 'page'.

			target = os.path.join(burst, stamptext[0])
			if os.path.isfile(target) :
				page = target
			stamptext.pop(0)

	###############################################################################
	############################ Generate svg file ################################
	###############################################################################

		# Open file
	#        with codecs.open(svg, 'wb', 'utf_8_sig') as fo :
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
				for txt in stamptext:
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


			# After generating the stamp page as svg it is converted to pdf with
			# subprocess.call(["rsvg-convert", "-f", "pdf", "-o", pdf, svg])

			subprocess.call(["rsvg-convert", "-f", "pdf", "-o", pdf, svg])

			# Then the content of the dummy pages 'page' are individually stamped
			# with the generated stamp pdf 'pdf', resulting in a stamped
			# dummy-page 'Mpage'

			subprocess.call(["pdftk", page, "stamp", pdf, "output", Mpage])


			# Mpage is a temporary file containing the stamped page, the file-names
			# are combined to one string by appending them to 'M_all_page

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
