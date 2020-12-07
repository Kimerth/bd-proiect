CREATE TABLE `Departments`
(
 `DepartmentID`    int NOT NULL PRIMARY KEY NUMBER GENERATED ALWAYS AS IDENTITY ,
 `Department Name` varchar(45) NOT NULL ,
 `Website`         varchar(45) NULL ,
);

CREATE TABLE `Researchers`
(
 `UserID`        int NOT NULL PRIMARY KEY NUMBER GENERATED ALWAYS AS IDENTITY ,
 `First Name`    varchar(45) NOT NULL ,
 `Last Name`     varchar(45) NOT NULL ,
 `DepartmentID`  int NOT NULL FOREIGN KEY REFERENCES `Departments` (`DepartmentID`),
 `Email Address` varchar(45) NOT NULL UNIQUE,
 `Phone Number`  varchar(45) NOT NULL UNIQUE,
 `Role`          varchar(45) NOT NULL CHECK (Role = 'tehnician' OR Role = 'laborant' OR Role = 'cercetator'),
);

CREATE TABLE `Tools`
(
 `DeviceID`       int NOT NULL PRIMARY KEY NUMBER GENERATED ALWAYS AS IDENTITY ,
 `Manufacturer`   varchar(45) NOT NULL ,
 `Model name`     varchar(45) NOT NULL ,
 `Serial Number`  varchar(45) NOT NULL UNIQUE,
 `Specifications` varchar(256) NULL ,
);

CREATE TABLE `Experiments`
(
 `ExperimentID` int NOT NULL PRIMARY KEY NUMBER GENERATED ALWAYS AS IDENTITY ,
 `UserID`       int NOT NULL FOREIGN KEY REFERENCES `Researchers` (`UserID`),
 `DeviceID`     int NOT NULL  FOREIGN KEY REFERENCES `Tools` (`DeviceID`),
 `Title`        varchar(45) NOT NULL ,
 `Description`  varchar(512) NOT NULL ,
 `Theory`       varchar(512) NOT NULL ,
);

CREATE TABLE `Results`
(
 `ResultID`     int NOT NULL PRIMARY KEY NUMBER GENERATED ALWAYS AS IDENTITY ,
 `ExperimentID` int NOT NULL FOREIGN KEY REFERENCES `Experiments` (`ExperimentID`),
 `Remarks`      varchar(512) NOT NULL ,
 `Observations` varchar(512) NOT NULL ,
 `Description`  varchar(512) NOT NULL ,
);

CREATE TABLE `Papers`
(
 `RaportID`     int NOT NULL PRIMARY KEY NUMBER GENERATED ALWAYS AS IDENTITY ,
 `ExperimentID` int NOT NULL FOREIGN KEY REFERENCES `Experiments` (`ExperimentID`),
 `Abstract`     varchar(2048) NOT NULL ,
 `Link to pdf`  varchar(45) NULL ,
);