import numpy as np
from numba import njit


@njit()
def new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod, maph, size, wall, mapc, exitx, exity):
    for i in range(hres):
        rot_i = rot + np.deg2rad(i / mod - 30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i / mod - 30))
        frame[i][:] = sky[int(np.rad2deg(rot_i) % 359)][:]

        x, y = posx, posy
        while maph[int(x) % (size - 1)][int(y) % (size - 1)] == 0:
            x, y = x + 0.01 * cos, y + 0.01 * sin

        n = abs((x - posx) / cos)
        h = int(halfvres / (n * cos2 + 0.001))

        xx = int(x * 3 % 1 * 99)
        if x % 1 < 0.02 or x % 1 > 0.98:
            xx = int(y * 3 % 1 * 99)
        yy = np.linspace(0, 3, h * 2) * 99 % 99

        shade = 0.3 + 0.7 * (h / halfvres)
        if shade > 1:
            shade = 1

        ash = 0
        if maph[int(x - 0.33) % (size - 1)][int(y - 0.33) % (size - 1)]:
            ash = 1

        if maph[int(x - 0.01) % (size - 1)][int(y - 0.01) % (size - 1)]:
            shade, ash = shade * 0.5, 0

        c = shade * mapc[int(x) % (size - 1)][int(y) % (size - 1)]
        for k in range(h * 2):
            if halfvres - h + k >= 0 and halfvres - h + k < 2 * halfvres:
                if ash and 1 - k / (2 * h) < 1 - xx / 99:
                    c, ash = 0.5 * c, 0
                frame[i][halfvres - h + k] = c * wall[xx][int(yy[k])]
                if halfvres + 3 * h - k < halfvres * 2:
                    frame[i][halfvres + 3 * h - k] = c * wall[xx][int(yy[k])]

        for j in range(halfvres - h):
            n = (halfvres / (halfvres - j)) / cos2
            x, y = posx + cos * n, posy + sin * n
            xx, yy = int(x * 2 % 1 * 99), int(y * 2 % 1 * 99)

            shade = 0.2 + 0.8 * (1 - j / halfvres)
            if maph[int(x - 0.33) % (size - 1)][int(y - 0.33) % (size - 1)]:
                shade = shade * 0.5
            elif ((maph[int(x - 0.33) % (size - 1)][int(y) % (size - 1)] and y % 1 > x % 1) or
                  (maph[int(x) % (size - 1)][int(y - 0.33) % (size - 1)] and x % 1 > y % 1)):
                shade = shade * 0.5

            frame[i][halfvres * 2 - j - 1] = shade * (floor[xx][yy] + frame[i][halfvres * 2 - j - 1]) / 2
            if int(x) == exitx and int(y) == exity and (x % 1 - 0.5) ** 2 + (y % 1 - 0.5) ** 2 < 0.2:
                ee = j / (10 * halfvres)
                frame[i][j:2 * halfvres - j] = (ee * np.ones(3) + frame[i][j:2 * halfvres - j]) / (1 + ee)

    return frame
