# autor: Bruno Messeder dos Anjos

import unittest
import board
from board.board import set_piece_position  # apenas para testes


class TestCase(unittest.TestCase):

    def test_01_get_spawn_points_ok(self):
        self.assertEqual({4: (2, 11), 5: (2, 12), 6: (3, 11), 7: (3, 12)}, board.get_spawn_positions(1))

        self.assertEqual({0: (2, 2), 1: (2, 3), 2: (3, 2), 3: (3, 3),
                          4: (2, 11), 5: (2, 12), 6: (3, 11), 7: (3, 12),
                          8: (11, 2), 9: (11, 3), 10: (12, 2), 11: (12, 3),
                          12: (11, 11), 13: (11, 12), 14: (12, 11), 15: (12, 12)
                          }, board.get_spawn_positions())

    def test_02_get_spawn_points_invalid_group(self):
        self.assertEqual(board.INVALID_GROUP, board.get_spawn_positions(-1))
        self.assertEqual(board.INVALID_GROUP, board.get_spawn_positions(4))

    def test_03_get_finish_point_ok(self):
        self.assertEqual((8, 7), board.get_finish_position(2))

    def test_04_get_finish_point_invalid_group(self):
        self.assertEqual(board.INVALID_GROUP, board.get_finish_position(-1))
        self.assertEqual(board.INVALID_GROUP, board.get_finish_position(4))

    def test_05_get_finish_points_ok(self):
        self.assertEqual([(7, 6), (6, 7), (8, 7), (7, 8)], board.get_finish_positions())

    def test_06_is_finish_point_ok(self):
        self.assertTrue(board.is_finish_position((7, 6)))
        self.assertTrue(board.is_finish_position((7, 6), 0))
        self.assertFalse(board.is_finish_position((7, 6), 1))
        self.assertFalse(board.is_finish_position((0, 0)))
        self.assertFalse(board.is_finish_position((-4, 100)))

    def test_07_is_finish_point_invalid_group(self):
        self.assertEqual(board.INVALID_GROUP, board.is_finish_position((1, 1), -1))
        self.assertEqual(board.INVALID_GROUP, board.is_finish_position((1, 1), 4))

    def test_08_overflow(self):
        self.assertEqual((7, 1), board.get_next_position((7, 5), 0, 2))
        self.assertEqual((1, 7), board.get_next_position((2, 7), 1, 6))

    def test_09_get_piece_positions_ok(self):
        self.assertEqual(board.get_spawn_positions(), board.get_pieces_positions())
        self.assertEqual(board.get_spawn_positions(1), board.get_pieces_positions(1))

    def test_10_get_piece_positions_invalid_group(self):
        self.assertEqual(board.INVALID_GROUP, board.get_pieces_positions(-1))
        self.assertEqual(board.INVALID_GROUP, board.get_pieces_positions(4))

    def test_11_get_piece_position_ok(self):
        self.assertEqual((12, 12), board.get_piece_position(15))

    def test_12_get_piece_position_invalid_piece_id(self):
        self.assertEqual(board.INVALID_PIECE_ID, board.get_piece_position(-1))
        self.assertEqual(board.INVALID_PIECE_ID, board.get_piece_position(16))

    def test_13_set_piece_pos_invalid_position(self):
        self.assertEqual(2, set_piece_position(0, (5, 5)))
        self.assertEqual(2, set_piece_position(0, (-1, -1)))
        self.assertEqual(2, set_piece_position(0, (7, 7)))

    def test_14_set_piece_pos_invalid_piece_id(self):
        self.assertEqual(board.INVALID_PIECE_ID, set_piece_position(-1, (-1, -1)))
        self.assertEqual(board.INVALID_PIECE_ID, set_piece_position(16, (-1, -1)))

    def test_15_set_piece_pos_invalid_position_for_group(self):
        # a posição (1, 7) é válida apenas para o grupo 1
        self.assertEqual(board.NOT_ON_PATH, set_piece_position(0, (1, 7)))
        self.assertEqual(board.NOT_ON_PATH, set_piece_position(1, (1, 7)))
        self.assertEqual(board.NOT_ON_PATH, set_piece_position(3, (1, 7)))
        self.assertIsNone(set_piece_position(5, (1, 7)))

    def test_16_get_pieces_at(self):
        set_piece_position(7, (6, 10))
        set_piece_position(8, (6, 10))
        set_piece_position(0, (6, 1))
        self.assertEqual([7, 8], board.get_pieces_at((6, 10)))
        self.assertEqual([0], board.get_pieces_at((6, 1)))
        self.assertEqual([], board.get_pieces_at((-1, -1)))
        self.assertEqual([], board.get_pieces_at((2, 2)))
        self.assertEqual([0, 7, 8], board.get_pieces_at([(2, 2), (6, 10), (6, 1)]))

    def test_17_get_possible_move_ok(self):
        set_piece_position(5, (0, 7))
        set_piece_position(0, (3, 6))
        # uma peça passando por outra peça
        self.assertEqual((1, 8), board.get_possible_move(0, 6))
        self.assertEqual((0, 7), board.get_possible_move(0, 4))
        # uma peça passando por um bloco
        set_piece_position(4, (0, 7))
        self.assertEqual((0, 6), board.get_possible_move(0, 6))
        self.assertEqual((0, 6), board.get_possible_move(0, 4))
        # um bloco passando por outro bloco
        set_piece_position(1, (3, 6))
        self.assertEqual((1, 8), board.get_possible_move(0, 6))
        self.assertEqual((1, 8), board.get_possible_move(1, 6))
        self.assertEqual((0, 7), board.get_possible_move(0, 4))
        # um bloco passando por uma peça
        set_piece_position(4, (1, 8))
        self.assertEqual((1, 8), board.get_possible_move(0, 6))
        self.assertEqual((0, 7), board.get_possible_move(0, 4))
        self.assertEqual((0, 7), board.get_possible_move(0, 4))
        # um bloco passando por uma peça, mesmo grupo
        set_piece_position(2, (2, 6))
        self.assertEqual((1, 8), board.get_possible_move(0, 6))
        self.assertIsNone(board.get_possible_move(0, 1))
        # um bloco passando por outro bloco, mesmo grupo
        set_piece_position(3, (2, 6))
        self.assertEqual((1, 8), board.get_possible_move(0, 6))
        self.assertIsNone(board.get_possible_move(0, 1))

    def test_18_possible_moves_ok(self):
        self.assertEqual({0: (1, 8), 1: (1, 8), 2: (2, 8), 3: (2, 8)}, board.get_possible_moves(0, 6))
        self.assertEqual({0: None, 1: None, 2: (1, 6), 3: (1, 6)}, board.get_possible_moves(0, 1))
        self.assertEqual({4: (3, 8), 5: (2, 7), 6: (2, 8), 7: (6, 12)}, board.get_possible_moves(1, 2))

    def test_19_possible_moves_invalid_group(self):
        self.assertEqual(board.INVALID_GROUP, board.get_possible_moves(-1, 1))
        self.assertEqual(board.INVALID_GROUP, board.get_possible_moves(4, 1))

    def test_20_possible_moves_negative_steps(self):
        self.assertEqual(board.NEGATIVE_STEPS, board.get_possible_moves(0, -1))

    def test_21_get_path_ok(self):
        self.assertEqual([(2, 2), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (5, 6)], board.get_path((2, 2), 0, 6))
        self.assertEqual([(8, 0), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5)], board.get_path((8, 0), 0, 6))
        self.assertEqual([(8, 0), (7, 0), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4)], board.get_path((8, 0), 1, 6))
        self.assertEqual([(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)], board.get_path((7, 1), 0, 5))
        self.assertEqual([(7, 3), (7, 4), (7, 5), (7, 6), (7, 1)], board.get_path((7, 3), 0, 6))
        self.assertEqual([(6, 1)], board.get_path((6, 1), 0, 0))

    def test_22_get_path_invalid_position(self):
        self.assertEqual(board.NOT_ON_PATH, board.get_path((0, 0), 0, 1))
        self.assertEqual(board.NOT_ON_PATH, board.get_path((-1, -1), 0, 1))
        self.assertEqual(board.NOT_ON_PATH, board.get_path((7, 7), 0, 1))
        self.assertEqual(board.NOT_ON_PATH, board.get_path((7, 7), 0, 0))

    def test_23_get_path_invalid_group(self):
        self.assertEqual(board.INVALID_GROUP, board.get_path((6, 1), -1, 1))
        self.assertEqual(board.INVALID_GROUP, board.get_path((6, 1), 4, 1))

    def test_24_get_path_negative_steps(self):
        self.assertEqual(board.NEGATIVE_STEPS, board.get_path((6, 1), 0, -1))
        self.assertEqual(board.NEGATIVE_STEPS, board.get_path((6, 1), 0, -10))

    def test_25_reset_board(self):
        self.assertTrue(board.get_pieces_positions() != board.get_spawn_positions())
        board.reset_board()
        self.assertEqual(board.get_spawn_positions(), board.get_pieces_positions())

    def test_26_move_piece_ok(self):
        board.reset_board()
        self.assertTrue(board.move_piece(0, 6))
        self.assertEqual((5, 6), board.get_piece_position(0))
        self.assertTrue(board.move_piece(0, 10))
        self.assertEqual((3, 8), board.get_piece_position(0))
        self.assertTrue(board.move_piece(4, 6))
        self.assertEqual((6, 9), board.get_piece_position(4))
        # a peça 4 passa pela peça 0. nada acontece
        self.assertEqual((3, 8), board.get_piece_position(0))
        # a peça 0 para na mesma casa da peça 4. a peça 4 volta para a origem
        self.assertTrue(board.move_piece(0, 3))
        self.assertEqual((2, 11), board.get_piece_position(4))
        self.assertTrue(board.move_piece(8, 6))
        self.assertTrue(board.move_piece(9, 6))
        # duas peças iguais na mesma casa andam juntas
        self.assertTrue(board.move_piece(8, 6))
        self.assertEqual((7, 0), board.get_piece_position(8))
        self.assertEqual((7, 0), board.get_piece_position(9))
        # um bloco passa por outro. nada acontece
        self.assertTrue(board.move_piece(9, 6))
        self.assertTrue(board.move_piece(1, 1))
        self.assertTrue(board.move_piece(2, 1))
        self.assertTrue(board.move_piece(1, 6))
        self.assertEqual((6, 5), board.get_piece_position(8))
        self.assertEqual((6, 5), board.get_piece_position(9))
        self.assertEqual((4, 6), board.get_piece_position(1))
        self.assertEqual((4, 6), board.get_piece_position(2))
        # uma peça não pode passar de um bloco
        self.assertTrue(board.move_piece(3, 6))
        self.assertEqual((6, 5), board.get_piece_position(8))
        self.assertEqual((6, 5), board.get_piece_position(9))
        self.assertEqual((6, 4), board.get_piece_position(3))

    def help_27_move_one_piece_to_finish(self, piece):
        for iteration in range(100):
            current_pos = board.get_piece_position(piece)
            board.move_piece(current_pos, 1)
            if piece in board.get_pieces_at(board.get_finish_position(piece // 4)):
                return

        self.assertTrue(False, 'piece moving loop took more than 100 iterations '
                               'to get to finish point. This should never happen')

    def test_27_all_pieces_from_spawn_to_finish_one_step(self):
        for piece in range(16):
            self.help_27_move_one_piece_to_finish(piece)


if __name__ == '__main__':
    unittest.main()
