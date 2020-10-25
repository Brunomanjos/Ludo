# Teste Automatizado do módulo Match
# Atualizado: 25/10/2020
# autor: Bruno Messeder dos Anjos

import unittest

import match
import board


class MatchTest(unittest.TestCase):

    def test_01_current_player_match_not_defined(self):
        self.assertEqual(match.MATCH_NOT_DEFINED, match.current_player())

    def test_02_make_move_match_not_defined(self):
        self.assertEqual(match.MATCH_NOT_DEFINED, match.make_move(1, 2))

    def test_03_player_groups_match_not_defined(self):
        self.assertEqual(match.MATCH_NOT_DEFINED, match.player_groups())

    def test_04_player_group_match_not_defined(self):
        self.assertEqual(match.MATCH_NOT_DEFINED, match.player_group(0))

    def test_05_close_match_not_defined(self):
        self.assertIsNone(match.close_match())

    def test_06_new_match_ok(self):
        self.assertTrue(match.new_match('Antônio', 'Bruno', 'Bot 1', 'Bot 2'))

    def test_07_new_match_in_progress(self):
        self.assertEqual(match.MATCH_IN_PROGRESS, match.new_match('Antônio', 'Bruno', 'Bot 1', 'Bot 2'))

    def test_08_current_player_ok(self):
        self.assertTrue(0 <= match.current_player() <= 3)

    def test_09_player_groups_ok(self):
        groups = match.player_groups()
        self.assertEqual(4, len(groups))
        for group in groups:
            self.assertTrue(0 <= group <= 3)

    def test_10_player_group_ok(self):
        self.assertTrue(0 <= match.player_group(2) <= 3)

    def test_11_player_group_invalid_player(self):
        self.assertEqual(match.INVALID_PLAYER, match.player_group(-1))
        self.assertEqual(match.INVALID_PLAYER, match.player_group(4))

    def test_12_make_move_invalid_piece(self):
        self.assertEqual(match.INVALID_PIECE, match.make_move(-1, 2))
        self.assertEqual(match.INVALID_PIECE, match.make_move(16, 2))

    def test_13_make_move_invalid_steps(self):
        self.assertEqual(match.INVALID_STEPS, match.make_move(0, 0))
        self.assertEqual(match.INVALID_STEPS, match.make_move(1, 7))

    def test_14_make_move_ok(self):
        player = match.current_player()
        group = match.player_group(player)
        piece = group * 4
        self.assertIsNone(match.make_move(piece, 6))
        self.assertEqual(player, match.current_player())
        self.assertIsNone(match.make_move(piece, 6))
        self.assertEqual(player, match.current_player())
        self.assertIsNone(match.make_move(piece, 6))
        self.assertNotEqual(player, match.current_player())


if __name__ == '__main__':
    unittest.main()
