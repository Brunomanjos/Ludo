# Sprites - GIF
# Atualizado: 15/12/2020
# Autor: Bruno Messeder dos Anjos

import io
import os
import time
from threading import Thread, Lock, Condition
import pygame
from PIL import Image

__all__ = ['GIF']

load_lock = Lock()


class GIF(pygame.sprite.Sprite):
    """
    Sprite que representa um GIF.
    """

    def __init__(self, path, loop, run_at_start=True, on_end=None, wait_first_frame=False, first_frame=0, **pos):
        pygame.sprite.Sprite.__init__(self)

        gif = Image.open(os.path.join('res', path))

        self._secs_on_screen = gif.info['duration'] / 1000
        self._last_img_time = 0
        self.loop = loop
        self._running = run_at_start
        self._loading = True
        self.on_end = on_end
        self._first_frame = first_frame

        self.images = []
        self._image_index = first_frame - 1
        self._await_condition = Condition()

        self._load_all_images(gif)

        if wait_first_frame:
            with self._await_condition:
                self._await_condition.wait()

        self.image = pygame.Surface(gif.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(**pos)

    def _load_all_images(self, gif):
        image_queue = [True]
        save_condition = Condition()

        def save_images():
            for frame in range(gif.n_frames):
                gif.seek(frame)
                image = io.BytesIO()
                gif.save(image, format='GIF')
                image.seek(0)
                image_queue.append(image)
                with save_condition:
                    save_condition.notify()

            image_queue[0] = False

        def load_images():
            while image_queue[0]:
                with save_condition:
                    save_condition.wait(0.01)

                while len(image_queue) > 1:
                    with load_lock:
                        surface = pygame.image.load(image_queue.pop(1))

                    if len(self.images) == 0:
                        self.image = surface
                        self._last_img_time = time.time()
                    self.images.append(surface)

                    with self._await_condition:
                        self._await_condition.notify()

            self._loading = False
            gif.close()

        Thread(target=save_images).start()
        Thread(target=load_images).start()

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
            self._image_index = self._first_frame

        self.image = self.images[self._image_index]

    def run(self):
        self._running = True
        self._image_index = self._first_frame - 1

    def stop(self):
        self._running = False

    def end_and_stop(self):
        if not self._running or not self.on_end:
            return

        self.on_end()
        self.stop()
