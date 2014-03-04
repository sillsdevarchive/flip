#!/usr/bin/python
# -*- coding: utf_8 -*-

import os, sys, shutil, re, codecs, subprocess, tempfile, pyPdf, csv, operator


# INITIAL SETTINGS
paperWidth = 483.02     # 6.71in at 72 dpi
paperHeight = 667.28    # 9.27in at 72 dpi

count = 0           # counter for signatures
countp = 0          # counter  of extracted pages
M_all_page = []     # list of appended individual stamped pages
locate = ""         # content of extractfile

# TEMPORARY FILES
combination = tempfile.NamedTemporaryFile().name
content = tempfile.NamedTemporaryFile().name
text = tempfile.NamedTemporaryFile().name
alltext = tempfile.NamedTemporaryFile().name
signature = tempfile.NamedTemporaryFile().name

# ARGUMENTS ENTERED AT THE TIME of calling the script, i.e.
# "./extract.py wholeNT.pdf", in which extract.py is sys.argv[0]
# (by default)and wholeNT.pdf is sys.argv[1].
# More arguments may be added as needed

procfile = sys.argv[1]

# DETERMINE THE NUMBER OF PAGES in the procfile pdf document

# pages in procfile
from pyPdf import PdfFileReader
pdf = PdfFileReader(open(procfile))
pdf.getNumPages()
allPages = pdf.getNumPages()

# less pages for testing
#allPages = 144               # by commenting/uncommenting the value
# in this and previous line allPages can be given another value to
# try out the code below

###############################################################################
############################# NUMBER OF SIGNATURES ############################
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
print "Short Signature? ";
if num16pSign%2 == 1:
	print "Yes, the modulus 2 of the number of 16 page lots is 1"
#       Modulus 2 of num16pSign will give 1 when the integer is odd
else:
	print "No, the modulus 2 of the number of 16 page lots is 0 "
#       and 0 when the integer is even
print ('\n')


###############################################################################
######################### BEGIN AND END OF SIGNATURES #########################
###############################################################################
#                                                                             #
# Calculate the start/end signature pages and write them in extractfile.      #
# Between begin and end of a signature are 31 pages                           #
# While count is less than the total number of signatures the calculation is  #
# countsimple addition of 31 pages between the first and last page of the     #
# signature (or 32 pages from start to start of the next)                     #
# The results of the calculation are written to the file 'signatures'.        #
###############################################################################

# SIGNATURE PAGES NUMBERS ARE GENERATED from second to penultimate

begSig = ", Start of Signature "
endSig = ", End of Signature "

with codecs.open(signature, 'wb') as fo :
	while count != num32pSign:
		if count <> 0:            # count is the signature number
			page = 0 + count * 32 # end of signature
								  # end signature 0 does not exist!

			fo.write(page.__str__().zfill(3))
#               page.__str__().zfill(3) ->  write signature end page number zfill(3)
#               is filling the numbers with leading zeros so they are all three digits long
#              and 001 will be the start figure when sorting the list
			fo.write(str (endSig))
#              str (endSig) -> end signature text
			fo.write(count.__str__())
#               count.__str__() ->  signature number
			fo.write('''\n''')
#               '\n' -> new line

			page = 1 + count * 32 # start of signature
								  # signature 1 is a special case!

			fo.write(page.__str__().zfill(3))
#               page.__str__().zfill(3) -> write next signature start number with leading zeros
			fo.write(str (begSig))
#               str (begSig) -> start signature text
			fo.write((count + 1).__str__())
#               count + 1).__str__() -> next signature number
	# IN CASE THERE IS a half signature the penultimate signature will be
	# the 16 page signature, this is added in the stamptext
			if count == num32pSign-1 and num16pSign%2 == 1:
				fo.write(''', CAUTION 16 page signature''')
#                   add  16 page warning
			fo.write('''\n''')
#               finish with new line
		count += 1

# IN CASE THERE IS A HALF SIGNATURE this is left out of the total figure. The signature configuration
# is completed with these 16 pages and a final 32 pages signature

	while count == num32pSign and num16pSign%2 == 1:

		page = page + 15
#           End of 16 page signature; there are 15 pages between start and end
#           because the LHS of page has the value of the RHS of the last start
#           number, hence only 15 is added

		fo.write(page.__str__().zfill(3))
#           page.__str__().zfill(3) -> end page half signature with leading zeros
		fo.write(str (endSig))
#           str (endSig) -> end signature text
		fo.write(count.__str__())
#           count.__str__() -> signature number
		fo.write('''\n''')
#           '\n' -> new line

		page = page + 1
		fo.write(page.__str__().zfill(3))
		fo.write(str (begSig))
		fo.write((count + 1).__str__())
		fo.write('''\n''')
#           page, start signature text, signature number and new line

		count += 1
		page = page + 31
#           there are 31 pages between start and end

		fo.write(page.__str__().zfill(3))
		fo.write(str (endSig))
		fo.write(count.__str__())
		fo.write(str (', last printed page'))
		fo.write('''\n''')
#           page, end signature text, signature number, last page warning, new line

