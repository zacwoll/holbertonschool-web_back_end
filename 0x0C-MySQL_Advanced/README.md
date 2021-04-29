# 0x0C. MySQL Advanced
This project is centered around more advanced techniques for using MySQL. These techniques include
- Database Indexing
- Stored Procedures
- Triggers
- Views
- Functions and Operators

## Learning Objectives
- How to create tables with constraints
- How to optimize queries by adding indexes
- What is and how to implement stored procedures and functions in MySQL
- What is and how to implement views in MySQL
- What is and how to implement triggers in MySQL

### Links to resources
[MySQL cheatsheet](https://devhints.io/mysql)
[MySQL Performance: How To Leverage MySQl Database Indexing](https://www.liquidweb.com/kb/mysql-optimization-how-to-leverage-mysql-database-indexing/)
[Stored Procedure](https://www.w3resource.com/mysql/mysql-procedure.php)
[Triggers](https://www.w3resource.com/mysql/mysql-triggers.php)
[Views](https://www.w3resource.com/mysql/mysql-views.php)
[Functions and Operators](https://dev.mysql.com/doc/refman/5.7/en/functions.html)
[Trigger Syntax and Examples](https://dev.mysql.com/doc/refman/5.7/en/trigger-syntax.html)
[CREATE TABLE Statement](https://dev.mysql.com/doc/refman/5.7/en/create-table.html)
[Create PROCEDURE and CREATE FUNCTION Statements](https://dev.mysql.com/doc/refman/5.7/en/create-procedure.html)
[CREATE INDEX Statement](https://dev.mysql.com/doc/refman/5.7/en/create-index.html)
[CREATE VIEW Statement](https://dev.mysql.com/doc/refman/5.7/en/create-view.html)


## 0x0C SQL Advanced Notes
The following is an explanation of the tasks and concepts taught in this project.

### Create a table named 'users'
```
CREATE TABLE \[If NOT EXISTS \] users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
```
This sql block creates a table (if a table with the same name doesn't already exists). id is the primary key we're indexing by, it auto increments and cannot be null. email and name are both fields that the sql entry contains, email cannot be null and must be unique, the same isn't true for name.

### Create a table with an enumerated field
```
CREATE TABLE IF NOT EXISTS users (
       id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
       email VARCHAR(255) NOT NULL UNIQUE,
       name VARCHAR(255),
       country ENUM('US', 'CO', 'TN') NOT NULL
);
```
Here, country is an enumerated fields with the possible options of 'US', 'CO', and 'TN'. It must not be null, which means it defaults to 'US', the first entry in the list, if it's unspecified.

### Create variables in a query
```
SELECT band_name, (IFNULL(split, 2020) - formed) lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
```
IFNULL is a pretty cool sql function that adds a default if there's no value for split in the entries found. lifespan is a variable we created from the arithmetic of `(IFNULL(split, 2020) - formed)`. The LIKE command returns all entries where style includes anything, including nothing, before and after 'Glam rock'.

### Create a Trigger
```
CREATE TRIGGER decrease_quantity
AFTER INSERT
ON orders
FOR EACH ROW
UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name
```
'decrease_quantity' is declared a trigger function in a mysql database as a function that runs an operation, when a new entry is added to orders, update the items in the storage, by setting their quantity to quantity minus the quantity in order, defined as NEW.number, where the name is identical to the new item_name. That was a mouthful, wasn't it.

### Create a Trigger that works conditionally
In this case, we set the new email for a user to 0 because it's being reset.
```
DELIMITER //
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
IF OLD.email <> NEW.email THEN
SET NEW.valid_email = 0;
END IF;
END;//
DELIMITER ;
```
The DELIMETER command changes what mysql interprets as the end of the line. This enables the ; delimiter used in the procedure body to be passed through to the server rather than being interpreted by mysql itself. Convention is to change the delimeter back to semicolon at the end of the trigger

### Create a PROCEDURE
A procedure is a series of statements encapsulated for use within the database. Procedures have a few benefits
1. Reduce the Network Traffic: Multiple SQL Statements are encapsulated in a stored procedure. When you execute it, instead of sending multiple queries, we are sending only the name and the parameters of the stored procedure
2. Easy to maintain: The stored procedure are reusable. We can implement the business logic within an SP, and it can be used by applications multiple times, or different modules of an application can use the same procedure. This way, a stored procedure makes the database more consistent. If any change is required, you need to make a change in the stored procedure only
3. Secure: The stored procedures are more secure than the AdHoc queries. The permission can be granted to the user to execute the stored procedure without giving permission to the tables used in the stored procedure. The stored procedure helps to prevent the database from SQL Injection

```
DELIMITER //
DROP PROCEDURE IF EXISTS AddBonus;
CREATE PROCEDURE AddBonus (
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN

INSERT INTO projects(name)
SELECT project_name
WHERE NOT EXISTS (SELECT * FROM projects WHERE name = project_name LIMIT 1);

INSERT INTO corrections(user_id, project_id, score)
VALUES (user_id, (SELECT id FROM projects WHERE name = project_name), score);

END;//
DELIMITER ;
```
In this code block, we create the procedure AddBonus, which adds score to a user's project. The Procedure takes in parameters of an id, a project name, and a score to add to the project, stored in anoother table called corrections. Utilizing this procedure, we simply insert into the corrections table the score given for the project.

### Create another procedure
```
-- Compute and store the average score for a student
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser
CREATE PROCEDURE Computer AverageScoreForUser (
    IN user_id INT
)
BEGIN

UPDATE users
SET average_score = (
    SELECT AVG(score) FROM corrections WHERE corrections.user_id = user_id
)
WHERE id = user_id;

END;//
DELIMITER ;
```
Same idea, when using this procedure, update users with a new average score from corrections.

### Create an Index
The CREATE INDEX statement is used to create indexes in tables.

Indexes are used to retrieve data from the database more quickly than otherwise. The users cannot see the indexes, they are just used to speed up searches/queries.

```
-- Create an index on the table names and the first letter of name
CREATE INDEX idx_name_first
ON names (name(1));
```

### Create a multi value index
```
-- Create an index on the table names and the first letter of name and score
CREATE INDEX idx_name_first_score
ON names (name(1), score);
```

### Create a Function
A function is a set of SQL statements that perform a specific task. Functions foster code reusability. If you have to repeatedly write large SQL scripts to perform the same task, you can create a function that performs that task. Next time instead of rewriting the SQL, you can simply call that function. A function accepts inputs in the form of parameters and returns a value. SQL Server comes with a set of built-in functions that perform a variety of tasks.

Of course, you could create a stored procedure to group a set of SQL statements and execute them, however, stored procedures cannot be called within SQL statements. Functions, on the other hand, can be. Also, another issue with functions is that they have to be called for each row. Therefore, if you are using functions with large data sets, you can hit performance issues.

```
-- Divide the first number by the second, or return 0 if the second number is 0
DELIMITER //
DROP FUNCTION IF EXISTS SafeDiv;
CREATE FUNCTION SafeDiv(
       a INT,
       b INT
)
RETURNS FLOAT
DETERMINISTIC
BEGIN

IF b = 0 THEN
   RETURN 0;
END IF;
RETURN a / b;

END;//
DELIMITER ;
```

This function is DETERMINISTIC, which means results won't be ran on the same data twice, the result is stored and presented every time it's asked for afterwards.

### Create a View
A view is a virtual table based on the result set of an SQL statement.
```
-- List all students with a score under 80 and no meetings in the past month
DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE SCORE < 80
AND last_meeting IS NULL
OR last_meeting < DATE_SUB(NOW(), INTERVAL 1 MONTH);
```

### More Procedures
#### Task 100
```
-- Compute and store the average weighted score for a student
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
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
DELIMITER ;
```
Here a new procedure is created to compute the average weighted score for a user. The next task will use this procedure on all data until it runs out of data. That condition, running out of data, is represented by SQLSTATE '02000' which requires defining something called a "HANDLER" for dealing with errors like that one, should it present itself.

#### Task 101
```
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
    CALL ComputerAverageWeightedScoreForUser(user_id);
UNTIL done END REPEAT;
CLOSE all_users;

END;//
DELIMITER ;
```