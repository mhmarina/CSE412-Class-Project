-- Add given valid response to “asked” table (correct or incorrect)
INSERT INTO Asked(as_sessionid, as_questionid, as_answeredby, as_answer, as_iscorrect) VALUES(:as_sessionid:, :as_questionid:, :as_answeredby:, :as_answer:, :as_iscorrect:);
