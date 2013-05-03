from onehot_generator import OneHotDatasetGenerator
import numpy

rng = numpy.random.RandomState(1345)
onehot_train_gen = OneHotDatasetGenerator(size_of_dataset=1000,
no_of_possible_variations=8, no_of_objects=10, rng=rng)

print "Generating the training dataset..."
ds = onehot_train_gen.generate_dataset()

print "Saving the training dataset..."

file = open("1hot_train_data_1000_80.npz", "wb")
numpy.savez(file, data=ds[0], labels=ds[1])

onehot_test_gen = OneHotDatasetGenerator(size_of_dataset=200, no_of_possible_variations=8, no_of_objects=10, rng=rng)
print "Generating the test dataset."
ds_test = onehot_test_gen.generate_dataset()

print "Saving the test dataset."

file = open("1hot_test_data_200_80.npz", "wb")
numpy.savez(file, data=ds_test[0], labels=ds_test[1])


