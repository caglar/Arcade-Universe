import numpy
from sprites import sprites_db


class Identify(object):
    """
    Scene generator.

    **Example:**

    .. code-block:: python

       gen = Identify(spritenames = "tetrist/tetrisl/tetrisj", seed = 932, w = 10, h = 10)
       # gen.nout = 1
       # gen.nclasses = [3]
       for ((x, y), sprite), target in gen:
           # target = [-1] -> None
           # target = [0] -> tetrist
           # target = [1] -> tetrisl
           # target = [2] -> tetrisj
           # 0 <= x < w, 0 <= y < h, sprite is a sprite object
           # the sprite's name corresponds to the target
           ...

    Each scene contains one sprite chosen from the list of ``spritenames``.
    ``spritenames`` must be a list of sprite names separated by "/", and the
    sprites described by these names must be found in
    ``spriteland.sprites_db``.  The sprite's location is picked randomly in the
    scene.

    The target is a vector containing one integer representing the id
    of the sprite in the scene. The id is the position of the sprite's name
    in the slash-separated spritenames.

    ``w`` and ``h`` are the width and the height of the scene,
    respectively.
    """
    def __init__(self, spritenames, seed, w, h):

        self.spritenames = map(str.upper, spritenames.split('/'))
        self.sprites = map(sprites_db.__getitem__, spritenames)

        self.out_format = 'array'
        self.out_dtype = 'uint8'
        self.nout = 1
        self.nclasses = [len(self.sprites)]

        self.w = w
        self.h = h

    def __iter__(self):
        sprites = self.sprites
        R = numpy.random.RandomState(self.seed)
        ri = R.random_integers
        while True:
            index = ri(0, len(sprites) - 1)
            sprite = sprites[index]
            yield [[(ri(0, self.w - sprite.w),
                     ri(0, self.h - sprite.h)), sprite]], numpy.array([index], dtype = self.out_dtype)

