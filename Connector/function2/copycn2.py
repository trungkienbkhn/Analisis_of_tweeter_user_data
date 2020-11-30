import psycopg2

conn = psycopg2.connect(database = "function2", user = "postgres", password = "s", host = "127.0.0.1", port = "5432")

cur = conn.cursor()

cur.execute(r"COPY tweeter FROM 'C:\Users\kiki\3_hieunk\Connector\function2\Data\user_tablecn2.csv' DELIMITER ',' CSV HEADER;")
conn.commit()
cur.execute(r"COPY tweet FROM 'C:\Users\kiki\3_hieunk\Connector\function2\Data\tweet_tablecn2.csv' DELIMITER ',' CSV HEADER;")
conn.commit()
cur.execute(r"COPY location FROM 'C:\Users\kiki\3_hieunk\Connector\function2\Data\locations.csv' DELIMITER ',' CSV HEADER;")
conn.commit()

print("Operation done successfully")
conn.close()
