"""
Various definitions/declarations:
1. Predefined symbols
"""

predefinedSymbols = [("R" + str(i), i) for i in range(16)] +\
    [("SCREEN", 16384), ("KBD", 24576)] +\
    [("SP", 0), ("LCL", 1), ("ARG", 2), ("THIS", 3), ("THAT", 4)]
