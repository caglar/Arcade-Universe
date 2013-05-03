from onehot_generator import OneHotDatasetGenerator
import numpy

rng = numpy.random.RandomState(1345)
onehot_train_gen = OneHotDatasetGenerator(size_of_dataset=200000,
no_of_possible_variations=1, no_of_objects=4, rng=rng)

print "Generating the training dataset..."
ds = onehot_train_gen.generate_dataset()

print "Saving the training dataset..."

file = open("1hot_train_data_200k_4.npz", "wb")
numpy.savez(file, data=ds[0], labels=ds[1])

onehot_test_gen = OneHotDatasetGenerator(size_of_dataset=20000,
no_of_possible_variations=1, no_of_objects=4, rng=rng)
print "Generating the test dataset."
ds_test = onehot_test_gen.generate_dataset()

print "Saving the test dataset."

file = open("1hot_test_data_20k_4.npz", "wb")
numpy.savez(file, data=ds_test[0], labels=ds_test[1])


