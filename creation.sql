CREATE TABLE `Departments`
(
 `DepartmentID`    int NOT NULL AUTO_INCREMENT ,
 `Department Name` varchar(45) NOT NULL ,
 `Website`         varchar(45) NULL ,

PRIMARY KEY (`DepartmentID`)
);

CREATE TABLE `Researchers`
(
 `UserID`        int NOT NULL AUTO_INCREMENT ,
 `First Name`    varchar(45) NOT NULL ,
 `Last Name`     varchar(45) NOT NULL ,
 `DepartmentID`  int NOT NULL ,
 `Email Address` varchar(45) NOT NULL ,
 `Phone Number`  varchar(45) NOT NULL ,
 `Role`          varchar(45) NOT NULL ,

PRIMARY KEY (`UserID`),
KEY `fkIdx_1` (`DepartmentID`),
CONSTRAINT `FK_1` FOREIGN KEY `fkIdx_1` (`DepartmentID`) REFERENCES `Departments` (`DepartmentID`)
);

CREATE TABLE `Tools`
(
 `DeviceID`       int NOT NULL AUTO_INCREMENT ,
 `Manufacturer`   varchar(45) NOT NULL ,
 `Model name`     varchar(45) NOT NULL ,
 `Serial Number`  varchar(45) NOT NULL ,
 `Specifications` varchar(256) NULL ,

PRIMARY KEY (`DeviceID`)
);

CREATE TABLE `Experiments`
(
 `ExperimentID` int NOT NULL AUTO_INCREMENT ,
 `UserID`       int NOT NULL ,
 `DeviceID`     int NOT NULL ,
 `Title`        varchar(45) NOT NULL ,
 `Description`  varchar(512) NOT NULL ,
 `Theory`       varchar(512) NOT NULL ,

PRIMARY KEY (`ExperimentID`),
KEY `fkIdx_2` (`UserID`),
CONSTRAINT `FK_2` FOREIGN KEY `fkIdx_2` (`UserID`) REFERENCES `Researchers` (`UserID`),
KEY `fkIdx_3` (`DeviceID`),
CONSTRAINT `FK_3` FOREIGN KEY `fkIdx_3` (`DeviceID`) REFERENCES `Tools` (`DeviceID`)
);

CREATE TABLE `Results`
(
 `ResultID`     int NOT NULL AUTO_INCREMENT ,
 `ExperimentID` int NOT NULL ,
 `Remarks`      varchar(512) NOT NULL ,
 `Observations` varchar(512) NOT NULL ,
 `Description`  varchar(512) NOT NULL ,

PRIMARY KEY (`ResultID`),
KEY `fkIdx_4` (`ExperimentID`),
CONSTRAINT `FK_4` FOREIGN KEY `fkIdx_4` (`ExperimentID`) REFERENCES `Experiments` (`ExperimentID`)
);

CREATE TABLE `Papers`
(
 `RaportID`     int NOT NULL AUTO_INCREMENT ,
 `ExperimentID` int NOT NULL ,
 `Abstract`     varchar(2048) NOT NULL ,
 `Link to pdf`  varchar(45) NULL ,

PRIMARY KEY (`RaportID`),
KEY `fkIdx_5` (`ExperimentID`),
CONSTRAINT `FK_5` FOREIGN KEY `fkIdx_5` (`ExperimentID`) REFERENCES `Experiments` (`ExperimentID`)
);