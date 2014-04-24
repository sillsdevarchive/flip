#!/usr/bin/python
# -*- coding: utf_8 -*-

# Import built-in Python modules we will need
import os, sys

# Add to our Python system lib path the folder where our custom modules are found
sys.path.insert(0, os.path.join(os.getcwd(), 'lib'))

# Now import the module we need
from pageMerge import PageMerge

# Instantiate the module
pMerge = PageMerge()

# Give the module the page dimensions we will be working with
pMerge.calculate(145, 210, 210, 297)

# Run the main function of the module
pMerge.center('Rompage.pdf', 'output.pdf')
