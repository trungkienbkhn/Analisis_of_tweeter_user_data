#tạo bảng tweet lưu ra file tweet_table.csv
import pandas as pd

hn = pd.read_csv("hanoi.csv")
user_id = hn['user_id'].values
tweet_id = hn['id'].values
content = hn['tweet'].values
like_count = hn['likes_count'].values
retweet_count = hn['retweets_count'].values
replie_count = hn['replies_count'].values
image = hn['photos'].values
link = hn['link'].values
date = hn['date'].values
place = []
image_url = []

for i in range(0, len(image)):
    t = image[i].lstrip("['").rstrip("']")
    image_url.append(t)

for i in range(0, len(link)):
    place.append('Hà Nội')

tweet = pd.DataFrame()
tweet['user_id'] = user_id
tweet['tweet_id'] = tweet_id
tweet['content'] = content
tweet['date'] = date
tweet['like_count'] = like_count
tweet['retweet_count'] = retweet_count
tweet['replie_count'] = replie_count
tweet['image_url'] = image_url
tweet['link'] = link
tweet['place'] = place
tweet.to_csv("tweet_table.csv")