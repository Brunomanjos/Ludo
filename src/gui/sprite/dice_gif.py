# Sprites - GIF do Dado
# Atualizado: 16/12/2020
# Autor: Bruno Messeder dos Anjos

import io
import os
import time
from threading import Thread, Lock, Condition
import pygame
from PIL import Image

__all__ = ['DiceGIF']

from gui.sprite import GIF


class DiceGIF(GIF):
    """
    Sprite que representa um GIF do dado.
    """

    def __init__(self, path):
        super().__init__(path, False, False, first_frame=5, center=(600, 451))
        self.on_hide = None

    def hide(self):
        self.kill()
        if self.on_hide:
            self.on_hide()
