-- select top player overall
SELECT u_userid FROM Users WHERE u_totalScore = (SELECT MAX(u_totalScore) FROM Users);

-- delete user
DELETE FROM Users WHERE u_userid = :u_userid:;

-- insert user
INSERT INTO Users(u_userid, u_totalScore, u_username) VALUES(:u_userid:, :u_totalScore:, :u_username:);

-- update user's score
UPDATE Users SET u_totalScore = u_totalScore + 1 WHERE u_userid = :u_userid:;
