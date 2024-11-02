-- Insert/ create new session
INSERT INTO TriviaSession(t_sessionid, t_startTime, t_stopTime) VALUES(:t_sessionid:, :t_startTime:, :t_stopTime:);

-- Delete session given session id
DELETE FROM TriviaSession WHERE t_sessionid = :t_sessionid:;

-- Clear all session
DELETE FROM TriviaSession;