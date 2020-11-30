import psycopg2

conn = psycopg2.connect(database="tweet_datacn2", user = "postgres", password = "kiena198", host = "127.0.0.1", port = "5432")

print("Opened database successfully")

cur = conn.cursor()
cur.execute('''CREATE TABLE TWEETER
      (ID                    BIGSERIAL        NOT NULL,
      NAME                   VARCHAR(100)             ,
      USERNAME               VARCHAR(100)     NOT NULL,
      NUMBER_TWEET           INT,
      NUMBER_FOLLOWING       INT,
      NUMBBER_FOLLOWER       INT,
      AVATAR_URL             VARCHAR(300),
      PRIMARY KEY (ID));''')

cur.execute('''CREATE TABLE TWEET
      (USER_ID     BIGSERIAL        NOT NULL,
      ID              BIGSERIAL        NOT NULL,
      CONTENT         TEXT,
      CREATE_AT       DATE,
      LIKE_COUNT      INT,
      RETWEET_COUNT   INT,
      REPLIE_COUNT   INT,
      IMAGE_URL       VARCHAR(300),
      LINK            VARCHAR(300),
      PRIMARY KEY (ID),
      FOREIGN KEY (USER_ID) REFERENCES TWEETER(ID));''')  

cur.execute('''create table location(
	ID       BIGSERIAL NOT NULL,
    KEYWORD  VARCHAR(100) NOT NULL,
    LOCATION VARCHAR(100) ,
    USER_ID  BIGSERIAL NOT NULL,
  	PRIMARY KEY (ID),
    FOREIGN KEY (USER_ID)  REFERENCES TWEETER(ID));''')  
print("Table created successfully")

conn.commit()
conn.close()