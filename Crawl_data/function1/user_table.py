#tạo bảng user lưu ra file user_table.csv
import pandas as pd

uc = pd.read_csv("user_crawl.csv")

user_id = uc['id'].values
name = uc['name'].values
username = uc['username'].values
location = uc['location'].values
number_tweet = uc['tweets'].values
number_following = uc['following'].values
number_follower = uc['followers'].values
avatar_url = uc['profile_image_url']

user = pd.DataFrame()
user['user_id'] = user_id
user['name'] = name
user['username'] = username
user['location'] = location
user['number_tweet'] = number_tweet
user['number_following'] = number_following
user['number_follower'] = number_follower
user['avatar_url'] = avatar_url
user.to_csv("user_table.csv")