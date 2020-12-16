# Sprites - PlayerDialog
# Atualizado: 15/12/2020
# Autor: Bruno Messeder dos Anjos

import pygame
from pygame.locals import *

import gui
from gui.sprite import EventSprite

__all__ = ['PlayerDialog']

dialog_images = [pygame.image.load('res/players/green/headliner_green.png'),
                 pygame.image.load('res/players/red/headliner_red.png'),
                 pygame.image.load('res/players/blue/headliner_blue.png'),
                 pygame.image.load('res/players/yellow/headliner_yellow.png')]


class PlayerDialog(EventSprite):
    """
    Sprite que representa um diálogo customizado para cada jogador.
    """

    def __init__(self):
        super().__init__([MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION])
        self._queue = []
        self.font_1 = pygame.font.Font('res/fonts/LemonMilk.otf', 25)
        self.font_2 = pygame.font.SysFont('Monospaced.ttf', 42)
        self.font = self.font_1
        self.image = pygame.Surface(gui.SIZE, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0, 147))
        self.end_dialog = False

    def show(self, message, player_color=None):
        self._queue.append([message, player_color])

    def mouse_down(self, event):
        return True

    def mouse_motion(self, event):
        return True

    def mouse_up(self, event):
        if self.end_dialog:
            self.end_dialog = False
            self._queue.pop(0)
            gui.show_main_menu()
        elif len(self._queue) == 0:
            self.image.fill((0, 0, 0, 147))
            self.kill()
        else:
            self._queue.pop(0)
            if len(self._queue) == 0:
                self.kill()

        return True

    def update(self):
        if len(self._queue) == 0:
            return

        self.image.fill((0, 0, 0, 147))

        text, image_index = self._queue[0]

        if image_index is None:
            fg = (0, 0, 0)
            self.font = self.font_2
        else:
            fg = (255, 255, 255)
            self.font = self.font_1

        lines = text.split('\n')
        text_surface = self._get_text_surface(lines)

        y = 0
        for line in lines:
            y += self._draw_line(text_surface, line, y, fg)

        render_rect = text_surface.get_rect(center=(self.rect.w / 2, self.rect.h / 2))

        if image_index is None:
            image = pygame.Surface((render_rect.w + 20, render_rect.h + 20))
            image.fill((255, 255, 255))
        else:
            image = dialog_images[image_index]

        image_rect = image.get_rect(center=gui.CENTER)

        self.image.blit(image, image_rect.topleft)

        self.image.blit(text_surface, render_rect)

    def _draw_line(self, surface, line, y, fg):
        line_render = self.font.render(line, 1, fg)
        line_w, line_h = line_render.get_rect().size
        line_rect = pygame.Rect(0, y, line_w, line_h)

        surface.blit(line_render, line_rect)
        return line_h

    def _get_text_surface(self, lines):
        render_w, render_h = 0, 0

        for line in lines:
            line_w, line_h = self.font.size(line)
            render_w = max(render_w, line_w)
            render_h += line_h

        return pygame.Surface((render_w, render_h), pygame.SRCALPHA)
