# Teste Automatizado do módulo Piece
# Atualizado: 15/11/2020
# Autor: Alberto Augusto Caldeira Brant

import unittest

import piece


class PieceTest(unittest.TestCase):
    def test_01_buscaGrupo(self):
        self.assertTrue(0 <= piece.buscaGrupo(0) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(1) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(2) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(3) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(4) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(5) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(6) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(7) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(8) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(9) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(10) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(11) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(12) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(13) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(14) <= 15)
        self.assertTrue(0 <= piece.buscaGrupo(15) <= 15)

    def test_02_todasPecas(self):
        self.assertEqual([0, 1, 2, 3], piece.todasPecas(0))
        self.assertEqual([4, 5, 6, 7], piece.todasPecas(1))
        self.assertEqual([8, 9, 10, 11], piece.todasPecas(2))
        self.assertEqual([12, 13, 14, 15], piece.todasPecas(3))

    def test_03_corPeca(self):
        self.assertEqual((0, 150, 0), piece.corPeca(0))
        self.assertEqual((0, 150, 0), piece.corPeca(1))
        self.assertEqual((0, 150, 0), piece.corPeca(2))
        self.assertEqual((0, 150, 0), piece.corPeca(3))

        self.assertEqual((150, 0, 0), piece.corPeca(4))
        self.assertEqual((150, 0, 0), piece.corPeca(5))
        self.assertEqual((150, 0, 0), piece.corPeca(6))
        self.assertEqual((150, 0, 0), piece.corPeca(7))

        self.assertEqual((0, 0, 150), piece.corPeca(8))
        self.assertEqual((0, 0, 150), piece.corPeca(9))
        self.assertEqual((0, 0, 150), piece.corPeca(10))
        self.assertEqual((0, 0, 150), piece.corPeca(11))

        self.assertEqual((150, 150, 0), piece.corPeca(12))
        self.assertEqual((150, 150, 0), piece.corPeca(13))
        self.assertEqual((150, 150, 0), piece.corPeca(14))
        self.assertEqual((150, 150, 0), piece.corPeca(15))


if __name__ == '__main__':
    unittest.main()
