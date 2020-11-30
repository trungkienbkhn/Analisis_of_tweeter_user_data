import pandas as pd
import math
from unidecode import unidecode

data = pd.read_csv("user_covid.csv")
a = data['location'].values
print("Tweets: ", len(a))
list_place = []
for i in range(0, len(a)):
    if (a[i] == a[i]):
        d = a[i].lower().replace(" ", "")
        if (d.count("-") > 0):        
            e = d.split("-")
        else: 
            e = d.split(",")

        for j in range(0, len(e)):
            if (e[j].isdigit() == False):
                list_place.append(unidecode(e[j]))

dem = 0
while (dem < 10):  
    max = 0
    j = 0
    for i in range(0, len(list_place)):
        if (max < list_place.count(list_place[i])):
            max = list_place.count(list_place[i])
            top = list_place[i]
    print(top, "~", max)
    while (list_place.count(top) > 0):
        if (list_place[j] == top):
            list_place.pop(j)
            j -= 1
        j += 1

    dem += 1
