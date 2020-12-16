# Sprites - Peça
# Atualizado: 15/12/2020
# Autor: Bruno Messeder dos Anjos

import pygame
from pygame import gfxdraw
from pygame.locals import *

import board
import piece
from gui.sprite.event_sprite import EventSprite

__all__ = ['PieceSprite']

images = {
    color: [pygame.image.load(f'res/players/{color}/{index}_{color}.png') for index in range(1, 5)] for color in
    ['blue', 'red', 'yellow', 'green']
}


class PieceSprite(EventSprite):
    """
    Sprite que representa uma peça do jogo.
    """

    def __init__(self, piece_id, **pos):
        super().__init__([])
        self.fg = (255, 255, 255)
        self.font = pygame.font.SysFont('monospace', 24, 1)
        self.piece_id = piece_id
        self.color = piece.corPeca(piece_id)

        self._images = images[piece.nomeCorPeca(piece_id)]
        self.image_index = 0
        self.image = self._images[0]
        self.rect = self.image.get_rect(**pos)

    def update_block(self):
        self.image_index = len(board.get_pieces_at(board.get_piece_position(self.piece_id))) - 1
        self.image = self._images[self.image_index]

    def collidepoint(self, point):
        radius = self.rect.w / 2

        dx = self.rect.centerx - point[0]
        dy = self.rect.bottom - radius - point[1]
        return dx ** 2 + dy ** 2 <= radius ** 2
