class Instruction(object):
    def __init__(self):
        pass

    def is_symbol_decl(self):
        return False

    def is_var_decl(self):
        return False

    def opcode(self):
        raise NotImplementedError("opcode is not implemented by Instruction class")

class AInstruction(Instruction):
    """
    @value
    """
    def __init__(self, value):
        Instruction.__init__(self)
        self.value = value

    def opcode(self):
        return "0"

def CInstruction(Instruction):
    """
    dest=comp;jump
    """
    def __init__(self, txt):
        Instruction.__init__(self, txt)

    def opcode(self):
        return "1"

def LabelDeclInstruction(Instruction):
    def __init__(self, txt):
        Instruction.__init__(self, txt)

    def is_symbol_decl(self):
        return True
