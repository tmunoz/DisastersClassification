import matplotlib.pyplot as plt
from datetime import datetime, timedelta, time

title = input("Insert Title: ") #format: Year Place deltaTime
title = title.split(' ')
f = open("../earthquakes/2015-Nepal-date.csv", "r")

dates = []
stamps = []
counts = []
i = 0
count = 0

firstLine = f.readline().strip()
firstLine = firstLine.split(';')[1]

stamps.append(datetime.strptime(firstLine, '%a %b %d %H:%M:%S %z %Y'))
# stamps.append(datetime.strptime(firstLine, '%m/%d/%Y %H:%M:%S'))

for line in f:
    line = line.strip()
    date = line.split(';')[1]
    dateParsed = datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y')
    # dateParsed = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
    
    # if dateParsed < (stamps[i] + timedelta(minutes=1)):
    if dateParsed < (stamps[i] + timedelta(seconds=1)):
        count += 1
    else:
        counts.append(count)
        # stamps.append(stamps[i] + timedelta(minutes=1))
        stamps.append(stamps[i] + timedelta(seconds=1))
        i += 1
        count = 1

f.close()

if len(stamps) > len(counts):
    counts.append(count)

x_axis = []
for elem in stamps:
    x_axis.append(time(elem.hour, elem.minute, elem.second))

y_axis = list(range(len(stamps)))
plt.ylabel('Tweets')
# plt.title('Cantidad de Tweets sobre terremotos cada ' + title[2][:-1] + ' minutos - ' + title[0] + ' ' + title[1])
plt.title('Cantidad de Tweets sobre terremotos cada ' + title[2][:-1] + ' segundos - ' + title[0] + ' ' + title[1])
plt.xticks(y_axis, x_axis)
plt.xticks(rotation=90)
plt.plot(y_axis, counts)
plt.subplots_adjust(bottom=.2)
plt.savefig('../plots/v2/Nepal/' + '_'.join(title))
plt.show()