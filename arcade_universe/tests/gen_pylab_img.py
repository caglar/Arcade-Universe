#!/usr/bin/env python

from web_graphics import gradient, RADIAL, NO_NOISE, get_pixel_intensities

from itertools import izip_longest
import numpy as np

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

width = 100
height = 100

img = get_pixel_intensities(width, height, gradient(RADIAL(0.5, 0.5), NO_NOISE,
    [(1.0, (0xDD, 0xDD, 0xDD), (0x10, 0x12, 0x13)),]))

img = np.array([sum(group) for group in (grouper(3, img, 0))])
img *= (255/img.max())

import pylab

img_ = img.reshape(width, height)
pylab.axis('off')
pylab.gray()
pylab.imshow(img_)
pylab.show()
