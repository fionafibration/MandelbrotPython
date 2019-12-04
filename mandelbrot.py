from math import *
from PIL import Image
from numpy import zeros, float32, uint8
from tqdm import *
from collections import *
from matplotlib import cm
from numba import jit
import numpy as np


def map_color(interp, map=None):
    if map is None:
        # Return an HSV mapping
        return [interp, 1, 1]
    else:
        # Perceptually uniform color mappings
        return cm.get_cmap(map)(clamp(interp))[:3]


def linear_interpolate(a, b, t):
    return a * (1 - t) + b * t


def iterate_complex(x0, y0, max_iter, divergence=15):
    z_real = z_imag = t_real = t_imag = k = 0

    #max_magnitude = -1

    # Find point of divergence and return diverged point + L2 norm of point
    while k <= max_iter and t_real + t_imag < divergence:
        z_imag = 2 * z_real * z_imag + y0

        z_real = t_real - t_imag + x0

        t_real = z_real ** 2

        t_imag = z_imag ** 2

        k += 1

        """
        # Used for orbit trap rendering
        if np.hypot(t_real, t_imag) > max_magnitude:
            max_magnitude = np.hypot(t_real, t_imag)
        """

    return k, t_real, t_imag, hypot(t_real, t_imag), #max_magnitude


# Clamp function, by default on the range [0, 1]
def clamp(x, min=0, max=1):
    if x > max:
        return max
    if x < min:
        return min
    return x


LOG_2_BASE = 1 / log(2)
HALF_LOG_2_BASE = log(0.5) * LOG_2_BASE


def logarithmic_smooth(max_iter, k, tr, ti):
    if tr + ti > 1.0:
        c = log(log(tr + ti))
    else:
        c = 0

    # Domain issues
    # return (5 + k - hlb - log(log(tr + ti)) * lb) / max_iter

    # Correct
    return clamp((5 + k - HALF_LOG_2_BASE - c * LOG_2_BASE), 0, max_iter)


def render(xD, yD, x0, x1, y0, y1, max_iter, sample_scale=2, colormap=None):
    xD_2 = xD * sample_scale
    yD_2 = yD * sample_scale

    x_scale = (x1 - x0) / xD_2
    y_scale = (y1 - y0) / yD_2

    histogram = defaultdict(lambda: 0)

    values = zeros((yD_2, xD_2), float32)

    pixels = zeros((yD_2, xD_2, 3), uint8)

    for xy in tqdm(range(yD_2 * xD_2)):
        Py, Px = xy // xD_2, xy % xD_2
        x0 = Px * x_scale + x0
        y0 = Py * y_scale + y0

        k, tr, ti, magnitude, *rest = iterate_complex(x0, y0, max_iter)

        # Smoothing and histogram for normalization
        adj = logarithmic_smooth(max_iter, k, tr, ti)

        values[Py, Px] = adj

        if adj < max_iter:
            histogram[floor(adj)] += 1

    total = sum(list(histogram.values()))

    hues = []
    accum = 0
    for i in range(max_iter):
        accum += histogram[i] / total
        hues.append(accum)
    hues.append(accum)

    for xy in tqdm(range(yD_2 * xD_2)):
        Py, Px = xy // xD_2, xy % xD_2

        adj = values[Py, Px].item()
        interp = 1 - linear_interpolate(hues[floor(adj)], hues[ceil(adj)], adj % 1)

        pixels[Py, Px] = tuple(map(
            lambda x: floor(x * 255),
            [0, 0, 0] if adj >= max_iter else map_color(interp, colormap)
        ))

    img = Image.fromarray(pixels, 'RGB')

    # Lanczos interpolation for rezise

    img = img.resize((xD, yD), Image.LANCZOS)

    img.save('test_out.png')

    img.show()


def test_render(x_dimen, max_iter, colormap='twilight'):
    yd = floor(x_dimen * 2 / 3)
    return render(x_dimen, yd, -2, 1, -1, 1, max_iter, 2, colormap)


# test_render(300, 30)

test_render(3000, 130)

# test_render(1500, 70)
