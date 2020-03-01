-- users(email, name, pwd, city, gender)
insert into users values ('email_1@gmail.com', 'Jimmy Yong', 'passw1', 'Edmonton', 'M');
insert into users values ('email_2@gmail.com', 'Garrick', 'passw2', 'Calgary', 'M');
insert into users values ('email_3@gmail.com', 'Rose', 'passw3', 'Calgary', 'F');
insert into users values ('email_4@gmail.com', 'Jimmy Birch', 'passw4', 'Edmonton', 'M');
insert into users values ('email_5@gmail.com', 'Abby', 'passw5', 'Toronto', 'F');
insert into users values ('email_6@gmail.com', 'John Doe', 'passw6', 'Edmonton', 'M');
insert into users values ('email_7@gmail.com', 'Eden', 'passw7', 'San Fran', 'F');
insert into users values ('email_8@gmail.com', 'Jimmy Hendrick', 'passw8', 'San Fran', 'M');
insert into users values ('email_9@gmail.com', 'Aisha', 'passw9', 'San Fran', 'F');
insert into users values ('email_10@gmail.com', 'name 10', 'passw10', 'Calgary', 'M');
insert into users values ('email_11@gmail.com', 'Ellen', 'passw11', 'Toronto', 'F');
insert into users values ('email_12@gmail.com', 'Elsa', 'passw12', 'Texus', 'F');
insert into users values ('email_13@gmail.com', 'Bella Birch', 'passw13', 'Red Deer', 'F');
insert into users values ('email_14@gmail.com', 'Jessica', 'passw14', 'New Yort', 'F');


-- products(pid, descr)
insert into products values ('p01', 'Product_1');
insert into products values ('p02', 'Product_2');
insert into products values ('p03', 'Product_3');
insert into products values ('p04', 'Product_4');
insert into products values ('p05', 'Product_5');
insert into products values ('p06', 'Product_6');
insert into products values ('p07', 'Product_7');
insert into products values ('p08', 'Product_8');
insert into products values ('p09', 'Product_9');
insert into products values ('p10', 'Product_10');
insert into products values ('p11', 'Product_11');
insert into products values ('p12', 'Product_12');


-- sales(sid, lister, pid, edate, descr, cond, rprice)
-- Need dates way in the past, way in the future, and some in the near future
    -- dates in the past
insert into sales values ('s01','email_14@gmail.com','p01','2019-03-23','new','Expired sale',300);
insert into sales values ('s02','email_10@gmail.com','p04','2019-05-05','new','Expired for sale',900);
insert into sales values ('s05','email_9@gmail.com','p05','2019-06-20','new','PS4 for sale',350);
insert into sales values ('s10','email_5@gmail.com','p10','2019-12-15','new','Xbox360 for sale',420);
insert into sales values ('s12','email_1@gmail.com','p06','2020-01-17','new','Expired sale',85);
    -- dates in the far future

    -- dates in the near future


-- bids(bid, bidder, sid, bdate, amount)
    -- bids that have won (sales that have expired):

    -- bids that are currently winning (top sales for active sales):

    -- other bids:


-- reviews(reviewer, reviewee, rating, rtext, rdate)


-- previews(rid, pid, reviewer, rating, rtext, rdate)