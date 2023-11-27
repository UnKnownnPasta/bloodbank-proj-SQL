create table if not exists Hospital (HospitalID int(4) primary key, HospitalName varchar(100) unique, Password varchar(20), Contact varchar(100), PinCode int(6) not null)
create table if not exists BloodTable (BloodType char(3), Units int not null, RhFactor char(1))
create table if not exists Recipient (ID int(4) primary key, Name varchar(40), Age int(3), Gender char(20), BloodGroup char(4), Donations int)

-- Tables and their coulmns:
--     Hopsital:  ID, Name, Password, Contact, Pincode
--     BloodTable:  Type, Amount, RhFactor
--     Recepients:   Name, Age, Gender, Blood Type, donation count, transfusions count
--     Records:   ID, Date, Action

insert into BloodTable values ('A', 0, '+'), ('A', 0, '-'), ('B', 0, '+'), ('B', 0, '-'), ('O', 0, '+'), ('O', 0, '-'), ('AB', 0, '+'), ('AB', 0, '-')
insert into Hospital values (1001, 'Fortis Hospital', 'fortis_admin', 'fortishospital@gmail.com', 366066)
insert into Hospital values (1002, 'Apollo Hospital', 'apollo_admin', 'apollohospital@gmail.com', 345356)
insert into Recipient values (2343, 'Ram', 34, 'M', 'O-', 0)