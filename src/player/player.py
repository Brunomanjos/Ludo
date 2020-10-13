# autor: Bruno Messeder dos Anjos

__all__ = ['set_player', 'set_players', 'get_player', 'get_players']

_players = ['', '', '', '']


def check_type(name):
    """Verifica se o nome de um jogador é string."""

    name_type = type(name)
    if name_type != str:
        raise TypeError(f'Name should be a string. Instead, it was {name_type.__name__}')


def check_types(name0, name1, name2, name3):
    """Verifica se o nome dos quatro jogadores são strings."""

    type0, type1, type2, type3 = type(name0), type(name1), type(name2), type(name3)
    if type0 != str or type1 != str or type2 != str or type3 != str:
        raise TypeError(f'All names should be strings. Instead, they were: {type0.__name__}, {type1.__name__}, '
                        f'{type2.__name__}, {type3.__name__}')


def set_player(player_id, name):
    """
    Define o nome de um jogador

    :param player_id: id do jogador (entre 0 e 3, inclusive)
    :param name: nome do jogador
    :return: True se o player_id for válido. False, caso contrário.
    """
    check_type(name)

    if player_id < 0 or player_id > 3:
        return False

    _players[player_id] = name

    return True


def set_players(name0, name1, name2, name3):
    """
    Define o nome dos quatro jogadores

    :param name0: nome do primeiro jogador
    :param name1: nome do segundo jogador
    :param name2: nome do terceiro jogador
    :param name3: nome do quarto jogador
    :return: None
    """
    check_types(name0, name1, name2, name3)

    global _players
    _players = [name0, name1, name2, name3]


def get_player(player_id):
    """
    Retorna o nome de um jogador.

    :param player_id: id do jogador (entre 0 e 3, inclusive)
    :return: nome do jogador, se player_id for válido. None, caso contrário
    """
    if player_id < 0 or player_id > 3:
        return

    return _players[player_id]


def get_players():
    """
    Retorna o nome dos quatro jogadores, em ordem de id

    :return: lista com os quatro jogadores
    """
    return _players.copy()
