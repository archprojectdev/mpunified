"""
__init__.py
"""

import signal
import types

from .Unifier import Unifier

unifier = Unifier()


def ump_run(function: types.FunctionType, args):
    """
    run()
    :param function:
    :param args:
    """
    return unifier.run(function, args)


def ump_while_true(sleep: float, function: types.FunctionType, args):
    """
    while_true()
    :param sleep:
    :param function:
    :param args:
    """
    return unifier.while_true(sleep, function, args)


def ump_for_range(gap: int, sleep: float, function: types.FunctionType, args):
    """
    for_range()
    :param gap:
    :param sleep:
    :param function:
    :param args:
    """
    return unifier.for_range(gap, sleep, function, args)


def ump_get_result(id):
    """
    get_result()
    :param id:
    """
    return unifier.get_result(id)


def signal_handler(_, __):
    """
    signal_handler()
    :param _:
    :param __:
    """
    unifier.breaker = True


signal.signal(signal.SIGINT, signal_handler)
