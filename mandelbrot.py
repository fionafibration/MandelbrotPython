from math import *
from PIL import Image
from numpy import zeros, float32, uint8
from tqdm import *
from collections import *
from matplotlib import cm


def lerp(a, b, t):
    return a * (1 - t) + b * t


def _mandelbrot(xD_1, yD_1, x1, x2, y1, y2, maxiter, scale=2, colormap=None):
    xD = xD_1 * scale
    yD = yD_1 * scale

    x_scale = (x2 - x1) / xD
    y_scale = (y2 - y1) / yD

    histogram = defaultdict(lambda: 0)

    values = zeros((yD, xD), float32)

    pixels = zeros((yD, xD, 3), uint8)

    for xy in tqdm(range(yD * xD)):
        Py, Px = xy // xD, xy % xD
        x0 = Px * x_scale + x1
        y0 = Py * y_scale + y1

        zr = zi = tr = ti = k = 0

        while k <= maxiter and tr + ti < 15:
            zi = 2 * zr * zi + y0
            zr = tr - ti + x0
            tr = zr ** 2
            ti = zi ** 2
            k += 1

        adj = smooth(maxiter, k, tr, ti)

        values[Py, Px] = adj

        if adj < maxiter:
            histogram[floor(adj)] += 1

    total = sum(list(histogram.values()))

    hues = []
    accum = 0
    for i in range(maxiter):
        accum += histogram[i] / total
        hues.append(accum)
    hues.append(accum)

    for xy in tqdm(range(yD * xD)):
        Py, Px = xy // xD, xy % xD

        adj = values[Py, Px].item()
        interp = 1 - lerp(hues[floor(adj)], hues[ceil(adj)], adj % 1)

        pixels[Py, Px] = tuple(map(
            lambda x: floor(x * 255),
            [0, 0, 0] if adj >= maxiter else color(interp, colormap)
        ))

    img = Image.fromarray(pixels, 'RGB')
    img = img.resize((xD_1, yD_1), Image.LANCZOS)
    img.save('mandeltest.png')
    img.show()


def color(interp, map=None):
    if map is None:
        return [interp, 1, 1]
    else:
        return cm.get_cmap(map)(clamp(interp))[:3]


lb = 1 / log(2)
hlb = log(0.5) * lb


def clamp(x, min=0, max=1):
    if x > max:
        return max
    if x < min:
        return min
    return x


def smooth(maxiter, k, tr, ti):
    if tr + ti > 1.0:
        c = log(log(tr + ti))
    else:
        c = 0
    return clamp((5 + k - hlb - c * lb), 0, maxiter)
    # return (5 + k - hlb - log(log(tr + ti)) * lb) / maxiter


def easybrot(xd, maxiter, colormap='twilight'):
    yd = floor(xd * 2 / 3)
    return _mandelbrot(xd, yd, -2, 1, -1, 1, maxiter, 2, colormap)


# easybrot(300, 30)

easybrot(3000, 130)

# easybrot(1500, 1000, 100)
