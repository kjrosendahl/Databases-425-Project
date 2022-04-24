/* select 'drop table '||table_name||' cascade constraints;' from user_tables; */

/*
Idea: 
each Inventory has a passkey that is required to send restock order. 
- gets around the problem of certain employees not being able to send an order
- also prevents problems with warehouses sending orders 
- any employee who works in a store and "knows" the passkey will be able to send a restock order for the appropriate inventory
*/

create table Inventory
(
InvID varchar(6), 
Passkey char(8) not null unique,
primary key (InvID)
);

/* Strong Relation */
create table Addresses 
( 
AddressID varchar(6), 
Street varchar(20), 
City varchar(20), 
State char(2), 
Zipcode char(5), 
Region varchar(10) check (Region in ('Northeast', 'Southwest', 'West', 'Southeast', 'Midwest')),
primary key (AddressID)
);

/* Strong Relation */
create table Stores
(
SID varchar(6), 
InvID varchar(6) unique not null, 
AddressID varchar(6) unique not null,
Name varchar(20), 
primary key (SID), 
foreign key (InvID) references Inventory,
foreign key (AddressID) references Addresses
);

/* Strong Relation */
create table Employees
(
EmpID varchar(8), 
SID varchar(6) not null, 
Name varchar(20), 
Title varchar(20),
Password varchar(20) check (length(Password) >= 6) not null, 
Salary numeric(12,2) check (salary >0), 
primary key (EmpID), 
foreign key (SID) references Stores(SID)
);

/* Strong Relation */
create table Warehouses
(
WID varchar(6), 
InvID varchar(6) unique not null, 
AddressID varchar(6) unique not null, 
primary key (WID), 
foreign key (InvID) references Inventory,
foreign key (AddressID) references Addresses
); 

/* Strong Relation */
create table Categories
(
CategoryID varchar(8), 
CategoryName varchar(20), 
primary key (CategoryID)
);

/* Strong Relation */
create table Brands
( 
BrandID varchar(8), 
BrandName varchar(20), 
primary key (BrandID)
); 

/* Strong Relation */
create table Products
(
PID varchar(8), 
BrandID varchar(8), 
CategoryID varchar(8), 
UPC char(12) not null, 
ProductName varchar(20), 
primary key (PID), 
foreign key (BrandID) references Brands, 
foreign key (CategoryID) references Categories
);

/* allows us to specify when products are actually packages of other products*/
create table Contains
(
PackID varchar(6),
CompID varchar(6),
primary key (PackID, CompID)
);

/* relates Product with Store/Warehouses based on InventoryIDs */
create table ProdInv
(
InvID varchar(6), 
PID varchar(8), 
Quantity int check (Quantity >= 0), 
Price numeric(8,2) check (Price >= 0),
primary key (InvID, PID)
); 

/* specifies the manufacturers that can make certain products */
create table Manufacturer
(
ManID varchar(6),
PID varchar(6),
Name varchar(20), 
primary key (ManID, PID)
); 

/* used for restocking orders */
create table Restock
(
RestockID varchar(12), 
InvID varchar(6) not null, 
ManID varchar(6) not null, 
Reordered date,
Status varchar(10) check (Status in ('Delivered', 'Pending', 'Cancelled'))
); 

/* similar to ProdInv: relates the restockID with products in the order */
create table RestockProd
(
RestockID varchar(12), 
PID varchar(8) not null, 
Quantity int check (Quantity > 0), 
primary key (RestockID, PID)
); 

/* start customer data*/ 

create table Customer 
(
CID varchar(12), 
Name varchar(20), 
Frequent varchar(5) check (Frequent in ('True', 'False')), 
primary key (CID)
); 

/* if no name, means they were in person only */
/* if name but no email, means they were infrequent customer ordering online */ 
/* if name and email, means they are a frequent customer with an account */ 
create table CustAddress 
(
CID varchar(12),  
Street varchar(20), 
City varchar(20), 
State char(2), 
Zipcode char(5), 
primary key (CID), 
foreign key (CID) references Customer
);

