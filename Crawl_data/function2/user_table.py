#tạo bảng user lưu ra file user_table.csv
import pandas as pd

uc = pd.read_csv("user_covid.csv")

user_id = []
name = []
username = []
number_tweet = []
number_following = []
number_follower = []
avatar_url = []

a = uc['location'].values
b = uc['id'].values #user_id
c = uc['name'].values
d = uc['username'].values
e = uc['tweets'].values
f = uc['following'].values
g = uc['followers'].values
h = uc['profile_image_url']

for i in range(0, len(a)):
    if (a[i] == a[i]):
        user_id.append(b[i])
        name.append(c[i])
        username.append(d[i])
        number_tweet.append(e[i])
        number_following.append(f[i])
        number_follower.append(g[i])
        avatar_url.append(h[i])

user = pd.DataFrame()
user['user_id'] = user_id
user['name'] = name
user['username'] = username
user['number_tweet'] = number_tweet
user['number_following'] = number_following
user['number_follower'] = number_follower
user['avatar_url'] = avatar_url
user.to_csv("user_table.csv")
