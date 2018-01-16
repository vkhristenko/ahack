import os, sys
import logging

#
# logging configuration
#
logging.basicConfig(level=logging.INFO)

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
path = "/Users/vk/software/BuildComputer/soft/nand2tetris/projects/06/pong/Pong.asm"

#
# Compile 
# 
c.compile(path)