/* necessary? */ 
create table Contractor 
 ( 
 CID varchar(12), 
 AccNo varchar(12) unique, 
 BillingAmt int check (BillingAmt > 0), 
 primary key (CID), 
 foreign key (CID) references Customer
 );

 /* used to keep track of frequent customers, which have online accounts */
 create table OnlineAcc 
 ( 
 CID varchar(12), 
 Email varchar(50) unique not null, 
 Password varchar(20) check (length(Password) >= 6) not null,
 primary key (CID), 
 foreign key (CID) references Customer 
 ); 
 
 /* similar to Restock details */
 create table Orders 
 ( 
 OrderID varchar(12), 
 CID varchar(12) not null, 
 InvID varchar(6) not null, 
 Status varchar(10) check (Status in ('Complete', 'Pending', 'Cancelled')),
 Total numeric(8,2) check (Total > 0) not null, 
 Odate date, 
 primary key (orderID), 
 foreign key (CID) references Customer
 ); 
 
/* similar to RestockProd */
create table OrderProd
(
OrderID varchar(12), 
PID varchar(8) not null, 
Quantity int check (Quantity > 0), 
primary key (OrderID, PID)
); 

create table Credit 
(
CID varchar(12), 
CardNo char(16) unique not null, 
Expr char(4) not null, 
CVV char(3) not null, 
Credit int not null,
primary key (CID), 
foreign key (CID) references Customer
); 

create table Shipping 
(
ShipID varchar(12), 
Company varchar(20), 
primary key (ShipID)
); 

create table OrderShip 
( 
OrderID varchar(12), 
ShipID varchar(12) not null, 
TrackNo char(16) not null, 
primary key (OrderID), 
foreign key (OrderID) references Orders, 
foreign key (ShipID) references Shipping
); 


/* add some data */

insert into Inventory values ('01', '7ef8ab3a');
insert into Inventory values ('02', '4cc3de21');
insert into Inventory values ('03', 'f3bab76d');
insert into Inventory values ('04', '3d3b65f2');
insert into Inventory values ('05', '1a1e8d35');
insert into Inventory values ('06', '56b3dc18');
insert into Inventory values ('07', '174cd2fe');
insert into Inventory values ('08', 'a12ef542');

insert into Addresses values ('001', '10 S State St', 'Chicago', 'IL', 60616, 'Midwest');
insert into Addresses values ('002', '19 Kitchen Ave', 'Kenosha', 'WI', 64921, 'Midwest');
insert into Addresses values ('003', '303 Brick Blvd', 'Los Angeles', 'CA', 39143, 'Southwest');
insert into Addresses values ('004', '49 Circle Ct', 'New York City', 'NY', 49120, 'Northeast');
insert into Addresses values ('005', '26 Hallie Rd', 'Austin', 'TX', 20194, 'Southwest');
insert into Addresses values ('006', '13880 Byrde Pt', 'Detroit', 'MI', 50332, 'Midwest');
insert into Addresses values ('007', '123 ABC Ave', 'Seattle', 'WA', 41001, 'West');
insert into Addresses values ('008', '556 Spin Rd', 'Miami', 'FL', 70021, 'Southeast');

insert into Stores values ('101', '06', '002', 'Super Electronics');
insert into Stores values ('102', '07', '003', 'Best Buys');
insert into Stores values ('103', '04', '004', 'Genius Bar');
insert into Stores values ('104', '05', '001', 'Electronics R Us'); 

insert into Warehouses values ('201', '08', '007');
insert into Warehouses values ('202', '01', '006');
insert into Warehouses values ('203', '02', '005');
insert into Warehouses values ('204', '03', '008');

