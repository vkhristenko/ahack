import defs
from paraser import Parser
from codegen import CodeGen
import sema

class SymbolTable(object):
    def __init__(self):
        self.pairs = {}
        pass

    def add(self, symbol, value):
        """
        Do not check that it exists - just add
        """
        self.pairs[symbol] = value

    def exists(self, symbol):
        return (symbol in self.pairs.keys())

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
        #
        # Initialization: initialize the SymbolTable
        #
        stable = SymbolTable()

        #
        # Initialize the Code Generator
        #
        translator = CodeGen(path.replace(".asm", ".hack"))

        #
        # Initialization: Add predefined symbols
        #
        for symbol,value in defs.predefinedSymbols:
            stable.add(symbol, value)

        #
        # set the current memory address to be 16
        # set the current instruction number to be 0
        #
        currentMemorySlot = 16
        currentInstruction = 0

        #
        # First Pass
        #
        with Parser(path) as p:
            command = p.next()
            while command is not None:
                instruction = sema.sema(command)
                if instruction.is_symbol_decl():
                    # if this is a pseudo command which declares the 
                    # goto label
                    address = currentInstruction
                    stable.add(instruction.symbol, address)
                    # decrement 1 cause we gonna increment down the road
                    currentInstruction-=1
                p.next()
                currentInstruction+=1

        #
        # Second Pass
        #
        with Parser(path) as p:
            command = p.next()
            while command is not None:
                instruction = sema.sema(command)
                #
                # check that we are getting the symbol decl again
                # just ignore it completely
                #
                if instruction.is_symbol_decl():
                    currentInstruction-=1

                #
                # If this is a variable decl
                #
                if instruction.is_var_decl():
                    if not stable.exists(instruction.symbol):
                        stable.add(instruction.symbol, currentMemorySlot)
                        currentMemorySlot+=1

                #
                # code generation:
                # Symbol Table is complete with either variables or label decls
                #
                translator.translate(instruction, stable)

                #
                # At this stage we have a meaningful instruction
                # We have to geneate code for it
                #
                p.next()
                currentInstruction++1

    def interpret(self, s):
        """
        Interpret a given string - generate the machine code...
        no execution...
        """
        pass
