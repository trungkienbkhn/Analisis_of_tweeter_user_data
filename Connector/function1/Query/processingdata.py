import pandas as pd
import ast
data = pd.read_csv('tweet_table.csv')
#print(data.shape)
#data1 = data.loc[:, ['id', 'tweet', 'likes_count', 'retweets_count', 'photos', 'video', 'hashtags', 'link']]
#data1.to_csv('hanoi_selected.csv',index=False)
data2 = data.loc[:, ['user_id', 'tweet_id', 'hashtags']]
a = data2.values
tweet_id = []
hashtag = []
for b in a:
  if (b[1] == '[]'):
    continue
  hashtags = b[1]
  hashtags = ast.literal_eval(hashtags)
  for sigle_hashtag in hashtags:
    tweet_id.append(b[0])
    hashtag.append(sigle_hashtag)
print(len(hashtag))
df = pd.DataFrame({"id": tweet_id, 
                  "hashtag": hashtag})
df.to_csv('hashtag_table.csv')