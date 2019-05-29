from math import*
from colorsys import*
from sys import*
from struct import*
from collections import *
def mandelbrot(xd,yd,o):
    xd *= 2
    yd *= 2
    pixels = {}
    pix2 = []
    histo = defaultdict(lambda:0)
    for Py in range(yd):
        for Px in range(xd):
            x0 = (Px / xd) * 3.0 - 2.0
            y0 = (Py / yd) * 2.0 - 1.0
            x, y = 0.0, 0.0
            k = 0
            while x * x + y * y <= 4.0 and k < o:
                xtemp = x*x - y*y + x0
                y = 2 * x * y + y0
                x = xtemp
                k += 1
            if k < o:
                zn = log(x * x + y * y) / 2
                nu = log(zn / log(2)) / log(2)
                k += 1 - nu
                histo[floor(k)] += 1
            pixels[(Px, Py)] = float(k)

    t = sum(histo.values())
    h = 0
    hues = []
    for i in range(o):
        h += histo[i] / t
        hues.append(h)
    hues.append(h)

    for Py in range(yd):
        for Px in range(xd):
            k = pixels[(Px, Py)]
            h = max(1 - (hues[floor(k)] * (1 - (k % 1)) + hues[ceil(k)] * (k % 1)), 0.0)

            pix2.append(col(h, 1.0, 1.0 if k < o else 0))
    targa(pix2, xd, yd)



# HSV to RGB.
def col(h,s,v):
    i=int(h*6)
    f,p=h*6-i,v*(1-s)
    q,t=v*(1-s*f),v*(1-s*(1-f))
    l=[(v,t,p),(q,v,p),(p,v,t),(p,v,q),(t,p,v),(v,p,q)][i%6]
    return list(floor(x * 255) for x in l)


def targa(pixels, w, h):
    f=open('out.tga', 'wb')
    header = b"\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00" + pack("<BBBB", 255 & w, 255 & (w >> 8), 255 & h, 255 & (h >> 8)) + b"\x18\x00"
    f.write(header)
    for pixel in pixels:
        f.write(pack("<BBB", *pixel))


mandelbrot(3000, 2000, 60)
