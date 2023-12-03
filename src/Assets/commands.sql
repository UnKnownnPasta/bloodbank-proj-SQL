create table if not exists Hospital (HospitalID int(4) primary key, HospitalName varchar(100) unique, Password varchar(20), Contact varchar(100))
create table if not exists BloodTable (BloodType char(3), Units int not null, RhFactor char(1))
create table if not exists Doctors (ID int(4) primary key, HospitalID int(4), Name varchar(40), Age int(3), Gender char(20), Email varchar(50), FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID))

-- Tables and their coulmns:
--     Hopsital:  HospitalID, HospitalName, Password, Contact
--     BloodTable:  BloodType, Units, RhFactor
--     Doctors:   ID, HospitalID, Name, Age, Gender, Email

insert into BloodTable values ('A', 0, '+'), ('A', 0, '-'), ('B', 0, '+'), ('B', 0, '-'), ('O', 0, '+'), ('O', 0, '-'), ('AB', 0, '+'), ('AB', 0, '-')

insert into Hospital values (1001, 'Apollo Hospital', 'apollo_admin', '324-6577-354');
insert into Hospital values (1002, 'Fortis Hospital', 'fortis_admin', '888-8383-343');

insert into Doctors values (1226, 1001, 'Ram Patel', 28, 'M', 'ram.patel@gmail.com');
insert into Doctors values (2354, 1001, 'Mia Lee', 30, 'F', 'mia.lee@gmail.com');

insert into Doctors values (4536, 1002, 'Ray Adams', 35, 'M', 'ray.adams@gmail.com');
insert into Doctors values (6456, 1002, 'Leo Foster', 25, 'M', 'leo.foster@gmail.com');
insert into Doctors values (5676, 1002, 'Zoe Lopez', 29, 'F', 'zoe.lopez@gmail.com');
insert into Doctors values (5656, 1002, 'Max Grant', 32, 'M', 'max.grant@gmail.com');