# Sprites - Transição
# Atualizado: 30/10/2020
# Autor: Bruno Messeder dos Anjos

import pygame

from gui import gui

__all__ = ['Transition']


class Transition(pygame.sprite.Sprite):

    def __init__(self, piece, new_pos, duration, on_end=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()

        self.piece = piece
        self.start_pos = piece.rect.center
        self.end_pos = new_pos
        self.duration = duration
        self.frames = duration * gui.FPS
        self._current_frame = 0
        self._on_end = on_end

        x0, y0 = self.start_pos
        x1, y1 = self.end_pos
        self.dx = x1 - x0
        self.dy = y1 - y0

    def update(self):
        self._current_frame += 1

        if self._current_frame == self.frames and self._on_end:
            self._on_end()
        if self._current_frame > self.frames:
            self.piece.rect.center = self.end_pos
            self.kill()

        self.piece.selected = False

        x, y = self.start_pos

        m = self._current_frame / self.frames
        if m > 0.5:
            t = 1 + 4 * (m - 1) ** 3
        else:
            t = 4 * m ** 3

        self.piece.rect.center = x + t * self.dx, y + t * self.dy
