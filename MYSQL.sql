create database iNeuron;

use iNeuron;

create table employees(emp_id INT ,
first_name varchar(50),
last_name varchar(50),
DOB date,
hire_date date,
position varchar(30),
salary float)

select * from employees;

insert into employees values(1,"Debasish","Nayak","2002-05-26","2023-06-20","Data scientist","25000.0");
insert into employees values(2,"Subasish","Ray","2003-08-2","2023-08-20","Data analysist","22000.0");
insert into employees values(3,"Aasish","Parida","2001-06-23","2023-03-20","Data engineer","23000.0");
insert into employees values(4,"Pritish","Swain","2000-02-16","2023-09-20","Data scientist","22200.0");


select * from employees;

set SQL_SAFE_UPDATES = 0;

update empolyees set salary=800000.0 where first_name="Debasish";

select * from employees;