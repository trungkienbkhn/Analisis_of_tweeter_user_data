import psycopg2

class GetPsql:
    conn = psycopg2.connect(database = "tweet_data",
                            user = "postgres",
                            password = "02103598",
                            host = "127.0.0.1",
                            port = "5432")
                            
    def __init__(self):
        self.cur = self.getdb()

    def close(self):
        self.conn.close()
    def commit(self):
        self.conn.commit()
    def getdb(self):
        return self.conn.cursor()

#get top hashtag
    def get_top_hashtag(self,location, from_date, to_date, limit):
        self.cur.execute('''with new_table as (
                                select tweet.id, hashtag.hashtag, tweet.create_at
                                from hashtag, tweet
                                where hashtag.location like '{}' and tweet.id = hashtag.tweet_id
                                and tweet.create_at between '{}' and '{}')
                            select hashtag, count(hashtag) as hashtag_count
                            from new_table
                            group by hashtag
                            order by hashtag_count desc
                            limit {} ;'''.format(location, from_date, to_date, limit))
        return self.cur.fetchall()
#get tweet from hashtag
    def get_tweet(self,hashtag):
        self.cur.execute('''with new_table as (
                                select tweet.id, tweet.content, hashtag.hashtag
	                            from tweet, hashtag
	                            where hashtag = '{}' and tweet.id = hashtag.tweet_id)
                            select id, content from new_table;'''.format(hashtag))
        return self.cur.fetchall()

a = GetPsql()
#b = a.get_top_hashtag('hanoi', '2020-03-22', '2020-03-24', 10)
b = a.get_tweet('#covid_19')
for tweet in b:
    print("id : ", tweet[0])
    print('content : ', tweet[1])
a.close()