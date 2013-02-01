from data_generator import PentominoGenerator

dt_gen = PentominoGenerator(batch_size=100, upper_bound=1000)

for data in dt_gen:
    print data.next()
