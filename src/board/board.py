__all__ = ['get_next_point', 'get_spawn_points', 'get_finish_points', 'get_finish_point', 'is_finish_point',
           'get_pieces_positions', 'get_piece_position', 'move_piece', 'reset_board', 'get_pieces_at',
           'get_possible_moves', 'get_path']


def next_point_on_segment(seg_point1, seg_point2, current_point):
    """
    Returns next point on segment that starts on point1 and ends at point2.
    The segment must be horizontal or vertical.

    :param seg_point1: first point on segment
    :param seg_point2: second point on segment
    :param current_point: current position on segment
    :return: next point on segment. None if position is not on segment
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
    Returns the next point on path.

    if position == points[-1], then next point will be outside path. In this case, will return 0

    :param path_points: point list that represents a path. must not be empty
    :param current_point: current point on path
    :return: next point on path. None if position is invalid. 0 if position == points[-1]
    """

    if current_point == path_points[-1]:
        return 0

    for index in range(len(path_points) - 1):
        point1, point2 = path_points[index], path_points[index + 1]
        next_p = next_point_on_segment(point1, point2, current_point)

        if next_p:
            return next_p


def next_point_on_central(current_point, piece_group):
    """
    :param current_point: current point. May or may not be on central path
    :param piece_group: group of the piece on current_point
    :return: next point if current_point is on central path of its piece_group. None otherwise
    """
    central = board['central'][piece_group]
    finish = board['finish'][piece_group]
    if current_point == central['from']:
        return central['to'], False

    next_p = next_point_on_segment(central['to'], finish, current_point)
    if next_p:
        return next_p, False
    elif current_point == finish:
        return central['to'], True


def next_point_on_main(current_point):
    """
    :param current_point: current point on main path
    :return: next point if current_point is on main path. None otherwise
    """
    for index, path in enumerate(board['main']):
        next_p = next_point_on_path(path, current_point)
        if next_p == 0:
            next_path = (index + 1) % 4
            return board['main'][next_path][0], False
        elif next_p:
            return next_p, False


def next_point_on_spawn(current_point, piece_group):
    """
    :param current_point: current point on spawn
    :param piece_group: group of the piece on current_point
    :return: next point if current_point is on spawn of its piece_group. None otherwise
    """
    spawn = board['spawn'][piece_group]
    if current_point in spawn['from']:
        return spawn['to'], False


def next_point_one_step(current_point, piece_group):
    """
    If current_point is invalid, will return None, False.
    Assumes that piece_group is valid.

    :param current_point: current point on board
    :param piece_group: group of the piece on current_point
    :return: a pair (point, overflow).
     The point is the next point on board.
     The overflow is a bool that indicates if the current point is the last on central path,
     and next point is at the beginning of the central path, causing the piece to go back
    to the beginning of the central path.
    """

    next_p = next_point_on_central(current_point, piece_group)
    if next_p:
        return next_p

    next_p = next_point_on_main(current_point)
    if next_p:
        return next_p

    next_p = next_point_on_spawn(current_point, piece_group)
    if next_p:
        return next_p

    return None, None


def get_next_point(current_point, piece_group, steps):
    """
    :param current_point: current point on board
    :param piece_group: group of the piece on current_point
    :param steps: how many positions will the piece move
    :return: next point if current_point is on board, piece_group is valid and steps >= 0.
     1 if current_point is invalid.
     2 if piece_group is invalid.
     3 if steps &lt 0.
    """

    if piece_group < 0 or piece_group > 3:
        return 2
    elif steps < 0:
        return 3

    position = current_point
    while steps > 0:
        position, overflow = next_point_one_step(position, piece_group)
        steps -= 1

        if position is None:
            return 1
        elif overflow:
            break

    return position


def get_spawn_points(piece_group=None):
    """
    :param piece_group: piece group related to the spawn points. If None, all groups will be considered.
    :return: spawn points of all groups, as a dict. The dict's keys are piece ids. None if piece_group is invalid.
    """

    if piece_group and (piece_group < 0 or piece_group > 3):
        return None

    spawns = {}

    for group, spawn in enumerate(board['spawn']):
        if piece_group is None or piece_group == group:
            for index, point in enumerate(spawn['from']):
                spawns[4 * group + index] = point

    return spawns


