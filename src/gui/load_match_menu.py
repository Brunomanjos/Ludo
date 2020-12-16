# Módulo GUI - Menu de Seleção de Partida já Começada
# Atualizado: 15/12/2020
# Autor: Bruno Messeder dos Anjos

import os
import re
from xml.etree.ElementTree import parse

import pygame

import match
from gui.sprite import *
from pygame.locals import *

__all__ = ['get']


def event_handler(event):
    import gui
    if event.key == K_ESCAPE:
        gui.show_main_menu()
        return True


def on_click(match_id):
    import gui

    def on_click_fun():
        if match.load_match(match_id) != match.INVALID_ID:
            gui.show_board()

    return on_click_fun


def load_matches():
    matches.clear()

    pattern = re.compile('match (\\d+).xml')

    directory = os.path.join(os.environ['appdata'], '.ludo')

    for file_name in os.listdir(directory):
        match = pattern.fullmatch(file_name)

        if not match:
            continue

        match_id = int(match.groups()[0])

        xml_root = parse(os.path.join(directory, file_name)).getroot()
        ended_element = xml_root.find('ended')
        if ended_element is not None and ended_element.text.strip().lower() == 'true':
            continue

        matches.append(match_id)

    matches.sort()


def load_page(new_page):
    import gui
    global page

    menu.remove(match_buttons)
    match_buttons.empty()

    for index in range(new_page * 8, (new_page + 1) * 8):
        if index >= len(matches):
            break
        match_id = matches[index]
        x = 150 * (-1 if index % 2 == 0 else 1) + gui.WIDTH / 2
        y = 150 * ((index % 8) // 2) - 260 + gui.HEIGHT / 2
        match_buttons.add(Button(
            (200, 60),
            f'Partida {match_id}',
            on_click(match_id),
            bg=(134, 184, 53),
            bg_image='green.png',
            center=(x, y)))

    menu.add(match_buttons)
    page = new_page
    update_buttons()


def update_buttons():
    next_match_index = (page + 1) * 8
    if next_match_index < len(matches):
        menu.add(next_page)
    else:
        menu.remove(next_page)

    if page > 0:
        menu.add(prev_page)
    else:
        menu.remove(prev_page)


def init():
    import gui

    global match_buttons, menu, next_page, prev_page

    bg = gui.BACKGROUND_GIF

    match_buttons = pygame.sprite.Group()

    title = Label((260, 50), 'Carregar Partida',
                  center=(gui.WIDTH / 2, gui.HEIGHT / 2 - 370))

    back = Button((160, 50),
                  'Voltar',
                  gui.show_main_menu,
                  bg=(134, 184, 53),
                  bg_image='red.png',
                  center=(gui.WIDTH / 2, gui.HEIGHT / 2 + 350))

    next_page = Button((160, 50),
                       '>',
                       lambda: load_page(page + 1),
                       bg=(134, 184, 53),
                       bg_image='blue.png',
                       midright=(gui.WIDTH - 30, gui.HEIGHT / 2 - 20))

    prev_page = Button((160, 50),
                       '<',
                       lambda: load_page(page - 1),
                       bg=(134, 184, 53),
                       bg_image='blue.png',
                       midleft=(30, gui.HEIGHT / 2 - 20))

    event = EventSprite([KEYDOWN], event_handler)

    menu = pygame.sprite.Group(bg, back, title, event)


def get():
    if not menu:
        init()

    load_matches()
    load_page(0)

    return menu


next_page, prev_page, match_buttons, menu = None, None, None, None
matches = []
page = 0
