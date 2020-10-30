# Sprites - Canvas
# Atualizado: 30/10/2020
# Autor: Bruno Messeder dos Anjos

import pygame

from gui.sprite.event_sprite import EventSprite

__all__ = ['Canvas']


class Canvas(EventSprite):

    def __init__(self, size, alpha=False, **pos):
        super().__init__([])

        if alpha:
            self.image = pygame.Surface(size, pygame.SRCALPHA)
        else:
            self.image = pygame.Surface(size)

        self.rect = self.image.get_rect(**pos)
