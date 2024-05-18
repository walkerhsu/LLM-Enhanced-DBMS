/* create and use database */
CREATE DATABASE `Working_Interview_Map_DB`; 
USE `Working_Interview_Map_DB`;


/* info */
CREATE TABLE `self` (
    `student_ID` varchar(10) NOT NULL,
	`name` varchar(10) NOT NULL,
    `department` varchar(10) NOT NULL,
    `year` int DEFAULT 1,
    PRIMARY KEY (`student_ID`)
);

INSERT INTO self
VALUES ('b10901036', '許景淯', '電機系', 3);

SELECT DATABASE();
SELECT * FROM self;


/* create table */
CREATE TABLE `student`(
	`student_ID` VARCHAR(15) PRIMARY KEY NOT NULL,
    `school` VARCHAR(40) NOT NULL,
    `name` VARCHAR(20) NOT NULL,
    `department` VARCHAR(20) NOT NULL,
    `year` INT NOT NULL DEFAULT 1,
    `age` INT NOT NULL DEFAULT 18
);

CREATE TABLE `recommender`(
	`recommender_ID` VARCHAR(15) PRIMARY KEY NOT NULL,
	`is_employee` BOOLEAN NOT NULL DEFAULT FALSE,
	`is_teacher` BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT `recommender_check` CHECK (`is_employee` != `is_teacher`)
);


CREATE TABLE `teacher` (
	`teacher_ID` VARCHAR(15) PRIMARY KEY NOT NULL,
    `name` VARCHAR(20) NOT NULL,
    `graduate_school` VARCHAR(40) NOT NULL,
    `research_domain` VARCHAR(100) NOT NULL,
    `lab_location` VARCHAR(20) NOT NULL,
    `recommender_ID` VARCHAR(15) DEFAULT NULL,
    CONSTRAINT `recommender_teacher_FK` FOREIGN KEY (`recommender_ID`) REFERENCES `recommender`(`recommender_ID`)
);

CREATE TABLE `employee`(
	`employee_ID` VARCHAR(15) PRIMARY KEY NOT NULL,
    `name` VARCHAR(20) NOT NULL,
    `workload` ENUM("low", "medium", "high") DEFAULT "medium" NOT NULL,
    `employed_type` ENUM("full_time", "intern") DEFAULT "intern" NOT NULL,
    `is_RD` BOOLEAN NOT NULL DEFAULT FALSE,
    `is_PM` BOOLEAN NOT NULL DEFAULT FALSE,
    `recommender_ID` VARCHAR(15) DEFAULT NULL,
    CONSTRAINT `recommender_emp_FK` FOREIGN KEY (`recommender_ID`) REFERENCES `recommender`(`recommender_ID`),
    CONSTRAINT `job_type_check` CHECK (`is_RD` = TRUE OR `is_PM` = TRUE)
);

CREATE TABLE `RD` (
	`employee_ID` VARCHAR(15) PRIMARY KEY NOT NULL,
    `project` VARCHAR(100) NOT NULL,
    `coding_language` VARCHAR(50) NOT NULL DEFAULT "Python",
    CONSTRAINT `RD_FK` FOREIGN KEY (`employee_ID`) REFERENCES `employee`(`employee_ID`)
);

CREATE TABLE `PM` (
	`employee_ID` VARCHAR(15) PRIMARY KEY,
    `product` VARCHAR(100) NOT NULL,
    `product_progress` ENUM("not started", "in progress", "completed") DEFAULT "not started" NOT NULL,
    CONSTRAINT `PM_FK` FOREIGN KEY (`employee_ID`) REFERENCES `employee` (`employee_ID`)
)

CREATE TABLE `intern` (
	`employee_ID` VARCHAR(15) PRIMARY KEY NOT NULL,
    `hourly_pay` INT NOT NULL DEFAULT 183,
    CONSTRAINT `hourly_pay_check` CHECK (`hourly_pay` >= 183),
    CONSTRAINT `intern_FK` FOREIGN KEY (`employee_ID`) REFERENCES `employee`(`employee_ID`)
);


