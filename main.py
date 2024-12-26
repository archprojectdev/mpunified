"""
main.py
"""

from mpunified.MPUnified import MPUnified
from Test_With_Auto_Collect import test_with_auto_collect_run
from Test_Without_Auto_Collect import test_without_auto_collect_run

import time
import sys
import signal

mpu = MPUnified()

# Chargement des processus à lancer
mpu.load("test_with_auto_collect", test_with_auto_collect_run)
mpu.load("test_without_auto_collect", test_without_auto_collect_run)

# Programmation du transfert du résultat du premier processus vers le second
# A la reception d’une nouvelle valeur
mpu.bind_transfert("test_with_auto_collect", "test_without_auto_collect")

# Lancement des processus
mpu.run("test_with_auto_collect")
mpu.run("test_without_auto_collect")


# ---------------------------------------------------------

def close_processus(_, __):
    """
    :param _:
    :param __:
    """
    mpu.stop()
    sys.exit(0)


signal.signal(signal.SIGINT, close_processus)

# ---------------------------------------------------------

# Envoi d’un lot de variable vers le processus test_with_auto_collect
mpu.set_var(
    "test_with_auto_collect",
    {
        "a": 0,
        "b": 1
    })

# ---------------------------------------------------------

while True:

    # Si le résultat du processus test_with_auto_collect contient la variable a.
    # Si la variable a contenu dans le tableau est égal à 5.
    if mpu.get_result("test_with_auto_collect", "a") == 5:

        # Return le résultat du processus test_with_auto_collect stocké dans le MPU
        print("test_with_auto_collect:" + str(mpu.get_result("test_with_auto_collect", "a")))

        # Return le résultat du processus test_without_auto_collect stocké dans le MPU
        print("test_without_auto_collect:" + str(mpu.get_result("test_without_auto_collect", "c")))

        # Suppression du résultat dans le stockage MPU
        mpu.delete_result("test_with_auto_collect")

        # Envoi d’un lot de variable vers le processus test_with_auto_collect
        mpu.set_var(
            "test_with_auto_collect",
            {
                "a": 0,
                "b": 1
            })

    time.sleep(0.1)
