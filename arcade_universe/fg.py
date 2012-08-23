import numpy as np
from gradient_textures import get_radial_img_data
from gradient_textures import get_gradient_img_data

class FGTextureType:
    PlainBin = "plainbin"
    PlainGray = "plaingray"
    GradientRadial = "gradientradial"
    GradientLinear = "gradientlinear"

class Foreground(object):

    def __init__(self,
            patch=None,
            texture=None,
            size=(0, 0),
            texture_type=FGTextureType.PlainBin,
            corruptor = None):

        self.size = size
        self.texture_type = texture_type
        self.corruptor = corruptor
        if texture is not None:
            self.texture = texture
        else:
            self.texture = self.generate_texture()

    def generate_texture(self):
        text = np.zeros((self.size[0], self.size[1]))
        if self.texture_type == FGTextureType.PlainBin:
            for i in xrange(self.size[0]):
                for j in xrange(self.size[1]):
                    text[i][j] = 1
        elif self.texture_type == FGTextureType.PlainGray:
            for i in xrange(self.size[0]):
                for j in xrange(self.size[1]):
                    text[i][j] = 255
        elif self.texture_type == FGTextureType.GradientRadial:
            text = get_radial_img_data(self.size[0], self.size[1])
        elif self.texture_type == FGTextureType.GradientLinear:
            text = get_gradient_img_data(self.size[0], self.size[1])
        if self.corruptor is not None:
            text = self.corruptor(text)
        return text
