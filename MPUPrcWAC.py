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

        new_vars = self.pipe.recv()
        for var in new_vars:
            self.__dict__[var] = new_vars[var]

    def pipe_send(self, new_vars: dict):
        """
        Function pipe_send()
        """

        self.pipe.send(new_vars)

    def start_collect(self):
        """
        Function start_collect()
        """

        thread = Thread(target=self.collect)
        thread.daemon = True
        thread.start()
