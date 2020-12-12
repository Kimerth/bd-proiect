CREATE TABLE "Buildings"
(
 "BuildingID"      int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 "Address"         varchar(45) NOT NULL ,
 "City"            varchar(45) NOT NULL ,
 "Zipcode"         varchar(45) NOT NULL 
);

CREATE TABLE "Departments"
(
 "DepartmentID"    int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 "Department Name" varchar(45) NOT NULL ,
 "BuildingID"      int NOT NULL REFERENCES "Buildings" ("BuildingID") UNIQUE ,
 "Website"         varchar(45) NULL
);

CREATE TABLE "Researchers"
(
 "UserID"        int GENERATED ALWAYS AS IDENTITY PRIMARY KEY ,
 "First Name"    varchar(45) NOT NULL ,
 "Last Name"     varchar(45) NOT NULL ,
 "DepartmentID"  int NOT NULL REFERENCES "Departments" ("DepartmentID"),
 "Email Address" varchar(45) NOT NULL UNIQUE,
 "Phone Number"  varchar(45) NOT NULL UNIQUE,
 "Role"          varchar(45) NOT NULL CHECK ("Role" = 'tehnician' OR "Role" = 'laborant' OR "Role" = 'cercetator') 
);

CREATE TABLE "Tools"
(
 "ToolID"         int GENERATED ALWAYS AS IDENTITY PRIMARY KEY ,
 "Manufacturer"   varchar(45) NOT NULL ,
 "Model name"     varchar(45) NOT NULL ,
 "Serial Number"  varchar(45) NOT NULL UNIQUE,
 "Specifications" varchar(256) NULL
);

CREATE TABLE "Experiments"
(
 "ExperimentID" int GENERATED ALWAYS AS IDENTITY PRIMARY KEY ,
 "Title"        varchar(45) NOT NULL ,
 "Description"  varchar(512) NOT NULL ,
 "Theory"       varchar(512) NOT NULL 
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
 "ResultID"     int  GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 "ExperimentID" int NOT NULL REFERENCES "Experiments" ("ExperimentID") ,
 "Remarks"      varchar(512) NOT NULL ,
 "Observations" varchar(512) NOT NULL ,
 "Description"  varchar(512) NOT NULL
);