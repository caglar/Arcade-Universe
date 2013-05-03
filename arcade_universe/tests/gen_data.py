from arcade_universe.data_generator import PentominoGenerator

dt_gen = PentominoGenerator(batch_size=100, upper_bound=1000)
i = 0

for data in dt_gen:
    i +=1
    print data
    print "Iteration: ", i

