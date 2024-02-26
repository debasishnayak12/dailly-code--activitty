show databases;

use world;

show tables;

select *from city;

select Name from city;

select ID from city;

select ID,Name from city where Name like'%ar%';




select city.Name,country.Code
from city
full join country on city.CountryCode=country.Code
order by city.Name;

use ineuron;

select * from employees;
drop table employees;

create table employees(
ID int ,
housenumber int unique,
pancard int unique,
first_name varchar(25),
last_name varchar(25),
salary int not null,
primary key(ID));

Alter table employees
add constraint uc_employee unique(pancard,last_name);

alter table employees
add unique(last_name);

insert into employees(ID,housenumber,pancard,first_name,last_name,salary) values
(1,1,1,"Krish","Naik",20000),
(2,2,2,"Krish1","Naik1",20000);

create table student(
id int auto_increment,
first_name varchar(25),
last_name varchar(25),
primary key(id)
);

##add constraint unique key
alter table student
add constraint uc_student unique(first_name,last_name);

## drop constraint unique key
alter table student
drop index uc_student;

insert into student(first_name,last_name) values
("Krish","Naik"),
("Krish","Naik");

drop table student;
drop table person;
create table person(
id int not null,
first_name varchar(25),
last_name varchar(25),
Age int,
primary key(id)
);

desc person;

alter table person
drop primary key;

alter table person
add constraint pk_person primary key(id,last_name);

insert into person values
(1,"krish","naik",32),
(2,"krish1","naik",32);

alter table person
drop primary key;

create table orders(
orderid int not null,
ordernumber int not null,
id int ,
primary key(orderid),
foreign key(id) references person(id)
);


insert into person values(1,"Krish","Naik",32),
(2,"Krish1","Naik1",31),
(3,"Sunny","Savita",30),
(4,"Krish2","Naik2",33);

insert into orders values(1,1,2);
select * from orders;

select * from person as ps inner join orders as od
on ps.id=od.id;

select * from person as ps inner join orders as od
on ps.id=od.id;

select * from person as ps left join orders as od
on ps.id=od.id;

select * from person as ps right join orders as od 
on ps.id=od.id;
use ineuron;
drop table customers;
create table customers(
id int auto_increment,
first_name varchar(25),
country varchar(25),
capital varchar(25),
primary key(id)
);

insert into customers(id,first_name,country,capital) values
(1,"Krish","India","Dekhi"),
(2,"tom","Australia","Canberra"),
(3,"Sunny","Maldives","Male"),
(4,"Darius","India","Delhi");

select * from customers;

select * from customers where country="India" or country="Maldives";

select * from customers where country !="India";

select * from customers where not country ="India";


use details;


select * from bank_details;

select * from bank_details where age between 30 and 50 order by age; ;

select * from bank_details where age<=60 and job="retired";


select * from bank_details; 


desc employees;

use world;

select * from city;

select * from country;

select * from city as ct inner join country as cr
on ct.CountryCode=cr.Code;

select * from city as ct left join country as cr 
on ct.CountryCode=cr.Code;

select * from city as ct right join country as cr 
on ct.Population=cr.Population;

select * from city as ct left join country as cr
on ct.Population=cr.Population order by ct.Name;

select * from country as cr left join city as ct 
on cr.Population=ct.Population;
select * from country as cr full outer join city as ct 
on cr.Code=ct.CountryCode;

SELECT city.CountryCode, country.Code
FROM City
FULL OUTER JOIN country ON city.Population=country.Population
ORDER BY city.Name;

select  Name from country where Name like'A%' group by Code;
select GNP from country where GNP > 100 group by GNP



select * from country;