import pygame as pg
import numpy as np

from new_frame import new_frame
from movement import movement
from gen_map import gen_map
from menu import main_menu
from monster import Monster
from health_bar import draw_health_bar

def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    running = True
    clock = pg.time.Clock()
    pg.mouse.set_visible(False)

    hres = 200  # horizontal resolution
    halfvres = 150  # vertical resolution/2

    mod = hres / 60  # scaling factor (60° fov)

    size = 25
    posx, posy, rot, maph, mapc, exitx, exity = gen_map(size)
    health = 100
    monster_list = [Monster(size, maph) for _ in range(5)]
    frame = np.random.uniform(0, 1, (hres, halfvres * 2, 3))
    sky = pg.image.load('sky.jpg')
    sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, halfvres * 2))) / 255
    floor = pg.surfarray.array3d(pg.image.load('floor.jpg')) / 255
    wall = pg.surfarray.array3d(pg.image.load('floor.jpg')) / 255
    pg.event.set_grab(1)

    while running:
        if int(posx) == exitx and int(posy) == exity:
            print("Gongratulations! You got out of the maze!")
            running = False
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False

        frame = new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod, maph, size,
                          wall, mapc, exitx, exity)

        surf = pg.surfarray.make_surface(frame * 255)
        surf = pg.transform.scale(surf, (800, 600))
        fps = int(clock.get_fps())
        pg.display.set_caption("Pycasting maze - FPS: " + str(fps))

        screen.blit(surf, (0, 0))
        draw_health_bar(screen, health)
        pg.display.update()

        posx, posy, rot = movement(posx, posy, rot, maph, clock.tick() / 500)

        # Monster logic
        for monster in monster_list:
            if monster.move_towards(posx, posy, maph):
                health -= 0.1  # Damage per frame
                if health <= 0:
                    print("You died!")
                    running = False


if __name__ == "__main__":
    if main_menu():
        main()
