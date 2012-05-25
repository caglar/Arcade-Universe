import numpy as np
from perlin import PerlinNoiseGenerator
from hilbert import HilbertCurves

class BGTextureType:
    Plain = "plain"
    Perlin = "perlin"
    Gaussian = "gaussian"
    HilbertCurve = "hilbert"
    PeanoCurve = "peano"

class Background(object):

    def __init__(self, texture=None, size = (0, 0),
            texture_type=BGTextureType.Plain,
            corruptor=None, hilbert_level=4):
        self.size = size
        self.texture_type = texture_type
        self.corruptor = corruptor
        self.hilbert_level = hilbert_level
        if texture is not None:
            self.texture = texture
        else:
            self.texture = self.generate_texture()

    def generate_texture(self):
        text = np.zeros((self.size[0], self.size[1]))
        if self.texture_type == BGTextureType.Plain:
            for i in xrange(self.size[0]):
                for j in xrange(self.size[1]):
                    text[i][j] = 0
        elif self.texture_type == BGTextureType.Perlin:
            perlin = PerlinNoiseGenerator(self.texture.shape[0],
                    self.texture.shape[1])
            text = perlin.get_background_noise()
        elif self.texture_type == BGTextureType.HilbertCurve:
            hcurves = HilbertCurves(self.size[0], self.size[1],
                    self.hilbert_level)
            self.texture = hcurves.gen_hilbert_curve()
        if self.corruptor is not None:
            text = self.corruptor(text)
        return text
