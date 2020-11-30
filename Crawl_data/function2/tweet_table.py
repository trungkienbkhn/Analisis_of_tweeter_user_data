#tạo bảng tweet lưu ra file tweet_table.csv
import pandas as pd

hn = pd.read_csv("vietnamcovid.csv")
user = pd.read_csv("user_table.csv")
userid = user['user_id'].values
user_id = []
tweet_id = []
content = []
like_count = []
retweet_count = []
replie_count = []
image = []
link = []
date = []
image_url = []
hashtag = []

a = hn['user_id'].values
b = hn['id'].values
c = hn['tweet'].values
d = hn['likes_count'].values
e = hn['retweets_count'].values
f = hn['replies_count'].values
g = hn['photos'].values
h = hn['link'].values
k = hn['date'].values
l = hn['hashtags'].values

for i in range(0,len(userid)):
    for j in range(0,len(a)):
        if (a[j] == userid[i]):
            user_id.append(a[j])
            tweet_id.append(b[j])
            content.append(c[j])
            like_count.append(d[j])
            retweet_count.append(e[j])
            replie_count.append(f[j])
            image_url.append(g[j])
            link.append(h[j])
            date.append(k[j])
            hashtag.append(l[j])

tweet = pd.DataFrame()
tweet['user_id'] = user_id
tweet['tweet_id'] = tweet_id
tweet['content'] = content
tweet['hashtag'] = hashtag
tweet['date'] = date
tweet['like_count'] = like_count
tweet['retweet_count'] = retweet_count
tweet['replie_count'] = replie_count
tweet['image_url'] = image_url
tweet['link'] = link
tweet.to_csv("tweet_table.csv")
