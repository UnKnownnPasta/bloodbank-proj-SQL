
-- New Tables
create table if not exists Hospital (HospitalID int(4) primary key, HospitalName varchar(100) unique, Password varchar(20), Contact varchar(100), PinCode int(6) not null)
create table if not exists BloodTable (BloodType char(2), Units int not null, RhFactor char(8))
create table if not exists Recipient (ID int(4) primary key, Name varchar(40), Age int(3), Gender char(20), BloodGroup char(4), Donations int, Transfusions int)
create table if not exists Record (ID int(4), Date date, Transfusion char(100),  foreign key (ID) REFERENCES Recipient(ID))

-- Tables and their coulmns:
--     Hopsital:  ID, Name, Password, Contact, Pincode
--     BloodTable:  Type, Amount, + or -
--     Recepients:   Name, Age, Gender, Blood Type, donation count, transfusions count
--     Records:   ID, Date, Action

-- Old tables
-- create table if not exists Donor (Name varchar(40), Age int(3), Gender char(20), BloodGroup char(2), HospitalID int(4), foreign key (HospitalID) references Hospital(HospitalID))
-- create table if not exists Recipient (Name varchar(40), Age int(3), DateOfTransfer date, HospitalID int(4), BloodType char(2), foreign key (HospitalID) references Hospital(HospitalID))