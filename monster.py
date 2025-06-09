import numpy as np
import pygame as pg
import random


class Monster(pygame.sprite.Sprite):
    def __init__(self, size, maph):
        while True:
            x, y = random.randint(1, size - 2), random.randint(1, size - 2)
            if maph[x][y] == 0:
                self.x = x + 0.5
                self.y = y + 0.5
                break

    def move_towards(self, px, py, maph):
        dx, dy = px - self.x, py - self.y
        dist = np.hypot(dx, dy)
        if dist < 0.2:
            return True  # touching player

        dx, dy = dx / dist, dy / dist
        nx, ny = self.x + dx * 0.01, self.y + dy * 0.01

        if not maph[int(nx)][int(ny)]:
            self.x, self.y = nx, ny

        return False
