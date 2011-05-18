
from gen import *
from dataset import *


# TETROMINO

tetromino_gen = lambda w, h: TwoGroups("tetrisi/tetriso/tetrist/tetrisl/tetrisj/tetriss/tetrisz",
                                       1010, w, h,
                                       n1 = 1, n2 = 2, rot = True, task = 1)
tetromino = lambda w, h: BugPlacer(tetromino_gen(w, h), True)
tetromino10x10 = tetromino(10, 10)
tetromino16x16 = tetromino(16, 16)


# PENTOMINO

pentomino_gen = lambda w, h: TwoGroups("pentl/pentn/pentp/pentf/penty/pentj/pentn2/pentq/pentf2/penty2",
                                       2020, w, h,
                                       n1 = 1, n2 = 2, rot = True, task = 1)
pentomino = lambda w, h: BugPlacer(pentomino_gen(w, h), True)
pentomino10x10 = pentomino(10, 10)
pentomino16x16 = pentomino(16, 16)


