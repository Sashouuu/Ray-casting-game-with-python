import numpy as np
import pygame as pg


def movement(posx: float, posy: float, rot: float, keys, clock):
    if keys[pg.K_LEFT] or keys[pg.K_a]:
        rot -= 0.003 * clock

    if keys[pg.K_RIGHT] or keys[pg.K_d]:
        rot += 0.003 * clock

    if keys[pg.K_UP] or keys[pg.K_w]:
        posx, posy = posx + np.cos(rot) * 0.003 * clock, posy + np.sin(rot) * 0.003 * clock

    if keys[pg.K_DOWN] or keys[pg.K_s]:
        posx, posy = posx - np.cos(rot) * 0.003 * clock, posy - np.sin(rot) * 0.003 * clock

    return posx, posy, rot
