"""
Various definitions/declarations:
1. Predefined symbols
"""

predefinedSymbols = [("R" + str(i), i) for i in range(16)] +\
    [("SCREEN", 16384), ("KBD", 24576)] +\
    [("SP", 0), ("LCL", 1), ("ARG", 2), ("THIS", 3), ("THAT", 4)]

if __name__ == "__main__":
    print "A list (size=%d) of predefined symbols: <Symbol> = Value" % len(predefinedSymbols)
    for symbol, value in predefinedSymbols:
        print "<{symbol}> = {value}".format(symbol=symbol, value=value)
