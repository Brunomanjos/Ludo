# Módulo Match
# Atualizado: 16/11/2020
# Autor: Bruno Messeder dos Anjos

from random import randint, shuffle
from time import time
from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, parse
from xml.dom.minidom import parseString
import os

import board
import database
import dice
import piece
import player

__all__ = ['new_match', 'play', 'current_player', 'load_match', 'close_match', 'can_play',
           'MATCH_NOT_DEFINED', 'INVALID_PIECE', 'INVALID_PLAYER', 'MATCH_ENDED', 'MATCH_IN_PROGRESS',
           'INVALID_DATA', 'DICE_NOT_THROWN', 'current_player_name', 'INVALID_ID', 'INVALID_STEPS', 'finished_players']

MATCH_NOT_DEFINED = -1
INVALID_PIECE = -2
INVALID_PLAYER = -3
MATCH_ENDED = -4
MATCH_IN_PROGRESS = -5
INVALID_DATA = -6
DICE_NOT_THROWN = -7
INVALID_STEPS = -8
INVALID_ID = -9

match: Optional[dict] = None

current_turn = 0


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
    global match, current_turn
    if match:
        return MATCH_IN_PROGRESS

    players = [p1, p2, p3, p4]
    shuffle(players)

    player.set_players(*players)
    board.reset_board()

    match = {
        'current_player': randint(0, 3),  # id do jogador atual. também é o grupo da peça do jogador atual
        'sequence': 0  # jogadas em sequência de um jogador. No máximo 3 antes de pular a vez
    }

    current_turn = 0

    database.execute('CREATE TABLE IF NOT EXISTS History(piece_id int, steps int NOT NULL, turn int NOT NULL)')
    database.execute('DELETE FROM History')

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
    elif piece_id is not None and piece.buscaGrupo(piece_id) == -1:
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
        save_move(None)
        return

    if player != piece.buscaGrupo(piece_id):
        return INVALID_PLAYER

    piece_pos = board.get_piece_position(piece_id)
    if piece_pos not in board.get_spawn_positions(player) or steps == 6:
        # move a peça se ela não estiver na posição inicial ou,
        # caso esteja, o número de paços seja igual a 6
        board.move_piece(piece_id, steps)
        save_move(piece_id)

    match['sequence'] += 1

    if steps < 6 or match['sequence'] >= 3:
        # muda o turno para o próximo jogador
        match['sequence'] = 0
        next_player()

    check_winner()

    dice.clear()


def save_move(piece_id):
    """
    Salva a jogada atual no banco de dados
    """

    global current_turn

    if piece_id is not None:
        database.execute(f'INSERT INTO History VALUES ({piece_id}, {dice.get()}, {current_turn})')
    else:
        database.execute(f'INSERT INTO History VALUES (NULL, 0, {current_turn})')

    current_turn += 1


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
        match['current_player'] = None


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


def load_match(match_id):
    """
    Carrega uma partida já começada.

    :param match_id: o id da partida
    :return: True caso a partida tenha sido carregada.
     MATCH_IN_PROGRESS caso já tenha uma partida em andamento.
     INVALID_ID caso o id da partida seja inválido.
     INVALID_DATA caso os dados da partida sejam inválidos.
    """

    global match, current_turn

    if match:
        return MATCH_IN_PROGRESS

    path = os.path.join(os.environ['appdata'], f'.ludo\\match {match_id}.xml')

    if not os.path.isfile(path):
        return INVALID_ID

    data = {}

    root = parse(path).getroot()
    players = root.find('players')

    if players is None:
        return INVALID_DATA

    for player_element in players:
        player.set_player(int(player_element.attrib['id']), player_element.text)

    match_id_element = root.find('matchID')
    if match_id_element is None:
        return INVALID_DATA

    data['id'] = int(match_id_element.text)

    current_player = root.find('currentPlayer')

    if current_player is None:
        return INVALID_DATA

    data['current_player'] = int(current_player.text)

    sequence = root.find('sequence')

    if sequence is None:
        return INVALID_DATA

    data['sequence'] = int(sequence.text)

    board.reset_board()
    database.execute('CREATE TABLE IF NOT EXISTS History(piece_id int, steps int NOT NULL, turn int NOT NULL)')
    database.execute('DELETE FROM History')

    for turn, move in enumerate(root.find('history')):
        piece_id = move.attrib['piece_id']
        steps = move.attrib['steps']

        current_turn = turn

        if piece_id != 'None':
            board.move_piece(int(piece_id), int(steps))
            database.execute(f'INSERT INTO History VALUES ({piece_id}, {steps}, {turn})')
        else:
            database.execute(f'INSERT INTO History VALUES (NULL, {steps}, {turn})')

    match = data

    return True


def close_match(save_match_data=True):
    """
    Fecha uma partida. A partina não pode ser continuada.

    :param save_match_data: Se verdadeiro, salva a partida em um arquivo xml
    :return: True caso tenha uma partida em andamento.
     False caso contrário.
    """
    global match

    if not match:
        return False

    if save_match_data:
        save_match()

    board.reset_board()
    dice.clear()
    match = None
    return True


def save_match():
    """
    Salva a partida atual em um arquivo xml
    """
    history = database.fetchall('SELECT piece_id, steps FROM History ORDER BY turn')

    root = Element('match')

    if 'id' in match:
        match_id = match['id']
    else:
        match_id = new_match_id()

    SubElement(root, 'matchID').text = str(match_id)
    SubElement(root, 'currentPlayer').text = str(match['current_player'])

    player_element = SubElement(root, 'players')
    for index, name in enumerate(player.get_players()):
        SubElement(player_element, 'player', {'id': str(index)}).text = name

    SubElement(root, 'sequence').text = str(match['sequence'])

    SubElement(root, 'ended').text = str(len(finished_players()) >= 3)

    history_element = SubElement(root, 'history')
    for (piece_id, steps) in history:
        SubElement(history_element, 'move', {'piece_id': str(piece_id), 'steps': str(steps)})

    data = parseString(ElementTree.tostring(root, 'utf-8')).toprettyxml(indent='  ')

    path = os.path.join(os.environ['appdata'], f'.ludo\\match {match_id}.xml')

    with open(path, 'w') as file:
        file.write(data)


def new_match_id():
    """
    Gera um novo id da partida, baseado nos jogos salvos na memória.
    :return: o novo id da partida
    """
    directory = os.path.join(os.environ['appdata'], '.ludo\\')

    if not os.path.exists(directory):
        os.mkdir(directory)

    match_id = 1

    file_name = 'match {}.xml'
    path = directory + file_name.format(match_id)

    while os.path.isfile(path):
        match_id += 1
        path = directory + file_name.format(match_id)

    return match_id


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
