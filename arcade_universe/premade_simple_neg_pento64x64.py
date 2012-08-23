from gen import *
from dataset import *
import numpy as np

from fg import Foreground, FGTextureType

def save_to_file(npy_file_name, n_examples, dataset, use_patch_centers=False, e=16):
    np_data = np.array(np.zeros(e**2))

    np_targets = np.array(np.zeros(1))
    if use_patch_centers:
        np_patch_centers = np.array(np.zeros(64))
    n_count = 0

    for data in dataset:
        if n_count == n_examples:
            break

        np_data = np.vstack((np_data, data[0]))
        np_targets = np.vstack((np_targets, data[1]))
        if use_patch_centers:
            np_patch_centers = np.vstack((np_patch_centers, data[2]))
        n_count+=1

    np_data = np_data[1:]
    np_data.dtype = np.float32

    np_targets = np_targets[1:]
    np_targets.dtype = np.uint8

    if use_patch_centers:
        np_patch_centers = np_patch_centers[1:]
        np_patch_centers.dtype = np.int8
        np_dataset = np.array([np_data, np_targets, np_patch_centers])
    else:
        np_dataset = np.array([np_data, np_targets])

    print "Converted %s to a numpy array." % npy_file_name
    np.save(npy_file_name, np_dataset)


if __name__=="__main__":
#   TETROMINO

    fg = Foreground(size=(16, 16), texture_type=FGTextureType.PlainBin)
    texture = fg.generate_texture()

#   PENTOMINO
    pentomino_gen = lambda w, h: TwoGroups("pentl/pentn/pentp/pentf/penty/pentj/pentn2/pentq/pentf2/penty2",
                                       2020, w, h,
                                       use_patch_centers=True,
                                       n1 = 1, n2 = 2, rot = True,
                                       patch_size=(16, 16),
                                       texture=texture, scale=True, task = 4)

    pentomino = lambda w, h: SpritePlacer(pentomino_gen(w, h), collision_check=True, enable_perlin=False)

    pentomino64x64 = pentomino(64, 64)

    pentomino_dir = "/data/lisa/data/pentomino/"

    pentomino64x64_raw = pentomino_dir + "pentomino64x64_300_presence.npy"

    print "Started saving pentomino64x64"
    no_of_examples = 300

    save_to_file(pentomino64x64_raw, no_of_examples, pentomino64x64,
            use_patch_centers=True, e=64)
