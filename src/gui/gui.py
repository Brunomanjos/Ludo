# Módulo GUI
# Atualizado: 12/11/2020
# Autor: Bruno Messeder dos Anjos

import os

import pygame
from pygame.locals import *

import database
import gui.board_screen
import gui.main_menu
import gui.set_players_menu
import match
from gui.sprite import *

__all__ = ['loop', 'show_main_menu', 'show_set_players_menu', 'show_board', 'WIDTH', 'HEIGHT', 'FPS', 'quit']

WIDTH = 1200
HEIGHT = 903
FPS = 60

BACKGROUND = (0, 0, 0)

pygame.init()
pygame.font.init()
pygame.key.set_repeat(400, 30)
os.environ['SDL_VIDEO_CENTERED'] = '1'

running = True
sprites = None
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def loop():
    while running:
        clock.tick(FPS)
        handle_events()
        update_screen()


def handle_events():
    for event in pygame.event.get():
        handle_event(event)


def handle_event(event):
    if event.type == QUIT or (
            event.type == KEYDOWN and
            event.key == 285 and
            event.mod & KMOD_LALT == KMOD_LALT):
        quit()

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
    match.close_match()
    database.close()
    pygame.quit()
    exit()


def show_main_menu():
    global sprites
    sprites = gui.main_menu.get()


def show_set_players_menu():
    global sprites
    sprites = gui.set_players_menu.get()


def show_board():
    global sprites
    sprites = gui.board_screen.get()
