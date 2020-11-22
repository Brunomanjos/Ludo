# Sprites - Transição
# Atualizado: 22/11/2020
# Autor: Bruno Messeder dos Anjos

import pygame

from gui import gui

__all__ = ['Transition']


class Transition(pygame.sprite.Sprite):
    """
    Animação que representa uma transição de um sprite para uma nova posição.
    """

    def __init__(self, sprite, new_pos, duration, on_end=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()

        self.sprite = sprite
        self.start_pos = sprite.rect.center
        self.end_pos = new_pos
        self.duration = duration
        self.frames = int(duration * gui.FPS)
        self._current_frame = 0
        self._on_end = on_end
        self._ended = False

        x0, y0 = self.start_pos
        x1, y1 = self.end_pos
        self.dx = x1 - x0
        self.dy = y1 - y0

    def update(self):
        self._current_frame += 1

        if self._current_frame >= self.frames:
            self.sprite.rect.center = self.end_pos
            self.kill()
            if not self._ended:
                self._ended = True
                if self._on_end:
                    self._on_end()

        x, y = self.start_pos

        m = self._current_frame / self.frames
        if m > 0.5:
            t = 1 + 4 * (m - 1) ** 3
        else:
            t = 4 * m ** 3

        self.sprite.rect.center = x + t * self.dx, y + t * self.dy
