import pandas as pd

hn = pd.read_csv("hanoi.csv")
a = hn['user_id'].values
b = hn['id'].values
c = hn['hashtags'].values
list_ht = []
user_id = []
tweet_id = []
location = []
print("Tweets: ", len(c))
for i in range(0, len(c)):
    if (c[i] != "[]"):
        e = c[i].split("', '")
        e[0] = e[0].lstrip("['")
        e[len(e)-1] = e[len(e)-1].rstrip("']")
        for j in range(0,len(e)):
            list_ht.append(e[j])
            user_id.append(a[i])
            tweet_id.append(b[i])
            location.append("hanoi")

hashtag = pd.DataFrame()
hashtag['hashtag'] = list_ht
hashtag['user_id'] = user_id
hashtag['tweet_id'] = tweet_id
hashtag['location'] = location
print(hashtag)
hashtag.to_csv("hashtag_table.csv")