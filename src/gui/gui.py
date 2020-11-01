# Módulo GUI
# Atualizado: 01/11/2020
# Autor: Bruno Messeder dos Anjos

import os

import pygame
from pygame.locals import *

import gui.board_screen
import gui.main_menu
import gui.set_players_menu
from gui.sprite import *

__all__ = ['loop', 'show_main_menu', 'show_set_players_menu', 'show_board', 'WIDTH', 'HEIGHT', 'FPS', 'quit']

WIDTH = 1200
HEIGHT = 903
FPS = 60

BACKGROUND = (0, 0, 0)

running = True
sprites = None
screen = None
clock = pygame.time.Clock()

pygame.init()
pygame.font.init()
pygame.key.set_repeat(400, 30)
os.environ['SDL_VIDEO_CENTERED'] = '1'


def init():
    global screen
    if not screen:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))


def loop():
    init()
    while running:
        clock.tick(FPS)
        handle_events()
        update_screen()


def handle_events():
    global running
    for event in pygame.event.get():
        if event.type == QUIT or (
                event.type == KEYDOWN and
                event.key == 285 and
                event.mod & KMOD_LALT == KMOD_LALT
        ):
            running = False
            pygame.quit()
            exit()
        handle_event(event)


def handle_event(event):
    event.consumed = False
    for sprite in sprites.sprites()[::-1]:
        if isinstance(sprite, EventSprite) and event.type in sprite.events:
            if sprite.handle_event(event):
                event.consumed = True


def update_screen():
    screen.fill(BACKGROUND)

    if sprites:
        sprites.update()
        sprites.draw(screen)

    pygame.display.flip()


def quit():
    global running
    running = False


def show_main_menu():
    global sprites
    init()
    sprites = gui.main_menu.get()


def show_set_players_menu():
    global sprites
    init()
    sprites = gui.set_players_menu.get()


def show_board():
    global sprites
    init()
    sprites = gui.board_screen.get()
