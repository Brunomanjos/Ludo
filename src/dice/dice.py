# Módulo Dice
# Atualizado: 13/11/2020
# Autor: Bruno Messeder dos Anjos

__all__ = ['throw', 'get', 'clear']

from random import randint

dice_value = None


def throw():
    """
    Joga o dado de seis lados.
    :return: o valor tirado no dado (entre 1 e 6, inclusive)
    """
    global dice_value
    dice_value = randint(1, 6)
    return dice_value


def get():
    """
    :return: o último valor tirado no dado.
     None, caso o dado não tenha sido jogado ou o último valor tenha sido apagado.
    """
    return dice_value


def clear():
    """
    Apaga o último valor tirado no dado.
    """
    global dice_value
    dice_value = None
