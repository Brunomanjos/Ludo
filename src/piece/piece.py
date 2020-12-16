# Módulo Piece
# Atualizado: 15/12/2020
# Autor: Alberto Augusto Caldeira Brant

__all__ = ['buscaGrupo', 'todasPecas', 'corPeca', 'nomeCorPeca']

'''
Grupo 0:
Cor verde
Peças id 0 a 3

Grupo 1:
Cor vermelha
Peças id 4 a 7

Grupo 2:
Cor azul
Peças id 8 a 11

Grupo 3:
Cor amarela
Peças id 12 a 15
'''


def buscaGrupo(idPeca):
    # Retorna o numero do grupo que tal peça pertence
    # Se retornar -1 o id da peça não é coerente

    if idPeca <= -1:
        return -1
    if 0 <= idPeca <= 3:
        return 0
    elif idPeca <= 7:
        return 1
    elif idPeca <= 11:
        return 2
    elif idPeca <= 15:
        return 3
    else:
        return -1


def todasPecas(grupo):
    # Apartir de um grupo retorna os id's das peças que pertencem ao mesmo

    if grupo == 0:
        return [0, 1, 2, 3]

    elif grupo == 1:
        return [4, 5, 6, 7]

    elif grupo == 2:
        return [8, 9, 10, 11]

    elif grupo == 3:
        return [12, 13, 14, 15]

    else:
        return -1


def corPeca(idPeca):
    # Retorna a cor da peça

    if 0 <= idPeca <= 3:
        color = (0, 150, 0)
        return color
    elif idPeca <= 7:
        color = (150, 0, 0)
        return color
    elif idPeca <= 11:
        color = (0, 0, 150)
        return color
    elif idPeca <= 15:
        color = (150, 150, 0)
        return color
    else:
        return -1


def nomeCorPeca(idPeca):
    # Retorna o nome da cor da peça

    if 0 <= idPeca <= 3:
        return 'green'
    elif idPeca <= 7:
        return 'red'
    elif idPeca <= 11:
        return 'blue'
    elif idPeca <= 15:
        return 'yellow'
    else:
        return -1