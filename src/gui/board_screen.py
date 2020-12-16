# Módulo GUI - Tela do Tabuleiro
# Atualizado: 15/12/2020
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


def check_play(piece):
    global show_next_player

    played_square = get_square((piece.rect.midbottom[0], piece.rect.midbottom[1] - 20))
    dice_value = dice.get()

    if dice_value is None:
        return

    possible_play = board.get_possible_move(piece.piece_id, dice_value)
    if possible_play != played_square:
        return

    last_player = match.current_player()

    play_result = match.play(piece.piece_id)

    show_next_player = match.current_player() != last_player

    if play_result is True:
        show_dice_button()


def on_piece_move(piece):
    check_play(piece)
    update_pieces_positions(True)


def show_dice_button():
    screen.add(dice_buttons[match.current_player()])

    if player_dialog in screen:
        screen.remove(player_dialog)
        screen.add(player_dialog)


def hide_dice_button():
    screen.remove(*dice_buttons)


def throw_dice_action():
    dice.throw()
    dice_value = dice.get()
    player_id = match.current_player()

    if not match.can_play(dice_value):
        show_dice_button()
        match.play(None)
        show_dialog(f'Tirou {dice_value} no dado', player_id)
        show_dialog('Sem jogadas', player_id)
        show_dialog(match.current_player_name(), match.current_player())
        hide_dice_button()
        show_dice_button()
    else:
        screen.remove(*dice_buttons)
        show_dialog(f'Tirou {dice_value} no dado', match.current_player())


def events_handler(event):
    if event.type == MOUSEBUTTONUP:
        for piece in selected_pieces:
            on_piece_move(piece)
        selected_pieces.clear()

    elif event.type == MOUSEBUTTONDOWN:
        pieces_at = get_pieces_at(event.pos)
        current = match.current_player()
        if get_square(event.pos) == board.get_finish_position(current) or event.button != BUTTON_LEFT:
            return
        selected_pieces.extend([piece for piece in pieces_at if piece.piece_id // 4 == current])

    elif event.type == MOUSEMOTION:
        for piece in selected_pieces:
            piece.rect.midbottom = event.pos[0], event.pos[1] + 20
        for piece in pieces:
            if piece.collidepoint(event.pos):
                highlight.hovering = piece.piece_id
                return
        highlight.hovering = None

    elif event.key == K_ESCAPE:
        toggle_pause_menu()

    dice_button = dice_buttons[match.current_player()]

    if event.type == KEYDOWN and event.key == K_SPACE and dice_button in screen \
            and not event.consumed and pause_menu not in screen:
        dice_button.action()


def get_pieces_at(pos):
    return [piece for piece in pieces if piece.collidepoint(pos)]


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
    global screen, pieces, offset_x, offset_y, square_size, dice_buttons, pause_menu, highlight, player_dialog

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
    dice_buttons = [Button((148, 50), 'Jogar', throw_dice_action,
                           bg_image=f'green_small.png', bg=(134, 184, 53),
                           center=(3 * square_size + offset_x, 3 * square_size + 4)),
                    Button((148, 50), 'Jogar', throw_dice_action,
                           bg_image=f'red_small.png', bg=(134, 184, 53),
                           center=(gui.WIDTH - 3 * square_size - offset_x, 3 * square_size + 4)),
                    Button((148, 50), 'Jogar', throw_dice_action,
                           bg_image=f'blue_small.png', bg=(134, 184, 53),
                           center=(gui.WIDTH - 3 * square_size - offset_x, gui.HEIGHT - 3 * square_size - 4)),
                    Button((148, 50), 'Jogar', throw_dice_action,
                           bg_image=f'yellow_small.png', bg=(134, 184, 53),
                           center=(3 * square_size + offset_x, gui.HEIGHT - 3 * square_size - 4))]

    # eventos
    events = EventSprite([MOUSEBUTTONUP, MOUSEBUTTONDOWN, MOUSEMOTION, KEYDOWN], events_handler)

    # nomes dos jogadores
    names = player.get_players()
    label_y = get_pos((3, 0))[1]

    players.append(Label((offset_x, 60), names[0],
                         font=pygame.font.Font('res/fonts/LemonMilklight.otf', 25),
                         midleft=(0, label_y)))
    players.append(Label((offset_x, 60), names[1],
                         font=pygame.font.Font('res/fonts/LemonMilklight.otf', 25),
                         midright=(gui.WIDTH, label_y)))

    label_y = get_pos((12, 0))[1]
    players.append(Label((offset_x, 60), names[2],
                         font=pygame.font.Font('res/fonts/LemonMilklight.otf', 25),
                         midright=(gui.WIDTH, label_y)))
    players.append(Label((offset_x, 60), names[3],
                         font=pygame.font.Font('res/fonts/LemonMilklight.otf', 25),
                         midleft=(0, label_y)))

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
                           bg=(255, 255, 255), fg=(134, 184, 53),
                           center=(gui.WIDTH / 2, gui.HEIGHT / 2 - 40))

    menu_exit = Button((200, 60), 'Sair', exit_game,
                       bg=(255, 255, 255), fg=(134, 184, 53),
                       center=(gui.WIDTH / 2, gui.HEIGHT / 2 + 40))

    pause_menu = pygame.sprite.Group(menu_bg, menu_continue, menu_exit)

    screen = pygame.sprite.Group(bg, image, highlight, pieces, events, players)


def get():
    """
    Inicializa a tela do tabuleiro e retorna os sprites presentes na tela.
    """
    global winners

    if not screen:
        init()

    update_pieces_positions(False)
    update_player_names()
    update_piece_block()
    show_dice_button()
    winners = match.winners()

    show_dialog(match.current_player_name(), match.current_player())
    screen.remove(pause_menu)

    return screen


pieces, players, selected_pieces, winners, dice_buttons = [], [], [], [], []
screen, pause_menu, highlight, player_dialog = None, None, None, None
square_size, offset_x, offset_y = 59, 0, 0
show_next_player = False
