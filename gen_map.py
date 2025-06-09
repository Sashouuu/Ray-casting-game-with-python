import numpy as np


def gen_map(size):
    mapc = np.random.uniform(0, 1, (size, size, 3))
    maph = np.random.choice([0, 0, 0, 0, 1, 1], (size, size))
    maph[0, :], maph[size - 1, :], maph[:, 0], maph[:, size - 1] = (1, 1, 1, 1)

    posx, posy, rot = 1.5, np.random.randint(1, size - 1) + .5, np.pi / 4
    x, y = int(posx), int(posy)
    maph[x][y] = 0
    count = 0
    while True:
        testx, testy = (x, y)
        if np.random.uniform() > 0.5:
            testx = testx + np.random.choice([-1, 1])
        else:
            testy = testy + np.random.choice([-1, 1])
        if testx > 0 and testx < size - 1 and testy > 0 and testy < size - 1:
            if maph[testx][testy] == 0 or count > 5:
                count = 0
                x, y = (testx, testy)
                maph[x][y] = 0
                if x == size - 2:
                    exitx, exity = (x, y)
                    break
            else:
                count = count + 1
    return posx, posy, rot, maph, mapc, exitx, exity
