#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a very simple way to get at values in a configuration file using an add-on module
# called ConfigObj (http://www.voidspace.org.uk/python/configobj.html)

# When Rapuma was installed, one of the modules that was installed with it was
# the python-configobj module which does not come in the standard Python installation
# but is found in the Ubuntu package manager
from configobj import ConfigObj

# This reads in an example file that I copied into the testing folder.
# In Rapuma this is loaded automatically and is available in every script.
layoutConfig = ConfigObj('layout.conf', encoding='utf-8')

# To call out a value in our loaded config object you do it as follows:
w = layoutConfig['PageLayout']['pageWidth']
h = layoutConfig['PageLayout']['pageHeight']

# Now print the values found
print 'Page Width =', w
print 'Page Height =', h

# Always remember that the values stored in the config are strings, not integers
# If you want to do calculations with them you need to convert them with int()
