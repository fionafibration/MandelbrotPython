from math import*

def mandelbrot(x,y):
    for Px in range(x * 2):
        for Py in range(y * 2):
            x0 = Px * (3.5 / (x * 2)) - 2.5
            y0 = Py * (2 / (y * 2)) - 1
            x, y = 0.0, 0.0
            k = 0
            while x * x + y * y <= 4.0 and k < 1000:
                xtemp = x*x - y*y + x0
                y = 2 * x * y + y0
                x = xtemp
                k += 1
            if k < 1000:
                log_zn = log(x * x + y * y) / 2
                nu = log(log_zn / log(2)) / log(2)
                k = k + 1 - nu
            c1, c2 = floor(k), floor(k+1)


