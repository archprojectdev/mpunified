"""
Test_Without_Auto_Collect.py
"""

from mpunified.MPUPrc import MPUPrc


class Test_Without_Auto_Collect(MPUPrc):
    """
    Class Test_Without_Auto_Collect
    """

    def __init__(self, pipe):
        super().__init__(pipe)
        self.c = 0
        self.a = 0

    def run(self):
        """
        Function run()
        """

        # Boucle d’addition de c = c + a
        # Attente d’une reception
        # Addition
        # Envoi de la nouvelle valeur de c vers le stockage de résultat
        while True:
            self.pipe_recv()
            self.c += self.a
            self.pipe_send({"c": self.c})


def test_without_auto_collect_run(pipe):
    """
    :param pipe:
    """
    test_without_auto_collect = Test_Without_Auto_Collect(pipe)
    test_without_auto_collect.run()
