import csv
import psycopg2
import os

# set environment variables like:
# export DBUSER="postgres" 
# etc

class DBManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect_and_init(self):
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
            
            self.conn = conn
            self.cursor = cursor

        except psycopg2.Error as e:
            self.close_connection()
            print(f"Database error: {e}")
        except Exception as e:
            self.close_connection()
            print(e)

    def close_connection(self):
        if(self.conn):
            self.conn.close()
            print("connection closed")
        
    def insert_user(self, u_userid, u_username):
        self.cursor.execute('''
        INSERT INTO Users(u_userid, u_totalScore, u_username) VALUES(%s, %s, %s);
        ''', [u_userid, 0, u_username])
        self.conn.commit()

    def delete_user(self, u_userid):
        self.cursor.execute('''
        DELETE FROM Users where u_userid = %s;
        ''', [u_userid])
        self.conn.commit()

    def select_top_players(self):
        self.cursor.execute('''
        SELECT u_userid FROM Users WHERE u_totalScore = (SELECT MAX(u_totalScore) FROM Users);  
        ''')
        return self.cursor.fetchall()
    
    def update_user_score(self, u_userid):
        self.cursor.execute('''
        UPDATE Users SET u_totalScore = u_totalscore+1 WHERE u_userid = %s;
        ''', [u_userid])
        self.conn.commit()

# test:
def main():
    db = DBManager()
    db.connect_and_init()
    db.insert_user("1020192", "marina239")
    print(db.select_top_players())
    db.update_user_score("1020192")
    db.update_user_score("1020192")
    db.update_user_score("1020192")
    db.insert_user("29", "pizzakdj")
    print(db.select_top_players())
    db.delete_user("1020192")
    print(db.select_top_players())
    db.insert_user("1020192", "marina239")
    print(db.select_top_players())

if __name__ == "__main__":
    main()
