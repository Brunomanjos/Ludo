# Módulo GUI - Assistir uma Partida
# Atualizado: 15/12/2020
# Autor: Bruno Messeder dos Anjos


__all__ = ['get']

import pygame
from pygame.locals import *

import board
import dice
import match
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
    new_position = int(x + square_size / 2), int(y + square_size - 10)

    if len(board.get_pieces_at(board.get_piece_position(piece.piece_id))) > 1:
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

    match.close_match(False)
    show_end_dialog('1º Lugar: {}\n2º Lugar: {}\n3º Lugar: {}\n4º Lugar: {}'.format(*names))


def show_dialog(text, player_id):
    player_dialog.show(text, player_id)
    screen.add(player_dialog)


def show_end_dialog(text):
    global end_dialog

    player_dialog.show(text)
    player_dialog.end_dialog = True
    screen.add(player_dialog)


def show_dice_button():
    screen.remove(*dice_buttons)

    screen.add(dice_buttons[match.current_player()])

    if player_dialog in screen:
        screen.remove(player_dialog)
        screen.add(player_dialog)


def hide_dice_button():
    screen.remove(*dice_buttons)


def throw_dice_action():
    global show_next_player

    def on_gif_end():
        show_dice_button()
        update_pieces_positions(True)

    dice_value = match.get_dice_value()

    if dice_value < 1: ...
        # on_match_end()

    screen.remove(*dice_buttons)
    show_dice_gif(dice_value, on_gif_end)

    last_player = match.current_player()

    match.next_move()

    show_next_player = match.current_player() != last_player


def show_dice_gif(dice_value, callback=None):
    dice_gif = dice_gifs[dice_value - 1]
    dice_gif.on_hide = callback
    screen.add(dice_gif)
    dice_gif.run()


def showing_gif():
    return any(gif in screen for gif in dice_gifs)


def hide_gif():
    for gif in dice_gifs:
        if gif in screen:
            gif.hide()


def events_handler(event):
    if showing_gif() and event.type == MOUSEBUTTONUP and not event.consumed:
        hide_gif()
        return

    if event.type == KEYDOWN and event.key == K_ESCAPE:
        toggle_pause_menu()


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
    events = EventSprite([KEYDOWN, MOUSEBUTTONUP], events_handler)

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

    menu_continue = Button((200, 60), 'Continuar', toggle_pause_menu,
                           bg=(255, 255, 255), bg_image='green.png',
                           center=(gui.WIDTH / 2, gui.HEIGHT / 2 - 80))

    menu_exit = Button((200, 60), 'Sair', exit_game,
                       bg=(255, 255, 255), bg_image='red.png',
                       center=(gui.WIDTH / 2, gui.HEIGHT / 2 + 80))

    pause_menu = pygame.sprite.Group(menu_bg, menu_continue, menu_exit)

    dice_gifs.extend(gui.DICE_GIFS)

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
    screen.remove(pause_menu, player_dialog)

    return screen


pieces, players, selected_pieces, winners, dice_buttons, dice_gifs = [], [], [], [], [], []
screen, pause_menu, highlight, player_dialog = None, None, None, None
square_size, offset_x, offset_y = 59, 0, 0
show_next_player = False
