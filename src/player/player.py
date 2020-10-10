__all__ = ['set_player', 'set_players', 'get_player', 'get_players']

_players = ['', '', '', '']


def check_type(name):
    name_type = type(name)
    if name_type != str:
        raise TypeError(f'Name should be a string. Instead, it was {name_type.__name__}')


def check_types(name1, name2, name3, name4):
    type1, type2, type3, type4 = type(name1), type(name2), type(name3), type(name4)
    if type1 != str or type2 != str or type3 != str or type4 != str:
        raise TypeError(f'All names should be strings. Instead, they were: {type1.__name__}, '
                        f'{type2.__name__}, {type3.__name__}, {type4.__name__}')


def set_player(index, name):
    """
    Set player name by its index
    :param index: player index
    :param name: player name
    :return: True if index is valid. False otherwise.
    """
    check_type(name)

    if index < 0 or index > 3:
        return False

    _players[index] = name

    return True


def set_players(name1, name2, name3, name4):
    """

    :param name1: first player name
    :param name2: second player name
    :param name3: third player name
    :param name4: fourth player name
    :return: always returns True
    """
    check_types(name1, name2, name3, name4)

    global _players
    _players = [name1, name2, name3, name4]
    return True


def get_player(index):
    """
    Returns a player name
    :param index: player index
    :return: player name, if index is valid. None otherwise
    """
    if index < 0 or index > 3:
        return

    return _players[index]


def get_players():
    """
    Returns all player names, ordered by their index
    :return: player names as list
    """
    return _players.copy()
