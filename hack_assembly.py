#!/usr/local/bin/python

import os, sys
import logging

#
# logging configuration
#
logging.basicConfig(level=logging.INFO)

#
# insert path to the package explicitly into the PYTHONPATH
#
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

#
# import the Assembly Compiler
#
from ahack.compiler import Compiler

#
# some inits
#
c = Compiler()
path = sys.argv[1]

#
# Compile 
#
c.compile(path)
