# Módulo GUI
# Atualizado: 12/11/2020
# Autor: Bruno Messeder dos Anjos

import os
import sys
from typing import Optional

import pygame
from pygame.locals import *

import database
import gui.board_screen
import gui.main_menu
import gui.set_players_menu
import match
from gui.sprite import *

__all__ = ['loop', 'show_main_menu', 'show_set_players_menu', 'show_board', 'WIDTH', 'HEIGHT', 'FPS', 'exit_gui']

WIDTH = 1200
HEIGHT = 903
FPS = 60

BACKGROUND = (0, 0, 0)

pygame.init()
pygame.font.init()
pygame.key.set_repeat(400, 30)
os.environ['SDL_VIDEO_CENTERED'] = '1'

running = True
sprites: Optional[pygame.sprite.Group] = None
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def loop():
    """
    Roda o loop da interface visual.
    """
    while running:
        clock.tick(FPS)
        handle_events()
        update_screen()


def handle_events():
    """
    Gerencia os eventos a cada frame
    """
    for event in pygame.event.get():
        handle_event(event)


def handle_event(event):
    """
    Gerencia um evento
    """
    if event.type == QUIT or (
            event.type == KEYDOWN and
            event.key == 285 and
            event.mod & KMOD_LALT == KMOD_LALT):
        exit_gui()

    event.consumed = False
    for sprite in sprites.sprites()[::-1]:
        if isinstance(sprite, EventSprite) and event.type in sprite.events:
            if sprite.handle_event(event):
                event.consumed = True


def update_screen():
    """
    Atualiza o gráfico a cada frame
    """
    screen.fill(BACKGROUND)

    if sprites:
        sprites.update()
        sprites.draw(screen)

    pygame.display.flip()


def exit_gui():
    """
    Para a execução do loop e fecha o programa.
    """
    global running
    running = False
    match.close_match()
    database.close()
    pygame.quit()
    sys.exit()


def show_main_menu():
    """
    Muda a tela atual para o menu principal
    """
    global sprites
    sprites = gui.main_menu.get()


def show_set_players_menu():
    """
    Muda a tela atual para o menu de definição dos nomes dos jogadores
    """
    global sprites
    sprites = gui.set_players_menu.get()


def show_board():
    """
    Muda a tela atual para a tela do tabuleiro
    """
    global sprites
    sprites = gui.board_screen.get()
