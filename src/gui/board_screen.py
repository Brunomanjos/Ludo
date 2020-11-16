# Módulo GUI - Tela do Tabuleiro
# Atualizado: 12/11/2020
# Autor: Bruno Messeder dos Anjos


__all__ = ['get']

from typing import Optional

import pygame
from pygame.locals import *

import board
import dice
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


def get_square(position):
    square_x = int((position[0] - offset_x - 2) / (square_size + 1))
    square_y = int((position[1] - offset_y - 2) / (square_size + 1))
    return square_y, square_x


def update_piece_position(piece, animated):
    piece_position = piece.rect.center
    piece_square = board.get_piece_position(piece.piece_id)
    new_position = get_pos(piece_square)
    x, y = new_position
    new_position = int(x + square_size / 2), int(y + square_size / 2)

    if new_position == piece_position:
        return
    elif animated:
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
    current_finished_players = set(match.finished_players())

    if current_finished_players == finished_players:
        return

    for player_id in current_finished_players:
        if player_id not in finished_players:
            finished_players.append(player_id)
            name = player.get_player(player_id)
            place = len(finished_players)
            show_dialog(f'{name}\nterminou em {place}º lugar')


def on_animation_end():
    global show_next_player

    update_blocks()
    update_finished_players()

    if show_next_player:
        player_name = match.current_player_name()
        if player_name == match.MATCH_ENDED:
            on_match_end()
            return
        show_dialog(f'Vez de {player_name}')
        show_next_player = False


def on_match_end():
    import gui
    # TODO show winners screen
    gui.show_main_menu()


def check_play(piece):
    global show_next_player

    played_square = get_square(piece.rect.center)
    dice_value = dice.get()

    if dice_value is None:
        return

    possible_play = board.get_possible_move(piece.piece_id, dice_value)
    if possible_play != played_square:
        return

    last_player = match.current_player()

    play_result = match.play(piece.piece_id)
    highlight_player()

    show_next_player = match.current_player() != last_player

    if play_result is None:
        show_dice_button()


def on_piece_move(piece):
    check_play(piece)
    update_pieces_positions(True)


def show_dice_button():
    screen.add(dice_button)


def hide_dice_button():
    screen.remove(dice_button)


def throw_dice_action():
    dice.throw()
    dice_value = dice.get()
    if not match.can_play(dice_value):
        show_dice_button()
        match.play(None)
        highlight_player()
        show_dialog(f'Tirou {dice_value} no dado\n\nNão há jogadas possíveis\n\nVez de {match.current_player_name()}')
    else:
        screen.remove(dice_button)
        show_dialog(f'Tirou {dice_value} no dado')


def events_handler(event):
    if event.type == MOUSEBUTTONUP:
        for piece in selected_pieces:
            on_piece_move(piece)
        selected_pieces.clear()

    elif event.type == MOUSEBUTTONDOWN:
        pieces_at = get_pieces_at(event.pos)
        current = match.current_player()
        if get_square(event.pos) == board.get_finish_position(current):
            return
        selected_pieces.extend([piece for piece in pieces_at if piece.piece_id // 4 == current])

    elif event.type == MOUSEMOTION:
        for piece in selected_pieces:
            piece.rect.center = event.pos
        for piece in pieces:
            if piece.collidepoint(event.pos):
                highlight.hovering = piece.piece_id
                return
        highlight.hovering = None

    elif event.key == K_ESCAPE:
        toggle_pause_menu()

    elif event.key == K_SPACE and dice_button in screen:
        dice_button.action()


def get_pieces_at(pos):
    return [piece for piece in pieces if piece.collidepoint(pos)]


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
    elif event.type == KEYDOWN and event.key == K_SPACE:
        hide_dialog()
    return True


def show_dialog(text):
    if dialog in screen:
        dialog_queue.append(text)
    else:
        dialog.sprites()[1].text = text
        screen.add(dialog)


def hide_dialog():
    dialog_queue.clear()
    screen.remove(dialog)


def toggle_pause_menu():
    if pause_menu in screen:
        screen.remove(pause_menu)
    else:
        screen.add(pause_menu)


def exit_game():
    import gui
    match.close_match()
    gui.show_main_menu()


def update_player_names():
    for index, name in enumerate(player.get_players()):
        players[index].text = name


def init():
    import gui
    global screen, pieces, offset_x, offset_y, square_size, dice_button, dialog, pause_menu, highlight

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

    # highlight
    highlight = MovementHighlight(image.rect)

    # botão
    dice_button = Button((148, 50), 'Jogar Dado', throw_dice_action,
                         bg=(134, 184, 53), bottomright=(gui.WIDTH, gui.HEIGHT))

    # eventos
    events = EventSprite([MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN], events_handler)

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

    screen = pygame.sprite.Group(bg, image, highlight, pieces,
                                 dice_button, events, players)


def get():
    """
    Inicializa a tela do tabuleiro e retorna os sprites presentes na tela.
    """
    global finished_players

    if not screen:
        init()

    update_pieces_positions(False)
    update_player_names()
    highlight_player()
    update_blocks()
    show_dice_button()
    finished_players = match.finished_players()

    show_dialog(f'Vez de {match.current_player_name()}')
    screen.remove(pause_menu)

    return screen


screen, dialog, dice_button, pause_menu, highlight = None, None, None, None, None
pieces, players, selected_pieces, finished_players, dialog_queue = [], [], [], [], []
square_size, offset_x, offset_y = 59, 0, 0
show_next_player = False
