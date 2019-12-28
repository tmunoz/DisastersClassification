from datetime import datetime, timedelta, time
import os

deltas = [1, 5, 10, 15]
deltas_secs = [10, 15, 30, 45]
outputTrainingFile = open("../vectors/data_training.csv", "w")
outputTrainingAnsFile = open("../vectors/data_training_ans.csv", "w")

datasets = [
    '2013-pakistan-date',
    '2014-California-date',
    '2014-Chile1-date',
    '2014-Chile2-date',
    '2015-Nepal-date',
    '2014_chile0_eq_es', # #
    '../captured/sortedChile1.csv',
    '../captured/sorted',
]

for dataset in datasets:
    print(dataset)
    for delta in deltas:
        file = open("../datasets/earthquakes/" + dataset + '.csv', "r")

        stamps = []
        counts = []
        i = 0
        count = 0

        firstLine = file.readline().strip()
        firstLine = firstLine.split(';')[1]
        
        if dataset != '2014_chile0_eq_es':
            stamps.append(datetime.strptime(firstLine, '%a %b %d %H:%M:%S %z %Y'))
        else:
            stamps.append(datetime.strptime(firstLine, '%m/%d/%Y %H:%M:%S'))

        for line in file:
            line = line.strip()
            date = line.split(';')[1]

            if dataset != '2014_chile0_eq_es':
                dateParsed = datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y')
            else:
                dateParsed = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
            
            if dateParsed < (stamps[i] + timedelta(minutes=delta)):
                count += 1
            else:
                counts.append(count)
                stamps.append(stamps[i] + timedelta(minutes=delta))
                i += 1
                count = 1

        if len(stamps) > len(counts):
            counts.append(count)
        print(len(counts))
        # Output to file
        if len(counts) >= 36:
            for i, count in enumerate(counts[:36]):
                if i != len(counts[:36]) - 1:
                    outputTrainingFile.write(str(count) + ', ')
                else:
                    outputTrainingFile.write(str(count) + '\n')
                    outputTrainingAnsFile.write(str(1) + '\n')

        file.close()

outputTrainingFile.close()