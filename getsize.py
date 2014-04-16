#!/usr/bin/python
# -*- coding: utf_8 -*-

import os, sys, shutil, re,  subprocess, codecs, pyPdf


from pyPdf import PdfFileReader
pdf = PdfFileReader(open("MALpage.pdf",'rb'))
var = pdf.getPage(0).mediaBox
print var
