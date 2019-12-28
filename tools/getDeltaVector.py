from datetime import datetime, timedelta, time
import os
import math

deltas_mins = [1, 5, 10, 15]
deltas_secs = [10, 15, 30, 45]
outputTrainingFile = open("../vectors/data_training.csv", "a")
outputTrainingAnsFile = open("../vectors/data_training_ans.csv", "a")

datasets = [
    '2013-pakistan-date',
    '2014-California-date',
    '2014-Chile1-date',
    '2014-Chile2-date',
    '2015-Nepal-date',
    '2014_chile0_eq_es', # #
    'sorted',
    'sortedChile1'
]

for dataset in datasets:
    print(dataset)
    for delta in deltas_secs:
        try:
            file = open("../datasets/earthquakes/" + dataset + '.csv', "r")
        except:
            file = open("../captured/" + dataset + '.csv', "r")

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
            
            if dateParsed < (stamps[i] + timedelta(seconds=delta)):
                count += 1
            else:
                counts.append(count)
                stamps.append(stamps[i] + timedelta(seconds=delta))
                i += 1
                count = 1

        if len(stamps) > len(counts):
            counts.append(count)
        print(len(counts))
        # Output to file

        div = math.floor(len(counts) / 36)

        if div > 0:
            index = 0
            while index < div:
                begin = 36 * index
                end = 36 * (index + 1)

                for i, count in enumerate(counts[begin:end]):
                    if i != len(counts[begin:end]) - 1:
                        outputTrainingFile.write(str(count) + ', ')
                    else:
                        outputTrainingFile.write(str(count) + '\n')
                        if dataset == 'sorted' or dataset == 'sortedChile1':
                            outputTrainingAnsFile.write(str(0) + '\n')
                        else:
                            outputTrainingAnsFile.write(str(1) + '\n')
                index += 1

        file.close()

outputTrainingFile.close()