# Teste Automatizado do módulo Match
# Atualizado: 30/10/2020
# autor: Bruno Messeder dos Anjos

import unittest

import dice
import match


class MatchTest(unittest.TestCase):

    def test_01_current_player_match_not_defined(self):
        self.assertEqual(match.MATCH_NOT_DEFINED, match.current_player())

    def test_02_make_move_match_not_defined(self):
        self.assertEqual(match.MATCH_NOT_DEFINED, match.play(1))

    def test_03_close_match_not_defined(self):
        self.assertIsNone(match.close_match())

    def test_04_can_play_match_not_defined(self):
        self.assertEqual(match.MATCH_NOT_DEFINED, match.can_play(1))

    def test_05_new_match_ok(self):
        self.assertTrue(match.new_match('Antônio', 'Bruno', 'Bot 1', 'Bot 2'))

    def test_06_new_match_in_progress(self):
        self.assertEqual(match.MATCH_IN_PROGRESS, match.new_match('Antônio', 'Bruno', 'Bot 1', 'Bot 2'))

    def test_07_current_player_ok(self):
        self.assertTrue(0 <= match.current_player() <= 3)

    def test_08_play_invalid_piece(self):
        self.assertEqual(match.INVALID_PIECE, match.play(-1))
        self.assertEqual(match.INVALID_PIECE, match.play(16))

    def test_09_play_dice_not_thrown(self):
        self.assertEqual(match.DICE_NOT_THROWN, match.play(0))
        self.assertEqual(match.DICE_NOT_THROWN, match.play(1))

    def test_10_play_ok(self):
        player = match.current_player()
        piece = player * 4

        dice.throw()
        self.assertIsNone(match.play(piece))

    def test_11_can_play_6(self):
        self.assertTrue(match.can_play(6))

    def test_12_can_play_invalid_steps(self):
        self.assertTrue(match.can_play(-1))
        self.assertTrue(match.can_play(7))

    def test_13_close_match_ok(self):
        self.assertIsInstance(match.close_match(), dict)
        self.assertEqual(match.MATCH_NOT_DEFINED, match.play(0))


if __name__ == '__main__':
    unittest.main()
