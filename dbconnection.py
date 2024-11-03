import psycopg2
import os

# set environment variables like:
# EXPORT DBUSER = "postgres" 
# etc

def main():
    conn_string = f"host='localhost' dbname='{os.environ['DBNAME']}' user='{os.environ['DBUSER']}' password='{os.environ['DBPASS']}'"
    print(f"Connecting to database...\n {conn_string}")
    conn = psycopg2.connect(conn_string)
    # use cursor obj to perform queries
    cursor = conn.cursor()
    print("Connected!")

    # create tables
    cursor.execute(open("database/schema.sql", "r").read())
if __name__ == "__main__":
    main()