# WHEN THERE IS NO HALF SIGNATURE the last signature counts 32 pages
# (add 31 to the last start page)

	if num16pSign%2 == 0:
		fo.write(page.__str__().zfill(3))
		fo.write(str (endSig))
		fo.write(count.__str__())
		fo.write(str (', last printed page'))
		fo.write('''\n''')
#           page, end signature text, signature number, last page warning, new line


###############################################################################
################## Combine signature pages with front matter ##################
###############################################################################

# Combine the files front_matter containing pages 1 thru start of the NT, the
# end of the NT and backmatter and signature containing the signature start and ends
# just generated into a CSV file
filename = ['front_matter', signature]
with open(combination,'wb') as newf:
	for f in filename:
		with open(f,'rb') as hf:
			newf.write(hf.read())

# The file file front_matter refers to pages in the range of the signature pages. The
# combination.csv file needs to be sorted, in order to get the pages in the print dummy in
# the proper order.
# open as csv file and sort

data = csv.reader(open(combination),delimiter=',')
sortedlist = sorted(data, key=operator.itemgetter(0))
# 0 in itemgetter of sortedlist specifies the sorting of the first column
# After sorting write the result to new CSV file
with open(content, "wb") as f:
	fileWriter = csv.writer(f, delimiter=',')
	for row in sortedlist:
		fileWriter.writerow(row)

# The last CSV file is sorted in the proper order, however the CSV format has line
# endings \r\n and those don't work in the svg generation. The CSV file is written
# to a plain text file

f = open(content)
lines = f.read()
txt=lines.strip('\r\n')
with codecs.open(text, 'wb') as textin :
	textin.write(txt)

# The plain text is converted into the format needed in the process with regexes
# replacing \r\n with \n; remove leading zeros, double commas and line final commas

txt = codecs.open(text, "rt").read()

# Replace \r\n with \n
txt = re.sub(ur'(.+)\r\n', ur'\1\n', txt)

# Remove leading zeros that were introduced in the signature figures
txt = re. sub(ur'0*(\d+)', ur'\1', txt)

# Delete double and single commas left over from the CSV operation
txt = re. sub(ur',,', ur'', txt)
txt = re. sub(ur',\n', ur'\n', txt)

# Write txt to alltext, the final text containing all information to generate
# the print dummy
codecs.open(alltext, "wt", encoding="utf_8_sig").write(txt)

###############################################################################
################################ EXTRACT  PAGES ###############################
###############################################################################

# Open extractfile for reading
with codecs.open(alltext, 'rt', encoding="utf_8_sig") as contents :
	lines = contents.read().split('\n')     # read text line by line
	for l in lines:
		locate = l.split(',')
		if locate <> [""]:
			countp += 1

#        svg = "stamp" + count.__str__() + ".svg"
#        pdf = "stamp" + count.__str__() + ".pdf"

# SET TEMPORARY FILENAMES for svg, pdf, Mpage and extract

		pdf = tempfile.NamedTemporaryFile().name
		svg = tempfile.NamedTemporaryFile().name
		Mpage = tempfile.NamedTemporaryFile().name
		extract = tempfile.NamedTemporaryFile().name


		fetch = locate[0]
		locate.pop(0)

# EXTRACTING THE PAGE PDF with pdftk
		subprocess.call(["pdftk", procfile, "cat", fetch, "output", extract])


#################################################################################
########################### GENERATE STAMP SVG FILE #############################
#################################################################################
#     Open file
		with codecs.open(svg, 'wb') as fo :

#     Write the svg introduction and page size to the open file. This part is
#     always the same except of the paper dimensions defined in the initial
#     settings

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

#     Generating the line(s) of text to be placed on the stamped page

			for retrieve in locate:
				stamptxt = retrieve
				fo.write('''   <tspan  x="78.9" dy="15">''')
				fo.write(str (stamptxt))
				fo.write('''</tspan>\n''')
			fo.write('''    </text>
  </g>
</svg>''')
			fo.close()
#################################################################################
###################### Convert svg and generate stamp pages #####################
#################################################################################


#     After generating the stamp page as svg it is converted to pdf
#     with subprocess.call(["rsvg-convert", "-f", "pdf", "-o", pdf, svg])

			subprocess.call(["rsvg-convert", "-f", "pdf", "-o", pdf, svg])

#     Then the content of the dummy pages 'extract' are individually
#     stamped with the generated stamp pdf 'pdf', resulting in a
#     single dummy-page 'Mpage'

			subprocess.call(["pdftk", extract, "stamp", pdf, "output", Mpage])

#      Mpage is a temporary file containing the stamped page, the file
#     names are combined to one string by appending them to 'M_all_page

			sys.stdout.write('>')       # write a dot for every Mpage done
			sys.stdout.flush()          # stop the cursor from going to the next line

			M_all_page.append(str(Mpage))

################################################################################
########################### Generating dummy file# #############################
################################################################################
#
#     The individual dummy pages are combined in the single file 'dummy.pdf'
#     which is the end-product of this operation
#
	cmd = []
	cmd.extend(["pdftk"])
	cmd.extend(M_all_page)
	cmd.extend(["cat", "output", "dummy.pdf"])
#
	subprocess.call(cmd)
#

	sys.stdout.write('>>> dummy.pdf DONE <<<')  # text to signal the end of the program
	sys.stdout.flush()
	print '\n'          # forcing a blank line between last text and prompt
