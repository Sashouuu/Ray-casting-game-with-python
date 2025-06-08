import numpy as np
from numba import njit
# accelerate numerical functions on both CPUs and GPUs using standard Python functions

@njit()
def new_frame(posx: float, posy: float, rot: float, frame, sky, ground, hres, halfvres, mod):
    for i in range(hres):
        rot_i = rot + np.deg2rad(i / mod - 30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i / mod - 30))  # cos2 -> fix fisheye effect
        # to fix fisheye effect we need to divide the distance "n" by the cosine of the difference
        # between the current column angle and the central angle

        frame[i][:] = sky[int(np.rad2deg(rot_i)) % 359][:] / 255

        for j in range(halfvres):
            n = (halfvres / (halfvres - j)) / cos2  # distance from floor to player
            x, y = posx + cos * n, posy + sin * n  # calculating position of each pixel
            xx, yy = int(x * 2 % 1 * 100), int(y * 2 % 1 * 33)
            # calculate texture coordinates based on the non-integer part of X and Y coordinates

            shade = 0.2 + 0.8 * (1 - j / halfvres)

            frame[i][halfvres * 2 - j - 1] = shade * ground[xx][yy] / 255
    return frame