CREATE TABLE `full_time` (
	`employee_ID` VARCHAR(15) PRIMARY KEY NOT NULL,
    `salary` INT NOT NULL DEFAULT 27470,
    CONSTRAINT `salary_check` CHECK (`salary` >= 27470),
    CONSTRAINT `full_time_FK` FOREIGN KEY (`employee_ID`) REFERENCES `employee`(`employee_ID`)
);

CREATE TABLE `company`(
	`name` VARCHAR(50) PRIMARY KEY NOT NULL,
    `website_link` VARCHAR(200) DEFAULT NULL,
    `location` VARCHAR (200) DEFAULT NULL
);

CREATE TABLE `emp_work_com`(
    `employee_ID` VARCHAR(15) NOT NULL,
    `company_name` VARCHAR(50) NOT NULL,
    `work_duration` DECIMAL(2,1) NOT NULL DEFAULT 1.0,
    CONSTRAINT `emp_work_com_PK` PRIMARY KEY (`employee_ID`, `company_name`),
    CONSTRAINT `emp_work_com_emp_FK` FOREIGN KEY (`employee_ID`) REFERENCES `employee`(`employee_ID`),
    CONSTRAINT `emp_work_com_com_FK` FOREIGN KEY (`company_name`) REFERENCES `company`(`name`)
);

CREATE TABLE `com_cooperate_com`(
    `company_name_1` VARCHAR(15) NOT NULL,
    `company_name_2` VARCHAR(50) NOT NULL,
    CONSTRAINT `com_cooperate_com_PK` PRIMARY KEY (`company_name_1`, `company_name_2`),
    CONSTRAINT `com_cooperate_com_com1_FK` FOREIGN KEY (`company_name_1`) REFERENCES `company`(`name`),
    CONSTRAINT `com_cooperate_com_com2_FK` FOREIGN KEY (`company_name_2`) REFERENCES `company`(`name`)
);

CREATE TABLE `courses`(
	`ID` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    `course_name` VARCHAR(30) NOT NULL,
	`school` VARCHAR(20) NOT NULL DEFAULT "NTU",
    `course_type` ENUM("required", "optional") NOT NULL DEFAULT "required",
    `recommender` VARCHAR(15) NOT NULL,
    `teacher_ID` VARCHAR(15) NOT NULL,
    CONSTRAINT `recommend_course_FK` FOREIGN KEY (`recommender`) REFERENCES `employee` (`employee_ID`),
    CONSTRAINT `teach_course_FK` FOREIGN KEY (`teacher_ID`) REFERENCES `teacher` (`teacher_ID`)
);

CREATE TABLE `recommend_course_reason`(
	`reason_ID` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    `reason` VARCHAR(100) NOT NULL,
    `course_ID` INT,
    CONSTRAINT `recommend_course_reason_FK` FOREIGN KEY (`course_ID`) REFERENCES `courses` (`ID`)
);

CREATE TABLE `recommender_employee`(
    `recommender_employee_ID` INT PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
    `recommender_ID` VARCHAR(15) NOT NULL,
    `employee_ID` VARCHAR(15) NOT NULL,
    CONSTRAINT `recommender_employee_recommender_FK` FOREIGN KEY (`recommender_ID`) REFERENCES `recommender`(`recommender_ID`),
    CONSTRAINT `recommender_employee_employee_FK` FOREIGN KEY (`employee_ID`) REFERENCES `employee`(`employee_ID`)
);

CREATE TABLE `recommend_employee_reason`(
	`reason_ID` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    `reason` VARCHAR(100) NOT NULL,
    `recommender_employee_ID` INT NOT NULL,
    CONSTRAINT `recommend_emp_reason_FK` FOREIGN KEY (`recommender_employee_ID`) REFERENCES `recommender_employee` (`recommender_employee_ID`)
);

