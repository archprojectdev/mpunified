"""
Class Unifier
"""

import time
import types

from uuid import uuid4
from threading import Thread

from multiprocessing import Process, Pipe
from unimultiprocessing.Subprocess import Subprocess


class Unifier:
    """
    Class Unifier
    """

    def __init__(self):
        """
        :param self:
        """

        self.master_pipes = {}
        self.slave_pipes = {}
        self.results = {}

        self.process_running = {}
        self.breaker = False

        self.thd_results = {}

        thread = Thread(target=self.break_process)
        thread.daemon = True
        thread.start()

    def process(self):
        """
        :param self:
        """

        id = str(uuid4())
        process_loaded = Subprocess(id)

        parent_conn, child_conn = Pipe()
        self.master_pipes[id] = [
            parent_conn,
            child_conn
        ]

        parent_conn, child_conn = Pipe()
        self.slave_pipes[id] = [
            parent_conn,
            child_conn
        ]

        self.thd_results[id] = Thread(target=self.result_process, args=(id, parent_conn))
        self.thd_results[id].daemon = True
        self.thd_results[id].start()

        return id, process_loaded, self.master_pipes[id], self.slave_pipes[id]

    def run(self, function, args):
        """
        :param self:
        :param function:
        :param args:
        """

        id, process_loaded, master_pipes, slave_pipes = self.process()

        self.process_running[id] = Process(
            target=process_loaded.run,
            args=(
                master_pipes[0],
                slave_pipes[1],
                function,
                *args
            ))
        self.process_running[id].start()

        return id

    def while_true(self, sleep: float, function: types.FunctionType, args):
        """
        :param self:
        :param sleep:
        :param function:
        :param args:
        """

        id, process_loaded, master_pipes, slave_pipes = self.process()

        self.process_running[id] = Process(
            target=process_loaded.while_true,
            args=(
                self.master_pipes[id][0],
                self.slave_pipes[id][1],
                sleep,
                function,
                *args
            ))
        self.process_running[id].start()

        return id

    def for_range(self, gap: int, sleep: float, function: types.FunctionType, args):
        """
        :param self:
        :param gap:
        :param sleep:
        :param function:
        :param args:
        """

        id, process_loaded, master_pipes, slave_pipes = self.process()

        self.process_running[id] = Process(
            target=process_loaded.for_range,
            args=(
                self.master_pipes[id][0],
                self.slave_pipes[id][1],
                gap,
                sleep,
                function,
                *args
            ))
        self.process_running[id].start()

        return id

    def result_process(self, id, parent_conn):
        """
        :param self:
        :param id:
        :param parent_conn:
        """

        while True:
            self.results[id] = parent_conn.recv()

    def get_result(self, id):
        """
        :param self:
        :param id:
        :return:
        """

        if id in self.results:
            return self.results[id]
        else:
            return None

    def break_process(self):
        """
        :param self:
        """

        i = 0

        while True:

            i += 1
            time.sleep(0.1)

            if self.breaker:
                for pipe in self.master_pipes:
                    self.master_pipes[pipe][1].send(True)
                break
