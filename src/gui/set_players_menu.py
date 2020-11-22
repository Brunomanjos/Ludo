# Módulo GUI - Menu de Definição dos Jogadores
# Atualizado: 01/11/2020
# Autor: Bruno Messeder dos Anjos

import pygame
from pygame.locals import *

import match
from gui.sprite import *

__all__ = ['get']


def event_handler(event):
    import gui
    if event.key == K_ESCAPE:
        gui.show_main_menu()
        return True
    elif event.key != K_TAB or dialog in menu:
        return False
    if event.mod & KMOD_LSHIFT:  # shift + tab
        select_previous()
    else:  # tab
        select_next()
    return True


def select_previous():
    if t1.selected:
        t1.selected = False
        t4.selected = True
    elif t2.selected:
        t2.selected = False
        t1.selected = True
    elif t3.selected:
        t3.selected = False
        t2.selected = True
    elif t4.selected:
        t4.selected = False
        t3.selected = True
    else:
        t4.selected = True


def select_next():
    if t4.selected:
        t4.selected = False
        t1.selected = True
    elif t3.selected:
        t3.selected = False
        t4.selected = True
    elif t2.selected:
        t2.selected = False
        t3.selected = True
    elif t1.selected:
        t1.selected = False
        t2.selected = True
    else:
        t1.selected = True


def new_match():
    import gui

    p1, p2, p3, p4 = t1.text.strip(), t2.text.strip(), t3.text.strip(), t4.text.strip()
    if not p1 or not p2 or not p3 or not p4:
        show_dialog()
    else:
        match.close_match()
        match.new_match(p1, p2, p3, p4)
        gui.show_board()


def show_dialog():
    if dialog not in menu:
        menu.add(dialog)


def hide_dialog():
    menu.remove(dialog)
    select_next()


def dialog_handler(event):
    if event.type == KEYDOWN and event.key == K_RETURN:
        hide_dialog()
    return True


def init():
    import gui
    global menu, t1, t2, t3, t4, dialog

    bg = Canvas((gui.WIDTH, gui.HEIGHT))
    bg.image.fill((100, 120, 150))

    b1 = Button((160, 50),
                'Voltar',
                gui.show_main_menu,
                bg=(134, 184, 53),
                center=(gui.WIDTH / 2 - 180, gui.HEIGHT / 2 + 160))

    b2 = Button((160, 50),
                'Começar Jogo',
                new_match,
                bg=(134, 184, 53),
                center=(gui.WIDTH / 2 + 180, gui.HEIGHT / 2 + 160))

    t1 = TextInput((250, 50), select_next,
                   center=(gui.WIDTH / 2 - 180, gui.HEIGHT / 2 - 120))

    l1 = Label((100, 40), 'Jogador 1', midbottom=t1.rect.midtop)

    t2 = TextInput((250, 50), select_next,
                   center=(gui.WIDTH / 2 + 180, gui.HEIGHT / 2 - 120))

    l2 = Label((100, 40), 'Jogador 2', midbottom=t2.rect.midtop)

    t3 = TextInput((250, 50), select_next,
                   center=(gui.WIDTH / 2 - 180, gui.HEIGHT / 2 + 50))

    l3 = Label((100, 40), 'Jogador 3', midbottom=t3.rect.midtop)

    t4 = TextInput((250, 50), b2.action,
                   center=(gui.WIDTH / 2 + 180, gui.HEIGHT / 2 + 50))

    l4 = Label((100, 40), 'Jogador 4', midbottom=t4.rect.midtop)

    event = EventSprite([KEYDOWN], event_handler)

    dialog_bg = Canvas((gui.WIDTH, gui.HEIGHT), True)
    dialog_bg.image.fill((0, 0, 0, 147))
    dialog_rect = Rect(0, 0, 300, 160)
    dialog_rect.center = (gui.WIDTH / 2, gui.HEIGHT / 2)
    dialog_bg.image.fill((255, 255, 255), dialog_rect)

    dialog_bg.events = [KEYDOWN, KEYUP, MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN]
    dialog_bg.handler = dialog_handler

    dialog_button = Button((160, 50), 'Ok', hide_dialog,
                           bg=(134, 184, 53),
                           center=(gui.WIDTH / 2, gui.HEIGHT / 2 + 30))

    dialog_label = Label((300, 40), 'Os nomes dos quatro\njogadores são obrigatórios!',
                         text_align=LEFT, center=(gui.WIDTH / 2, gui.HEIGHT / 2 - 40))

    dialog = pygame.sprite.Group(dialog_bg, dialog_label, dialog_button)

    menu = pygame.sprite.Group(bg, t1, t2, t3, t4, l1, l2, l3, l4, b1, b2, event)


def get():
    """
    Inicializa a tela de definição dos jogadores e retorna os sprites presentes na tela.
    """

    if not menu:
        init()

    t1.selected = True
    t2.selected = False
    t3.selected = False
    t4.selected = False
    t1.text = ''
    t2.text = ''
    t3.text = ''
    t4.text = ''
    menu.remove(dialog)

    return menu


t1, t2, t3, t4, menu, dialog = None, None, None, None, None, None
