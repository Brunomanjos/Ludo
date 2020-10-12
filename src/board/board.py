__all__ = ['get_next_point', 'get_spawn_points', 'get_finish_points', 'get_finish_point', 'is_finish_point',
           'get_pieces_positions', 'get_piece_position', 'move_piece', 'reset_board', 'get_pieces_at',
           'get_possible_moves', 'get_path', 'END_OF_PATH', 'NOT_ON_PATH', 'INVALID_GROUP', 'NEGATIVE_STEPS',
           'INVALID_PIECE_ID']

END_OF_PATH = 1
NOT_ON_PATH = 2
INVALID_GROUP = 3
NEGATIVE_STEPS = 4
INVALID_PIECE_ID = 5


def next_point_on_segment(seg_point1, seg_point2, current_point):
    """
    Retorna o próximo ponto em um segmento entre seg_point1 e seg_point2.
    O segmento deve ser horizontal ou vertical.

    :param seg_point1: primeiro ponto do segmento
    :param seg_point2: segundo ponto do segmento
    :param current_point: ponto atual no segmento
    :return: próximo ponto no segmento, caso o ponto atual pertença ao segmento
     e seja diferente de seg_point2. None, caso contrário.
    """

    y1, x1 = seg_point1
    y2, x2 = seg_point2
    y, x = current_point

    if y1 == y2:
        # horizontal
        if x2 > x1 and x1 <= x < x2 and y == y1:
            return y, x + 1
        elif x1 > x2 and x2 < x <= x1 and y == y1:
            return y, x - 1
    elif x1 == x2:
        # vertical
        if y2 > y1 and y1 <= y < y2 and x == x1:
            return y + 1, x
        elif y1 > y2 and y2 < y <= y1 and x == x1:
            return y - 1, x
    else:
        raise ValueError(f'internal error: segment must be horizontal or vertical: ({seg_point1}), ({seg_point2})')


def next_point_on_path(path_points, current_point):
    """
    Retorna o próximo ponto em um caminho (conjunto de segmentos).

    Caso current_point seja igual a path_points[-1], o próximo ponto será fora do caminho.
    Nesse caso, será retornado END_OF_PATH.

    :param path_points: lista de pontos que configuram um caminho (conjunto de segmentos)
    :param current_point: ponto atual no caminho
    :return: próximo ponto no caminho, caso current_point pertença ao caminho e
     seja diferente de path_points[-1]. END_OF_PATH se current_point for igual a path_points[-1].
     NOT_ON_PATH, se o ponto não pertencer ao caminho.
    """

    if current_point == path_points[-1]:
        return END_OF_PATH

    for index in range(len(path_points) - 1):
        # forma segmentos para cada par de pontos e tenta pegar o próximo ponto no segmento.
        point1, point2 = path_points[index], path_points[index + 1]
        next_p = next_point_on_segment(point1, point2, current_point)

        if next_p:
            return next_p

    return NOT_ON_PATH


def next_point_on_central(current_point, piece_group):
    """
    Retorna o próximo ponto no caminho central (última reta em que as peças passam para chegar no centro do
    tabuleiro) e um indicativo (True/False) de overflow: Se verdaderio, significa que a peça excedeu o limite
    de movimento e passou da posição final, voltando para o início do caminho central.

    :param current_point: ponto atual. Pode não pertencer ao caminho central
    :param piece_group: grupo da peça que está na posição current_point. Supõe que o grupo é válido
    :return: próximo ponto no caminho central e o indicativo de overflow, caso current_point percença
     ao caminho cetral e esse caminho seja válido para o grupo dado em piece_group. (NOT_ON_PATH, False), caso contrário.
    """

    central = board['central'][piece_group]  # caminho central para o grupo de piece_group

    next_p = next_point_on_segment(central['from'], central['to'], current_point)

    if next_p:
        return next_p, False
    elif current_point == central['to']:
        next_p = next_point_on_segment(central['from'], central['to'], central['from'])
        return next_p, True

    return NOT_ON_PATH, False


def next_point_on_main(current_point):
    """
    Retorna o próximo ponto no caminho principal (caminho por onde as peças andam logo após sairem da origem).
    Não considera o caminho central caso uma peça precise entrar nele.

    :param current_point: ponto atual no caminho. Pode não pertencer ao caminho principal
    :return: próximo ponto no caminho principal, caso current_point pertença ao caminho
     principal. None, caso contrário.
    """
    for path_index, path in enumerate(board['main']):
        next_p = next_point_on_path(path, current_point)
        if next_p == END_OF_PATH:
            # retorna o primeiro ponto do próximo caminho
            # como o caminho é em loop, caso path_index for 3 (último caminho), o próximo caminho é 0
            next_path = (path_index + 1) % 4
            return board['main'][next_path][0]
        elif isinstance(next_p, tuple):
            return next_p


