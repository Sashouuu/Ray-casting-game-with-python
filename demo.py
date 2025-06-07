import pygame as pg
import numpy as np


def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))  # sets game screen size
    is_running = True  # if True game is running
    clock = pg.time.Clock()

    hres = 120  # horizontal resolution
    halfvres = 100  # vetcial resolution / 2
    mod = hres / 60  # scaling factor (60 fov)

    posx, posy, rot = 0, 0, 0
    frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))

    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False  # if the close button is pressed the game stops

        for i in range(hres):
            rot_i = rot + np.deg2rad(i / mod - 30)
            sin, cos = np.sin(rot_i), np.cos(rot_i)

            for j in range(halfvres):
                n = halfvres / (halfvres - j)  # distance from floor to player
                x, y = posx + cos * n, posy + sin * n  # calculating position of each pixel

                if int(x) % 2 == int(y) % 2:
                    frame[i][halfvres * 2 - j - 1] = [0, 0, 0]
                else:
                    frame[i][halfvres * 2 - j - 1] = [1, 1, 1]

        # transforming frame into a surface so it can be displayed
        surf = pg.surfarray.make_surface(frame * 255)
        surf = pg.transform.scale(surf, (800, 600))

        screen.blit(surf, (0, 0))  # placing surface in the top left corner of game screen
        pg.display.update()

        posx, posy, rot = movement(posx, posy, rot, pg.key.get_pressed())


def movement(posx, posy, rot, keys):
    if keys[pg.K_LEFT] or keys[ord("a")]:
        rot -= 0.1

    if keys[pg.K_RIGHT] or keys[ord("d")]:
        rot += 0.1

    if keys[pg.K_UP] or keys[ord("w")]:
        posx, posy = posx + np.cos(rot) * 0.1, posy + np.sin(rot) * 0.1

    if keys[pg.K_DOWN] or keys[ord("s")]:
        posx, posy = posx - np.cos(rot) * 0.1, posy - np.sin(rot) * 0.1

    return posx, posy, rot


if __name__ == "__main__":
    main()
    pg.quit()
