-- select all questions given category
SELECT q_questionText FROM Questions WHERE q_category = :q_category:;

-- select all questions
SELECT q_questionText FROM Questions;

-- return hint given q id
SELECT q_hint FROM Questions WHERE q_questionid = :q_questionid:;