def get_finish_points():
    """
    :return: finish points for all piece groups, where the nth element on the list if the finish point of the nth group.
    """
    return board['finish'].copy()


def get_finish_point(piece_group):
    """
    :param piece_group: group relative to the finish point.
    :return: finish point of the piece_group. None if piece_group is invalid
    """

    if piece_group < 0 or piece_group > 3:
        return
    return board['finish'][piece_group]


def is_finish_point(point, piece_group=None):
    """

    :param point: point to check if is a finish point.
    :param piece_group: piece group of the piece on this point, or None (default) if can be any group.
    :return: True if the point is a finish point for the given piece_group.
     False if the point is not a finish point and the piece_group is valid.
     1 if piece_group is invalid.
    """

    if piece_group is None:
        return point in board['finish']
    elif piece_group < 0 or piece_group > 3:
        return 1
    return point == board['finish'][piece_group]


def reset_board():
    """
    Resets the board to the original state. All pieces will go back to their spawn.
    :return: None
    """
    global pieces
    pieces = get_spawn_points()


def get_pieces_positions(piece_group=None):
    """
    :param piece_group: filters pieces by group. If None, all groups will be considered
    :return: dict of piece positions given piece_group filter, where the dict's key is the piece_id.
     None if piece_group is invalid
    """
    if piece_group and (piece_group < 0 or piece_group > 3):
        return None

    positions = pieces.copy()
    if piece_group is not None:
        start_id = 4 * piece_group
        end_id = start_id + 4
        positions = {piece_id: position for piece_id, position in positions.items() if start_id <= piece_id < end_id}

    return positions


def get_piece_position(piece_id):
    """
    :param piece_id: piece's id
    :return: piece's position if piece_id is valid. None otherwise
    """
    if piece_id < 0 or piece_id > 15:
        return
    return pieces[piece_id]


def get_pieces_at(position_filter):
    """
    :param position_filter: where to check for pieces. Can be a position or a list of positions
    :return: all pieces at the given position as a list, where the values are the pieces' ids
    """

    if isinstance(position_filter, list):
        return [piece_id for piece_id, piece_pos in pieces.items() if piece_pos in position_filter]

    return [piece_id for piece_id, piece_pos in pieces.items() if piece_pos == position_filter]


def is_valid_position(position, piece_group):
    return get_next_point(position, piece_group, 1) != 1


def move_piece(piece_id, new_position):
    """
    Moves a piece to a new position.
    :param piece_id: piece's id
    :param new_position: new piece position
    :return: 0 if piece was moved, 1 if piece_id is invalid and 2 if new_position is invalid for the given piece.
    """

    if piece_id < 0 or piece_id > 15:
        return 1

    if not is_valid_position(new_position, piece_id // 4):
        return 2

    pieces[piece_id] = new_position

    return 0


def get_possible_moves(piece_group, steps):
    """
    :param piece_group: pieces' group
    :param steps: how many positions would the piece move
    :return: all possible moves for pieces from piece_group as a dictionary
     where the keys are the pieces' ids.
     1 if piece_group is invalid.
     2 if steps < 0
    """
    if piece_group < 0 or piece_group > 3:
        return 1
    elif steps < 0:
        return 2

    start_id = 4 * piece_group
    end_id = start_id + 4

    return {piece_id: get_next_point(pieces[piece_id], piece_group, steps) for piece_id in range(start_id, end_id)}


def get_path(from_pos, piece_group, steps):
    """
    :param from_pos: initial position from path
    :param piece_group: piece group, to determine when the piece should enter to the central path
    :param steps: how many steps will the piece move
    :return: a list with all points between start and end positions.
     If a overflow occurs, the path will end at the beginning of the central path.
     1 if from_pos is invalid.
     2 if piece_group is invalid.
     3 if steps < 0.
    """

    if not is_valid_position(from_pos, piece_group):
        return 1
    elif piece_group < 0 or piece_group > 3:
        return 2
    elif steps < 0:
        return 3

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
        'to': (7, 1)
    }, {
        'from': (0, 7),
        'to': (1, 7)
    }, {
        'from': (14, 7),
        'to': (13, 7)
    }, {
        'from': (7, 14),
        'to': (7, 13)
    }],
    'finish': [(7, 6), (6, 7), (8, 7), (7, 8)]
}

pieces = get_spawn_points()
