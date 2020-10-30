# Módulo Dice
# Atualizado: 26/10/2020
# Autor: Bruno Messeder dos Anjos

__all__ = ['throw', 'get', 'clear']

from random import randint

dice_value = None


def throw():
    global dice_value
    dice_value = randint(1, 6)
    return dice_value


def get():
    return dice_value


def clear():
    global dice_value
    dice_value = None
