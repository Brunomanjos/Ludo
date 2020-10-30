# Sprites - Peça
# Atualizado: 30/10/2020
# Autor: Bruno Messeder dos Anjos

import pygame
from pygame import gfxdraw
from pygame.locals import *

from gui.sprite.event_sprite import EventSprite

__all__ = ['PieceSprite']

radius = 25
colors = [(0, 150, 0), (150, 0, 0), (150, 150, 0), (0, 0, 150)]


class PieceSprite(EventSprite):

    def __init__(self, piece_id, **pos):
        super().__init__([])
        self.image = pygame.Surface((2 * radius + 1, 2 * radius + 1), SRCALPHA)
        self.rect = self.image.get_rect(**pos)
        self.fg = (255, 255, 255)
        self.font = pygame.font.SysFont('monospace', 24, 1)
        self.piece_id = piece_id
        # TODO self.color = piece.get_color(piece)
        self.text = ''
        self.color = colors[piece_id // 4]

    def update(self):
        gfxdraw.aacircle(self.image, radius, radius, radius, self.color)
        gfxdraw.filled_circle(self.image, radius, radius, radius, self.color)

        text_render = self.font.render(self.text, 1, self.fg)
        text_w, text_h = text_render.get_rect().size
        text_rect = pygame.rect.Rect(0, 0, text_w, text_h)
        text_rect.center = self.rect.w / 2, self.rect.h / 2
        self.image.blit(text_render, text_rect)

    def collidepoint(self, point):
        dx = self.rect.centerx - point[0]
        dy = self.rect.centery - point[1]
        return dx ** 2 + dy ** 2 <= radius ** 2
