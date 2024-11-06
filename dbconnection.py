import csv
import psycopg2
import os

# set environment variables like:
# EXPORT DBUSER = "postgres" 
# etc

def main():
    conn_string = f"host='localhost' dbname='{os.environ['DBNAME']}' user='{os.environ['DBUSER']}' password='{os.environ['DBPASS']}'"
    print(f"Connecting to database...\n {conn_string}")
    conn = None
    try:
        conn = psycopg2.connect(conn_string)
        print("Connected!")
        # use cursor obj to perform queries
        cursor = conn.cursor()
        # create tables if they do not exist
        # read CREATE queries from schema.sql
        cursor.execute(open("database/schema.sql", "r").read())
        conn.commit()
        # check if questions table exists
        cursor.execute('''
                        SELECT COUNT(1) WHERE EXISTS (SELECT * FROM Questions)
                            ''')
        questions_exist = cursor.fetchone()[0]
        # populate questions and answers
        if not questions_exist:
            with open('database/Questions.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    cursor.execute('''
                        INSERT INTO Questions VALUES (%s, %s, %s, %s)
                    ''', row
                )
            conn.commit()
            with open('database/Answers.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader) # Skip the header row.
                for row in reader:
                    cursor.execute('''
                        INSERT INTO Answers VALUES (%s, %s, %s, %s)
                    ''', row
                )
            conn.commit()
        else:
            print("Questions (and answers) table already populated")
        # test
        cursor.execute("SELECT * FROM Questions")
        questions = cursor.fetchall()
        for question in questions:
            print(question)

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(e)
    finally:
        if(conn):
            conn.close()
            print("Connection closed")

    # create tables
if __name__ == "__main__":
    main()