insert into Employees values ('101001', '101', 'John Smith', 'Manager', 'password', 45000);
insert into Employees values ('101002', '101', 'Jim Smalls', 'Associate', 'spyder21', 21000);
insert into Employees values ('101003', '101', 'Melissa Kuhn', 'Associate', 'marky1078', 24000);
insert into Employees values ('102001', '102', 'Spencer Dyer', 'Manager', 'spence201', 490000);
insert into Employees values ('102002', '102', 'Chris Payton', 'Associate', 'electronics', 32000); 
insert into Employees values ('103001', '103', 'Hannah Banana', 'Manager', 'fruits', 50000); 
insert into Employees values ('103002', '103', 'RJ Turtle', 'Associate', 'chipsanddip', 30000); 
insert into Employees values ('104001', '104', 'Ellie Jackson', 'Manager', 'jump4joy', 55000);

insert into Categories values ('0001', 'Camera'); 
insert into Categories values ('0002', 'Phone'); 
insert into Categories values ('0003', 'Computer'); 
insert into Categories values ('0004', 'TV'); 
insert into Categories values ('0005', 'Mouse'); 
insert into Categories values ('0006', 'Keyboard'); 
insert into Categories values ('0007', 'Video Games'); 

insert into Brands values ('0001', 'Samsung'); 
insert into Brands values ('0002', 'Apple'); 
insert into Brands values ('0003', 'Android');
insert into Brands values ('0004', 'Windows'); 
insert into Brands values ('0005', 'Kodak'); 
insert into Brands values ('0006', 'Nintendo'); 
insert into Brands values ('0007', 'Acer'); 
insert into Brands values ('0008', 'Sony'); 

insert into Products values ('1030', '0001', '0004', '000000000000', 'Racer TV'); 
insert into Products values ('1042', '0002', '0002', '000010000020', 'iPhone 6s'); 
insert into Products values ('1043', '0002', '0002', '103050000000', 'iPhone 11'); 
insert into Products values ('1044', '0002', '0003', '590000000203', 'Macbook 12');
insert into Products values ('2002', '0003', '0002', '400010000034', 'Galaxy 10'); 
insert into Products values ('2003', '0003', '0002', '290000028032', 'SS A8'); 
insert into Products values ('2042', '0004', '0003', '940000020003', 'HP 13 Laptop'); 
insert into Products values ('2045', '0004', '0003', '003000300030', 'ASUS 5 Laptop');
insert into Products values ('2050', '0007', '0004', '193000200010', 'Nitro Acer 5 Laptop'); 
insert into Products values ('2340', '0005', '0001', '104910000201', 'Base Camera');
insert into Products values ('2342', '0005', '0001', '102000301859', 'Film Camera'); 
insert into Products values ('3080', null, '0006', '930000203001', 'Mech Keyboard'); 
insert into Products values ('3090', null, '0006', '050000402032', 'Light up Keyboard'); 
insert into Products values ('3100', null, '0005', '399000291100', 'Logitech USB'); 
insert into Products values ('5000', '0006', '0007', '130000002011', 'Mario Kart'); 
insert into Products values ('5001', '0006', '0007', '399800000301', 'Legend of Zelda'); 
insert into Products values ('5002', '0006', '0007', '500030004002', 'Smash Ultimate'); 
insert into Products values ('5003', '0008', '0007', '370000010002', 'Spyro'); 
insert into Products values ('1031', '0008', '0004', '900040004000', '56in TV'); 

insert into ProdInv values ('01', '3090', 10, 100); 
insert into ProdInv values ('01', '2050', 7, 1000); 
insert into ProdInv values ('01', '5000', 12, 60); 
insert into ProdInv values ('01', '5001', 8, 40); 
insert into ProdInv values ('01', '2003', 20, 700);
insert into ProdInv values ('02', '3080', 5, 80); 
insert into ProdInv values ('02', '3090', 10, 100); 
insert into ProdInv values ('02', '2042', 40, 950); 
insert into ProdInv values ('02', '1043', 20, 1200); 
insert into ProdInv values ('02', '5001', 20, 50); 
insert into ProdInv values ('02', '3100', 12, 15); 
insert into ProdInv values ('03', '1030', 6, 550); 
insert into ProdInv values ('03', '2340', 3, 200); 
insert into ProdInv values ('03', '5002', 20, 65);
insert into ProdInv values ('04', '1042', 10, 660); 
insert into ProdInv values ('04', '1043', 12, 770); 
insert into ProdInv values ('04', '1044', 25, 1400); 
insert into ProdInv values ('04', '2002', 1, 500); 
insert into ProdInv values ('05', '2002', 29, 450); 
insert into ProdInv values ('05', '2045', 50, 2000); 
insert into ProdInv values ('05', '2342', 10, 580); 
insert into ProdInv values ('06', '2045', 14, 2100); 
insert into ProdInv values ('06', '1031', 15, 800); 
insert into ProdInv values ('06', '3080', 100, 120); 
insert into ProdInv values ('07', '5000', 120, 50); 
insert into ProdInv values ('07', '5001', 400, 40); 
insert into ProdInv values ('07', '5002', 340, 60); 
insert into ProdInv values ('07', '5003', 310, 35); 
insert into ProdInv values ('08', '1031', 95, 740); 
insert into ProdInv values ('08', '2002', 100, 1150); 

