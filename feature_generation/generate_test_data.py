import random

data_f = open('data.txt', 'w')
feature_f = open('features.txt', 'w')

for i in range(100):
    data_line = str(i)
    feature_line = str(i)

    if random.random() > 0.5:
        data_line += ',1'
    else:
        data_line += ',-1'

    for j in range(10):
        feature_line += ',' + str(random.random())

    data_f.write(data_line + '\n')
    feature_f.write(feature_line + '\n')

data_f.close()
feature_f.close()
