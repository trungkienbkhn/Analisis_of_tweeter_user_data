import psycopg2

conn = psycopg2.connect(database = "function1",
                        user = "postgres",
                        password = "s",
                        host = "127.0.0.1",
                        port = "5432")

print("Opened database successfully")

cur = conn.cursor()
cur.execute('''CREATE TABLE TWEETER
      (ID                    BIGSERIAL        NOT NULL,
      NAME                   VARCHAR(100)             ,
      USERNAME               VARCHAR(100)     NOT NULL,
      LOCATION               VARCHAR(200),
      NUMBER_TWEET           INT,
      NUMBER_FOLLOWING       INT,
      NUMBBER_FOLLOWER       INT,
      AVATAR_URL             VARCHAR(300),
      PRIMARY KEY (ID));
      ''')

cur.execute('''CREATE TABLE TWEET
      (TWEETER_ID     BIGSERIAL        NOT NULL,
      ID              BIGSERIAL        NOT NULL,
      CONTENT         TEXT,
      CREATE_AT       DATE,
      LIKE_COUNT      INT,
      RETWEET_COUNT   INT,
      REPLIE_COUNT   INT,
      IMAGE_URL       VARCHAR(300),
      LINK            VARCHAR(300),
      PLACE           VARCHAR(200),
      PRIMARY KEY (ID),
      FOREIGN KEY (TWEETER_ID) REFERENCES TWEETER(ID));
      ''')  

cur.execute('''create table hashtag(
	ID       BIGSERIAL NOT NULL,
      HASHTAG  VARCHAR(100) NOT NULL,
      USER_ID  BIGSERIAL NOT NULL,
	TWEET_ID BIGSERIAL NOT NULL,
      LOCATION VARCHAR(100) ,
  	PRIMARY KEY (ID),
	FOREIGN KEY (TWEET_ID) REFERENCES tweet(ID),
      FOREIGN KEY (USER_ID)  REFERENCES TWEETER(ID));
      ''')  
print("Table created successfully")

conn.commit()
conn.close()