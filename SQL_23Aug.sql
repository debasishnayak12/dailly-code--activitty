use world;

select distinct cr.Name,cr.Code from country as cr inner join city as ct on cr.Code=ct.CountryCode;

select distinctrow * from country  full join city  ;

select * from city full join country;

select distinct Continent  from country where Population >400000;

select * from city where Name like'%d';

select * from city where Name like '%df%';

select * from city where Name like 'a%';

select District from city where CountryCode in ('NLD' and 'DZA');

select Name from city where Population between 280000 and 4000000 ;

select * from city where Name like'g%' ;

select * from city ;


create database college;

use college;

create table student(
id int primary key,
name varchar(40),
age int not null);

insert into student values(1,"Aman",27),
(2,"Sradha",24);

select * from student;
drop table temp1;
create table temp1(
id int,
name varchar(40),
city varchar(40),
primary key(id,name)
);

insert into temp1 values(101,"Debu","Pune");
drop table salary;
create table salary(
id int ,
salary int default 25000,
age int check (age>=18));

insert into salary (id,age) values(101,21);


select * from salary;

use college;
drop table  if exists student;
create table student(
rollno int primary key,
name varchar(25),
marks int not null,
grade varchar(36),
city varchar(25)
);

insert into student
(rollno,name,marks,grade,city)
values
(101,"Anil",78,"C","Pune"),
(102,"Bhumika",93,"A","Mumbai"),
(103,"Chetan",85,"B","Mumbai"),
(104,"Dhruv",96,"A","Delhi"),
(105,"Emanuel",12,"f","Delhi"),
(106,"Farah",82,"B","Delhi");

select name,marks from student;

select city from student;

select distinct city from student;

select *
 from student
 where marks>80;
select * from student;

