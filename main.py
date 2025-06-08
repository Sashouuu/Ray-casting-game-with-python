import pygame as pg
import numpy as np
from movement import movement
from rendering import new_frame
from numba import njit  # accelerate numerical functions on both CPUs and GPUs using standard Python functions


def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))  # sets game screen size
    is_running = True  # if True game is running
    clock = pg.time.Clock()

    hres = 120  # horizontal resolution
    halfvres = 100  # vertical resolution / 2
    mod = hres / 60  # scaling factor (60 degrees fov)

    posx, posy, rot = 0, 0, 0
    frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))

    sky = pg.image.load("sky.jpg")
    sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, halfvres * 2)))
    ground = pg.surfarray.array3d(pg.image.load("floor.jpg"))

    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False  # if the close button is pressed the game stops

        new_frame(posx, posy, rot, frame, sky, ground, hres, halfvres, mod)

        # transforming frame into a surface so it can be displayed
        surf = pg.surfarray.make_surface(frame * 255)
        surf = pg.transform.scale(surf, (800, 600))
        fps = int(clock.get_fps())
        pg.display.set_caption(f"Pycasting maze - FPS:{fps}")

        screen.blit(surf, (0, 0))  # placing surface in the top left corner of game screen
        pg.display.update()

        posx, posy, rot = movement(posx, posy, rot, pg.key.get_pressed(), clock.tick())



if __name__ == "__main__":
    main()
    pg.quit()