insert into Manufacturer values ('01', '1030', 'ManuA');
insert into Manufacturer values ('01', '1031', 'ManuA'); 
insert into Manufacturer values ('01', '1042', 'ManuA'); 
insert into Manufacturer values ('01', '1043', 'ManuA'); 
insert into Manufacturer values ('01', '1044', 'ManuA'); 
insert into Manufacturer values ('01', '2002', 'ManuA'); 
insert into Manufacturer values ('01', '2003', 'ManuA'); 
insert into Manufacturer values ('02', '2042', 'ManuB'); 
insert into Manufacturer values ('02', '2045', 'ManuB'); 
insert into Manufacturer values ('02', '2050', 'ManuB');
insert into Manufacturer values ('03', '2340', 'ManuC'); 
insert into Manufacturer values ('03', '2342', 'ManuC'); 
insert into Manufacturer values ('03', '3080', 'ManuC'); 
insert into Manufacturer values ('03', '3090', 'ManuC'); 
insert into Manufacturer values ('03', '3100', 'ManuC');
insert into Manufacturer values ('04', '5000', 'ManuD'); 
insert into Manufacturer values ('04', '5001', 'ManuD'); 
insert into Manufacturer values ('04', '5002', 'ManuD'); 
insert into Manufacturer values ('04', '5003', 'ManuD');

insert into Restock values ('000001', '01', '03', date '2022-04-23', 'Pending'); 

insert into RestockProd values ('000001', '3080', 20); 
insert into RestockProd values ('000001', '3100', 50); 

insert into Customer values ('0001', 'Kaylee Rosendahl', 'True'); 
insert into CustAddress values ('0001', '3241 S Wabash Ave', 'Chicago', 'IL', 60616); 
insert into OnlineAcc values ('0001', 'krosendahl@hawk.iit.edu', '425Databases'); 

insert into Orders values ('100001', '0001', '07', 'Complete', 185, date '2022-04-24');
insert into OrderProd values ('100001', '5000', 1); 
insert into OrderProd values ('100001', '5001', 1); 
insert into OrderProd values ('100001', '5002', 1); 
insert into OrderProd values ('100001', '5003', 1); 
insert into Credit values ('0001', '1234567800000000', '0199', '000', 1000); 

insert into Shipping values ('12345', 'UPS'); 
insert into Shipping values ('67890', 'FedEx'); 

insert into OrderShip values ('100001', '12345', '1234123412341234'); 


/* example query: find the address of any stores that hold Legend of Zelda BOTW */ 
select street, city, state 
<<<<<<< HEAD
from Addresses natural join stores 
where sid in (select sid from stores natural join ProdInv 
    where PID = '5001');
    
/* find product names, quantity from all orders given by Kaylee */ 
select ProductName, Quantity
from Orders natural join OrderProd natural join Products 
where CID = (select CID from Customer where Name = 'Kaylee Rosendahl');

=======
from addresses natural join stores 
where sid in (select sid from inventory natural join stores natural join ProdInv 
    where PID = '5001'); 
>>>>>>> 3e2a2ad22c0bc7f79bee6f0536b01d8f7cdb1048
