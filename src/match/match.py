# Módulo Match
# Atualizado: 21/11/2020
# Autor: Bruno Messeder dos Anjos

import re
from random import randint, shuffle
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
           'CANNOT_MOVE_PIECE', 'MATCH_NOT_DEFINED', 'INVALID_PIECE', 'INVALID_PLAYER',
           'MATCH_ENDED', 'MATCH_IN_PROGRESS', 'INVALID_DATA', 'DICE_NOT_THROWN',
           'current_player_name', 'INVALID_ID', 'INVALID_STEPS', 'winners']

MATCH_NOT_DEFINED = -1
INVALID_PIECE = -2
INVALID_PLAYER = -3
MATCH_ENDED = -4
MATCH_IN_PROGRESS = -5
INVALID_DATA = -6
DICE_NOT_THROWN = -7
INVALID_STEPS = -8
INVALID_ID = -9
CANNOT_MOVE_PIECE = -10

# versão dos arquivos xml, para evitar erros ao carregar uma partida
_XML_VERSION = '0.7'

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
        'sequence': 0,  # jogadas em sequência de um jogador. No máximo 3 antes de pular a vez
        'winners': []  # os índices dos ganhadores, em ordem
    }

    current_turn = 0

    database.execute('CREATE TABLE IF NOT EXISTS History(piece_id int, steps int NOT NULL, turn int NOT NULL)')
    database.execute('DELETE FROM History')

    return True


def play(piece_id):
    """
    Faz uma jogada, movendo uma peça

    :param piece_id: id da peça, ou None, caso não haja jogada possível para o jogador atual.
    :return: True caso a jogada tenha sido efetuada.
     CANNOT_MOVE_PIECE caso a peça não possa ser movida.
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
        save_move(None)
        return

    if player != piece.buscaGrupo(piece_id):
        return INVALID_PLAYER

    piece_pos = board.get_piece_position(piece_id)

    # a peça não pode ser movida caso esteja no spawn e steps não for 1 ou 6.
    if piece_pos in board.get_spawn_positions(player).values() and steps not in [1, 6]:
        return CANNOT_MOVE_PIECE

    board.move_piece(piece_id, steps)
    save_move(piece_id)

    match['sequence'] += 1

    if steps < 6 or match['sequence'] >= 3:
        # muda o turno para o próximo jogador
        match['sequence'] = 0
        next_player()

    check_match_end()

    dice.clear()

    return True


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


def winners():
    """
    :return: lista dos jogadores (índices) que terminaram de jogar, em ordem.
    """
    return match['winners']


def next_player():
    """
    Passa a vez para o próximo jogador.
    """

    check_match_end()
    if current_player() == MATCH_ENDED:
        return

    next = (current_player() + 1) % 4

    finished = winners()
    while next in finished:
        next = (next + 1) % 4  # passa pelos jogadores até achar um que não tenha terminado de jogar.

    match['current_player'] = next


def check_match_end():
    """
    Verifica se o jogo acabou. O jogo acaba quando todas as peças de três jogadores chegam ao centro do tabuleiro.
    """

    for player in range(4):
        pos = board.get_finish_position(player)
        if len(board.get_pieces_at(pos)) == 4 and player not in winners():
            match['winners'].append(player)
            break

    if len(winners()) == 3:
        for last_place in range(4):
            if last_place not in winners():
                match['winners'].append(last_place)
                break

    if len(winners()) >= 3:
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


def get_match(match_id):
    """
    Retorna o conteúdo de uma partida salva.

    :param match_id: o id da partida
    :return: dados da partida em um dicionário, caso a partida tenha sido carregada.
     INVALID_ID caso o id da partida seja inválido.
     INVALID_DATA caso os dados da partida sejam inválidos.
    """

    if match:
        return MATCH_IN_PROGRESS

    path = os.path.join(os.environ['appdata'], f'.ludo\\match {match_id}.xml')

    if not os.path.isfile(path):
        return INVALID_ID

    data = {'players': {}, 'history': []}

    root = parse(path).getroot()
    players = root.find('players')

    if players is None:
        return INVALID_DATA

    for player_element in players:
        data['players'][int(player_element.attrib['id'])] = player_element.text

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

    winners_element = root.find('winners')

    data['winners'] = [-1] * len(winners_element)

    for winner in winners_element:
        data['winners'][int(winner.attrib['index'])] = int(winner.text)

    for move in root.find('history'):
        piece_id = move.attrib['piece_id']
        steps = move.attrib['steps']
        turn = int(move.attrib['turn'])
        data['history'].append({'piece_id': piece_id, 'steps': steps, 'turn': turn})

    # ordena o histórico a partir do turno
    data['history'].sort(key=lambda e: e['turn'])

    return data


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

    data = get_match(match_id)
    if data in [INVALID_ID, MATCH_IN_PROGRESS, INVALID_DATA]:
        return data

    for index, name in data['players'].items():
        player.set_player(index, name)

    board.reset_board()
    database.execute('CREATE TABLE IF NOT EXISTS History(piece_id int, steps int NOT NULL, turn int NOT NULL)')
    database.execute('DELETE FROM History')

    for move in data['history']:
        piece_id = move['piece_id']
        steps = move['steps']
        turn = move['turn']

        if piece_id != 'None':
            board.move_piece(int(piece_id), int(steps))
            database.execute(f'INSERT INTO History VALUES ({piece_id}, {steps}, {turn})')
        else:
            database.execute(f'INSERT INTO History VALUES (NULL, {steps}, {turn})')

    match = data
    current_turn = len(data['history'])


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
    history = database.fetchall('SELECT piece_id, steps, turn FROM History ORDER BY turn')

    root = Element('match')

    SubElement(root, 'version').text = _XML_VERSION

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

    winners_element = SubElement(root, 'winners')
    for index, winner in enumerate(match['winners']):
        SubElement(winners_element, 'winner', {'index': str(index)}).text = str(winner)

    SubElement(root, 'ended').text = str(len(match['winners']) >= 3)

    history_element = SubElement(root, 'history')
    for (piece_id, steps, turn) in history:
        SubElement(history_element, 'move', {'piece_id': str(piece_id), 'steps': str(steps), 'turn': str(turn)})

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


def check_files():
    pattern = re.compile('match (\\d+).xml')

    directory = os.path.join(os.environ['appdata'], '.ludo')

    for file_name in os.listdir(directory):
        match = pattern.fullmatch(file_name)
        path = os.path.join(directory, file_name)

        if not match:
            continue

        xml_root = parse(path).getroot()
        version = xml_root.find('version')
        if version is None or version.text != _XML_VERSION:
            os.remove(path)


check_files()
