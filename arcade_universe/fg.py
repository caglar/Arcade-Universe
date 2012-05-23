import numpy as np

class TextureType:
    Plain = "plain"
    Gradient = "gradient"
    GradientWNoise = "gradientwnoise"

class Foreground(object):

    def __init__(self, texture=None, texture_type=TextureType.Plain, size=(0,0)):
        pass

    def get_texture(self):
        pass
