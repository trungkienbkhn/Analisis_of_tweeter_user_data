import pandas as pd 
en = pd.read_csv("content4.csv")
a = en['tweet'].values
tweet = pd.DataFrame()
b = []
for i in range(0,len(a)):
    b.append(a[i])
tweet['content'] = b
tweet.to_csv("vi4.csv")
