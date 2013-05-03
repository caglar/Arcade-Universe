from gen import *
from pdataset import *
import numpy as np
import argparse

from arcade_universe.fg import Foreground, FGTextureType
import time

class PentominoGenerator(object):

    def __init__(self,
        batch_size,
        use_patch_centers=False,
        seed=1321, patch_size=(8, 8),
        enable_perlin=False,
        task=4,
        upper_bound=10000000):

        self.batch_size = batch_size
        self.use_patch_centers = use_patch_centers
        self.upper_bound = upper_bound
        self.pix_per_patch = np.prod(patch_size)

        fg = Foreground(size=patch_size, texture_type=FGTextureType.PlainBin)
        texture = fg.generate_texture()

        self.n_examples = 0

        # PENTOMINO
        self.pentomino_gen = lambda w, h: TwoGroups("pentl/pentn/pentp/pentf/penty/pentj/pentn2/pentq/pentf2/penty2",
                                       seed,
                                       w,
                                       h,
                                       use_patch_centers=False,
                                       n1=1,
                                       n2=2,
                                       rot=True,
                                       texture=texture,
                                       scale=True,
                                       center_objects=True,
                                       patch_size=patch_size,
                                       task=task)

        pentomino = SpritePlacer(self.pentomino_gen(64, 64),
            collision_check=True,
            enable_perlin=enable_perlin)

        self.pentomino_data_gen = pentomino

    def __iter__(self):
        return self.next()

    def next(self):
        #import ipdb; ipdb.set_trace()
        np_data = np.array(np.zeros(self.pix_per_patch**2))
        #Target variables
        np_targets = np.asarray(np.zeros(1), dtype="float32")
        n_count = 0
        for data in self.pentomino_data_gen:
            if self.n_examples < self.upper_bound:
                np_data = np.vstack((np_data, data[0]))
                np_targets = np.vstack((np_targets, data[1]))
                if n_count < self.batch_size:
                    if n_count == 0:
                        np_data = np_data[1:]
                        np_targets = np_targets[1:]

                    batched_data = numpy.array([np_data, np_targets])
                    n_count +=1
                    self.n_examples +=1
                else:
                    n_count = 0
                    np_data = np.array(np.zeros(self.pix_per_patch**2))
                    #Target variables
                    np_targets = np.asarray(np.zeros(1), dtype="float32")
                    yield batched_data
            else:
                raise StopIteration()

