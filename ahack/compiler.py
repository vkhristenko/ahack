

class Compiler(object):
    """
    Hack Assembly Compiler - top abstraction. 
    """
    def __init__(self):
        pass

    def compile(self, path):
        """
        Compile the provided assembly file and generate the Hack Machine Code

        The Assembly Process:
        1. Initialization
            - Construct an empty symbol table
            - Add pre-defined symbols
        2. First Pass
            - Scan the entire source file
            - For each instruction of the form (XXX)
                -> Add the pair (xxx, address) to the symbol table, where
                address is the number of the instruction following (XXX)
        3. Second Passs
            - Set n to 16
            - Scan the entire program and for each instruction:
                -> If (symbol, value) is found, use value to complete the instructions
                    translation.
                -> If not found
                    - Add (symbol, n) to the SymbolTable
                    - Use n to complete the instruction's translation
                    - n++
            - If the instruction is a C-instruction, complete the instruction's 
                translation
            - Write the translated instruction to he output file
        """
        pass
#        with Parser(path) as p:
#            # fetch the next instruction
#            inst = p.next()
#            # for each instruction, 
#            while inst is not None:

    def interpret(self, s):
        """
        Interpret a given string - generate the machine code...
        no execution...
        """
        pass
