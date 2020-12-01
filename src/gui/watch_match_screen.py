# Módulo GUI - Assistir uma Partida
# Atualizado: 30/11/2020
# Autor: Bruno Messeder dos Anjos


__all__ = ['get']

from typing import Optional

import pygame
from pygame.locals import *

import board
import match
import piece
import player
from gui.sprite import *


def get_pos(square, offset=True):
    x = square[1] * (square_size + 1) + 2
    y = square[0] * (square_size + 1) + 2
    if offset:
        x += offset_x
        y += offset_y
    return int(x), int(y)


def update_piece_position(piece, animated):
    piece_position = piece.rect.center
    piece_square = board.get_piece_position(piece.piece_id)
    new_position = get_pos(piece_square)
    x, y = new_position
    new_position = int(x + square_size / 2), int(y + square_size / 2)

    if new_position == piece_position:
        return
    elif animated:
        new_transition = Transition(piece, new_position, 0.3, on_animation_end)
        for transition in screen:
            if new_transition.equals(transition):
                return

        screen.add(Transition(piece, new_position, 0.3, on_animation_end))
    else:
        piece.rect.center = new_position


def update_pieces_positions(animated):
    for piece in pieces:
        update_piece_position(piece, animated)


def update_blocks():
    for piece in pieces:
        pieces_at_same_pos = len(board.get_pieces_at(board.get_piece_position(piece.piece_id)))
        if pieces_at_same_pos == 1:
            piece.text = ''
        else:
            piece.text = str(pieces_at_same_pos)


def update_finished_players():
    current_finished_players = set(match.winners())

    if current_finished_players == winners:
        return

    for player_id in current_finished_players:
        if player_id not in winners:
            winners.append(player_id)
            name = player.get_player(player_id)
            place = len(winners)
            show_dialog(f'{name}\nterminou em {place}º lugar')


def on_animation_end():
    update_blocks()
    update_finished_players()

    if match.current_player_name() == match.MATCH_ENDED:
        on_match_end()


def on_match_end():
    names = [player.get_player(index) for index in match.winners()]

    match.close_match()
    show_end_dialog('1º Lugar: {}\n2º Lugar: {}\n3º Lugar: {}\n4º Lugar: {}'.format(*names))


def show_end_dialog(text):
    global end_dialog

    show_dialog(text)
    end_dialog = True


def events_handler(event):
    if event.type == KEYDOWN and event.key == K_ESCAPE:
        toggle_pause_menu()

    if pause_menu in dialog or dialog in screen or event.consumed:
        return

    elif (event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYDOWN and event.key == K_RIGHT):
        match.next_move()
        update_pieces_positions(True)
        highlight_player()


def highlight_player():
    highlight = match.current_player()
    for index, player in enumerate(players):
        if index == highlight:
            player.bg = piece.corPeca(index * 4)
        else:
            player.bg = (0, 0, 0, 0)


def dialog_handler(event):
    if event.consumed:
        return
    elif event.type == MOUSEBUTTONUP:
        if dialog_queue:
            dialog.sprites()[1].text = dialog_queue.pop(0)
        else:
            hide_dialog()
    elif event.type == KEYDOWN and event.key == K_SPACE and pause_menu not in screen:
        hide_dialog()
    return True


def show_dialog(text):
    if dialog in screen:
        dialog_queue.append(text)
    else:
        dialog.sprites()[1].text = text
        screen.add(dialog)


def hide_dialog():
    import gui

    dialog_queue.clear()
    screen.remove(dialog)
    if end_dialog:
        gui.show_main_menu()


def toggle_pause_menu():
    if pause_menu in screen:
        screen.remove(pause_menu)
    else:
        screen.add(pause_menu)


def exit_game():
    import gui
    match.close_match(False)
    gui.show_main_menu()


def update_player_names():
    for index, name in enumerate(player.get_players()):
        players[index].text = name


def init():
    import gui
    global screen, pieces, offset_x, offset_y, square_size, dialog, pause_menu

    # background
    bg = Canvas((gui.WIDTH, gui.HEIGHT))
    bg.image.fill((200, 200, 200))

    # tabuleiro
    image = Image('Tabuleiro.png', (gui.HEIGHT, gui.HEIGHT))
    image.rect.center = (gui.WIDTH / 2, gui.HEIGHT / 2)

    offset_x = image.rect.left
    offset_y = image.rect.top

    # peças
    pieces = [PieceSprite(piece) for piece in range(16)]

    # eventos
    events = EventSprite([MOUSEBUTTONUP, KEYDOWN, KEYUP], events_handler)

    # nomes dos jogadores
    names = player.get_players()
    label_y = get_pos((3, 0))[1]
    players.append(Label((offset_x, 60), names[0], midleft=(0, label_y)))
    players.append(Label((offset_x, 60), names[1], midright=(gui.WIDTH, label_y)))
    label_y = get_pos((12, 0))[1]
    players.append(Label((offset_x, 60), names[2], midright=(gui.WIDTH, label_y)))
    players.append(Label((offset_x, 60), names[3], midleft=(0, label_y)))

    # diálogo de jogada
    dialog_bg = Canvas((gui.WIDTH, gui.HEIGHT), True)
    dialog_bg.image.fill((0, 0, 0, 147))
    dialog_bg.events = [MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, KEYDOWN]
    dialog_bg.handler = dialog_handler

    dialog_label = Label((270, 120), '', bg=(255, 255, 255), center=(gui.WIDTH / 2, gui.HEIGHT / 2))

    dialog = pygame.sprite.Group(dialog_bg, dialog_label)

    # menu de pause
    menu_bg = Canvas((gui.WIDTH, gui.HEIGHT), True)
    menu_bg.image.fill((0, 0, 0, 147))
    menu_bg.events = [MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION]
    menu_bg.handler = lambda e: True
    menu_rect = Rect(0, 0, 300, 200)
    menu_rect.center = (gui.WIDTH / 2, gui.HEIGHT / 2)
    menu_bg.image.fill((255, 255, 255), menu_rect)

    menu_continue = Button((200, 60), 'Continuar', toggle_pause_menu,
                           bg=(255, 255, 255), fg=(134, 184, 53),
                           center=(gui.WIDTH / 2, gui.HEIGHT / 2 - 40))

    menu_exit = Button((200, 60), 'Sair', exit_game,
                       bg=(255, 255, 255), fg=(134, 184, 53),
                       center=(gui.WIDTH / 2, gui.HEIGHT / 2 + 40))

    pause_menu = pygame.sprite.Group(menu_bg, menu_continue, menu_exit)

    screen = pygame.sprite.Group(bg, image, pieces, events, players)


def get():
    """
    Inicializa a tela do tabuleiro e retorna os sprites presentes na tela.
    """
    global end_dialog

    if not screen:
        init()

    update_pieces_positions(False)
    update_player_names()
    highlight_player()
    update_blocks()
    end_dialog = False

    screen.remove(pause_menu)

    return screen


screen, dialog, pause_menu = None, None, None
pieces, players, winners, dialog_queue = [], [], [], []
square_size, offset_x, offset_y = 59, 0, 0
end_dialog = False
