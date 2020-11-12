# Teste Automatizado do módulo Database
# Atualizado: 09/11/2020
# Autor: Bruno Messeder dos Anjos

import unittest

import database


# TODO document

class DatabaseTest(unittest.TestCase):

    def test_01_drop_table(self):
        self.assertTrue(database.execute('DROP TABLE IF EXISTS TestTable'))

    def test_02_create_table(self):
        self.assertTrue(database.execute('CREATE TABLE TestTable(a int, b varchar(255), c bool)'))

    def test_03_insert(self):
        self.assertTrue(database.execute("INSERT INTO TestTable VALUES (42, 'Bruno', false)"))

    def test_04_fetch_one(self):
        self.assertEqual((42, 'Bruno', 0), database.fetchone('SELECT * FROM TestTable'))

    def test_05_fetch_all(self):
        self.assertTrue(database.execute("INSERT INTO TestTable VALUES (37, 'João', true)"))
        self.assertEqual({(42, 'Bruno', 0), (37, 'João', 1)}, set(database.fetchall('SELECT * FROM TestTable')))

    def test_06_drop_table(self):
        self.assertTrue(database.execute('DROP TABLE TestTable'))


if __name__ == '__main__':
    unittest.main()
