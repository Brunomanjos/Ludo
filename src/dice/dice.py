# Módulo Board
# Atualizado: 14/10/2020
# autor: Bruno Messeder dos Anjos

__all__ = ['throw', 'get', 'clear']

from random import randint

dice_value = 6  # TODO change to None


def throw():
    global dice_value
    dice_value = randint(1, 6)
    return dice_value


def get():
    return dice_value


def clear():
    global dice_value
    dice_value = None