CREATE TABLE `working_interview`(
	`interview_ID` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    `time` DATE NOT NULL,
    `form` ENUM("online", "physical", "both") DEFAULT "physical" NOT NULL,
    `student_ID` VARCHAR(15) NOT NULL,
    `employee_ID` VARCHAR(15) NOT NULL,
    CONSTRAINT `student_interview_FK` FOREIGN KEY (`student_ID`) REFERENCES `student`(`student_ID`)
);


/* insert */
INSERT INTO `student`
VALUES 
('b10901036', 'NTU', 'Walker', 'EE', 3, 20),
('b10901039', 'NTU', 'David', 'EE', 3, 21),
('b11901174', 'NTU', 'Oscar', 'EE', 2, 20);

Insert INTO `teacher`
VALUES
('t123456789', '李琳山', 'Stanford', 'Computer Processing of Speech Signals', 'EE2-520', DEFAULT);

INSERT INTO `recommender`
VALUES
('t987654321', FALSE, TRUE),
('t224466880', FALSE, TRUE),
('e222222222', TRUE, FALSE);;

Insert INTO `teacher`
VALUE
('t987654321', '李宏毅', 'NTU', 'AI', 'EE2-508', 't987654321'),
('t224466880', '葉丙成', 'University of Michigan', 'Wireless Networks', 'EE2-248', 't224466880');

INSERT INTO `employee`
VALUES
('e111111111', '劉一', 'low', 'intern',         TRUE , FALSE, DEFAULT),
('e222222222', '陳二', 'medium', 'full_time',   TRUE , FALSE, 'e222222222'),
('e333333333', '張三', 'high', 'full_time',     TRUE , TRUE, DEFAULT),
('e444444444', '李四', 'medium', 'intern',      FALSE, TRUE, DEFAULT),
('e555555555', '王五', 'low', 'intern',         FALSE, TRUE, DEFAULT),
('e666666666', '趙六', 'medium', 'full_time',   TRUE , FALSE, DEFAULT);

INSERT INTO `RD`
VALUES
('e111111111', 'prompt engineering for LLM', 'Python'),
('e222222222', 'BlueVista app development', 'Flutter & Firebase'),
('e333333333', 'Database for Working Interview Map', 'MySQL'),
('e666666666', 'Dijkstra algorithm for computer network', 'C++ & GoLang');

INSERT INTO `PM`
VALUES
('e333333333', 'Working Interview Map', 'completed'),
('e444444444', 'EEVOLUTION Club', DEFAULT),
('e555555555', 'LightDance App', 'in progress');

INSERT INTO `intern`
VALUES
('e111111111', 250),
('e444444444', 240),
('e555555555', 230);

INSERT INTO `full_time`
VALUES
('e222222222', 45000),
('e333333333', 80000),
('e666666666', 58000);

INSERT INTO `company`
VALUES
('Google_Software', 'https://buildyourfuture.withgoogle.com/internships', '220新北市板橋區遠東路66號'),
('Google_Hardware', 'https://buildyourfuture.withgoogle.com/internships', '110615台北市信義區信義路五段7號73樓'),
('Microsoft', 'https://www.microsoft.com/taiwan/campus/', '110台北市信義區忠孝東路五段68號19樓'),
('Line', 'https://techblog.lycorp.co.jp/zh-hant/line-tech-fresh-2024-summer', '114台北市內湖區瑞光路333號'),
('WorldQuant', 'https://www.worldquant.com/', '110台北市信義區松高路1號19樓');

INSERT INTO `emp_work_com`
VALUES
('e111111111', 'Google_Software', 0.2),
('e222222222', 'Google_Software', 4),
('e333333333', 'Microsoft', 3),
('e333333333', 'Line', DEFAULT),
('e444444444', 'WorldQuant', 0.2),
('e555555555', 'Line', DEFAULT),
('e666666666', 'Google_Hardware', 2);

INSERT INTO `com_cooperate_com`
VALUES
('Google_Software', 'Google_Hardware'),
('Microsoft', 'Line'),
('Google_Software', 'Line');

