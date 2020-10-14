# autor: Bruno Messeder dos Anjos

import unittest
import player


class PlayerTest(unittest.TestCase):

    def test_01_set_player_ok(self):
        self.assertTrue(player.set_player(0, 'Bruno'))

    def test_02_set_player_invalid_index(self):
        self.assertFalse(player.set_player(-1, 'Bruno'))
        self.assertFalse(player.set_player(4, 'Bruno'))

    def test_03_set_player_invalid_type(self):
        with self.assertRaises(TypeError) as handler:
            player.set_player(0, 3)
        print('Expected exception:', handler.exception)

    def test_04_get_player_ok(self):
        self.assertEqual('Bruno', player.get_player(0))
        self.assertEqual('', player.get_player(3))

    def test_05_get_player_invalid_index(self):
        self.assertIsNone(player.get_player(-1))
        self.assertIsNone(player.get_player(4))

    def test_06_set_players_ok(self):
        player.set_players('Antônio', 'Bernardo', 'Bruno', 'Bot')
        self.assertEqual('Antônio', player.get_player(0))
        self.assertEqual('Bernardo', player.get_player(1))
        self.assertEqual('Bruno', player.get_player(2))
        self.assertEqual('Bot', player.get_player(3))

    def test_07_set_players_invalid_type(self):
        with self.assertRaises(TypeError) as handler:
            player.set_players('Antônio', 'Bernardo', 'Bruno', None)

        print('Expected exception:', handler.exception)

    def test_08_get_players(self):
        self.assertEqual(['Antônio', 'Bernardo', 'Bruno', 'Bot'], player.get_players())


if __name__ == '__main__':
    unittest.main()
