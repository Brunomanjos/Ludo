# Sprites - Imagem
# Atualizado: 30/10/2020
# Autor: Bruno Messeder dos Anjos

import os

import pygame

__all__ = ['Image']


class Image(pygame.sprite.Sprite):
    """
    Sprite que representa uma imagem.
    """

    def __init__(self, path, img_size=None, **pos):
        pygame.sprite.Sprite.__init__(self)

        if img_size:
            self.image = pygame.Surface(img_size)
            image = pygame.image.load(os.path.join('res', path))
            self.image.blit(pygame.transform.smoothscale(image, img_size), (0, 0))
        else:
            self.image = pygame.image.load(os.path.join('res', path))

        self.rect = self.image.get_rect(**pos)
