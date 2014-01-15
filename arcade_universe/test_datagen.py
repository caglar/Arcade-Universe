from data_generator import PentominoGenerator
import time
import numpy

data_gen = PentominoGenerator(batch_size=500, use_patch_centers=True)
i=0
time_begin = time.time()
past = None
m_data = None
times = []
for data in data_gen:
    print "Iteration... %d " % (i)

    if i == 4:
        break
    future = data
    if past and numpy.all(past[0]==future[0]):
        print "Fucked up!"
        break
    m_data = data[0]
    #print future
    time_end = time.time()
    time_taken = time_end - time_begin
    times.append(time_taken)
    print 'iteration %d takes %f' %(i, time_taken)
    time_begin = time_end
    i +=1
    past = future

print "On average %f time is consumed." % numpy.mean(times)
numpy.save("my_data.npy", m_data)
