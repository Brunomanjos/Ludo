# Sprites - GIF
# Atualizado: 08/12/2020
# Autor: Bruno Messeder dos Anjos

import io
import time
from threading import Thread, Lock
from PIL import Image
import pygame

__all__ = ['GIF']

load_lock = Lock()


class GIF(pygame.sprite.Sprite):
    """
    Sprite que representa um GIF.
    """

    def __init__(self, path, loop, run_at_start, on_end=None, img_size=None, **pos):
        pygame.sprite.Sprite.__init__(self)

        gif = Image.open(path)

        self._secs_on_screen = gif.info['duration'] / 1000
        self._last_img_time = time.time()
        self.loop = loop
        self._running = run_at_start
        self._loading = True
        self.on_end = on_end

        self.images = []
        self._image_index = -1
        Thread(target=self._load_all_images, args=[gif, img_size]).start()

        self.image = pygame.Surface(img_size or gif.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(**pos)

    def _load_all_images(self, gif, img_size):
        def get_surface():
            gif.seek(frame)
            image = io.BytesIO()
            gif.save(image, format='GIF')
            image.seek(0)

            with load_lock:
                surface = pygame.image.load(image)

            if img_size:
                resized_surface = pygame.Surface(img_size)
                resized_surface.blit(pygame.transform.scale(surface, img_size), (0, 0))
                return resized_surface

            return surface

        for frame in range(gif.n_frames):
            surface = get_surface()

            if frame > 0:
                blit_surface = self.images[-1].copy()
                blit_surface.blit(surface, (0, 0))
                surface = blit_surface
            else:
                self.image = surface
            self.images.append(surface)

        self._loading = False
        gif.close()

    def update(self):
        if not self._running:
            return

        now = time.time()

        if now - self._last_img_time < self._secs_on_screen:
            return

        self._last_img_time = now
        self._image_index += 1

        if self._image_index >= len(self.images):
            if self._loading:
                self._image_index -= 1
                return
            if self.on_end:
                self.on_end()
            if not self.loop:
                self._running = False
                return
            self._image_index = 0

        self.image = self.images[self._image_index]

    def run(self):
        if self._running is False:
            self._running = True
            self._image_index = -1

    def stop(self):
        self._running = False
