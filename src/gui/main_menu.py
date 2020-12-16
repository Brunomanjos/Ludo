# Módulo GUI - Menu Principal
# Atualizado: 12/11/2020
# Autor: Bruno Messeder dos Anjos

import pygame

from gui.sprite import *

__all__ = ['get']


def match_history_action():
    import gui
    gui.show_load_watch_match_menu()


def load_match_action():
    import gui
    gui.show_load_match_menu()


def init():
    import gui
    global menu

    logo = Image('main menu/LUDO TITULO PRINCIPAL.png', midtop=(gui.WIDTH / 2, 64))

    new_game = Button((272, 109),
                      'Novo Jogo',
                      gui.show_set_players_menu,
                      bg=(255, 255, 255, 255),
                      bg_image='green.png',
                      center=(gui.WIDTH / 2, gui.HEIGHT / 2 - 160))

    load_game = Button((272, 109),
                       'Carregar',
                       load_match_action,
                       bg=(255, 255, 255, 255),
                       bg_image='blue.png',
                       center=(gui.WIDTH / 2, gui.HEIGHT / 2 - 20))

    match_history = Button((272, 109),
                           'Histórico',
                           match_history_action,
                           bg=(255, 255, 255, 255),
                           bg_image='yellow.png',
                           center=(gui.WIDTH / 2, gui.HEIGHT / 2 + 120))

    exit = Button((272, 109),
                  'Sair',
                  gui.exit_gui,
                  bg=(255, 255, 255, 255),
                  bg_image='red.png',
                  center=(gui.WIDTH / 2, gui.HEIGHT / 2 + 260))

    bg = gui.BACKGROUND_GIF

    menu = pygame.sprite.Group(bg, logo, new_game, load_game, match_history, exit)


def get():
    """
    Inicializa a tela do menu principal e retorna os sprites presentes na tela.
    """
    if not menu:
        init()
    return menu


menu = None
