import numpy as np
from numba import njit


# accelerate numerical functions on both CPUs and GPUs using standard Python functions

@njit()
def new_frame(posx: float, posy: float, rot: float, frame, sky, ground, hres, halfvres, mod, mapa, size, wall, mapc):
    for i in range(hres):
        rot_i = rot + np.deg2rad(i / mod - 30)  # angle of each column
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i / mod - 30))  # cos2 -> fix fisheye effect
        # to fix fisheye effect we need to divide the distance "n" by the cosine of the difference
        # between the current column angle and the central angle
        frame[i][:] = sky[int(np.rad2deg(rot_i)) % 359][:] / 255  # sky texture

        x, y = posx, posy
        while mapa[int(x) % (size - 1)][int(y) % (size - 1)] == 0:
            x, y = x + 0.02 * cos, y + 0.02 * sin

        n = abs((x - posx) / cos)
        h = int(halfvres / (n * cos2 + 0.001))

        xx = int(x * 2 % 1 * 99)
        if x % 1 < 0.02 or x % 1 > 0.98:
            xx = int(y * 2 % 1 * 99)
        yy = np.linspace(0, 198, h * 2) % 99

        shade = 0.3 + 0.7 * (h / halfvres)
        if shade > 1:
            shade = 1
        c = shade * mapc[int(x) % (size - 1)][int(y) % (size - 1)]
        for k in range(h * 2):
            if halfvres - h + k >= 0 and halfvres - h + k < 2 * halfvres:
                frame[i][halfvres - h + k] = c * wall[xx][int(yy[k])]
                if halfvres + 3 * h - k < halfvres * 2:
                    frame[i][halfvres + 3 * h - k] = c * wall[xx][int(yy[k])]

        for j in range(halfvres - h):  # pass trhough all the pixels in bottom half of screen
            n = (halfvres / (halfvres - j)) / cos2  # distance from floor to player
            x, y = posx + cos * n, posy + sin * n  # calculating position of each pixel
            xx, yy = int(x * 2 % 1 * 99), int(y * 2 % 1 * 99)
            # calculate texture coordinates based on the non-integer part of X and Y coordinates

            shade = 0.2 + 0.8 * (1 - j / halfvres)

            frame[i][halfvres * 2 - j - 1] = (shade * ground[xx][yy] / 255 + frame[i][halfvres*2-j-1])/2

    return frame
