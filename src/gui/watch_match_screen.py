# Módulo GUI - Assistir uma Partida
# Atualizado: 15/12/2020
# Autor: Bruno Messeder dos Anjos


__all__ = ['get']

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
    piece_position = piece.rect.midbottom
    piece_square = board.get_piece_position(piece.piece_id)
    new_position = get_pos(piece_square)
    x, y = new_position
    new_position = int(x + square_size / 2), int(y + square_size - 3)

    if new_position == piece_position:
        return
    elif animated:
        screen.add(Transition(piece, new_position, 0.3, on_animation_end))
    else:
        piece.rect.midbottom = new_position


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
            show_dialog(f'{name}\nterminou em {place}º lugar', player_id)


def update_piece_block():
    for piece in pieces:
        piece.update_block()


def on_animation_end():
    global show_next_player

    update_piece_block()

    update_finished_players()

    if show_next_player:
        player_name = match.current_player_name()
        if player_name == match.MATCH_ENDED:
            on_match_end()
            return

        show_dialog(player_name, match.current_player())
        show_next_player = False


def on_match_end():
    names = [player.get_player(index) for index in match.winners()]

    match.close_match()
    show_end_dialog('1º Lugar: {}\n2º Lugar: {}\n3º Lugar: {}\n4º Lugar: {}'.format(*names))


def show_dialog(text, player_id):
    player_dialog.show(text, player_id)
    screen.add(player_dialog)


def show_end_dialog(text):
    global end_dialog

    player_dialog.show(text)
    player_dialog.end_dialog = True
    screen.add(player_dialog)


def events_handler(event):
    global show_next_player

    if event.type == KEYDOWN and event.key == K_ESCAPE:
        toggle_pause_menu()

    if player_dialog in screen or event.consumed:
        return

    elif (event.type == MOUSEBUTTONUP and event.button == 1) or (event.type == KEYDOWN and event.key == K_RIGHT):
        current_player = match.current_player()
        match.next_move()
        if match.current_player() != current_player:
            show_next_player = True

        update_pieces_positions(True)


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
    global screen, pieces, offset_x, offset_y, square_size, pause_menu, player_dialog

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
    player_dialog = PlayerDialog()

    # menu de pause
    menu_bg = Canvas((gui.WIDTH, gui.HEIGHT), True)
    menu_bg.image.fill((0, 0, 0, 147))
    menu_bg.events = [MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION]
    menu_bg.handler = lambda e: True
    menu_rect = Rect(0, 0, 300, 200)
    menu_rect.center = (gui.WIDTH / 2, gui.HEIGHT / 2)
    menu_bg.image.fill((255, 255, 255), menu_rect)

    menu_continue = Button((200, 60), 'Continuar', toggle_pause_menu,
                           bg=(255, 255, 255), bg_image='green_small.png',
                           center=(gui.WIDTH / 2, gui.HEIGHT / 2 - 45))

    menu_exit = Button((200, 60), 'Sair', exit_game,
                       bg=(255, 255, 255), bg_image='red_small.png',
                       center=(gui.WIDTH / 2, gui.HEIGHT / 2 + 45))

    pause_menu = pygame.sprite.Group(menu_bg, menu_continue, menu_exit)

    screen = pygame.sprite.Group(bg, image, pieces, events, players)


def get():
    """
    Inicializa a tela do tabuleiro e retorna os sprites presentes na tela.
    """

    if not screen:
        init()

    update_pieces_positions(False)
    update_player_names()
    update_blocks()

    screen.remove(pause_menu)

    return screen


screen, pause_menu, player_dialog = None, None, None
pieces, players, winners = [], [], []
square_size, offset_x, offset_y = 59, 0, 0
show_next_player = False
