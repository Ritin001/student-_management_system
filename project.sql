CREATE DATABASE IF NOT EXISTS school_db;
USE school_db;

CREATE USER IF NOT EXISTS 'project'@'localhost' IDENTIFIED BY 'ritin150';
GRANT ALL PRIVILEGES ON school_db.* TO 'project'@'localhost';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'project'@'localhost';

DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS marks;
DROP TABLE IF EXISTS sports;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    student_class VARCHAR(50)
);

CREATE TABLE marks (
    student_id INT,
    subject VARCHAR(100),
    marks INT,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE attendance (
    student_id INT,
    date DATE,
    status VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

CREATE TABLE sports (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    sports_name VARCHAR(100),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

INSERT INTO students (name, age, student_class) VALUES
('John Doe', 15, '10th Grade'),
('Jane Smith', 14, '9th Grade'),
('Mike Johnson', 16, '11th Grade'),
('Emily Davis', 14, '9th Grade');

INSERT INTO marks (student_id, subject, marks) VALUES
(1, 'Mathematics', 85),
(1, 'Science', 90),
(2, 'Mathematics', 75),
(2, 'Science', 80),
(3, 'Mathematics', 95),
(3, 'Science', 88),
(4, 'Mathematics', 78),
(4, 'Science', 82);

INSERT INTO attendance (student_id, date, status) VALUES
(1, '2025-02-18', 'Present'),
(2, '2025-02-18', 'Absent'),
(3, '2025-02-18', 'Present'),
(4, '2025-02-18', 'Present');

INSERT INTO sports (student_id, name, sports_name) VALUES
(1, 'John Doe', 'Football'),
(2, 'Jane Smith', 'Basketball'),
(3, 'Mike Johnson', 'Cricket'),
(4, 'Emily Davis', 'Badminton');

SELECT * FROM students;
INSERT INTO students (name, age, student_class)
VALUES ('ritin', 19, '12th Grade');




SELECT * FROM students;
DELETE FROM students
WHERE id = 6;




SELECT * FROM students;
UPDATE students
SET name = 'Jane Doe', student_class = '12th Grade'
WHERE id = 3;


show tables;
CREATE TABLE demo (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    sports_name VARCHAR(100),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);
drop table demo;