INSERT INTO `courses`
VALUES
(DEFAULT, '生成式AI', 'NTU', "optional", 'e111111111', 't987654321');

INSERT INTO `recommend_course_reason`
VALUES
(DEFAULT, 'GenAI為目前的趨勢，必須要會', last_insert_id()),
(DEFAULT, '一堂課2000個同學修課/旁聽，肯定是好課！', last_insert_id());

INSERT INTO `courses`
VALUES
(DEFAULT, '機率與統計', 'NTU', DEFAULT, 'e333333333', 't224466880');

INSERT INTO `recommend_course_reason`
VALUES
(DEFAULT, '翻轉教育很棒', last_insert_id()),
(DEFAULT, '機率到處都用得到，跟信號系統一樣重要', last_insert_id());

INSERT INTO `courses`
VALUES
(DEFAULT, '信號與系統', 'NTU', DEFAULT, 'e666666666', 't123456789');

INSERT INTO `recommend_course_reason`
VALUES
(DEFAULT, '老師教學風趣', last_insert_id()),
(DEFAULT, '課程內容豐富，對於未來相當有幫助', last_insert_id());

INSERT INTO `recommender_employee`
VALUE
(DEFAULT, 't987654321', 'e111111111');

INSERT INTO `recommend_employee_reason`
VALUE
(DEFAULT, '劉一在校成績優異，學習能力佳', last_insert_id()),
(DEFAULT, '劉一對機器學習相當了解。', last_insert_id());

INSERT INTO `recommender_employee`
VALUE
(DEFAULT, 't224466880', 'e333333333');

INSERT INTO `recommend_employee_reason`
VALUE
(DEFAULT, '張三擁有追根究底的精神。', last_insert_id()),
(DEFAULT, '張三對Database相當了解。', last_insert_id());

INSERT INTO `recommender_employee`
VALUE
(DEFAULT, 'e222222222', 'e666666666');

INSERT INTO `recommend_employee_reason`
VALUE
(DEFAULT, '趙六熱愛參加黑客松競賽，對於硬體技術相當有自信。', last_insert_id());

INSERT INTO `working_interview`
VALUES
(DEFAULT, '2023-12-31', 'online', 'b10901036', 'e111111111'),
(DEFAULT, '2024-01-01', 'both', 'b10901036', 'e222222222'),
(DEFAULT, '2024-02-01', DEFAULT, 'b10901039', 'e333333333'),
(DEFAULT, '2024-02-27', DEFAULT, 'b11901174', 'e444444444'),
(DEFAULT, '2024-03-01', DEFAULT, 'b11901174', 'e555555555'),
(DEFAULT, '2024-03-27', 'online', 'b10901039', 'e666666666');


/* create two views (Each view should be based on two tables.)*/
CREATE VIEW `courses_view` AS
SELECT courses.course_name, teacher.name, courses.course_type
FROM courses, teacher
WHERE courses.teacher_ID = teacher.teacher_ID;

CREATE VIEW `interns_view` AS
SELECT employee.name, employee.workload, intern.hourly_pay
FROM employee, intern
WHERE employee.employee_ID = intern.employee_ID;


/* select from all tables and views */
SELECT * FROM `student`;    
SELECT * FROM `recommender`;
SELECT * FROM `teacher`;
SELECT * FROM `employee`;
SELECT * FROM `RD`;
SELECT * FROM `PM`;
SELECT * FROM `intern`;
SELECT * FROM `full_time`;
SELECT * FROM `company`;
SELECT * FROM `emp_work_com`;
SELECT * FROM `com_cooperate_com`;
SELECT * FROM `courses`;
SELECT * FROM `recommend_course_reason`;
SELECT * FROM `recommender_employee`;
SELECT * FROM `recommend_employee_reason`;
SELECT * FROM `working_interview`;
SELECT * FROM `courses_view`;
SELECT * FROM `interns_view`;


/* drop database */
DROP DATABASE IF EXISTS `Working_Interview_Map_DB`;