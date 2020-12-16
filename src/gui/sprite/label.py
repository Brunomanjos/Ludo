# Sprites - Label
# Atualizado: 15/12/2020
# Autor: Bruno Messeder dos Anjos

import pygame

__all__ = ['Label', 'CENTER', 'LEFT', 'RIGHT']

CENTER = 1
LEFT = 2
RIGHT = 3


class Label(pygame.sprite.Sprite):
    """
    Sprite que representa um texto.
    O texto pode ter múltiplas linhas e pode ser alinhado no centro, na esquerda ou na direita.
    """

    def __init__(self, size, text, font=None, bg=(0, 0, 0, 0), fg=(0, 0, 0), text_align=CENTER, **pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(**pos)
        self.font = font or pygame.font.Font('res/fonts/LemonMilk.otf', 25)
        self.bg = bg
        self.fg = fg
        self.text = text
        self.align = text_align

    def update(self):
        self.image.fill(self.bg)

        lines = self.text.split('\n')
        text_surface = self._get_text_surface(lines)

        y = 0
        for line in lines:
            y += self._draw_line(text_surface, line, y)

        render_rect = text_surface.get_rect(center=(self.rect.w / 2, self.rect.h / 2))

        self.image.blit(text_surface, render_rect)

    def _draw_line(self, surface, line, y):
        render_w = surface.get_rect().w

        line_render = self.font.render(line, 1, self.fg)
        line_w, line_h = line_render.get_rect().size
        line_rect = pygame.Rect(0, y, line_w, line_h)

        if self.align == RIGHT:
            line_rect.right = render_w
        elif self.align == CENTER:
            line_rect.centerx = render_w / 2

        surface.blit(line_render, line_rect)
        return line_h

    def _get_text_surface(self, lines):
        render_w, render_h = 0, 0

        for line in lines:
            line_w, line_h = self.font.size(line)
            render_w = max(render_w, line_w)
            render_h += line_h

        return pygame.Surface((render_w, render_h), pygame.SRCALPHA)
