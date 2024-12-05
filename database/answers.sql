-- check if given answer is correct
SELECT a_isCorrect FROM ANSWERS JOIN Questions ON q_questionid = a_questionid WHERE a_answerid = :a_answerid: AND q_questionid = :q_questionid;

-- return correct answer given question id
SELECT a_answertext FROM Answers JOIN Questions ON a_questionid = q_questionid WHERE a_isCorrect = :a_isCorrect: AND a_questionid = :a_questionid;
