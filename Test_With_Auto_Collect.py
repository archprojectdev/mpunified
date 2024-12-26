"""
Test_With_Auto_Collect.py
"""

import time
from mpunified.MPUPrcWAC import MPUPrcWAC


class Test_With_Auto_Collect(MPUPrcWAC):
    """
    Class Test_With_Auto_Collect
    """

    def __init__(self, pipe):
        super().__init__(pipe)
        self.a = 0
        self.b = 0

    def run(self):
        """
        Function run()
        """

        # Attente d’une premiere reception
        self.pipe_recv()

        # Démarrage de la collecte automatique
        self.start_collect()

        # Boucle d’addition de a = a + b
        # Envoi de la nouvelle valeur de a vers le stockage de résultat
        # Temporisation d’une seconde
        while True:
            self.a += self.b
            self.pipe_send({"a": self.a})
            time.sleep(1)


def test_with_auto_collect_run(pipe):
    """
    :param pipe:
    """
    test_with_auto_collect = Test_With_Auto_Collect(pipe)
    test_with_auto_collect.run()
