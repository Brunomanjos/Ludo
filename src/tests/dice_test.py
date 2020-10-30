# Teste Automatizado do módulo Dice
# Atualizado: 26/10/2020
# Autor: Bruno Messeder dos Anjos


import unittest

import dice


class DiceTest(unittest.TestCase):
    def test_01_throw_ok(self):
        self.assertTrue(1 <= dice.throw() <= 6)

    def test_02_get_ok(self):
        self.assertTrue(1 <= dice.get() <= 6)
        self.assertEqual(dice.throw(), dice.get())

    def test_03_clear_ok(self):
        dice.clear()
        self.assertIsNone(dice.get())


if __name__ == '__main__':
    unittest.main()
