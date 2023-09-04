use details;


show tables;

select * from stationdata;

select * from stationdata where Lat_n > 100;

select City from stationdata where Long_w <50;

select City,ID from stationdata where state like'A%';

select * from stationdata where Lat_n between 50 and 100;

select * from stationdata where Long_w between 50 and 100;

select * from stationdata where ID > 600;

select * from stationdata where ID between 700 and 750;

select *from stationdata where City ="Roy";

select * from stationdata where City like "%c";

select Lat_n from stationdata where ID in (627,536,735);

select * from city;

select Name from city where CountryCode in ('USA','BRA');

select * from city order by Name;

select * from city order by Name desc;

select * from city where Population > 1900000;

select Name from city where ID between 300 and 700 group by Name;

select Name from city group by Name;

select * from city as ct inner join stationdata as sd 
on ct.ID=sd.ID;

select * from city  as ct left join stationdata as sd 
on ct.ID=sd.ID;

select * from city as ct right join stationdata as sd 
on ct.ID=sd.ID;

select * from city  full join stationdata ;

select * from stationdata as sd left join city as ct
on sd.ID = ct.ID ;

select * from stationdata as sd right join city as ct 
on sd.ID = ct.ID;

select * from city full join stationdata ;
select * from city where Name='Boulder';

select * from stationdata where City like'A%';

select * from city where Name like 'A%';
select *from city where name like 'A%';
select*from city where name like 'D%';

show databases ;

use college;

show tables;

select *from students;

select* from students where  grade='A';

select stu_name from  students where city='Delhi';

select * from students where rollno between 100 and 103;

select marks from students where grade='B';

select * from teacher;

select  * from students as st inner join teacher as tc 
on st.rollno = tc.id;

use world;

select * from city;

select * from city where Name like 'A%';

select * from city where Name like 'B%';

select Name from city where ID between 40 and 50;

select Name ,CountryCode from city ;

select Name,District from city  ;

select ID,Population from city;

select * from city where Population > 400000;

select * from city where ID in(1,5,6);

select * from city where District like 'A%';

select *from city where Name like 'A%';

select * from city where CountryCode in ('NLD','AUS');

select * from city where ID between 101 and 110;

select distinct Name from city ;

##select count(*) as distinctcity from (select distinct Name from city ##for ms access.

select count(distinct Name ) from city;

select distinct CountryCode from city;

select count(distinct CountryCode) from city;

select distinct District from city  ;

select count(distinct District) from city;

select count(distinct ID ) from city ;

select * from city where Name='kabul' ;
select * from city where Name like 'A%';

select ID from city where CountryCode="AUS" ;

select Name from city where CountryCode="NLD";

select * from city where Population > 500000;

select Name from city order by Name ;

select Name from city order by Name desc;

select CountryCode from city order by CountryCode;

select * from city where ID between 101 and 110;


select * from city where CountryCode in ('USA','NLD');


select * from city;

desc city;
select *from stationdata; 
select * from city;

select * from city where 