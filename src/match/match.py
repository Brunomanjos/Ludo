# Módulo Match
# Atualizado: 24/10/2020
# autor: Bruno Messeder dos Anjos

from random import shuffle, randint

import board
import player

__all__ = ['new_match', 'make_move', 'current_player', 'player_groups', 'player_group', 'load_match',
           'close_match', 'MATCH_NOT_DEFINED', 'INVALID_PIECE', 'INVALID_PLAYER', 'MATCH_ENDED',
           'INVALID_STEPS', 'MATCH_IN_PROGRESS', 'INVALID_DATA']

MATCH_NOT_DEFINED = -1
INVALID_PIECE = -2
INVALID_PLAYER = -3
MATCH_ENDED = -4
INVALID_STEPS = -5
MATCH_IN_PROGRESS = -6
INVALID_DATA = -7

match = None


def new_match(p1, p2, p3, p4):
    """
    Cria uma nova partida, caso nenhuma partida esteja em andamento
    :param p1: nome do primeiro jogador
    :param p2: nome do segundo jogador
    :param p3: nome do terceiro jogador
    :param p4: nome do quarto jogador
    :return: True caso a partida tenha sido criada.
     MATCH_IN_PROGRESS caso já tenha uma partida em andamento.
    """
    global match
    if match:
        return MATCH_IN_PROGRESS

    groups = [0, 1, 2, 3]
    shuffle(groups)

    player.set_players(p1, p2, p3, p4)

    match = {
        'current_player': randint(0, 3),  # id do jogador atual
        'groups': groups,  # grupo das peças dos jogadores
        'history': [],  # histórico da partida. Cada elemento é a jogada feita em uma rodada, da forma (peça, paços)
        'sequence': 0  # jogadas em sequência de um jogador. No máximo 3 antes de pular a vez
    }

    return True


def make_move(piece_id, steps):
    """
    Move um peça

    :param piece_id: id da peça
    :param steps: quantas casas a peça vai se mover
    :return: True caso a jogada tenha sido efetuada.
     MATCH_NOT_DEFINED caso a partida não tenha sido definida
     INVALID_PIECE caso o id da peça seja seja inválido.
     INVALID_PLAYER caso a peça não pertença ao jogador do turno atual.
     MATCH_ENDED caso a partida tenha terminado.
     INVALID_STEPS caso o número de paços seja inválido.
    """
    if not match:
        return MATCH_NOT_DEFINED
    elif piece_id < 0 or piece_id > 15:
        return INVALID_PIECE

    current = current_player()
    if current == MATCH_ENDED:
        return MATCH_ENDED

    group = player_group(current)
    if group != piece_id // 4:
        return INVALID_PLAYER

    if steps < 1 or steps > 6:
        return INVALID_STEPS

    piece_pos = board.get_piece_position(piece_id)
    if piece_pos not in board.get_spawn_positions(group) or steps == 6:
        # move a peça se ela não estiver na posição inicial ou,
        # caso esteja, o número de paços seja igual a 6
        board.move_piece(piece_id, steps)

    if steps < 6 or match['sequence'] >= 3:
        # muda o turno para o próximo jogador
        match['sequence'] = 0
        match['current_player'] = (match['current_player'] + 1) % 4
    else:
        # continua o turno com o mesmo jogador
        match['sequence'] += 1

    print(board.get_pieces_positions())


def current_player():
    """
    :return: o jogador atual, caso haja um partida em andamento.
    MATCH_ENDED caso a partida tenha terminado.
    MATCH_NOT_DEFINED caso a partida não tenha sido definida
    """
    if not match:
        return MATCH_NOT_DEFINED

    current = match['current_player']

    if current is None:
        return MATCH_ENDED

    return current


def player_groups():
    """
    :return: Os grupos dos jogadores em uma lista (o índice da lista é o índice do jogador)
     caso tenha uma partida em andamento. MATCH_NOT_DEFINED caso contrário.
    """
    if not match:
        return MATCH_NOT_DEFINED

    return match['groups'].copy()


def player_group(player_index):
    """
    :param player_index: índice do jogador
    :return: o grupo de um jogador caso tenha uma partida em andamento e o índice do jogador seja válido.
     MATCH_NOT_DEFINED caso não tenha uma partida em andamento.
     INVALID_PLAYER caso o índice do jogador seja inválido.
    """
    if not match:
        return MATCH_NOT_DEFINED
    elif player_index < 0 or player_index > 3:
        return INVALID_PLAYER

    return match['groups'][player_index]


def load_match(match_data):
    """
    Carrega uma partida já começada.
    :param match_data: dados da partida
    :return: True caso a partida tenha sido carregada.
     MATCH_IN_PROGRESS caso já tenha uma partida em andamento.
     INVALID_DATA caso os dados da partida sejam inválidos.
    """
    global match

    if match:
        return MATCH_IN_PROGRESS

    if valid_data(match_data):
        match = match_data
        load_pieces_positions()
        return True
    return INVALID_DATA


def valid_data(data):
    """
    Valida os dados da partida para evitar erros.
    :param data: dados da partida
    :return: True caso os dados sejam válidos. False caso contrário.
    """

    # verifica se os dados estão em um dicionário
    if not isinstance(data, dict):
        return False

    # verifica a existência dos itens no dicionário
    for item in ['current_player', 'groups', 'history', 'sequence']:
        if item not in data:
            return False

    # verifica o jogador atual como 0, 1, 2, 3 ou None
    if data['current_player'] not in [0, 1, 2, 3, None]:
        return False

    # verifica se os grupos das peças são uma lista com 4 elementos
    groups = data['groups']
    if not isinstance(groups, list) or len(groups) != 4:
        return False

    # verifica se cada elemento do grupo das peças é um inteiro entre 0 e 3
    for value in groups:
        if not isinstance(value, int) or not (0 <= value <= 3):
            return False

    # verifica se o histórico é uma lista
    history = data['history']
    if not isinstance(history, list):
        return False

    # verifica se cada valor do histórico é uma tupla da forma (peça, paços)
    for value in history:
        if not isinstance(value, tuple) or len(value) != 2:
            return False

        piece, steps = value
        if not isinstance(piece, int) or not (0 <= piece <= 15) \
                or not isinstance(steps, int) or not (1 <= steps <= 6):
            return False

    return True


def load_pieces_positions():
    """
    Move as peças de acordo com o histórico da partida carregada
    """

    board.reset_board()
    for piece, steps in match['history']:
        board.move_piece(piece, steps)


def close_match():
    """
    Fecha uma partida. A partina não pode ser continuada.
    :return: os dados da partida caso tenha uma partida em andamento.
     None caso contrário.
    """
    global match

    try:
        return match
    finally:
        match = None
