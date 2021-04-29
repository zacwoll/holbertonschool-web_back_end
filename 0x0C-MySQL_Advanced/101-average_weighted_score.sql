-- Compute and store the average weighted score for a student
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (
       IN user_id INT
)
BEGIN

UPDATE users
SET average_score = (SELECT SUM(score * weight) / (SELECT SUM(weight))
FROM projects
INNER JOIN corrections
WHERE projects.id = corrections.project_id
AND corrections.user_id = user_id)
WHERE users.id = user_id;

END;//

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
DECLARE done BOOLEAN DEFAULT 0;
DECLARE user_id INT;
DECLARE all_users CURSOR FOR SELECT id FROM users;
-- SQLSTATE '02000' is no more data'
DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;

OPEN all_users;
REPEAT
    FETCH all_users INTO user_id;
    CALL ComputeAverageWeightedScoreForUser(user_id);
UNTIL done END REPEAT;
CLOSE all_users;

END;//
DELIMITER ;