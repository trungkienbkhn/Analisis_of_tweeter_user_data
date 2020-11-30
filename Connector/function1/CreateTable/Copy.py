import psycopg2
import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
conn = psycopg2.connect(database = "function1",
                        user = "postgres",
                        password = "s",
                        host = "127.0.0.1",
                        port = "5432")

cur = conn.cursor()
user_link = "COPY tweeter FROM "+"'"+BASE_DIR+"/Data/users_hanoi_hcm_table.csv"+"'"+" DELIMITER ',' CSV HEADER;"
tweet_link = "COPY tweet FROM "+"'"+BASE_DIR+"/Data/tweets_hanoi_hcm_table.csv"+"'"+" DELIMITER ',' CSV HEADER;"
hashtag_link = "COPY hashtag FROM "+"'"+BASE_DIR+"/Data/hashtags_hanoi_hcm_table.csv"+"'"+" DELIMITER ',' CSV HEADER;"
cur.execute(user_link)
conn.commit()

cur.execute(tweet_link)
conn.commit()

cur.execute(hashtag_link)
conn.commit()

print("Operation done successfully")
conn.close()