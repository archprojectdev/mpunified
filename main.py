"""
main.py
"""

import time
from threading import Thread

from unimultiprocessing import ump_while_true, ump_get_result

it = 0


def my_name(nm, nt):
    """
    :param nm:
    :param nt:
    """

    global it

    it += 1
    res = nm + " " + nt + " : " + str(it)
    return res


# ------------------------------------------------------------

def get_my_name(pids):
    """
    :param pids:
    """
    while True:
        for pid in pids:
            print(ump_get_result(ids[pid]))
        time.sleep(1)


# ------------------------------------------------------------

names = ["charlie", "jeremy", "simon", "sebastien", "karen"]
ids = {}

for name in names:
    ids[name] = ump_while_true(
        sleep=0.001, function=my_name,
        args=("mon nom est", name))

thread = Thread(target=get_my_name, args=(ids,))
thread.daemon = True
thread.start()
