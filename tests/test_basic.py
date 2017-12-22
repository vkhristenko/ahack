import os, sys

#
# insert path to the package explicitly into the PYTHONPATH
#
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#
# import the Assembly Compiler
#
from ahack.compiler import Compiler

#
# some inits
#
c = Compiler()
path = "test_asm_file.asm"

#
# Compile 
# 
c.compile(path)
