# Sprites - Botão
# Atualizado: 30/10/2020
# Autor: Bruno Messeder dos Anjos


import pygame
from pygame.locals import *

from gui.sprite.event_sprite import EventSprite

__all__ = ['Button']


def darker(color):
    return tuple(value * 0.8 for value in color)


class Button(EventSprite):
    """
    Sprite que representa um botão.
    """

    def __init__(self, size, text, action, font=None, fg=(255, 255, 255), bg=(0, 0, 0), **pos):
        super().__init__([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN])
        self._selected = False

        self.font = font or pygame.font.SysFont('monospace', 16, 1)
        self.text = text

        self.bg = bg
        self._bg_fill = bg
        self.fg = fg
        self._fg_fill = fg

        self.image = pygame.Surface(size, pygame.SRCALPHA)

        self.rect = self.image.get_rect(**pos)

        self.action = action

    def mouse_down(self, event):
        if event.consumed:
            self._selected = False
            return False

        self._selected = self.rect.collidepoint(event.pos)
        if self._selected:
            self._bg_fill = darker(darker(self.bg))
            self._fg_fill = darker(darker(self.fg))
        return self._selected

    def mouse_up(self, event):
        if event.consumed:
            self._selected = False
            return False

        if not self.rect.collidepoint(event.pos):
            self._bg_fill = self.bg
            self._fg_fill = self.fg
            return False
        elif not self._selected:
            self._bg_fill = darker(self.bg)
            self._fg_fill = darker(self.fg)
            return False
        elif self.action:
            self.action()
        self._bg_fill = self.bg
        self._fg_fill = self.fg
        return True

    def mouse_motion(self, event):
        if event.consumed:
            return False
        elif not self.rect.collidepoint(event.pos):
            self._bg_fill = self.bg
            self._fg_fill = self.fg
            return False
        elif pygame.mouse.get_pressed()[0] and self._selected:
            self._bg_fill = darker(darker(self.bg))
            self._fg_fill = darker(darker(self.fg))
        else:
            self._bg_fill = darker(self.bg)
            self._fg_fill = darker(self.fg)
        return True

    def update(self):
        self.image.fill(self._bg_fill)

        text_render = self.font.render(self.text, 1, self._fg_fill)
        text_w, text_h = text_render.get_rect().size

        center_rect = pygame.rect.Rect(0, 0, text_w, text_h)
        center_rect.center = self.rect.w / 2, self.rect.h / 2
        self.image.blit(text_render, center_rect)
