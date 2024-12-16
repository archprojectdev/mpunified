"""
Class Subprocess
"""

import time
import signal

from concurrent.futures import ThreadPoolExecutor


class Subprocess:
    """
    Class Subprocess
    """

    def __init__(self, name):
        """
        :param self:
        :param name:
        """

        self.name = str(name)
        self.breaker = False

        self.parent_conn = None
        self.child_conn = None

        self.sleep = None
        self.gap = None
        self.process = None
        self.args = None
        self.result = None

    def signal_handler(self, _, __):
        """
        :param self:
        :param _:
        :param __:
        """

        self.breaker = True

    def breaker_check(self):
        """
        :param self:
        """

        while True:
            if self.parent_conn.recv() or self.breaker:
                if self.breaker:
                    break
                else:
                    self.breaker = True
                    print("Process " + self.name + " in stopping.")
                    break
            time.sleep(0.5)

    def encap_run(self):
        """
        :param self:
        """

        self.result = self.process(*self.args)
        self.child_conn.send(self.result)
        self.breaker = True

        print("Process " + self.name + " is stopped.")

    def encap_while_true(self):
        """
        :param self:
        """

        while True:

            if self.breaker:
                break

            try:
                self.result = self.process(*self.args)
                self.child_conn.send(self.result)
            except Exception as Err:
                print(Err)

            time.sleep(self.sleep)

        print("Process " + self.name + " is stopped.")

    def encap_for_range(self):
        """
        :param self:
        """

        for it in range(self.gap):

            if self.breaker:
                break

            try:
                self.result = self.process(*self.args)
                self.child_conn.send(self.result)
            except Exception as Err:
                print(Err)

            time.sleep(self.sleep)

        print("Process " + self.name + " is stopped.")

    def while_true(self, parent_conn, child_conn, sleep, function, *args):
        """
        :param self:
        :param parent_conn:
        :param child_conn:
        :param sleep:
        :param function:
        :param args:
        """

        self.parent_conn = parent_conn
        self.child_conn = child_conn
        self.sleep = sleep
        self.process = function
        self.args = args

        signal.signal(signal.SIGINT, self.signal_handler)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(self.breaker_check)
            e.submit(self.encap_while_true)

    def for_range(self, parent_conn, child_conn, gap, sleep, function, *args):
        """
        :param self:
        :param parent_conn:
        :param child_conn:
        :param gap:
        :param sleep:
        :param function:
        :param args:
        """

        self.parent_conn = parent_conn
        self.child_conn = child_conn
        self.gap = gap
        self.sleep = sleep
        self.process = function
        self.args = args

        signal.signal(signal.SIGINT, self.signal_handler)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(self.breaker_check)
            e.submit(self.encap_for_range)

    def run(self, parent_conn, child_conn, function, *args):
        """
        :param self:
        :param parent_conn:
        :param child_conn:
        :param function:
        :param args:
        """

        self.parent_conn = parent_conn
        self.child_conn = child_conn
        self.process = function
        self.args = args

        signal.signal(signal.SIGINT, self.signal_handler)

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(self.breaker_check)
            e.submit(self.encap_run)
