import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# save numpy array as csv file
from numpy import asarray
from numpy import savetxt

f = open("./captured/sorted", "r")

dates = []
stamps = []
counts = []
i=0
count = 0

firstLine = f.readline().strip()
firstLine = firstLine.split(';')[1]
stamps.append(datetime.strptime(firstLine, '%a %b %d %H:%M:%S %z %Y'))

for line in f:
    line=line.strip()
    date = line.split(';')[1]
    # print(date)
    dateParsed = datetime.strptime(date, '%a %b %d %H:%M:%S %z %Y')
    
    if dateParsed < (stamps[i] + timedelta(minutes=15)):
        count+=1
    else:
        counts.append(count)
        stamps.append(stamps[i]+timedelta(minutes=15))
        i+=1
        count=1


if len(stamps) > len(counts):
    counts.append(count)

for j in range (len(stamps)):
    # print(stamps[j], counts[j])
    print(counts[j])

for elem in stamps:
    elem=elem.time

# define data
data = asarray([counts])
# save to csv file
savetxt('data2.csv', data, delimiter=',')

x = [j for j in range(0, len(stamps))]
plt.ylabel('Tweets')
plt.title('Cantidad de Tweets sobre terremotos cada 5 minutos - 2013 Pakistan')
plt.xticks(x, stamps)
plt.xticks(rotation=90)
plt.plot(x, counts)
plt.show()