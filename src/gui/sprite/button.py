# Sprites - Botão
# Atualizado: 14/12/2020
# Autor: Bruno Messeder dos Anjos
import os

import pygame
from pygame.locals import *

from gui.sprite.event_sprite import EventSprite

__all__ = ['Button']


def darker(color):
    if len(color) == 3:
        return tuple(value * 0.8 for value in color)

    r, g, b, a = color

    return 0.8 * r, 0.8 * g, 0.8 * b, min(a / 0.8, 255)


class Button(EventSprite):
    """
    Sprite que representa um botão.
    """

    def __init__(self, size, text, action, fg=(0, 0, 0), bg=(0, 0, 0), bg_image=None, **pos):
        super().__init__([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN])
        self._selected = False

        self.font = pygame.font.Font('res/fonts/LemonMilklight.otf', 25)
        self.text = text

        self.bg = bg
        self.fg = fg
        self._selection_level = 0

        if bg_image:
            image = pygame.image.load(os.path.join('res/buttons/', bg_image))
            size = image.get_rect().size
            avg_size = int(0.95 * size[0]), int(0.95 * size[1])
            small_size = int(0.95 * avg_size[0]), int(0.95 * avg_size[1])

            avg_image = pygame.transform.smoothscale(image, avg_size)
            small_image = pygame.transform.smoothscale(image, small_size)

            self.bg_images = [image, avg_image, small_image]
        else:
            self.bg_images = None

        self.image = pygame.Surface(size, pygame.SRCALPHA)

        self.rect = self.image.get_rect(**pos)

        self.action = action

    def mouse_down(self, event):
        if event.consumed:
            self._selected = False
            return False

        self._selected = event.button == BUTTON_LEFT and self.rect.collidepoint(event.pos)
        if self._selected:
            self._selection_level = 2
            self._selection_level = 2
        return self._selected

    def mouse_up(self, event):
        if event.consumed:
            self._selected = False
            self._selection_level = 0
            return False

        if not self.rect.collidepoint(event.pos):
            self._selection_level = 0
            return False
        elif not self._selected:
            self._selection_level = 1
            return False
        elif self.action:
            self.action()
        self._selection_level = 0
        return True

    def mouse_motion(self, event):
        if event.consumed:
            self._selection_level = 0
            return False
        elif not self.rect.collidepoint(event.pos):
            self._selection_level = 0
            return False
        elif pygame.mouse.get_pressed()[0] and self._selected:
            self._selection_level = 2
        else:
            self._selection_level = 1
        return True

    def update(self):
        bg, fg = self.bg, self.fg
        for level in range(self._selection_level):
            bg, fg = darker(bg), darker(fg)

        if self.bg_images is not None:
            image = self.bg_images[self._selection_level]
            x, y = image.get_rect(center=(self.rect.w / 2, self.rect.h / 2)).topleft

            self.image.fill((0, 0, 0, 0))
            self.image.blit(image, (x, y))
        else:
            self.image.fill(bg)

        font = self.font

        if self.bg_images is not None:
            font = pygame.font.Font('res/fonts/LemonMilklight.otf', int(25 * 0.95 ** self._selection_level))

        text_render = font.render(self.text, 1, self.fg)
        text_w, text_h = text_render.get_rect().size

        center_rect = pygame.rect.Rect(0, 0, text_w, text_h)
        center_rect.center = self.rect.w / 2, self.rect.h / 2
        self.image.blit(text_render, center_rect)