def next_point_on_spawn(current_point, piece_group):
    """
    Retorna o próximo ponto da origem das peças.

    :param current_point: ponto atual. Pode não pertencer à origem
    :param piece_group: grupo da peça que está na posição current_point. Supõe que o grupo é válido
    :return: próximo ponto, no caminho central, caso o ponto atual
     pertença à origem do grupo piece_group. None, caso contrário
    """
    spawn = board['spawn'][piece_group]
    if current_point in spawn['from']:
        return spawn['to']


def next_point_one_step(current_point, piece_group):
    """
    Retorna o próximo ponto no tabulerio e um indicativo de overflow
    (definido em next_point_on_central), caso o ponto atual seja válido.

    :param current_point: ponto atual no tabuleiro
    :param piece_group: grupo da peça que está na posição current_point. Supõe que o grupo é válido
    :return: próximo ponto no tabuleiro e o indicativo de overflow, caso o ponto pertença ao tabuleiro.
     (None, False), caso contrário
    """

    next_p, overflow = next_point_on_central(current_point, piece_group)
    if isinstance(next_p, tuple):
        return next_p, overflow

    next_p = next_point_on_main(current_point)
    if isinstance(next_p, tuple):
        return next_p, False

    next_p = next_point_on_spawn(current_point, piece_group)
    if isinstance(next_p, tuple):
        return next_p, False

    return None, False


def get_next_point(current_point, piece_group, steps):
    """
    Retorna um ponto a 'steps' paços do ponto atual.

    :param current_point: ponto atual no tabuleiro
    :param piece_group: grupo da peça que está na posição current_point (entre 0 e 3, inclusive)
    :param steps: quantos paços a peça vai andar
    :return: próximo ponto no tabuleiro, caso current_point pertença ao tabuleiro,
     piece_group seja válido e steps >= 0. NOT_ON_PATH, caso o ponto não pertença ao tabuleiro ou
     seja invádio para o grupo piece_group.
     INVALID_GROUP, caso o grupo seja inválido. NEVATIVE_STEPS, caso steps seja negativo.
    """

    if piece_group < 0 or piece_group > 3:
        return INVALID_GROUP
    elif steps < 0:
        return NEGATIVE_STEPS

    position = current_point
    for step in range(steps):
        position, overflow = next_point_one_step(position, piece_group)

        if position is None:
            return NOT_ON_PATH
        elif overflow:
            break

    return position


def get_spawn_points(piece_group=None):
    """
    Retorna os pontos de origem das peças, como um dicionário, em que as chaves são os ids das peças

    :param piece_group: grupo das peças da origem desejada. Se for None, todos os grupos serão considerados
    :return: pontos de origem do grupo desejado, caso piece_group seja válido. INVALID_GROUP caso contrário.
    """

    if piece_group and (piece_group < 0 or piece_group > 3):
        return INVALID_GROUP

    spawns = {}

    for group, spawn in enumerate(board['spawn']):
        if piece_group is None or piece_group == group:
            for index, point in enumerate(spawn['from']):
                spawns[4 * group + index] = point

    return spawns


def get_finish_points():
    """
    :return: pontos finais de todos os grupos de peças em uma lista em que os índices são os grupos das peças.
    """
    return [board['central'][group]['to'] for group in range(4)]


def get_finish_point(piece_group):
    """
    :param piece_group: group relativo ao ponto final.
    :return: ponto final do grupo piece_group, caso piece_group seja válido. INVALID_GROUP, caso contrário.
    """

    if piece_group < 0 or piece_group > 3:
        return INVALID_GROUP

    return board['central'][piece_group]['to']


def is_finish_point(point, piece_group=None):
    """
    Verifica se o ponto é um ponto final.

    :param point: point a ser verificado
    :param piece_group: grupo da peça no ponto 'point', ou None se puder ser ponto final de qualquer grupo
    :return: INVALID_GROUP, caso o grupo seja inválido.
     True, caso o ponto seja ponto final do grupo piece_group. False, caso contrário.
    """

    if piece_group is None:
        return point in get_finish_points()
    elif piece_group < 0 or piece_group > 3:
        return INVALID_GROUP
    return point == get_finish_point(piece_group)


def reset_board():
    """
    Move todas as peças para suas posições de origem.

    :return: None
    """
    global pieces
    pieces = get_spawn_points()


def get_pieces_positions(piece_group=None):
    """
    Retorna as posições das peças, filtradas por grupo.

    :param piece_group: grupo das peças. Se for None, considera todas as peças
    :return: posições das peças em um dicionário, em que as chaves são os ids das peças,
     caso o piece_group seja válido. INVALID_GROUP, caso contrário
    """
    if piece_group and (piece_group < 0 or piece_group > 3):
        return INVALID_GROUP

    positions = pieces.copy()
    if piece_group is not None:
        start_id = 4 * piece_group
        end_id = start_id + 4
        positions = {piece_id: position for piece_id, position in positions.items() if start_id <= piece_id < end_id}

    return positions


