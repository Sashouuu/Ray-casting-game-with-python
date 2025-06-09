import pygame as pg
import numpy as np

def movement(posx, posy, rot, maph, et):
    pressed_keys = pg.key.get_pressed()
    x, y, diag = posx, posy, rot
    p_mouse = pg.mouse.get_rel()
    rot = rot + np.clip((p_mouse[0]) / 200, -0.2, .2)

    if pressed_keys[pg.K_UP] or pressed_keys[ord('w')]:
        x, y, diag = x + et * np.cos(rot), y + et * np.sin(rot), 1

    elif pressed_keys[pg.K_DOWN] or pressed_keys[ord('s')]:
        x, y, diag = x - et * np.cos(rot), y - et * np.sin(rot), 1

    if pressed_keys[pg.K_LEFT] or pressed_keys[ord('a')]:
        et = et / (diag + 1)
        x, y = x + et * np.sin(rot), y - et * np.cos(rot)

    elif pressed_keys[pg.K_RIGHT] or pressed_keys[ord('d')]:
        et = et / (diag + 1)
        x, y = x - et * np.sin(rot), y + et * np.cos(rot)

    if not (maph[int(x - 0.2)][int(y)] or maph[int(x + 0.2)][int(y)] or
            maph[int(x)][int(y - 0.2)] or maph[int(x)][int(y + 0.2)]):
        posx, posy = x, y

    elif not (maph[int(posx - 0.2)][int(y)] or maph[int(posx + 0.2)][int(y)] or
              maph[int(posx)][int(y - 0.2)] or maph[int(posx)][int(y + 0.2)]):
        posy = y

    elif not (maph[int(x - 0.2)][int(posy)] or maph[int(x + 0.2)][int(posy)] or
              maph[int(x)][int(posy - 0.2)] or maph[int(x)][int(posy + 0.2)]):
        posx = x

    return posx, posy, rot