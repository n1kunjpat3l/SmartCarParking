create database ITPCarPark;
Use ITPCarPark;

----- CREATE TABLE STATEMENTS -----

CREATE TABLE CarParks(
CarParkID    	VARCHAR(10)  NOT NULL,
CarParkName 	VARCHAR(20),
TotalCapacity  INT,  
PRIMARY KEY(CarParkID));


CREATE TABLE CarParkData(
CarParkID VARCHAR(10) NOT NULL,
SlotsAvailable INT NOT NULL,
DataDate DATE,
PRIMARY KEY(CarParkID),
FOREIGN KEY(CarParkID) REFERENCES CarParks(CarParkID));

CREATE TABLE ClassificationData(
ID int NOT NULL AUTO_INCREMENT,
CarParkID VARCHAR(10) NOT NULL
Classifications TEXT,
Date_Of_Classification DateTime,
PRIMARY KEY(ID),
FOREIGN KEY(CarParkID) REFERENCES CarParks(CarParkID));


----- insert Data -----

insert into CarParks values('P1','Car Park 1',100);
insert into CarParks values('P2','Car Park 2',100);
insert into CarParks values('P3','Car Park 3',100);
insert into CarParks values('P4','Car Park 4',100);
insert into CarParks values('P5','Car Park 5',100);
insert into CarParks values('P6','Car Park 6',100);
insert into CarParks values('P7','Car Park 7',100);

insert into CarParkData values ('P6',40,'2017/10/17'); --yyyy/mm/dd