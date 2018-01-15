import defs
from parser import Parser
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

class InputFeeder(object):
    def __init__(self, path):
        self,path = path

    def next(self):
        return None

    def __enter__(self):
        self.f = open(self.path)

    def __exit__(self):
        self.f.close()

class OutputFeeder(object):
    def __init__(self, path):
        self.path = path

    def next(self, instruction):
        self.f.write(instruction+"\n")

    def __enter__(self):
        self.f = open(self.path)

    def __exit__(self):
        self.f.close()

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
        # Create a Symbol Table and add all the predefined symbols
        # Create a Parser
        #
        stable = SymbolTable()
        psr = Parser()
        for symbol,value in defs.predefinedSymbols:
            self.stable.add(symbol, value)

        #
        # Initialize the Code Generator
        #
        translator = CodeGen(path.replace(".asm", ".hack"))

        #
        # set the current memory address to be 16
        # set the current instruction number to be 0
        #
        currentMemorySlot = 16
        currentInstruction = 0

        #
        # First Pass
        #
        with InputFeeder(path) as feeder:
            cmd_str = feeder.next()
            while cmd_str is not None:
                token = psr.parse(cmd_str)
                if token.is_symbol_decl():
                    # if this is a pseudo command which declares the 
                    # goto label
                    address = currentInstruction
                    stable.add(token.symbol, address)
                    # decrement 1 cause we gonna increment down the road
                    currentInstruction-=1
                cmd_str = feeder.next()
                currentInstruction+=1

        #
        # Second Pass
        #
        currentInstruction = 0
        with InputFeeder(path) as feeder:
            with OutputFeeder(path.replace(".asm", ".hack")) as out:
                cmd = feeder.next()
                while cmd is not None:
                    token = psr.parse(cmd_str)
                    #
                    # check that we are getting the symbol decl again
                    # just ignore it completely
                    #
                    if token.is_symbol_decl(): 
                        feeder.next()
                        continue

                    #
                    # If this is a variable decl
                    #   add this variable to the Symbol Table
                    #
                    if token.is_var_decl():
                        if not stable.exists(instruction.symbol):
                            stable.add(instruction.symbol, currentMemorySlot)
                            currentMemorySlot+=1

                    #
                    # code generation:
                    # Symbol Table is complete with either variables or label decls
                    # We equip each token with the knowledge how to translate itself
                    #
                    instruction = token.translate(stable)

                    #
                    # At this stage we have a meaningful instruction
                    # We have to geneate code for it
                    #
                    feeder.next()
                    currentInstruction+=1
