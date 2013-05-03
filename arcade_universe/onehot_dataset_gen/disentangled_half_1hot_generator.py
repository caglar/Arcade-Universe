import numpy

class DisentagledHalfOneHotDatasetGenerator(object):

    def __init__(self,
        size_of_dataset,
        no_of_scales=2,
        no_of_rotations=4,
        no_of_patches=64,
        no_of_objects=10,
        rng=None):

        if rng is not None:
            self.rng = rng
        else:
            self.rng = numpy.random.RandomState(1234)

        self.no_of_scales = no_of_scales
        self.no_of_rotations = no_of_rotations
        self.no_of_patches = no_of_patches
        self.no_of_objects = no_of_objects
        self.no_of_patches = no_of_patches
        self.size_of_dataset = size_of_dataset
        self.no_of_possible_variations = no_of_scales + no_of_rotations
        self.initialize_dataset()

    def initialize_dataset(self):
        total_variations = self.no_of_possible_variations + self.no_of_objects
        empty_patch = numpy.zeros(total_variations, dtype="uint8")
        img = numpy.repeat([empty_patch], self.no_of_patches, axis=0)
        dataset = numpy.repeat([img], self.size_of_dataset, axis=0)
        return dataset

    def randomly_choose_patches(self):
        patches = range(self.no_of_patches)
        first_patch = self.rng.random_integers(self.no_of_patches) - 1
        patches.remove(first_patch)
        second_patch = patches[self.rng.random_integers(self.no_of_patches-1) - 1]
        patches.remove(second_patch)
        third_patch = patches[self.rng.random_integers(self.no_of_patches-2) - 1]
        return [first_patch, second_patch, third_patch]

    def randomly_choose_objects(self):
        objects = range(self.no_of_objects)
        first_obj = self.rng.random_integers(self.no_of_objects) - 1
        objects.remove(first_obj)
        second_obj = objects[self.rng.random_integers(self.no_of_objects - 1) - 1]
        return first_obj, second_obj

    def get_transformations(self):
        rotation_var = self.rng.random_integers(self.no_of_rotations)
        scale_var = self.rng.random_integers(self.no_of_scales)
        rotation_idx = self.no_of_objects + rotation_var - 1
        scale_idx = self.no_of_objects + self.no_of_rotations + scale_var - 1
        return rotation_idx, scale_idx

    def generate_dataset(self):
        data = self.initialize_dataset()
        labels = numpy.zeros(self.size_of_dataset, dtype="uint8")
        for i in xrange(self.size_of_dataset):
            label = self.rng.random_integers(2) - 1
            first_patch, second_patch, third_patch = self.randomly_choose_patches()
            first_type, second_type = self.randomly_choose_objects()
            first_obj_transformations = self.get_transformations()
            second_obj_transformations = self.get_transformations()
            third_obj_transformations = self.get_transformations()

            labels[i] = label

            data[i][first_patch][0] = 0
            data[i][second_patch][0] = 0
            data[i][third_patch][0] = 0

            #Place the first two objects int their patches and assign their
            #patch values
            data[i][first_patch][first_type] = 1
            data[i][first_patch][first_obj_transformations[0]] = 1
            data[i][first_patch][first_obj_transformations[1]] = 1

            data[i][second_patch][first_type] = 1
            data[i][second_patch][second_obj_transformations[0]] = 1
            data[i][second_patch][second_obj_transformations[1]] = 1

            #All the objects are in the image are the same type.
            if label == 0:
                data[i][third_patch][first_type] = 1
                data[i][third_patch][third_obj_transformations[0]] = 1
                data[i][third_patch][third_obj_transformations[1]] = 1
            #There is a different object in the image.
            if label == 1:
                data[i][third_patch][second_type] = 1
                data[i][third_patch][third_obj_transformations[0]] = 1
                data[i][third_patch][third_obj_transformations[1]] = 1

        return [data, labels]
