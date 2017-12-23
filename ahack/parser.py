class Parser(object):
    """
    Parser Class - 
    """
    def __init__(self, path):
        self.path = path

    def next(self):
        """
        retrieve the next instruction
        """
        pass

    def __enter__(self):
        self.f = open(self.path)
        pass

    def __exit__(self):
        # just close the input file
        self.f.close()
