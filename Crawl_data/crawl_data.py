import twint 
c = twint.Config()

#tìm kiếm đưa dữ liệu ra dạng list
c.Since = "2020-03-20"
c.Until = "2020-04-08"
c.Geo = "48.880048,2.385939,1km"
#c.Geo = "21.006111, 105.843056, 20km"
c.Limit = 20
c.Store_object = True
twint.run.Search(c)
tweets = twint.output.tweets_list
for tweet in tweets:
    print ('ID: {}'.format(tweet.hashtags))

#tìm kiếm bài viết trong vùng lưu ra file csv. vd file hanoi.csv
#c.Since = "2020-03-20"
#c.Until = "2020-04-08"
#c.Geo = "48.880048,2.385939,1km"
#c.Store_csv = True
#c.Output = "hanoi.csv"
#twint.run.Search(c)

#tìm kiếm user theo id. vd lưu ra file user_crawl
#c.User_id = ""
#c.Store_csv = True
#c.Output = "user_crawl.csv"
#twint.run.Lookup(c)

#tìm kiếm bài viết tiếng việt theo hashtag
#c.Search = "covid"
#c.Since = "2020-03-20"
#c.Until = "2020-04-08"
#c.Lang = "vi"
#c.Store_csv = True
#c.Output = "vietnamcovid.csv"
#twint.run.Search(c)