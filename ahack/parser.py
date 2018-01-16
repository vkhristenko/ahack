class Parser(object):
    def __init__(self, path, logger):
        self.path = path
        self.logger = logger
        self.A_COMMAND = 0
        self.L_COMMAND = 1
        self.C_COMMAND = 2

    def __enter__(self):
        self.f = open(self.path, "r")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()

    def hasMoreCommands(self):
        while True:
            # strip and remove all the white spaces
            #line = self.f.readline().strip().replace(" ", "")
            line = self.f.readline()
            self.logger.debug("line = %s" % line)
            if line == "":
                # EOF
                return False

            line = line.strip().replace(" ", "")
            if line == "":
                continue
            elif line == "\n":
                # empty line
                continue
            elif line.startswith("//"):
                # comment
                continue
            else:
                self.line = line
                return True
        

    def advance(self):
        self.logger.debug("Parser.advance: line=%s" % self.line)
        if "//" in self.line:
            self.line = self.line.split("//")[0]
        if self.line.startswith("@"):
            self._symbol = self.line[1:]
            self.type = self.A_COMMAND
        elif self.line.startswith("(") and self.line.endswith(")"):
            self._symbol = self.line[1:-1]
            self.type = self.L_COMMAND
        else:
            self.type = self.C_COMMAND

            self._dest = None
            self._comp = None
            self._jump = None
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
                        self._jump = ""
                else:
                    self._jump = ""
                    self._comp = try_jump[0]
            elif len(try_dest) == 1:
                # no destination!
                self._dest = ""
                try_jump = self.line.split(";")
                if len(try_jump) == 2:
                    self._comp = try_jump[0]
                    self._jump = try_jump[1]
                    if self._jump=="":
                        self._jump = ""
                else:
                    self._jump = ""
                    self._comp = try_jump[0]

            self.logger.debug("jump=%s dest=%s comp=%s" % (
                              self._jump, self._dest, self._comp))

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
