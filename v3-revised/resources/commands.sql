
-- New Tables
create table if not exists Hospital (HospitalID int(4) primary key, HospitalName varchar(100) unique, Password varchar(20), Contact varchar(100), PinCode char(6) not null)
create table if not exists BloodTable (BloodType char(2), Units int not null, RhFactor char(8))
create table if not exists Recipient (Name varchar(40), Age int(3), Gender char(20), BloodGroup char(2), HospitalID int(4), Donations int, Transfusions int,  foreign key (HospitalID) REFERENCES Hospital(HospitalID))

-- Tables and their coulmns:
--     Hopsital:  ID, Name, Password, Contact, Pincode
--     BloodTable:  Type, Amount, + or -
--     Recepients:   Name, Age, Gender, Blood Type, ID, donation count, transfusions count


-- Old tables
-- create table if not exists Donor (Name varchar(40), Age int(3), Gender char(20), BloodGroup char(2), HospitalID int(4), foreign key (HospitalID) references Hospital(HospitalID))
-- create table if not exists Recipient (Name varchar(40), Age int(3), DateOfTransfer date, HospitalID int(4), BloodType char(2), foreign key (HospitalID) references Hospital(HospitalID))