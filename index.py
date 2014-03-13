#!/usr/bin/python
# -*- coding: utf_8 -*-

import os, sys, shutil, re, codecs, subprocess, tempfile, pyPdf, csv, operator


# INITIAL SETTINGS
paperWidth = 483.02     # 6.71in at 72 dpi
paperHeight = 667.28    # 9.27in at 72 dpi


# Open extractfile for reading
with codecs.open('TOC_Short.csv', 'rt') as contents :
	lines = contents.read().split('\n')     # read text line by line
	for l in lines:
		locate = l.split(',')
		if locate <> [""]:

			count = float(locate[0])
			print count,
			firstPage = locate[1]
			print firstPage,
			lastPage = locate[2]
			print lastPage,
			bookLen = firstPage + "-" + str (lastPage)
			print bookLen,
			bookName = locate[3]
			print bookName
			extract = bookName + '.pdf'
			abcissa_odd = paperWidth -36 - 18
			abcissa_even = 36
			ordinate = 165.00 + count*14.94
			ordinate_text = ordinate + 7.00
			out_odd = bookName + '_odd.pdf'
			print out_odd
			out_index_odd = bookName + '_index_odd.pdf'
			out_even =bookName + '_even.pdf'
			out_index_even = bookName + '_index_even.pdf'
			out_index = bookName + '_index.pdf'

#        pdf = tempfile.NamedTemporaryFile().name
#        svg = tempfile.NamedTemporaryFile().name
#        Mpage = tempfile.NamedTemporaryFile().name
#        extract = tempfile.NamedTemporaryFile().name
#

#            fetch = locate[1]
#            print fetch
#        locate.pop(0)
#
## EXTRACTING THE PAGE PDF with pdftk
			subprocess.call(["pdftk", 'wholeNT.pdf', "cat", bookLen, "output", extract])
			if count <> 1.0:

##     Open file
#            with codecs.open('indexNull.svg', 'wb') as fnull :
#
##     Write the svg introduction and page size to the open file. This part is
##     always the same except of the paper dimensions defined in the initial
##     settings
#
#                fnull.write( '''<?xml version="1.0" standalone="no"?>
#<!DOCTYPE svg SYSTEM "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
#<svg xmlns="http://www.w3.org/2000/svg"
#     version="1.1" width="''')
#                fnull.write(str (paperWidth))
#                fnull.write( '''" height="''')
#                fnull.write(str (paperHeight))
#                fnull.write( '''">
#  <g>
#    <title>indexNull</title>
#    <desc>
#      SVG file without index rectangles for front and back matter
#    </desc>
#  </g>
#</svg>''')
#                fnull.close()

#     Open file
				with codecs.open('indexOdd.svg', 'wb') as fodd :

	#     Write the svg introduction and page size to the open file. This part is
	#     always the same except of the paper dimensions defined in the initial
	#     settings

					fodd.write( '''<?xml version="1.0" standalone="no"?>
	<!DOCTYPE svg SYSTEM "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
	<svg xmlns="http://www.w3.org/2000/svg"
		 version="1.1" width="''')
					fodd.write(str (paperWidth))
					fodd.write( '''" height="''')
					fodd.write(str (paperHeight))
					fodd.write( '''">
	  <g>
		<title>indexOdd</title>
		<desc>
		  SVG file without with an index rectangle on the outside of the page (odd right and even left side) for odd pages
		</desc>
			this is for odd pages
		<rect
		   width = "18"
		   height = "10"
		   x = "''')
					fodd.write(str (abcissa_odd))
					fodd.write( '''"\ny = "''')
					fodd.write(str (ordinate))
					fodd.write('''"
			style="fill:#000000;fill-opacity:1;stroke:#000000;stroke-width:0.31999999;stroke-linecap:square;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0" />
		   <text  x = "''')
					fodd.write(str (abcissa_odd))
					fodd.write( '''" y = "''')
					fodd.write(str (ordinate_text))
					fodd.write('''"
		   style="font-family: Charis SIL;font-style:regular;font-size:7;fill:rgb(255,255,255)">MAT</text>
	  </g>
	</svg>''')
					fodd.close()

	#     Open file
				with codecs.open('indexEven.svg', 'wb') as feven :

	#     Write the svg introduction and page size to the open file. This part is
	#     always the same except of the paper dimensions defined in the initial
	#     settings

					feven.write( '''<?xml version="1.0" standalone="no"?>
	<!DOCTYPE svg SYSTEM "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
	<svg xmlns="http://www.w3.org/2000/svg"
		 version="1.1" width="''')
					feven.write(str (paperWidth))
					feven.write( '''" height="''')
					feven.write(str (paperHeight))
					feven.write( '''">
	  <g>
		<title>indexEven</title>
		<desc>
		  SVG file without with an index rectangle on the outside of the page (even right and even left side) for even pages
		</desc>
			this is for even pages
		<rect
		   width = "18"
		   height = "10"
		   x = "''')
					feven.write(str (abcissa_even))
					feven.write( '''"\ny = "''')
					feven.write(str (ordinate))
					feven.write('''"
		   style="fill:#000000;fill-opacity:1;stroke:#000000;stroke-width:0.31999999;stroke-linecap:square;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0" />
		   <text  x = "''')
					feven.write(str (abcissa_even))
					feven.write( '''" y = "''')
					feven.write(str (ordinate_text))
					feven.write('''"
					 style="font-family: Charis SIL;font-style:regular;font-size:7;fill:rgb(255,255,255)">MAT</text>
	  </g>
	</svg>''')
					feven.close()

	# convert indexNull.svg to indexNull.pdf for FRT and TOP
#                    subprocess.call(["rsvg-convert", "-f", "pdf", "-o","indexNull.pdf", "indexNull.svg"])

	# convert indexOdd.svg to indexOdd.pdf for odd pages of MAT thru REV
					subprocess.call(["rsvg-convert", "-f", "pdf", "-o","indexOdd.pdf", "indexOdd.svg"])

	# convert indexEven.svg to indexEven .pdf for even pages of MAT thru REV
					subprocess.call(["rsvg-convert", "-f", "pdf", "-o","indexEven.pdf", "indexEven.svg"])
					print extract
#                    cmd_odd=[]
#                    cmd_odd.extend(["pdftk"])
#                    cmd_odd.extend(["A="])
#                    cmd_odd.extend([str(extract)])
#                    cmd_odd.extend(["cat"])
#                    cmd_odd.extend(["Aodd"])
#                    cmd_odd.extend(["output"])
#                    cmd_odd.extend([str(out_odd)])
#                    print cmd_odd
#    # Generate a pdf with only odd pages
#                    subprocess.call(cmd_odd)
					subprocess.call(["pdftk", "A=", extract, "cat", "Aodd", "output", out_odd])
#
#    # Stamp odd pages with indexOdd.pdf
#                    subprocess.call(["pdftk",  out_odd, "stamp indexOdd.pdf output", out_index_odd])
#
#    # Generate a pdf with only even pages
#                    subprocess.call(["pdftk", "A=", extract, "cat", "A", even, "output", out_even])
#
#    # Stamp even pages with indexEven.pdf
#                    subprocess.call(["pdftk", out_even, "stamp indexEven.pdf output", out_index_even])
#
#    # Combine odd and even pages to the original pdf now with indexes
#                    subprocess.call(["pdftk", "A=", out_index_odd, "B=", out_index_even, "shuffle A B output", out_index])
