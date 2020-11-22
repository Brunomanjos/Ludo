# Sprites - Highlight de Movimentos
# Atualizado: 01/11/2020
# Autor: Bruno Messeder dos Anjos

import pygame

import board
import dice
import gui
import gui.board_screen
import match

__all__ = ['MovementHighlight']

import piece


class MovementHighlight(pygame.sprite.Sprite):
    """
    Sprite que representa o highlight das peças do jogador atual.
    """

    def __init__(self, board_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((board_rect.w, board_rect.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=board_rect.center)
        self._anim_frame = 0
        self._alpha = 0
        self.hovering = None

    def update(self):
        self.image.fill((0, 0, 0, 0))

        dice_value = dice.get()

        if dice_value is None:
            self._anim_frame = 0
            return

        player = match.current_player()

        if player == match.MATCH_NOT_DEFINED:
            return

        moves = board.get_possible_moves(player, dice_value)

        if self.hovering in moves:
            if moves[self.hovering] is None:
                moves = {}
            else:
                moves = {self.hovering: moves[self.hovering]}

        self._anim_frame += 1
        if self._anim_frame > 1.5 * gui.FPS:
            self._anim_frame = 0

        t = self._anim_frame / (1.5 * gui.FPS)

        if t < 0.25:
            self._alpha = 200 * t / 0.25
        elif t < 0.5:
            self._alpha = 200
        elif t < 0.75:
            self._alpha = 200 * (0.75 - t) / 0.25
        else:
            self._alpha = 0

        for move in set(moves.values()):
            self._draw_highlight(move, player)

    def _draw_highlight(self, position, player):
        if position is None:
            return

        size = gui.board_screen.square_size

        highlight = pygame.Surface((size, size))
        highlight.set_alpha(self._alpha)
        highlight.fill(piece.corPeca(player * 4))
        rect = highlight.get_rect(topleft=gui.board_screen.get_pos(position, False))

        self.image.blit(highlight, rect)
