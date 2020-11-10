# Teste Automatizado do módulo Database
# Atualizado: 09/11/2020
# Autor: Bruno Messeder dos Anjos

import unittest

import database


class DatabaseTest(unittest.TestCase):

    def test_01_clear_table(self):
        pass
        # self.assertTrue(database.execute_and_close('delete from TestTable'))


if __name__ == '__main__':
    unittest.main()
