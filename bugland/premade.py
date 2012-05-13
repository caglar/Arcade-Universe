from gen import *
from dataset import *
import numpy as np

def save_to_file(npy_file_name, n_examples, dataset, e=16):
    np_data = np.array(np.zeros(e**2))
    np_targets = np.array(np.zeros(1))
    n_count = 0

    for data in dataset:
        if n_count == n_examples:
            break
        np_data = np.vstack((np_data, data[0]))
        np_targets = np.vstack((np_targets, data[1]))
        n_count+=1

    np_dataset = np.array([np_data, np_targets])
    print "Converted %s to a numpy array." % npy_file_name
    np.save(npy_file_name, np_dataset)

if __name__=="__main__":
    # TETROMINO
    tetromino_gen = lambda w, h: TwoGroups("tetrisi/tetriso/tetrist/tetrisl/tetrisj/tetriss/tetrisz",
                                       1010, w, h,
                                       n1 = 1, n2 = 2, rot = True, scale=True, task = 1)

    tetromino = lambda w, h: BugPlacer(tetromino_gen(w, h), collision_check=True)
    tetromino10x10 = tetromino(10, 10)
    tetromino16x16 = tetromino(16, 16)

    # PENTOMINO
    pentomino_gen = lambda w, h: TwoGroups("pentl/pentn/pentp/pentf/penty/pentj/pentn2/pentq/pentf2/penty2",
                                       2020, w, h,
                                       n1 = 1, n2 = 2, rot = True, scale=True, task = 1)

    pentomino = lambda w, h: BugPlacer(pentomino_gen(w, h), collision_check=True, enable_perlin=True)
    pentomino10x10 = pentomino(10, 10)
#    pentomino16x16 = pentomino(16, 16)
    pentomino32x32 = pentomino(32, 32)

    pentomino_dir = "/home/caglar/Datasets/tetropentomino/"
    tetromino_dir = "/home/caglar/Datasets/tetropentomino/"

    pentomino16x16_raw = pentomino_dir + "pentomino16x16_raw.npy"
    pentomino32x32_raw = pentomino_dir + "pentomino32x32_raw.npy"
    tetromino16x16_raw = tetromino_dir + "tetromino16x16_raw.npy"

    print "Started saving pentomino16x16"
 #   save_to_file(pentomino16x16_raw, 100, pentomino16x16)

    print "Started saving tetromino16x16"
    save_to_file(tetromino16x16_raw, 100, tetromino16x16)

    print "Started saving pentomino32x32"
    save_to_file(pentomino32x32_raw, 100, pentomino32x32, e=32)
