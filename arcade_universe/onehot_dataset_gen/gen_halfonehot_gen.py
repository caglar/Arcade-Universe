from half_onehot_generator import HalfOneHotDatasetGenerator
import numpy

rng = numpy.random.RandomState(1345)
onehot_train_gen = HalfOneHotDatasetGenerator(size_of_dataset=100000,
no_of_possible_variations=1, no_of_objects=10, rng=rng)

print "Generating the training dataset..."
ds = onehot_train_gen.generate_dataset()

print "Saving the training dataset..."

file = open("half1hot_train_data_100k_10.npz", "wb")
numpy.savez(file, data=ds[0], labels=ds[1])

onehot_test_gen = HalfOneHotDatasetGenerator(size_of_dataset=20000,
no_of_possible_variations=1, no_of_objects=10, rng=rng)
print "Generating the test dataset."
ds_test = onehot_test_gen.generate_dataset()

print "Saving the test dataset."

file = open("half1hot_test_data_20k_10.npz", "wb")
numpy.savez(file, data=ds_test[0], labels=ds_test[1])
