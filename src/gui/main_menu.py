# Módulo GUI - Menu Principal
# Atualizado: 12/11/2020
# Autor: Bruno Messeder dos Anjos

import pygame

import match
from gui.sprite import *

__all__ = ['get']


def match_history_action():
    pass  # TODO show watch match menu


def load_match_action():
    import gui
    match.load_match(1)
    gui.show_board()
    # TODO show load match menu


def init():
    import gui
    global menu

    new_game = Button((240, 80),
                      'Novo Jogo',
                      gui.show_set_players_menu,
                      bg=(134, 184, 53),
                      center=(gui.WIDTH / 2, gui.HEIGHT / 2 - 180))

    load_game = Button((240, 80),
                       'Carregar Partida',
                       load_match_action,
                       bg=(134, 184, 53),
                       center=(gui.WIDTH / 2, gui.HEIGHT / 2 - 60))

    match_history = Button((240, 80),
                           'Histórico de Partidas',
                           match_history_action,
                           bg=(134, 184, 53),
                           center=(gui.WIDTH / 2, gui.HEIGHT / 2 + 60))

    exit = Button((240, 80),
                  'Sair',
                  gui.exit_gui,
                  bg=(134, 184, 53),
                  center=(gui.WIDTH / 2, gui.HEIGHT / 2 + 180))

    bg = Canvas((gui.WIDTH, gui.HEIGHT))
    bg.image.fill((100, 100, 100))

    menu = pygame.sprite.Group(bg, new_game, load_game, match_history, exit)


def get():
    """
    Inicializa a tela do menu principal e retorna os sprites presentes na tela.
    """
    if not menu:
        init()
    return menu


menu = None
