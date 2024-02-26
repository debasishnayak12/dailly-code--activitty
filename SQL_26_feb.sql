use world;
select * from city;
select Name  from city;
select * from city where Name like"%A";

select * from city where Name like 'A%';

select * from city where CountryCode="NLD";

select Population from city where Population > 400000;

select count(Name) from city where Population<4000000;

select max(Population) from city ;

select min(Population) from city;

create table shoping(
sl_no int primary key,
items varchar(25),
price float);

select * from shoping;

insert into  shoping(sl_no,items,price) values (1,"Biscuit",40),
(2,"Tea",30);

select * from shoping;

delete from shoping where items="Tea";

drop table shoping;

select * from shoping;

select * from city;

select * from city where CountryCode="AFG" and District like'Q%';

select * from city where CountryCode="NLD" or CountryCode="AFG";

select * from Country;

select * from city as ct left join Country as cr 
on ct.CountryCode=cr.Code ;

select * from city as ct right join Country as cr 
on ct.CountryCode=cr.Code;

select CountryCode,count(CountryCode) as no_of_code from city group by CountryCode;

select  * from Country where Code="NLD";

select * from city where CountryCode in ("NLD");

select Name from city where District in ("Utrecht","Noord-Brabant") group by Name;

select Code,count(Code) from Country group by COde;

use sales;

select * from product;

select sum(unit_price) from product;

select product_name from product where unit_price between 100 and 300;

select * from product;

select count(*) from product;

use world;

select * from city;

select count(*) from city;

select Name from city where District in("Qandahar") group by Name;

select ID,Name,Population from city where Population > 6000000 order by Name ;

select count(Name) as count_name from city;

Select * from city where name like "A%" ;

Select * from city as CT left join Country as cr 
on CT.countrycode=cr.Code;

Select * from country where code='NLD';






