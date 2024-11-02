-- insert player and session into plays
INSERT INTO Player(p_userid, p_sessionId, p_score) VALUES(:p_userid:, :p_sessionId:, :p_score:);

-- update user's session score if answer is correct
UPDATE Plays SET p_score = p_score + 1 WHERE p_userid = :p_userid: AND p_sessionid = :p_sessionId:;

-- return winner in current session
SELECT p_userid FROM Plays WHERE p_score = (SELECT MAX(p_score) FROM Plays);
