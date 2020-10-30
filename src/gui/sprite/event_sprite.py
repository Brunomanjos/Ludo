# Sprites - Eventos
# Atualizado: 30/10/2020
# Autor: Bruno Messeder dos Anjos

import pygame
from pygame.locals import *

__all__ = ['EventSprite']


class EventSprite(pygame.sprite.Sprite):

    def __init__(self, events, handler=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.events = events
        self.handler = handler

    def handle_event(self, event):
        if self.handler:
            return self.handler(event)
        elif event.type == KEYDOWN:
            return self.key_down(event)
        elif event.type == KEYUP:
            return self.key_up(event)
        elif event.type == MOUSEMOTION:
            return self.mouse_motion(event)
        elif event.type == MOUSEBUTTONUP:
            return self.mouse_up(event)
        elif event.type == MOUSEBUTTONDOWN:
            return self.mouse_down(event)
