import matplotlib.pyplot as plt
from datetime import datetime, timedelta


f = open("sorted.csv", "r")

dates = []
stamps = []
counts = []
i=0
count = 0

stamps.append(datetime.strptime("3/28/2016 08:29:37", '%m/%d/%Y %H:%M:%S'))


# print(stamp+timedelta(minutes=5))
# if test > (stamp + timedelta(minutes=20)):
#     print("yep")

for line in f:
    line=line.strip()
    date = line.split(';')[1]
    print(date)
    dateParsed = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
    
    if dateParsed < (stamps[i] + timedelta(minutes=5)):
        count+=1
    else:
        counts.append(count)
        stamps.append(stamps[i]+timedelta(minutes=5))
        i+=1
        count=1
    
    # print(dateParsed)

if len(stamps) > len(counts):
    counts.append(count)

for j in range (len(stamps)):
    print(stamps[j], counts[j])

x = [j for j in range(0, len(stamps))]
plt.ylabel('Tweets')
plt.title('Cantidad de Tweets sobre terremotos cada 5 minutos')
plt.xticks(x, stamps)
plt.xticks(rotation=90)
plt.plot(x, counts)
plt.show()