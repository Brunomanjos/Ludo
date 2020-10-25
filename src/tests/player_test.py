# Teste Automatizado do módulo Player
# Atualizado: 25/10/2020
# autor: Bruno Messeder dos Anjos

import unittest

import player


class PlayerTest(unittest.TestCase):

    def test_01_set_players_ok(self):
        player.set_players('Antônio', 'Bruno', 'Bot 1', 'Bot 2')
        self.assertEqual('Antônio', player.get_player(0))
        self.assertEqual('Bruno', player.get_player(1))
        self.assertEqual('Bot 1', player.get_player(2))
        self.assertEqual('Bot 2', player.get_player(3))

    def test_02_set_players_invalid_type(self):
        with self.assertRaises(TypeError):
            player.set_players('Antônio', 'Bernardo', 'Bruno', None)

    def test_03_get_players(self):
        self.assertEqual(['Antônio', 'Bruno', 'Bot 1', 'Bot 2'], player.get_players())

    def test_04_set_player_ok(self):
        self.assertTrue(player.set_player(0, 'Bruno'))

    def test_05_set_player_invalid_index(self):
        self.assertFalse(player.set_player(-1, 'Bruno'))
        self.assertFalse(player.set_player(4, 'Bruno'))

    def test_06_set_player_invalid_type(self):
        with self.assertRaises(TypeError):
            player.set_player(0, 3)

    def test_07_get_player_ok(self):
        self.assertEqual('Bruno', player.get_player(0))
        self.assertEqual('Bot 2', player.get_player(3))

    def test_08_get_player_invalid_index(self):
        self.assertIsNone(player.get_player(-1))
        self.assertIsNone(player.get_player(4))


if __name__ == '__main__':
    unittest.main()
