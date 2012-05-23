import random
import colorsys

import numpy as np
from itertools import izip_longest

def get_radial_img_data(width, height):
    return get_data(width, height, gradient(RADIAL(0.5, 0.5), NO_NOISE,
        [(1.0, (0xDD, 0xDD, 0xDD), (0x10, 0x12, 0x13)),]))

def get_gradient_img_data(width, height):
    return get_data(width, height, gradient(LINEAR_Y, NO_NOISE,
        [(1.00, (0x00, 0x11, 0x33), (0x00, 0x55, 0x77)),]))

def get_data(width, height, rgb_func):
    def grouper(n, iterable, fillvalue=None):
        "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)

    img = get_pixel_intensities(width, height, rgb_func)
    img = np.array([sum(group) for group in (grouper(3, img, 0))])
    img *= (255/img.max())
    img = img.reshape(width, height)
    return img

def get_pixel_intensities(width, height, rgb_func):
    fw = float(width)
    fh = float(height)
    data = np.array([])

    for y in xrange(height):
        fy = float(y)
        for x in xrange(width):
            fx = float(x)
            data = np.concatenate((data, [min(255, max(0, int(v * 255))) for v in rgb_func(fx / fw, fy / fh)]))
    return data

def linear_gradient(start_value, stop_value, start_offset=0.0, stop_offset=1.0):
    return lambda offset: (start_value + ((offset - start_offset) / (stop_offset - start_offset) * (stop_value - start_value))) / 255.0

def LINEAR_Y(x, y):
    return y

def LINEAR_X(x, y):
    return x

def RADIAL(center_x, center_y):
    return lambda x, y: (x - center_x) ** 2 + (y - center_y) ** 2

def NO_NOISE(r, g, b):
    return r, g, b

def GAUSSIAN(sigma):
    def add_noise(r, g, b):
        d = random.gauss(0, sigma)
        return r + d, g + d, b + d
    return add_noise

def HSV(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return 255 * r, 255 * g, 255 * b

def hexstring_to_rgb(s):
    r = int(s[1:3], 16)
    g = int(s[3:5], 16)
    b = int(s[5:7], 16)
    return r, g, b

def gradient(value_func, noise_func, DATA):
    def gradient_function(x, y):
        initial_offset = 0.0
        v = value_func(x, y)
        for offset, start, end in DATA:
            if isinstance(start, str) and start.startswith("#"):
                start = hexstring_to_rgb(start)
            if isinstance(end, str) and end.startswith("#"):
                end = hexstring_to_rgb(end)
            if v < offset:
                r = linear_gradient(start[0], end[0], initial_offset, offset)(v)
                g = linear_gradient(start[1], end[1], initial_offset, offset)(v)
                b = linear_gradient(start[2], end[2], initial_offset, offset)(v)
                return noise_func(r, g, b)
            initial_offset = offset
        return noise_func(end[0] / 255.0, end[1] / 255.0, end[2] / 255.0)
    return gradient_function
