"""
MPUPrcWAC.py
"""

from threading import Thread


class MPUPrcWAC:
    """
    Class MPUPrcWAC
    """

    def __init__(self, pipe):
        self.pipe = pipe

    def collect(self):
        """
        Function collect()
        """

        while True:
            self.pipe_recv()

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

    def start_collect(self):
        """
        Function start_collect()
        """

        thread = Thread(target=self.collect)
        thread.daemon = True
        thread.start()
