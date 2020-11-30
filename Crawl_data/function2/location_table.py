import pandas as pd
import math
from unidecode import unidecode

data = pd.read_csv("user_covid.csv")
a = data['location'].values
b = data['id'].values
location = []
user_id = []
for i in range(0, len(a)):
    if (a[i] == a[i]):
        d = a[i].lower().replace(" ", "")
        if (d.count("-") > 0):        
            e = d.split("-")
        else: 
            e = d.split(",")
        for j in range(0, len(e)):
            if (e[j].isdigit() == False):
                location.append(unidecode(e[j]))
                user_id.append(b[i])

location_table = pd.DataFrame()
location_table['location'] = location
location_table['user_id'] = user_id
location_table.to_csv("location_table.csv")
