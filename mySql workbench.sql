show databases;

use details;
create table bank_details(
age int not null,
job varchar(30),
marital varchar(30),
education varchar(30),
`default` varchar(30),
balance int,
housing varchar(30),
loan varchar(30),
contact varchar(30),
`day` int,
`month` varchar(30),
duration int,
campaign int,
pdays int,
previous int,
poutcome varchar(30),
y varchar(30));
show tables;

select *from bank_details;
desc bank_details;

show databases;

select * from bank_details where age > 30;

select * from bank_details where balance < 0;

insert into bank_details values(
48,"management","divorced","tertiary","no",-244,"yes","no","unknown",5,"may",253,1,-1,0,"unknown","no"),
(42,"admin.","single","secondary","no",-76,"yes","no","unknown",5,"may",787,1,-1,0,"unknown","no"),
(24,"technician","single","secondary","no",-103,"yes","yes","unknown",5,"may",145,1,-1,0,"unknown","no"),
(58,"self-employed","married","tertiary","no",-364,"yes","no","unknown",5,"may",355,1,-1,0,"unknown","no"),
(36,"admin.","single","primary","no",-171,"yes","no","unknown",5,"may",242,1,-1,0,"unknown","no"),
(53,"technician","married","secondary","no",-3,"no","no","unknown",5,"may",1666,1,-1,0,"unknown","no"),
(55,"technician","divorced","secondary","no",0,"no","no","unknown",5,"may",160,1,-1,0,"unknown","no");

select  * from bank_details where balance < 0;

select * from bank_details where housing='no' and balance=0;

select avg(balance) from bank_details;

select * from bank_details where balance=(select min(balance) from bank_details);

select * from bank_details where balance=(select max(balance) from bank_details);

select * from bank_details where loan='yes';

select avg(balance) from bank_details where job='admin.';

select * from bank_details where job='unknown';

