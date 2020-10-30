# Módulo GUI - Tela do Tabuleiro
# Atualizado: 30/10/2020
# Autor: Bruno Messeder dos Anjos


__all__ = ['get']

import pygame
from pygame.locals import *

import board
import dice
import match
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
    print(square_y, square_x)
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
        screen.add(Transition(piece, new_position, 0.3, update_piece_text))
    else:
        piece.rect.center = new_position


def update_pieces_positions(animated):
    for piece in pieces:
        update_piece_position(piece, animated)


def update_piece_text():
    for piece in pieces:
        pieces_at_same_pos = len(board.get_pieces_at(board.get_piece_position(piece.piece_id)))
        if pieces_at_same_pos == 1:
            piece.text = ''
        else:
            piece.text = str(pieces_at_same_pos)


def check_play(piece):
    played_square = get_square(piece.rect.center)
    dice_value = dice.get()

    if dice_value is None:
        return

    possible_play = board.get_possible_move(piece.piece_id, dice_value)
    if possible_play != played_square:
        return

    play_result = match.play(piece.piece_id)
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
    screen.remove(dice_button)
    check_possible_moves()


def check_possible_moves():
    if not match.can_play(dice.get()):
        print(f'Cannot play {dice.get()}: {match.current_player()}')
        show_dice_button()
        match.play(None)
        # TODO show skip player screen


def drag_event_handler(event):
    if event.type == MOUSEBUTTONUP:
        for piece in selected_pieces:
            on_piece_move(piece)
        selected_pieces.clear()
    elif event.type == MOUSEBUTTONDOWN:
        selected_pieces.extend(get_pieces_at(event.pos))
    else:
        for piece in selected_pieces:
            piece.rect.center = event.pos


def get_pieces_at(pos):
    return [piece for piece in pieces if piece.collidepoint(pos)]


def init():
    import gui
    global screen, pieces, offset_x, offset_y, square_size, dice_button

    bg = Canvas((gui.WIDTH, gui.HEIGHT))
    bg.image.fill((90, 90, 90))

    image = Image('Tabuleiro.png', (gui.HEIGHT, gui.HEIGHT))
    image.rect.center = (gui.WIDTH / 2, gui.HEIGHT / 2)

    offset_x = image.rect.left
    offset_y = image.rect.top

    pieces = [PieceSprite(piece) for piece in range(16)]

    highlight = MovementHighlight(image.rect)

    # TODO add pause menu

    dice_button = Button((150, 50), 'Jogar Dado', throw_dice_action,
                         bg=(134, 184, 53), bottomright=(gui.WIDTH, gui.HEIGHT))

    drag_event = EventSprite([MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION], drag_event_handler)

    screen = pygame.sprite.Group(bg, image, highlight, pieces, dice_button, drag_event)


def get():
    if not screen:
        init()

    update_pieces_positions(False)
    print(square_size)

    return screen


screen, dice_button = None, None
pieces = []
square_size, offset_x, offset_y = 59, 0, 0
selected_pieces = []
