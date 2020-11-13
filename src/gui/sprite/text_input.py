# Sprites - Entrada de Texto
# Atualizado: 30/10/2020
# Autor: Bruno Messeder dos Anjos

import pygame
from pygame.locals import *

import gui
from gui.sprite.event_sprite import EventSprite

__all__ = ['TextInput']


class TextInput(EventSprite):
    """
    Sprite que representa uma entrada de texto.
    """

    def __init__(self, size, action, bg=(255, 255, 255), fg=(0, 0, 0),
                 font=None, **pos):
        super().__init__([KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION])
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(**pos)
        self.action = action
        self.font = font or pygame.font.SysFont('monospace', 16)
        self.bg = bg
        self.fg = fg
        self.text = ""
        self.selected = False
        self._caret_index = 0
        self._caret_anim_frame = 0

    def key_down(self, event):
        if event.consumed or not self.selected:
            return False

        key = event.key
        if key == K_BACKSPACE:
            index = self._caret_index
            if index != 0:
                self.text = self.text[:index - 1] + self.text[index:]
                self._caret_index -= 1
        elif key == K_DELETE:
            index = self._caret_index
            self.text = self.text[:index] + self.text[index + 1:]
        elif key == K_RETURN or key == K_KP_ENTER:
            if self.action:
                self.action()
        elif key == K_LEFT:
            self._caret_index = max(0, self._caret_index - 1)
        elif key == K_RIGHT:
            self._caret_index = min(len(self.text), self._caret_index + 1)
        elif key == K_HOME or key == K_UP:
            self._caret_index = 0
        elif key == K_END or key == K_DOWN:
            self._caret_index = len(self.text)
        elif event.dict.get('unicode', None) and repr(event.unicode)[1] != '\\':  # printable character
            index = self._caret_index
            self.text = self.text[:index] + event.unicode + self.text[index:]
            self._caret_index += 1

        self._caret_anim_frame = 0
        return True

    def mouse_down(self, event):
        if event.consumed or not self.rect.collidepoint(event.pos):
            self.selected = False
            return False
        elif event.button != 1:
            return False

        self._caret_anim_frame = 0
        self.selected = self.rect.collidepoint(event.pos)
        if self.selected:
            self._select_char_at(event.pos)

        return self.selected

    def mouse_up(self, event):
        if self.selected:
            self._select_char_at(event.pos)
            return True

    def mouse_motion(self, event):
        if not event.consumed and event.buttons[0] and self.selected:
            self._select_char_at(event.pos)
            self._caret_anim_frame = 0
            return True

    def _select_char_at(self, pos):
        if len(self.text) == 0:
            return

        x = pos[0] - self.rect.x - 5
        index = 0
        text_render = self.font.render(self.text[0], 1, self.fg)
        while x > text_render.get_rect().w and index <= len(self.text):
            index += 1
            text_render = self.font.render(self.text[:index], 1, self.fg)
        self._caret_index = max(0, index - 1)

    def update(self):
        self.image.fill(self.bg)
        self._draw_text()
        self._draw_caret()

    def _draw_text(self):
        text_render = self.font.render(self.text, 1, self.fg)
        text_w, text_h = text_render.get_rect().size

        text_rect = pygame.rect.Rect(0, 0, text_w, text_h)
        text_rect.midleft = 10, self.rect.h / 2
        self.image.blit(text_render, text_rect)

    def _draw_caret(self):
        if not self.selected:
            self._caret_anim_frame = 0
            return

        self._caret_anim_frame += 1

        if self._caret_anim_frame > gui.FPS:
            self._caret_anim_frame = 0
        elif self._caret_anim_frame > gui.FPS / 2:
            return

        w, h = self.font.size(self.text[0:self._caret_index])
        caret_rect = pygame.rect.Rect(9 + w, self.rect.h / 2 - h / 2, 2, h)
        self.image.fill((0, 0, 0), caret_rect)
