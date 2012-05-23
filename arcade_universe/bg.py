import numpy as np
from perlin import PerlinNoiseGenerator

class TextureType:
    Plain = "plain"
    Perlin = "perlin"
    Gaussian = "gaussian"
    HilbertCurve = "hilbert"
    PeanoCurve = "peano"

class Background(object):

    def __init__(self, texture=None, texture_type=TextureType.Plain):
        self.texture_type = texture_type
        if texture is not None:
            self.texture = texture
        else:
            self.texture = self.generate_texture()

    def get_texture(self):
        text = np.zeros((self.texture.shape[0], self.texture.shape[1]))

        if self.texture_type == TextureType.Plain:
            for i in xrange(self.texture.shape[0]):
                for j in xrange(self.texture.shape[1]):
                    text[i][j] = 0
        elif self.texture_type == TextureType.Perlin:
            perlin = PerlinNoiseGenerator(self.texture.shape[0],
                    self.texture.shape[1])
            text = perlin.get_background_noise()

