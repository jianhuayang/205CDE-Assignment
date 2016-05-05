DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS contact;
DROP TABLE IF EXISTS mailing;
DROP TRIGGER IF EXISTS mailingTrigger;

CREATE TABLE `user` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`first_name`	VARCHAR(100),
	`last_name`	VARCHAR(100),
	`login`	VARCHAR(50) UNIQUE,
	`email`	VARCHAR(120),
	`password`	VARCHAR(64)
);

INSERT INTO `user` (id,first_name,last_name,login,email,password) VALUES 
(1,'Test','User','test','test@gmail.com','pbkdf2:sha1:1000$6Gjda7cd$9308c9dd372b625d99c23d86202869e3bf12ef3e'),
(2,'Benjamin','Bogdanovic','ben','ben@ben.com','pbkdf2:sha1:1000$6Gjda7cd$9308c9dd372b625d99c23d86202869e3bf12ef3e');

CREATE TABLE `contact` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	VARCHAR(100),
	`email`	VARCHAR(150),
	`message`	TEXT,
	`mailing` INTEGER(1)
);

INSERT INTO `contact` (id,name,email,message,mailing) VALUES 
(1,'Benjamin Bogdanovic','benjamin@gmail.com','Best coffee evere!',1),
(2,'Oliver Bogdanovic','oliver@gmail.com','Amazing cofeee!',1),
(3,'Harrison Stevens','harrison.stevens10@hotmail.co.uk','Love the coffee!',1);

CREATE TABLE `mailing` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	VARCHAR(100),
	`email`	VARCHAR(150)
);

INSERT INTO `mailing` (id,name,email) VALUES 
(1,'Benjamin Bogdanovic','benjamin@gmail.com'),
(2,'Oliver Bogdanovic','oliver@gmail.com'),
(3,'Harrison Stevens','harrison.stevens10@hotmail.co.uk');

CREATE TRIGGER `mailingTrigger`
AFTER INSERT ON `contact` 
WHEN new.mailing = 1
BEGIN
INSERT INTO mailing (name, email) VALUES (new.name , new.email);
END;