class TwoGroups(object):
    """
    Scene generator.

    **Example:**

    ..code-block:: python

       gen = TwoGroups(spritenames = "tetrist/tetrisl/tetrisj", seed = 666, w = 10, h = 10,
                       n1 = 1, n2 = 2, rot = False, task = 1)
       # task = 1 means that:
       #  gen.nout = 1
       #  gen.nclasses = [3]
       for scene, target in gen:
           # target = [0] -> tetrist
           # target = [1] -> tetrisl
           # target = [2] -> tetrisj
           # scene_n = (x_n, y_n), sprite_n
           # 0 <= x_n < w, 0 <= y_n < h, sprite_n is a sprite object
           # first n1 sprites correspond to the target
           # others correspond to one of the two other possible sprites
           # NOTE: This is for **task 1**. targets work differently for tasks 2 and 3
           ...

    **Defaults:** ``n1 = 1, n2 = 2, rot = False, task = 1``

    Each scene contains ``n1`` sprites of one type and ``n2`` sprites from
    another type, both chosen randomly from a list of sprites defined by
    ``spritenames``. ``spritenames`` must be a list of sprite names separated
    by "/", and the sprites described by these names must be found in
    ``spriteland.sprites_db``. ``n1`` must be different from ``n2``. If
    ``rot`` is True, the sprites may be randomly rotated.
    If ``scale`` is True, the sprites can be randomly scaled.
    The target depends on the value of the task parameter:

    ``task = 1`` -> The target is a vector containing one integer
    representing the id of the sprite of which there are ``n1`` of in the
    scene. The id is the position of the sprite's name in the
    slash-separated spritenames. *This is the default*.

    ``task = 2`` -> Same as task 1, but the id is the one of the sprite
    of which there are ``n2`` of.

    ``task = 3`` -> The target is a vector containing two integers,
    respectively the id of the shape there are ``n1`` occurrences of
    and the id of the shape there are ``n2`` occurrences of.

    The object's ``nout`` field contains the length of the target
    vector and the object's ``nclasses`` field contains a vector of
    length ``nout`` where each element is the number of possible sprites.

    The ``seed`` controls the random number generation, so different
    seeds lead to different scenes.

    ``w`` and ``h`` are the width and the height of the scene,
    respectively.
    """
    def __init__(self, spritenames, seed, w, h, n1 = 1, n2 = 2, rot = False,
             scale = False, texture=None, use_patch_centers=False, patch_size=(8, 8), task = 1):

        if n1 == n2:
            raise ValueError('n1 must be different from n2', n1, n2)

        self.use_patch_centers = use_patch_centers

        self.spritenames = map(str.upper, spritenames.split('/'))
        sprites = map(sprites_db.__getitem__, self.spritenames)
        if len(sprites) < 2:
            raise ValueError("There must be at least two possible sprites.")
        self.sprites = [sprite.margin(1) for sprite in sprites]

        if texture is not None:
            for i in xrange(len(sprites)):
                self.sprites[i].set_texture(texture)

        self.seed = seed
        self.n1 = n1
        self.n2 = n2
        self.rot = rot
        self.scale = scale
        self.task = task

        self.out_format = 'array'
        self.out_dtype = 'uint8'

        if task == 1 or task == 2:
            self.nout = 1
            self.nclasses = [len(self.sprites)]
        elif task == 3:
            self.nout = 2
            self.nclasses = [len(self.sprites)] * 2
        else:
            raise ValueError("task must be 1, 2 or 3")

        self.patch_objects = numpy.zeros((w/patch_size[0], h/patch_size[1]))
        self.patch_objects.fill(-1) # -1 is for No Object - Only background pixels

        #The number of rows and cols for the patches
        self.nrows_patches = h / patch_size[0]
        self.ncols_patches = w / patch_size[1]

        if use_patch_centers:
            self.patch_centers = self.gen_patch_centers(patch_size)

        self.w = w
        self.h = h

    def gen_patch_centers(self, patch_size=(8,8)):
        first_center = (patch_size[0]/2, patch_size[1]/2)
        patch_centers = []

        for i in xrange(self.nrows_patches):
            for j in xrange(self.ncols_patches):
                patch_centers.append((i * patch_size[0] + first_center[0],
                    j * patch_size[1] + first_center[1]))
        return numpy.array(patch_centers)

    def __iter__(self):

        R = numpy.random.RandomState(self.seed)
        ri = R.random_integers
        while True:

            index1 = ri(0, len(self.sprites)-1)
            index2 = ri(0, len(self.sprites)-1)

            while index1 == index2:
                index2 = ri(0, len(self.sprites)-1)

            sprites1 = [self.sprites[index1]] * self.n1
            sprites2 = [self.sprites[index2]] * self.n2

            if self.rot:
                sprites1 = [sprite.rotate(ri(0, 3) * 90) for sprite in sprites1]
                sprites2 = [sprite.rotate(ri(0, 3) * 90) for sprite in sprites2]

            if self.scale:
                sprites1 = [sprite.scale(ri(1, 2)) for sprite in sprites1]
                sprites2 = [sprite.scale(ri(1, 2)) for sprite in sprites2]

            descr = []

            if self.use_patch_centers:
                for sprite in sprites1 + sprites2:
                    self.patch_center = self.patch_centers[ri(0, self.patch_centers.shape[0] - 1)]
                    sprite.center_loc = self.patch_center
                    descr.append((self.patch_center, sprite))
            else:
                for sprite in sprites1 + sprites2:
                    descr.append(((ri(0, self.w - sprite.w), ri(0, self.h - sprite.h)), sprite))

            if self.task == 1:
                yield descr, numpy.array([index1], dtype = self.out_dtype)
            elif self.task == 2:
                yield descr, numpy.array([index2], dtype = self.out_dtype)
            else:
                yield descr, numpy.array([index1, index2], dtype = self.out_dtype)

