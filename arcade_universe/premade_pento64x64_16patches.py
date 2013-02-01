from gen import *
from dataset import *
import numpy as np
import argparse

from fg import Foreground, FGTextureType

import time

def save_to_file(npy_file_name, n_examples, dataset, use_patch_centers=False, e=16):
    #The pentomino images
    np_data = np.array(np.zeros(e**2))

    #Target variables
    np_targets = np.array(np.zeros(1))

    if use_patch_centers:
        np_patch_centers = np.array(np.zeros(16))

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
    np_data = np.float32(np_data)

    np_targets = np_targets[1:]
    np_targets = np.uint8(np_targets)

    if use_patch_centers:
        np_patch_centers = np_patch_centers[1:]
        np_patch_centers = np.int8(np_patch_centers)
        np_dataset = np.array([np_data, np_targets, np_patch_centers])
    else:
        np_dataset = np.array([np_data, np_targets])
    print "Converted %s to a numpy array." % npy_file_name
    np.save(npy_file_name, np_dataset)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="premade script")

    parser.add_argument("--seed", action="store", help="seed for the random number generator", type=int)

    parser.add_argument("--no-of-exs", action="store", help="the number of examples", type=int, required=True)

    parser.add_argument("--bg-texture-type",
                        action="store",
                        choices=["perlin", "hilbert", "plain"],
                        help="Determine the type of the texture for the background. Default is plain binary.")

    parser.add_argument("--task",
        action="store",
        choices=[1, 2, 3, 4],
        help="Determine the type of the texture for the background. Default is plain binary.",
        default=1,
        type=int)

    parser.add_argument("--fg-texture-type", action="store",
        choices=["gradient_rad", "gradient_lin", "plain"],
        help="Determine the type of the texture for the foreground. Default is plain binary.")

    parser.add_argument("--out-file-name", action="store", help="The output file name.", required=True)

    parser.add_argument("--center-objects", action="store", choices=[0, 1], help="To center the \
    objects set this flag to 1", default=0, type=int)

    args = parser.parse_args()

    seed = args.seed
    task = args.task
    no_of_exs = args.no_of_exs
    texture_type = args.fg_texture_type
    bg_texture_type = args.bg_texture_type
    out_file_name = args.out_file_name
    center_objs = args.center_objects
    patch_size = (8, 8)

    if out_file_name is None:
        raise Exception("The output file name can not be empty.")

    if seed is None:
        seed = int(time.time())

    if no_of_exs is None:
        no_of_exs = 20000

    if texture_type is None:
        texture_type = "plain"
    if texture_type == "plain":
        fg = Foreground(size=patch_size, texture_type=FGTextureType.PlainBin)
    elif texture_type == "gradient_rad":
        fg = Foreground(size=patch_size, texture_type=FGTextureType.GradientRadial)
    elif texture_type == "gradient_lin":
        fg = Foreground(size=patch_size, texture_type=FGTextureType.GradientLinear)

    texture = fg.generate_texture()

    # PENTOMINO
    pentomino_gen = lambda w, h: TwoGroups("pentl/pentn/pentp/pentf/penty/pentj/pentn2/pentq/pentf2/penty2",
                                       seed,
                                       w,
                                       h,
                                       use_patch_centers=True,
                                       n1=1,
                                       n2=2,
                                       rot=True,
                                       texture=texture,
                                       scale=True,
                                       center_objects=center_objs,
                                       patch_size=patch_size,
                                       task=task)

    if bg_texture_type == "perlin":
        enable_perlin = True
    else:
        enable_perlin = False

    pentomino = lambda w, h: SpritePlacer(pentomino_gen(w, h), collision_check=True, enable_perlin=enable_perlin)
    pentomino64x64 = pentomino(64, 64)
    pentomino_dir = "/RQusagers/gulcehre/dataset/pentomino/rnd_pieces/"
    pentomino64x64_file = pentomino_dir + out_file_name + "_seed_" + str(seed) + "_16patches_rnd" + ".npy"

    print "Started saving pentomino64x64"
    save_to_file(pentomino64x64_file, no_of_exs, pentomino64x64, use_patch_centers=True, e=64)

