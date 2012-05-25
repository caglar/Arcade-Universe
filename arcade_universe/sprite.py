import numpy

class Sprite(object):

    """
    A Sprite is a sort of arcade game sprite saved in the bugs_db database.
    Creates a Sprite with the specified name and whose pixel
    representation is given by ``patch`` (a 2D array where 0 is the
    background and 1 is a pixel of the bug). The ``mask`` of the Sprite
    is the space that "belongs" to it (so two bugs are said to overlap
    if their masks overlap). The mask defaults to the same thing as
    the patch if it is not given.
    """

    def __init__(self, name, patch, texture=None, mask=None, center_loc=(0, 0)):
        self.name = name
        self.patch = numpy.array(patch)
        self.textured_patch = patch
        if texture is None:
            self.has_textured_patch = False
            self.texture = None
        else:
            self.has_textured_patch = True
            self.texture = texture
            self.textured_patch = numpy.zeros(patch.shape)
            self.set_texture()
        if mask is None:
            self.mask = self.patch
        else:
            self.mask = numpy.array(mask)
        self.center_loc = center_loc
        self.center_of_mass = self.get_center_of_mass()

    def set_texture(self, texture=None):
        if texture is None:
            texture = self.texture 
        else:
            self.texture = texture
        for i in xrange(self.patch.shape[0]):
            for j in xrange(self.patch.shape[1]):
                if self.patch[i][j] == 1:
                    self.textured_patch[i][j] = texture[i][j]

    def get_center_of_mass(self):
        pixel_coords = []
        for i in xrange(self.patch.shape[0]):
            for j in xrange(self.patch.shape[1]):
                if self.patch[i][j] == 1:
                    pixel_coords.append([i, j])
        return numpy.mean(pixel_coords, axis=0)

    def rotate(self, angle):
        """
        Rotate the Sprite by the specified angle, in degrees. Only
        orthogonal rotations (multiples of 90 degrees) are supported,
        so one may choose between 0, 90, 180 and 270.
        """
        angle %= 360
        if angle not in (0, 90, 180, 270):
            raise ValueError('angle must be one of: 0, 90, 180, 270')
        if angle == 0:
            return self
        if angle == 90:
            return Sprite(self.name,
                       patch=self.patch.T,
                       texture=self.texture,
                       mask=self.mask.T,
                       center_loc=self.center_loc).hflip()

        if angle >= 180:
            return self.hflip().vflip().rotate(angle-180)

    def hflip(self):
        """
        Returns a Sprite that's flipped horizontally relative to this one
        (symmetry around the y axis).
        """
        return Sprite(self.name,
                   self.patch[:, ::-1],
                   texture=self.texture,
                   mask=self.mask[:, ::-1],
                   center_loc=self.center_loc)

    def vflip(self):
        """
        Returns a Sprite that's flipped vertically relative to this one
        (symmetry around the x axis).
        """
        return Sprite(self.name,
                   self.patch[::-1],
                   texture=self.texture,
                   mask=self.mask[::-1],
                   center_loc=self.center_loc)

    def scale(self, xscale, yscale = None):
        """
        Returns a new Sprite scaled as specified. xscale and yscale must
        be integers. Each pixel of the original bug will be mapped to
        a xscale by yscale block of pixels.
        """
        if yscale is None: yscale = xscale
        if not isinstance(xscale, int) or not isinstance(yscale, int):
            raise TypeError("xscale and yscale must be integers.")
        prows, pcols = self.patch.shape
        mrows, mcols = self.mask.shape
        patch = numpy.zeros((prows*yscale, pcols*xscale))
        mask = numpy.zeros((mrows*yscale, mcols*xscale))
        for i in xrange(yscale):
            for j in xrange(xscale):
                patch[i:prows*yscale:yscale, j:pcols*xscale:xscale] = self.patch
                mask[i:mrows*yscale:yscale, j:mcols*xscale:xscale] = self.mask

        return Sprite(self.name, patch, texture=self.texture, mask=mask, center_loc=self.center_loc)

    def margin(self, margin):
        """
        Creates a Sprite whose mask is the patch enlarged by margin
        pixels all around.
        """
        mr, mc = self.patch.shape[0]+margin*2, self.patch.shape[1]+margin*2
        mask = numpy.zeros((mr, mc), dtype = 'int')
        m = margin*2 + 1
        for i in xrange(m):
            for j in xrange(m):
                mask[i:mr-m+1+i, j:mc-m+1+j] |= self.patch
        b = Sprite(self.name,
                self.patch,
                texture = self.texture,
                mask=mask,
                center_loc=self.center_loc)
        return b

    def total_mask(self):
        """
        Creates a Sprite whose mask is the whole rectangle.
        """
        return Sprite(self.name,
                   self.patch,
                   texture=self.texture,
                   mask=numpy.ones(self.mask.shape),
                   center_loc=self.center_loc)

    def fit_mask(self):
        """
        Returns a Sprite whose mask is this Sprite's patch.
        """
        return Sprite(self.name,
                   self.patch,
                   texture=self.texture,
                   mask=self.patch,
                   center_loc=self.center_loc)

    def __str__(self):
        return self.name + '\n' + '\n'.join(' '.join('x' if x else ' ' for x in row) for row in self.patch)

    h = property(lambda self: self.patch.shape[0], doc = "Property that returns the bug's height.")
    w = property(lambda self: self.patch.shape[1], doc = "Property that returns the bug's width.")

    mh = property(lambda self: self.mask.shape[0], doc = "Property that returns the bug's mask's height.")
    mw = property(lambda self: self.mask.shape[1], doc = "Property that returns the bug's mask's height.")

    marginh = property(lambda self: (self.mh-self.h)/2, doc = "Property that returns the difference between the bug's height and the bug's mask's height.")
    marginw = property(lambda self: (self.mw-self.w)/2, doc = "Property that returns the difference between the bug's width and the bug's mask's width.")
