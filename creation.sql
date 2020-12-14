CREATE TABLE "Buildings"
(
 "BuildingID"      int GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1) PRIMARY KEY,
 "Address"         varchar2(45) NOT NULL ,
 "City"            varchar2(45) NOT NULL ,
 "Zipcode"         varchar2(45) NOT NULL 
);

CREATE TABLE "Departments"
(
 "DepartmentID"    int GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1) PRIMARY KEY,
 "Department Name" varchar2(45) NOT NULL ,
 "BuildingID"      int NOT NULL REFERENCES "Buildings" ("BuildingID") UNIQUE ,
 "Website"         varchar2(45) NULL
);

CREATE TABLE "Researchers"
(
 "UserID"        int GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1)  PRIMARY KEY ,
 "First Name"    varchar2(45) NOT NULL ,
 "Last Name"     varchar2(45) NOT NULL ,
 "DepartmentID"  int NOT NULL REFERENCES "Departments" ("DepartmentID"),
 "Email Address" varchar2(45) NOT NULL UNIQUE,
 "Phone Number"  varchar2(45) NOT NULL UNIQUE,
 "Role"          varchar2(45) NOT NULL CHECK ("Role" = 'tehnician' OR "Role" = 'laborant' OR "Role" = 'cercetator') 
);

CREATE TABLE "Tools"
(
 "ToolID"         int GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1)  PRIMARY KEY ,
 "Manufacturer"   varchar2(45) NOT NULL ,
 "Model name"     varchar2(45) NOT NULL ,
 "Serial Number"  varchar2(45) NOT NULL UNIQUE,
 "Specifications" varchar2(1024) NULL
);

CREATE TABLE "Experiments"
(
 "ExperimentID" int GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1)  PRIMARY KEY ,
 "Title"        varchar2(256) NOT NULL ,
 "Description"  varchar2(2048) NOT NULL ,
 "Theory"       varchar2(2048) NOT NULL 
);

CREATE TABLE "ExperimentsResearchersRelation"
(
 "ExperimentID" int NOT NULL REFERENCES "Experiments" ("ExperimentID"),
 "UserID"       int NOT NULL REFERENCES "Researchers" ("UserID")
);

CREATE TABLE "ExperimentsToolsRelation"
(
 "ExperimentID" int NOT NULL REFERENCES "Experiments" ("ExperimentID") ,
 "ToolID"       int NOT NULL REFERENCES "Tools" ("ToolID")
);

CREATE TABLE "Results"
(
 "ResultID"     int GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1)  PRIMARY KEY,
 "ExperimentID" int NOT NULL REFERENCES "Experiments" ("ExperimentID") ,
 "Remarks"      varchar2(4000) NOT NULL ,
 "Observations" varchar2(4000) NOT NULL ,
 "Description"  varchar2(4000) NOT NULL
);