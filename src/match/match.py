# Módulo Match
# Atualizado: 01/11/2020
# Autor: Bruno Messeder dos Anjos

from random import randint, shuffle

import board
import dice
import player

__all__ = ['new_match', 'play', 'current_player', 'load_match', 'close_match', 'can_play',
           'MATCH_NOT_DEFINED', 'INVALID_PIECE', 'INVALID_PLAYER', 'MATCH_ENDED',
           'MATCH_IN_PROGRESS', 'INVALID_DATA', 'DICE_NOT_THROWN', 'current_player_name']

MATCH_NOT_DEFINED = -1
INVALID_PIECE = -2
INVALID_PLAYER = -3
MATCH_ENDED = -4
MATCH_IN_PROGRESS = -5
INVALID_DATA = -6
DICE_NOT_THROWN = -7
INVALID_STEPS = -8

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

    players = [p1, p2, p3, p4]
    shuffle(players)

    player.set_players(*players)
    board.reset_board()

    match = {
        'current_player': randint(0, 3),  # id do jogador atual. também é o grupo da peça do jogador atual
        'history': [],  # histórico da partida. Cada elemento é a jogada feita em uma rodada, da forma (peça, paços)
        'sequence': 0  # jogadas em sequência de um jogador. No máximo 3 antes de pular a vez
    }

    return True


def play(piece_id):
    """
    Faz uma jogada, movendo uma peça

    :param piece_id: id da peça, ou None, caso não haja jogada possível para o jogador atual.
    :return: None caso a jogada tenha sido efetuada.
     MATCH_NOT_DEFINED caso a partida não tenha sido definida
     INVALID_PIECE caso o id da peça seja seja inválido.
     DICE_NOT_THROWN caso o dado não tenha sido jogado nessa rodada.
     INVALID_PLAYER caso a peça não pertença ao jogador do turno atual.
     MATCH_ENDED caso a partida tenha terminado.
    """
    if not match:
        return MATCH_NOT_DEFINED
    elif piece_id is not None and (piece_id < 0 or piece_id > 15):
        return INVALID_PIECE

    steps = dice.get()

    if steps is None:
        return DICE_NOT_THROWN

    player = current_player()
    if player == MATCH_ENDED:
        return MATCH_ENDED

    if piece_id is None:
        # Só pode ser None se não há jogada possível
        if can_play(steps):
            return INVALID_PIECE
        dice.clear()
        next_player()
        check_winner()
        return

    if player != piece_id // 4:
        return INVALID_PLAYER

    piece_pos = board.get_piece_position(piece_id)
    if piece_pos not in board.get_spawn_positions(player) or steps == 6:
        # move a peça se ela não estiver na posição inicial ou,
        # caso esteja, o número de paços seja igual a 6
        board.move_piece(piece_id, steps)

    match['sequence'] += 1

    if steps < 6 or match['sequence'] >= 3:
        # muda o turno para o próximo jogador
        match['sequence'] = 0
        next_player()

    check_winner()

    dice.clear()


def finished_players():
    """
    :return: lista dos jogadores que acabaram de jogar.
    """
    players = []

    for player in range(4):
        pieces = board.get_pieces_at(board.get_finish_position(player))
        if len(pieces) == 4:
            players.append(player)

    return players


def next_player():
    """
    Passa a vez para o próximo jogador.
    """
    next = (current_player() + 1) % 4
    finished = finished_players()
    if len(finished) >= 3:
        return  # o jogo acabou. 3 ou 4 jogadores acabaram

    while next in finished:
        next = (next + 1) % 4  # passa pelos jogadores até achar um que não tenha terminado de jogar.

    match['current_player'] = next


def check_winner():
    """
    Verifica se o jogo acabou. O jogo acaba quando todas as peças de três jogadores chegam ao centro do tabuleiro.
    """

    if len(finished_players()) >= 3:
        match['current_plaer'] = None


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


def current_player_name():
    """
    :return: o nome do jogador atual, caso haja um partida em andamento.
    MATCH_ENDED caso a partida tenha terminado.
    MATCH_NOT_DEFINED caso a partida não tenha sido definida
    """
    if not match:
        return MATCH_NOT_DEFINED

    current = match['current_player']

    if current is None:
        return MATCH_ENDED

    return player.get_player(current)


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
    for item in ['current_player', 'history', 'sequence']:
        if item not in data:
            return False

    # verifica o jogador atual como 0, 1, 2, 3 ou None
    if data['current_player'] not in [0, 1, 2, 3, None]:
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


def can_play(steps):
    """
    Verifica se o jogador atual pode fazer uma jogada caso tire um valor específico no dado.

    :type steps: quantidade hipotética tirada no dado
    :return: True caso o jogador possa fazer a jogada. False caso contrário.
     MATCH_NOT_DEFINED caso a partida não tenha sido definida.
     MATCH_ENDED caso a partida tenha acabado.
     INVALID_STEPS caso steps seja 1 ou steps > 6
    """
    if not match:
        return MATCH_NOT_DEFINED

    player = match['current_player']

    if player is None:
        return MATCH_ENDED
    elif steps < 1 or steps > 6:
        return INVALID_STEPS

    moves = board.get_possible_moves(player, steps)
    if not any(moves.values()):
        return False

    if steps == 6:
        return True

    piece_pos = board.get_spawn_positions()
    spawn_pos = board.get_spawn_positions(player)

    # retorna verdadeiro se existe pelo menos uma peça fora da origem com steps < 6
    return piece_pos != spawn_pos
