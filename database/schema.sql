CREATE TABLE IF NOT EXISTS Users (
    u_userid BIGINT PRIMARY KEY,
    u_totalScore INTEGER,
    u_username VARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS TriviaSession (
	t_sessionid BIGINT PRIMARY KEY,
	t_startTime TIMESTAMP,
	t_stopTime TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Plays (
	p_userid BIGINT,
	p_sessionId BIGINT,
	p_score INTEGER,
	PRIMARY KEY (p_userid, p_sessionId),
	FOREIGN KEY (p_userid) REFERENCES Users(u_userid) ON DELETE CASCADE,
	FOREIGN KEY (p_sessionId) REFERENCES TriviaSession(t_sessionid)ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Questions (
	q_questionid INTEGER PRIMARY KEY,
	q_hint VARCHAR(255),
	q_category VARCHAR(255),
	q_questionText VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Answers (
	a_answerid CHAR(1),
	a_questionid INTEGER,
	a_answertext VARCHAR(255) NOT NULL,
a_isCorrect BOOLEAN,
	PRIMARY KEY (a_answerid, a_questionid),
	FOREIGN KEY (a_questionid) REFERENCES Questions(q_questionid)ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS Asked (
	as_sessionid BIGINT,
	as_questionid INTEGER,
	as_answeredby BIGINT,
	as_answer CHAR(1),
	as_iscorrect BOOLEAN,
	PRIMARY KEY (as_sessionid, as_questionid, as_answeredby),
	FOREIGN KEY (as_sessionid) REFERENCES TriviaSession(t_sessionid),
	FOREIGN KEY (as_questionid) REFERENCES Questions(q_questionid),
	FOREIGN KEY (as_answeredby) REFERENCES Users(u_userid)
);
