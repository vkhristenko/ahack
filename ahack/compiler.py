import defs, codegen
from parser import Parser
import logging
import copy

class SymbolTable(object):
    def __init__(self):
        self.pairs = {}
        pass

    def add(self, symbol, value):
        """
        Do not check that it exists - just add
        """
        self.pairs[symbol] = copy.copy(value)

    def exists(self, symbol):
        """
        Check if this symbol is in the Table
        """
        return (symbol in self.pairs.keys())

    def getAddress(self, symbol):
        """
        Get the Address of the symbol
        """
        return self.pairs[symbol]

class Compiler(object):
    """
    Hack Assembly Compiler - top abstraction. 
    """
    def __init__(self):
        self.logger = logging.getLogger("ahack")

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
        self.logger.info("Compiling hack assembly file: %s" % path)

        # 
        # Create a Symbol Table and add all the predefined symbols
        # Create a Parser
        #
        self.logger.info("Phase: Initialization")
        stable = SymbolTable()
        for symbol,value in defs.predefinedSymbols:
            stable.add(symbol, value)

        #
        # set the current instruction number to be 0
        #
        currentInstruction = 0

        #
        # First Pass: Add Label Declarations into the SymbolTable
        #
        self.logger.info("Phase: First Pass")
        with Parser(path, self.logger) as p:
            while p.hasMoreCommands():
                # read the next command
                p.advance()

                # if this is a label declaration => add to the Symbol Table
                # and proceed to the next instruction in the loop
                if p.commandType() == p.L_COMMAND:
                    stable.add(p.symbol(), currentInstruction)
                    continue

                # increment the instruction number and continue
                currentInstruction+=1

        #
        # Second Pass
        # 
        self.logger.info("Phase: Second Pass")
        with Parser(path, self.logger) as p:
            # open up the output file
            with open(path.replace(".asm", ".hack"), "w") as outFile:
                # set the instruction back to 0
                currentInstruction = 0
                # set the starting memory slot to 16 - for variable declarations
                currentMemorySlot = 16
                inc_memory = False

                while p.hasMoreCommands():
                    # parse the next command line
                    p.advance()

                    # if this is the L_COMMAND -> continue
                    if p.commandType() == p.L_COMMAND:
                        continue

                    # if this is A-instruction
                    if p.commandType() == p.A_COMMAND:
                        # if this is not an int => check if in stable
                        if not p.symbol().isdigit():
                            if not stable.exists(p.symbol()):
                                stable.add(p.symbol(), currentMemorySlot)
                                # we must follow up to the next memory slot
                                currentMemorySlot += 1
                            hack_instruction = format(stable.getAddress(p.symbol()),
                                "016b")
                        else:
                            hack_instruction = format(int(p.symbol()), "016b")
                    elif p.commandType() == p.C_COMMAND:
                        hack_instruction = "111" + codegen.comp(p.comp()) +\
                                        codegen.dest(p.dest())+\
                                        codegen.jump(p.jump())
                    else:
                        raise NotImplementedError("There are only 3 types of commands for the Hack Assembly Specification")

                    # write to the output file
                    self.logger.debug("hack instruction = %s" % hack_instruction)
                    outFile.write(hack_instruction+"\n")

                    # increment the instruction's counter
                    currentInstruction+=1
