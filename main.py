import datetime
import numpy

array=[i for i in numpy.arange(1000000)]

arraynp=numpy.array([i for i in numpy.arange(1000000)])


# start=datetime.datetime.now()
# for i in array:
#     pass
# print(datetime.datetime.now()-start)

start=datetime.datetime.now()
for i in arraynp:
    pass
print(datetime.datetime.now()-start)