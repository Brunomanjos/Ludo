# Teste Automatizado do módulo Board
# Atualizado: 30/10/2020
# autor: Bruno Messeder dos Anjos

import unittest

import board


class BoardTest(unittest.TestCase):

    def test_01_get_spawn_points_ok(self):
        self.assertEqual({4: (1, 10), 5: (1, 13), 6: (4, 10), 7: (4, 13)}, board.get_spawn_positions(1))

        self.assertEqual({0: (1, 1), 1: (1, 4), 2: (4, 1), 3: (4, 4),
                          4: (1, 10), 5: (1, 13), 6: (4, 10), 7: (4, 13),
                          8: (10, 1), 9: (10, 4), 10: (13, 1), 11: (13, 4),
                          12: (10, 10), 13: (10, 13), 14: (13, 10), 15: (13, 13)
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

    def test_06_get_piece_positions_ok(self):
        self.assertEqual(board.get_spawn_positions(), board.get_pieces_positions())
        self.assertEqual(board.get_spawn_positions(1), board.get_pieces_positions(1))

    def test_07_get_piece_positions_invalid_group(self):
        self.assertEqual(board.INVALID_GROUP, board.get_pieces_positions(-1))
        self.assertEqual(board.INVALID_GROUP, board.get_pieces_positions(4))

    def test_08_get_piece_position_ok(self):
        self.assertEqual((13, 13), board.get_piece_position(15))

    def test_09_get_piece_position_invalid_piece_id(self):
        self.assertEqual(board.INVALID_PIECE_ID, board.get_piece_position(-1))
        self.assertEqual(board.INVALID_PIECE_ID, board.get_piece_position(16))

    def test_10_set_piece_pos_invalid_piece_id(self):
        self.assertEqual(board.INVALID_PIECE_ID, board.set_piece_position(-1, (-1, -1)))
        self.assertEqual(board.INVALID_PIECE_ID, board.set_piece_position(16, (-1, -1)))

    def test_11_set_piece_pos_invalid_position_for_group(self):
        # a posição (1, 7) é válida apenas para o grupo 1
        self.assertEqual(board.NOT_ON_PATH, board.set_piece_position(0, (1, 7)))
        self.assertEqual(board.NOT_ON_PATH, board.set_piece_position(1, (1, 7)))
        self.assertEqual(board.NOT_ON_PATH, board.set_piece_position(3, (1, 7)))
        self.assertIsNone(board.set_piece_position(5, (1, 7)))

    def test_12_get_pieces_at(self):
        board.set_piece_position(7, (6, 10))
        board.set_piece_position(8, (6, 10))
        board.set_piece_position(0, (6, 1))
        self.assertEqual([7, 8], board.get_pieces_at((6, 10)))
        self.assertEqual([0], board.get_pieces_at((6, 1)))
        self.assertEqual([], board.get_pieces_at((-1, -1)))
        self.assertEqual([], board.get_pieces_at((2, 2)))
        self.assertEqual([0, 7, 8], board.get_pieces_at([(2, 2), (6, 10), (6, 1)]))

    def test_13_get_possible_move_ok(self):
        board.set_piece_position(5, (0, 7))
        board.set_piece_position(0, (3, 6))
        # uma peça passando por outra peça
        self.assertEqual((1, 8), board.get_possible_move(0, 6))
        self.assertEqual((0, 7), board.get_possible_move(0, 4))
        # uma peça passando por um bloco
        board.set_piece_position(4, (0, 7))
        self.assertEqual((0, 6), board.get_possible_move(0, 6))
        self.assertEqual((0, 6), board.get_possible_move(0, 4))
        # um bloco passando por outro bloco
        board.set_piece_position(1, (3, 6))
        self.assertEqual((1, 8), board.get_possible_move(0, 6))
        self.assertEqual((1, 8), board.get_possible_move(1, 6))
        self.assertEqual((0, 7), board.get_possible_move(0, 4))
        # um bloco passando por uma peça
        board.set_piece_position(4, (1, 8))
        self.assertEqual((1, 8), board.get_possible_move(0, 6))
        self.assertEqual((0, 7), board.get_possible_move(0, 4))
        self.assertEqual((0, 7), board.get_possible_move(0, 4))
        # um bloco passando por uma peça, mesmo grupo
        board.set_piece_position(2, (2, 6))
        self.assertEqual((1, 8), board.get_possible_move(0, 6))
        self.assertEqual((3, 6), board.get_possible_move(0, 1))
        # um bloco passando por outro bloco, mesmo grupo
        board.set_piece_position(3, (2, 6))
        self.assertEqual((1, 8), board.get_possible_move(0, 6))
        self.assertEqual((3, 6), board.get_possible_move(0, 1))

    def test_14_possible_moves_ok(self):
        self.assertEqual({0: (1, 8), 1: (1, 8), 2: (2, 8), 3: (2, 8)}, board.get_possible_moves(0, 6))
        self.assertEqual({0: (3, 6), 1: (3, 6), 2: (1, 6), 3: (1, 6)}, board.get_possible_moves(0, 1))
        self.assertEqual({4: (3, 8), 5: (2, 7), 6: None, 7: (6, 12)}, board.get_possible_moves(1, 2))

    def test_15_possible_moves_invalid_group(self):
        self.assertEqual(board.INVALID_GROUP, board.get_possible_moves(-1, 1))
        self.assertEqual(board.INVALID_GROUP, board.get_possible_moves(4, 1))

    def test_16_possible_moves_negative_steps(self):
        self.assertEqual(board.NEGATIVE_STEPS, board.get_possible_moves(0, -1))

    def test_17_reset_board(self):
        self.assertTrue(board.get_pieces_positions() != board.get_spawn_positions())
        board.reset_board()
        self.assertEqual(board.get_spawn_positions(), board.get_pieces_positions())

    def test_18_move_piece_ok(self):
        self.assertTrue(board.move_piece(0, 6))
        self.assertEqual((5, 6), board.get_piece_position(0))
        self.assertTrue(board.move_piece(0, 10))
        self.assertEqual((3, 8), board.get_piece_position(0))

    def test_19_move_one_piece_through_other(self):
        self.assertTrue(board.move_piece(4, 6))
        self.assertEqual((6, 9), board.get_piece_position(4))
        self.assertEqual((3, 8), board.get_piece_position(0))

    def test_20_move_one_piece_to_other_different_group(self):
        self.assertTrue(board.move_piece(0, 3))
        self.assertEqual((1, 10), board.get_piece_position(4))

    def test_21_move_one_piece_to_other_same_group(self):
        self.assertTrue(board.move_piece(8, 6))
        self.assertTrue(board.move_piece(9, 6))
        self.assertEqual((8, 5), board.get_piece_position(8))
        self.assertEqual((8, 5), board.get_piece_position(8))

    def test_22_move_piece_group(self):
        self.assertTrue(board.move_piece(8, 6))
        self.assertEqual((7, 0), board.get_piece_position(8))
        self.assertEqual((7, 0), board.get_piece_position(9))

    def test_23_move_one_block_through_other(self):
        self.assertTrue(board.move_piece(9, 8))
        self.assertTrue(board.move_piece(1, 6))
        self.assertTrue(board.move_piece(2, 6))
        self.assertTrue(board.move_piece(1, 3))
        self.assertEqual((4, 6), board.get_piece_position(8))
        self.assertEqual((4, 6), board.get_piece_position(9))
        self.assertEqual((2, 6), board.get_piece_position(1))
        self.assertEqual((2, 6), board.get_piece_position(2))

    def test_24_move_one_piece_through_block(self):
        self.assertTrue(board.move_piece(3, 6))
        self.assertEqual((4, 6), board.get_piece_position(8))
        self.assertEqual((4, 6), board.get_piece_position(9))
        self.assertEqual((5, 6), board.get_piece_position(3))

    def help_25_move_one_piece_to_finish(self, piece):
        board.move_piece(piece, 6)
        for iteration in range(100):
            board.move_piece(piece, 1)
            if piece in board.get_pieces_at(board.get_finish_position(piece // 4)):
                return

        self.assertTrue(False, 'piece moving loop took more than 100 iterations '
                               'to get to finish point. This should never happen')

    def test_25_all_pieces_from_spawn_to_finish_one_step(self):
        board.reset_board()
        for piece in range(16):
            self.help_25_move_one_piece_to_finish(piece)


if __name__ == '__main__':
    unittest.main()
