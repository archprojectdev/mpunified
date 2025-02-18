class MPUPrc:

    def __init__(self, pipe):
        self.pipe = pipe

    def pipe_recv(self):

        new_vars = self.pipe.recv()
        for var in new_vars:
            self.__dict__[var] = new_vars[var]

    def pipe_send(self, new_vars: dict):

        self.pipe.send(new_vars)
