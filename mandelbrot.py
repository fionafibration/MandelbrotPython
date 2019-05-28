from math import*
from colorsys import*
from sys import*
from struct import*
def mandelbrot(xd,yd):
    for Px in range(xd * 2):
        for Py in range(yd * 2):
            x0 = Px * (3.5 / (xd * 2)) - 2.5
            y0 = Py * (2 / (yd * 2)) - 1
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


# HSV to RGB.
def col(h,s,v):
    i=int(h*6)
    f,p=h*6-i,v*(1-s)
    q,t=v*(1-s*f),v*(1-s*(1-f))
    return [(v,t,p),(q,v,p),(p,v,t),(p,v,q),(t,p,v),(v,p,q)][i%6]


def targa(pixels, w, h):
    stdout.write("\x00" + )


"""
Targa in C


#include <stdio.h>
#include <string.h>

enum { width = 550, height = 400 };

int main(void) {
  static unsigned char pixels[width * height * 3];
  static unsigned char tga[18];
  unsigned char *p;
  size_t x, y;

  p = pixels;
  for (y = 0; y < height; y++) {
    for (x = 0; x < width; x++) {
      *p++ = 255 * ((float)y / height);
      *p++ = 255 * ((float)x / width);
      *p++ = 255 * ((float)y / height);
    }
  }
  tga[2] = 2;
  tga[12] = 255 & width;
  tga[13] = 255 & (width >> 8);
  tga[14] = 255 & height;
  tga[15] = 255 & (height >> 8);
  tga[16] = 24;
  tga[17] = 32;
  return !((1 == fwrite(tga, sizeof(tga), 1, stdout)) &&
           (1 == fwrite(pixels, sizeof(pixels), 1, stdout)));
}"""