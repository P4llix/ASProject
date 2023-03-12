CREATE TABLE `USER` (
  `ROWID` int PRIMARY KEY AUTO_INCREMENT,
  `FIRSTNAME` varchar(255) NOT NULL,
  `LASTNAME` varchar(255) NOT NULL,
  `PHONE` int DEFAULT null,
  `BIRTHDAY` date DEFAULT null,
  `EMAIL` varchar(255) DEFAULT null,
  `STATUS` int DEFAULT 1,
  `COMMENT` varchar(255) DEFAULT null,
  `TIMESTAMP` date DEFAULT (now()),
  `CREATED_BY` int NOT NULL,
  `MODIFIED_DATE` date DEFAULT (now()),
  `MODIFIED_BY` int NOT NULL
);

CREATE TABLE `ROLE` (
  `ROWID` int PRIMARY KEY AUTO_INCREMENT,
  `NAME` varchar(255) NOT NULL,
  `DESCRIPTION` varchar(255) DEFAULT null,
  `STATUS` int DEFAULT 1,
  `TIMESTAMP` DATE DEFAULT (now())
);

CREATE TABLE `USER_ROLE` (
  `ROWID` int PRIMARY KEY AUTO_INCREMENT,
  `USER` int NOT NULL,
  `ROLE` int NOT NULL,
  `STATUS` int NOT NULL,
  `TIMESTAMP` date DEFAULT (now())
);

CREATE TABLE `TASK` (
  `ROWID` int PRIMARY KEY AUTO_INCREMENT,
  `EXERCISE` int,
  `QUANTITY` int NOT NULL,
  `COMMENT` varchar(255) DEFAULT null
);

CREATE TABLE `EXERCISE` (
  `ROWID` int PRIMARY KEY AUTO_INCREMENT,
  `NAME` varchar(255) NOT NULL,
  `DESCRIPTION` varchar(255) DEFAULT null,
  `LINK` varchar(255) DEFAULT null
);

CREATE TABLE `DAILY_TASK` (
  `ROWID` int PRIMARY KEY AUTO_INCREMENT,
  `AUTHOR` int NOT NULL,
  `TASK` int NOT NULL,
  `DATE` date NOT NULL,
  `COMMENT` varchar(255) DEFAULT null
);

CREATE TABLE `USER_DAILY_TASK` (
  `ROWID` int PRIMARY KEY AUTO_INCREMENT,
  `USER` int NOT NULL,
  `JUDGE` int NOT NULL,
  `DAILY_TASK` int NOT NULL,
  `LINK` varchar(255) DEFAULT null,
  `MARK` decimal DEFAULT null,
  `COMMENT` varchar(255) DEFAULT null,
  `TIMESTAMP` date DEFAULT (now()),
  `MODIFIED_DATE` date DEFAULT (now()),
  `MODIFIED_BY` int NOT NULL
);

CREATE TABLE `CREDENTIAL` (
  `ROWID` int PRIMARY KEY AUTO_INCREMENT,
  `USER` int NOT NULL,
  `LOGIN` varchar(255) NOT NULL,
  `PASSWORD` varchar(255) NOT NULL
);




insert into CREDENTIAL (`USER`, `LOGIN`, `PASSWORD`) values (1,'admin','admin');
insert into CREDENTIAL (`USER`, `LOGIN`, `PASSWORD`) values (2,'mod','mod');
insert into CREDENTIAL (`USER`, `LOGIN`, `PASSWORD`) values (3,'user','user');

insert into ROLE (`NAME`, `DESCRIPTION`, `STATUS`) values ('ADMIN','Admin role', 1);
insert into ROLE (`NAME`, `DESCRIPTION`, `STATUS`) values ('USER','User role', 1);
insert into ROLE (`NAME`, `DESCRIPTION`, `STATUS`) values ('MOD','Mod role', 1);

insert into USER 
(`FIRSTNAME`, `LASTNAME`, `PHONE`, `BIRTHDAY`, `EMAIL`, `STATUS`, `CREATED_BY`) values 
('Pabian','Kusek', 111222333, '2000-01-01', 'example@gmail.com', 1, 1);

insert into USER 
(`FIRSTNAME`, `LASTNAME`, `PHONE`, `BIRTHDAY`, `EMAIL`, `STATUS`, `CREATED_BY`) values 
('Bartosz','Oleksa', 333222111, '2001-10-21', 'example2@gmail.com', 1, 1);

