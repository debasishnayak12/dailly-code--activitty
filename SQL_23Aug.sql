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
use college;
insert into students
(rollno,stu_name,marks,grade,city)
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
 where marks>80 and city="Mumbai";
 
 select * from student where marks!=90;
 
 select * from student where city="Delhi" or marks>80;
 
 select * from student where marks between 80 and 90;
 
 select * from student
 where 
 city in ("Delhi","Mumbai");
 
 select * from student
 where 
 marks not in (80,90,85);
 
 select * from student
 limit 3;
 
 select name from student
 where 
 city ="Mumbai" limit 2;
 
 select * from student
 order by city asc;
 
 select * from student 
 order by name desc;
 
 select * 
 from student 
 order by marks desc
 limit 3;
 
 select count(marks) from student;
 
 select max(marks) from student;
 
 select min(marks) from student;
 
 select avg(marks) from student;
 
 select city,count(name)
 from student
 group by city;
 
 select city,avg(marks)
 from student 
 group by city
 order by city;
 
 select count(name),city
 from student
 group by city
 having max(marks) >90;
 
 select city
 from student
 where grade="A"
 group by city
 having max(marks) >90
 order by city desc ;
 
 update student
 set grade="O"
 where grade="A";
 
 set sql_safe_updates=0;
 
 update student
 set marks="82"
 where marks=12;
 
 update student 
 set marks=marks+1;
 
 delete from student
 where marks <33;
 
 create table dept(
 id int primary key,
 name varchar(25)
 );
 
 insert into  dept
 values
 (101,"English"),
 (102,"IT");
 
 select * from dept;
 
 drop table teacher;
 
 create table teacher (
 id int primary key,
 name varchar(25),
 dept_id int,
 foreign key (dept_id) references dept(id)
 on delete cascade
 on  update cascade);
 
 insert  into teacher
 values
 (101,"Adam",101),
 (102,"Eve",102);
 
 update dept 
 set id=103
 where id=102;
 
 
 select * from teacher;
 
 
alter table student
add column age int;

alter table student
drop column age ;

alter table student
rename to students;

alter table students
change column name stu_name varchar(26);

alter table students
add column age int not null default 19;

alter table students
modify age varchar(26);

alter table students
change column age stu_age int;

truncate table students;


 select * from students;
 
 alter table students
 drop column stu_age;
 
 delete from students
 where marks<80;
 
 
use college;
