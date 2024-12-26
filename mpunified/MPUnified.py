"""
MPUnified.py
"""


import copy

from multiprocessing import Process, Pipe
from threading import Thread

import time


class MPUnified:
    """
    Class Ump
    """

    def __init__(self):

        self.breaker = False

        self.pipes = {}
        self.functions = {}
        self.process = {}
        self.result = {}

        self.transferts = {}

        thread = Thread(target=self.collect)
        thread.daemon = True
        thread.start()

    def load(self, id, function):
        """
        Function load()
        :param id:
        :param function:
        """

        self.pipes[id] = Pipe(duplex=True)
        self.functions[id] = function
        self.process[id] = None
        self.result[id] = None

    def bind_transfert(self, transmitter_id, receiver_id):
        """
        Function bind_transfert()
        :param self:
        :param transmitter_id:
        :param receiver_id:
        """

        if transmitter_id not in self.process:
            print("MPUnified: bind_transfert()")
            print(transmitter_id + " not exist in process.")
        elif receiver_id not in self.process:
            print("MPUnified: bind_transfert()")
            print(receiver_id + " not exist in process.")
        else:
            if transmitter_id not in self.transferts:
                self.transferts[transmitter_id] = []
            self.transferts[transmitter_id].append(receiver_id)

    def stop(self):
        """
        Function signal_handler()
        :param self:
        """
        for id in self.process:
            self.process[id].terminate()

    def run(self, id):
        """
        Function run()
        :param self:
        :param id:
        """
        if id not in self.process:
            print("MPUnified: run()")
            print(id + " not exist in process.")
        else:
            self.process[id] = Process(
                target=self.functions[id],
                args=(self.pipes[id][1],))
            self.process[id].start()

    def get_result(self, id, var):
        """
        Function get_result()
        :param self:
        :param id:
        :param var:
        :return:
        """

        if id not in self.process:
            print("MPUnified: get_result()")
            print(id + " not exist in process.")
        else:
            if var is not None and self.result[id] is not None:
                if var in self.result[id]:
                    return self.result[id][var]
                else:
                    return None
            else:
                return self.result[id]

    def set_var(self, id, vars):
        """
        Function set_var()
        :param self:
        :param id:
        :param vars:
        """

        if id not in self.process:
            print("MPUnified: set_var()")
            print(id + " not exist in process.")
        else:
            self.pipes[id][0].send(vars)

    def collect(self):
        """
        Function collect()
        :param self:
        """

        while True:
            if self.breaker:
                break

            pipes = copy.copy(self.pipes)

            for pipe in pipes:

                if self.pipes[pipe][0].poll(0):
                    self.result[pipe] = self.pipes[pipe][0].recv()

                    transferts = copy.copy(self.transferts)

                    if pipe in transferts:
                        for transfert in self.transferts[pipe]:
                            self.set_var(
                                transfert,
                                self.result[pipe]
                            )

                    del transferts
            del pipes

            time.sleep(0.1)