insert into USER 
(`FIRSTNAME`, `LASTNAME`, `PHONE`, `BIRTHDAY`, `EMAIL`, `STATUS`, `CREATED_BY`) values 
('Serafin','Lubar', 123456789, '2011-12-19', 'example3@gmail.com', 1, 1);

insert into USER 
(`FIRSTNAME`, `LASTNAME`, `PHONE`, `BIRTHDAY`, `EMAIL`, `STATUS`, `CREATED_BY`) values 
('Lucyna','Kukulska', 098123456, '1998-02-01', 'example4@gmail.com', 1, 2);

insert into USER 
(`FIRSTNAME`, `LASTNAME`, `PHONE`, `BIRTHDAY`, `EMAIL`, `STATUS`, `CREATED_BY`) values 
('Hanna','Minkowska', 123443210, '2001-10-11', 'example5@gmail.com', 1, 2);

insert into USER_ROLE (`USER`, `ROLE`, `STATUS`) values (1, 1, 1);
insert into USER_ROLE (`USER`, `ROLE`, `STATUS`) values (2, 1, 1);
insert into USER_ROLE (`USER`, `ROLE`, `STATUS`) values (3, 2, 1);

insert into EXERCISE (`NAME`, `DESCRIPTION`, `LINK`) values ("Brzuszki", "Brzuszki klasyczne", "link.com");
insert into EXERCISE (`NAME`, `DESCRIPTION`, `LINK`) values ("Pajacyki", "Pajacyki zwykle", "link2.com");
insert into EXERCISE (`NAME`, `DESCRIPTION`, `LINK`) values ("Plank", "Deska", "link3.com");

insert into TASK (`EXERCISE`, `QUANTITY`) values (1, 40);
insert into TASK (`EXERCISE`, `QUANTITY`) values (1, 20);
insert into TASK (`EXERCISE`, `QUANTITY`) values (2, 20);
insert into TASK (`EXERCISE`, `QUANTITY`) values (3, 60);
insert into TASK (`EXERCISE`, `QUANTITY`) values (3, 120);

insert into DAILY_TASK (`AUTHOR`, `TASK`, `DATE`) values (1, 1, "2022-10-16");
insert into DAILY_TASK (`AUTHOR`, `TASK`, `DATE`) values (1, 2, "2022-10-16");
insert into DAILY_TASK (`AUTHOR`, `TASK`, `DATE`) values (1, 2, "2022-10-17");
insert into DAILY_TASK (`AUTHOR`, `TASK`, `DATE`) values (1, 3, "2022-10-17");
insert into DAILY_TASK (`AUTHOR`, `TASK`, `DATE`) values (1, 5, "2022-10-17");
insert into DAILY_TASK (`AUTHOR`, `TASK`, `DATE`) values (1, 4, "2022-10-18");
insert into DAILY_TASK (`AUTHOR`, `TASK`, `DATE`) values (1, 5, "2022-10-18");


ALTER TABLE `USER` ADD FOREIGN KEY (`CREATED_BY`) REFERENCES `USER` (`ROWID`);
ALTER TABLE `USER` ADD FOREIGN KEY (`MODIFIED_BY`) REFERENCES `USER` (`ROWID`);
ALTER TABLE `USER_ROLE` ADD FOREIGN KEY (`USER`) REFERENCES `USER` (`ROWID`);
ALTER TABLE `USER_ROLE` ADD FOREIGN KEY (`ROLE`) REFERENCES `ROLE` (`ROWID`);
ALTER TABLE `TASK` ADD FOREIGN KEY (`EXERCISE`) REFERENCES `EXERCISE` (`ROWID`);
ALTER TABLE `DAILY_TASK` ADD FOREIGN KEY (`AUTHOR`) REFERENCES `USER` (`ROWID`);
ALTER TABLE `DAILY_TASK` ADD FOREIGN KEY (`TASK`) REFERENCES `TASK` (`ROWID`);
ALTER TABLE `USER_DAILY_TASK` ADD FOREIGN KEY (`USER`) REFERENCES `USER` (`ROWID`);
ALTER TABLE `USER_DAILY_TASK` ADD FOREIGN KEY (`JUDGE`) REFERENCES `USER` (`ROWID`);
ALTER TABLE `USER_DAILY_TASK` ADD FOREIGN KEY (`DAILY_TASK`) REFERENCES `DAILY_TASK` (`ROWID`);
ALTER TABLE `USER_DAILY_TASK` ADD FOREIGN KEY (`MODIFIED_BY`) REFERENCES `USER` (`ROWID`);
ALTER TABLE `CREDENTIAL` ADD FOREIGN KEY (`USER`) REFERENCES `USER` (`ROWID`);