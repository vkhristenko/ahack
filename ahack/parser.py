class Token(object):
    def __init__(self):
        pass

    def is_white_space(self):
        raise NotImplementedError("Base Token class does not implement anything")

    def is_symbol_decl(self):
        raise NotImplementedError("Base Token class does not implement anything")

    def is_var_decl(self):
        raise NotImplementedError("Base Token class does not implement anything")

    def translate(self, stable):
        raise NotImplementedError("Base Token class does not implement anything")

class WhiteSpaceToken(Token):
    def __init__(self):
        Token.__init__(self)

    def is_white_space(self):
        return True

class CInstruction(Token):
    def __init__(self):
        Token.__init__(self)

    def is_white_space(self):
        return False

    def is_symbol_decl(self):
        return False

    def is_var_decl(self):
        return False

class Parser(object):
    """
    Parser Class - 
    """
    def __init__(self, path):
        pass

    def parse(self, cmd):
        pass