def get_piece_position(piece_id):
    """
    :param piece_id: id da peça
    :return: posição da peça, caso piece_id seja válido. INVALID_PIECE_ID, caso contrário.
    """
    if piece_id < 0 or piece_id > 15:
        return INVALID_PIECE_ID
    return pieces[piece_id]


def get_pieces_at(position_filter):
    """
    Retorna todas as peças dado o filtro de posições.

    :param position_filter: onde verificar a existencia de peças. Pode ser uma posição ou uma lista de posições
    :return: todas as peças nas posições em position_filter, em uma lista em que os valores são os ids das peças
    """

    if isinstance(position_filter, list):
        return [piece_id for piece_id, piece_pos in pieces.items() if piece_pos in position_filter]

    return [piece_id for piece_id, piece_pos in pieces.items() if piece_pos == position_filter]


def is_valid_position(position, piece_group):
    """
    Verifica se uma posição é válida (pertence ao tabuleiro e pode ser conter uma peça do grupo piece_group)
    :param position: posição a ser verificada
    :param piece_group: grupo da peça na posição position
    :return: True, caso o ponto seja válido. False caso contrário
    """
    return get_next_point(position, piece_group, 1) != NOT_ON_PATH


def move_piece(piece_id, new_position):
    """
    Move a peça para uma nova posição.

    :param piece_id: id da peça
    :param new_position: nova posição
    :return: None caso a peça tenha sido movida. INVALID_PIECE_ID caso o id seja inválido.
     NOT_ON_PATH, caso a posição não seja válida para a peça.
    """

    if piece_id < 0 or piece_id > 15:
        return INVALID_PIECE_ID

    if not is_valid_position(new_position, piece_id // 4):
        return NOT_ON_PATH

    pieces[piece_id] = new_position


def get_possible_moves(piece_group, steps):
    """
    Retorna todas as jogadas possíveis para um grupo de peças.

    :param piece_group: grupos de peças
    :param steps: quantas posições as peças podem se mover
    :return: todas as jogadas possíveis para o grupo de peças, em um dicionário em que as
     chaves são os ids das peças, case o grupo seja válido e steps >= 0.
     INVALID_GROUP, caso o grupo seja inválido. NEGATIVE_STEPS, caso steps seja negativo.
    """
    if piece_group < 0 or piece_group > 3:
        return INVALID_GROUP
    elif steps < 0:
        return NEGATIVE_STEPS

    start_id = 4 * piece_group
    end_id = start_id + 4

    return {piece_id: get_next_point(pieces[piece_id], piece_group, steps) for piece_id in range(start_id, end_id)}


def get_path(from_pos, piece_group, steps):
    """
    Retorna uma lista com todos os pontos desde from_pos até from_pos + steps.

    :param from_pos: posição inical do caminho
    :param piece_group: grupo da peça que andará pelo caminho
    :param steps: quantas posições a peça irá se mover
    :return: lista com todos os pontos do caminho, considerando possível overflow,
     caso from_pos pertença seja válido para o grupo piece_group, piece_group seja válido e steps >= 0.
     INVALID_GROUP, caso o grupo seja inválido.
     NOT_ON_PATH, caso from_pos não seja válido para o grupo piece_group.
     NEGATIVE_STEPS, caso steps seja negativo.
    """
    if piece_group < 0 or piece_group > 3:
        return INVALID_GROUP
    elif not is_valid_position(from_pos, piece_group):
        return NOT_ON_PATH
    elif steps < 0:
        return NEGATIVE_STEPS

    path = [from_pos]
    while steps > 0:
        position, overflow = next_point_one_step(path[-1], piece_group)
        steps -= 1
        path.append(position)

        if position is None:
            return 1
        elif overflow:
            break
    return path


board = {
    'spawn': [{
        'from': [(2, 2), (2, 3), (3, 2), (3, 3)],
        'to': (6, 1)
    }, {
        'from': [(2, 11), (2, 12), (3, 11), (3, 12)],
        'to': (1, 8)
    }, {
        'from': [(11, 2), (11, 3), (12, 2), (12, 3)],
        'to': (13, 6)
    }, {
        'from': [(11, 11), (11, 12), (12, 11), (12, 12)],
        'to': (8, 13)
    }],
    'main': [
        [(8, 5), (8, 0), (6, 0), (6, 5)],
        [(5, 6), (0, 6), (0, 8), (5, 8)],
        [(6, 9), (6, 14), (8, 14), (8, 9)],
        [(9, 8), (14, 8), (14, 6), (9, 6)]
    ],
    'central': [{
        'from': (7, 0),
        'to': (7, 6)
    }, {
        'from': (0, 7),
        'to': (6, 7)
    }, {
        'from': (14, 7),
        'to': (8, 7)
    }, {
        'from': (7, 14),
        'to': (7, 8)
    }]
}

pieces = get_spawn_points()
