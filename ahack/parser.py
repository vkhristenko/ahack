class Parser(object):
    def __init__(self, path):
        self.path = path
        self.A_COMMAND = 0
        self.L_COMMAND = 1
        self.C_COMMAND = 2

    def __enter__(self):
        self.f = open(self.path, "r")

    def __exit__(self):
        self.f.close()

    def hasMoreCommands(self):
        while True:
            # strip and remove all the white spaces
            line = self.f.readline().strip().replace(" ", "")
            if line == "":
                # EOF
                return False
            elif line == "\n":
                # empty lien
                continue
            elif line.startswith("//"):
                # comment
                continue
            else:
                self.line = line
                return True
        

    def advance(self):
        if self.line.startswith("@"):
            self._symbol = self.line[1:]
            self.type = self.A_COMMAND
        elif self.line.startswith("(") and self.line.endswith(")"):
            self._symbol = self.line[1:-1]
            self.type = self.L_COMMAND
        else:
            self.type = self.C_COMMAND

            # try to split on destination
            try_dest = self.line.split("=")
            if len(try_dest)==2:
                # got the destination part
                self._dest = try_dest[0] 
                # try to split on jump
                try_jump = try_dest[1].split(";")
                if (len(try_jump) == 2):
                    self._comp = try_jump[0]
                    self._jump = try_jump[1]
                    if self._jump=="": 
                        self._jump = None
                else:
                    self._jump = None
                    self._comp = try_jump[0]
            elif len(try_dest) == 1:
                # no destination!
                self._dest = None
                try_jump = self.line.split(";")
                if len(try_jump) == 2:
                    self._comp = try_jump[0]
                    self._jump = try_jump[1]
                    if self._jump=="":
                        self._jump = None
                else:
                    self._jump = None
                    self._comp = try_jump[0]

    def commandType(self):
        return self.type

    def symbol(self):
        return self._symbol

    def dest(self):
        return self._dest

    def comp(self):
        return self._comp

    def jump(self):
        return self._jump
