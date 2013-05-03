import numpy as np
import math

def get_patches(mat, patch_size=(4,4)):
    if mat.ndim == 1:
        dim = math.sqrt(mat.shape[0])
        mat.reshape((dim, dim))

    mat_rows = mat.shape[0]
    mat_cols = mat.shape[1]
    patches = None

    for i in xrange(mat_rows / patch_size[0]):
        for j in xrange(mat_cols / patch_size[1]):
            print patches
            patch = mat[i * patch_size[0]: (i + 1)* patch_size[0], j * patch_size[0]: (j + 1) * patch_size[1]]
            if patches is None:
                patches = patch
            else:
                if patches.ndim != patch.ndim:
                    patches = np.vstack((patches, [patch]))
                else:
                    patches = np.vstack(([patches], [patch]))
    return patches

arr = np.array(xrange(32 * 32)).reshape(32, 32)
patches = get_patches(arr)
print patches
