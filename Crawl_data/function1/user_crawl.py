import twint
import pandas as pd

hn = pd.read_csv("hanoi.csv")
user = hn['user_id'].values
id = pd.DataFrame()
id['id'] = user
id = id.drop_duplicates()
list_id = id['id'].values
a = []

for i in range(0,len(list_id)):
    a.append(list_id[i])

for j in range(0,len(a)):
     c = twint.Config()
     c.User_id = a[j]
     c.Store_csv = True
     c.Output = "user_crawl.csv"
#     c.Hide_output = True
     twint.run.Lookup(c)