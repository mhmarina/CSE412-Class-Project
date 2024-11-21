import csv
import psycopg2
import os
import datetime

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

    def insert_trivia_session(self, session_id: int, start_time: datetime.datetime) -> None:
        """
        Inserts a new trivia session into the `triviasession` table.

        :param session_id: Unique ID for the trivia session.
        :param start_time: Start time of the session.
        """
        query = """
        INSERT INTO triviasession (t_sessionid, t_starttime)
        VALUES (%s, %s)
        """
        try:
            self.cursor.execute(query, (session_id, start_time))
            self.conn.commit()
            print(f"Trivia session {session_id} started at {start_time} has been inserted into the database.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error inserting trivia session: {e}")

    def get_random_question(self):
        """
        Fetch a random question from the Questions table.

        :return: A tuple containing the question details (id, hint, category, text), or None if no questions are available.
        """
        query = """
        SELECT q_questionid, q_hint, q_category, q_questiontext
        FROM questions
        ORDER BY RANDOM()
        LIMIT 1
        """
        try:
            self.cursor.execute(query)
            question = self.cursor.fetchone()
            if question:
                return question  # Returns a tuple (id, hint, category, questiontext)
            else:
                print("No questions available in the database.")
                return None
        except Exception as e:
            print(f"Error fetching random question: {e}")
            return None

    def insert_asked(self, session_id, question_id, answered_by, answer, is_correct):
        try:
            # Step 1: Ensure the user exists in the `Users` table
            self.cursor.execute(
                '''
                SELECT COUNT(*) FROM users WHERE u_userid = %s;
                ''',
                [answered_by]
            )
            user_exists = self.cursor.fetchone()[0]

            if not user_exists:
                # If the user does not exist, insert the user with default values
                self.cursor.execute(
                    '''
                    INSERT INTO users (u_userid, u_totalScore, u_username) 
                    VALUES (%s, %s, %s);
                    ''',
                    [answered_by, 0, f"User_{answered_by}"]  # Default username
                )
                self.conn.commit()
                print(f"Inserted new user: {answered_by}")

            # Step 2: Insert the `asked` entry
            self.cursor.execute(
                '''
                INSERT INTO asked (as_sessionid, as_questionid, as_answeredby, as_answer, as_iscorrect) 
                VALUES (%s, %s, %s, %s, %s);
                ''',
                [session_id, question_id, answered_by, answer, is_correct]
            )
            self.conn.commit()
            print(f"Inserted asked entry for session {session_id}, question {question_id}, answered by {answered_by}")

        except Exception as e:
            self.conn.rollback()
            print(f"Error inserting/updating asked entry: {e}")

    def get_answers_for_question(self, question_id):
        """
        Fetch all answers for a given question ID from the Answers table.
        """
        try:
            self.cursor.execute('''
                SELECT a_answerid, a_questionid, a_answertext, a_iscorrect
                FROM answers
                WHERE a_questionid = %s;
            ''', (question_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching answers for question {question_id}: {e}")
            return None
        
    def insert_asked(self, session_id, question_id, answered_by, answer, is_correct):
        """
        Insert or update an entry in the asked table.
        """
        try:
            # Check if the question was already inserted
            self.cursor.execute('''
                SELECT 1 
                FROM asked 
                WHERE as_sessionid = %s AND as_questionid = %s AND as_answeredby = %s;
            ''', (session_id, question_id, answered_by))
            exists = self.cursor.fetchone()

            if exists:
                # Update the record if it already exists
                self.cursor.execute('''
                    UPDATE asked
                    SET as_answer = %s, as_iscorrect = %s
                    WHERE as_sessionid = %s AND as_questionid = %s AND as_answeredby = %s;
                ''', (answer, is_correct, session_id, question_id, answered_by))
            else:
                # Insert a new record
                self.cursor.execute('''
                    INSERT INTO asked (as_sessionid, as_questionid, as_answeredby, as_answer, as_iscorrect)
                    VALUES (%s, %s, %s, %s, %s);
                ''', (session_id, question_id, answered_by, answer, is_correct))
            
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error inserting/updating asked entry: {e}")

    def insert_play(self, user_id, session_id, points):
        """
        Update the user's score in the Users table for a given session.
        """
        try:
            # Update the user's total score
            self.cursor.execute('''
                UPDATE users
                SET u_totalScore = u_totalScore + %s
                WHERE u_userid = %s;
            ''', (points, user_id))
            
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating play: {e}")

    def insert_user(self, u_userid, u_username):
        try:
            self.cursor.execute('''
            INSERT INTO users (u_userid, u_totalscore, u_username)
            VALUES (%s, %s, %s);
            ''', [u_userid, 0, u_username])
            self.conn.commit()
            print(f"User {u_username} (ID: {u_userid}) inserted successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error inserting user: {e}")

    def get_answers_for_question(self, question_id):
        """Fetch multiple-choice answers for a given question."""
        try:
            self.cursor.execute('''
                SELECT a_answerid, a_questionid, a_answertext, a_iscorrect
                FROM answers
                WHERE a_questionid = %s
                ORDER BY a_answerid
            ''', [question_id])
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching answers for question {question_id}: {e}")
            return []
        
    def update_asked(self, session_id, question_id, answered_by, answer, is_correct):
        """Update an entry in the 'asked' table after the user answers the question."""
        try:
            self.cursor.execute('''
                UPDATE asked
                SET as_answer = %s, as_iscorrect = %s
                WHERE as_sessionid = %s AND as_questionid = %s AND as_answeredby = %s
            ''', [answer, is_correct, session_id, question_id, answered_by])
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating asked entry: {e}")

    def get_top_users(self, limit=10):
        """
        Retrieve the top users based on their total score.

        :param limit: The maximum number of users to return.
        :return: A list of tuples containing user information (user_id, username, total_score).
        """
        try:
            self.cursor.execute('''
                SELECT u_userid, u_username, u_totalscore
                FROM users
                ORDER BY u_totalscore DESC
                LIMIT %s;
            ''', (limit,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving top users: {e}")
            return []
        
    def update_session_stop_time(self, session_id, stop_time):
        """
        Update the stop time for a trivia session.

        :param session_id: The ID of the session to update.
        :param stop_time: The stop time to set for the session.
        """
        try:
            self.cursor.execute('''
                UPDATE triviasession
                SET t_stoptime = %s
                WHERE t_sessionid = %s;
            ''', (stop_time, session_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating session stop time: {e}")

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
