# Sprites - Transição do Menu Principal
# Atualizado: 15/12/2020
# Autor: Bruno Messeder dos Anjos

import pygame

from gui import gui

__all__ = ['MainTransition']


class MainTransition(pygame.sprite.Sprite):
    """
    Animação que representa a transição do logo no menu principal.
    """

    def __init__(self, logo, on_end=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()

        self.logo = logo
        self.logo_image = logo.image.copy()
        self.logo_rect = self.logo.rect.copy()
        self.start_pos = logo.rect.midtop
        self.end_pos = gui.WIDTH / 2, 64
        self.duration = 2
        self.frames = int(2 * gui.FPS)
        self._current_frame = 0
        self._on_end = on_end
        self._ended = False

        x0, y0 = self.start_pos
        x1, y1 = self.end_pos
        self.dx = x1 - x0
        self.dy = y1 - y0
        self.dw, self.dh = logo.rect.size

    def update(self):
        self._current_frame += 1

        if self._current_frame >= self.frames:
            self.logo.rect = self.logo_rect
            self.logo.image = self.logo_image
            self.kill()
            if not self._ended:
                self._ended = True
                if self._on_end:
                    self._on_end()

        x, y = self.start_pos

        m = self._current_frame / self.frames
        if m < 0.5:
            t = 0
        else:
            t = 4 * (m - 0.5) ** 2

        size = int(2 * self.logo_rect.w - t * self.dw), int(2 * self.logo_rect.h - t * self.dh)

        self.logo.image = pygame.transform.smoothscale(self.logo_image, size)
        self.logo.rect = self.logo.image.get_rect(midtop=(x + t * self.dx, y + t * self.dy))

    def equals(self, other):
        if not isinstance(other, MainTransition):
            return False

        return self.logo == other.logo and self.end_pos == other.end_pos
