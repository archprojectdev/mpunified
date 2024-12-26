"""
MPUPrc.py
"""


class MPUPrc:
    """
    Class MPUPrc
    """

    def __init__(self, pipe):
        self.pipe = pipe

    def pipe_recv(self):
        """
        Function pipe_recv()
        """

        vars = self.pipe.recv()
        for var in vars:
            self.__dict__[var] = vars[var]

    def pipe_send(self, vars: dict):
        """
        Function pipe_send()
        """

        self.pipe.send(vars)
