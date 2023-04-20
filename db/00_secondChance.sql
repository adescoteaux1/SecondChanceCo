CREATE DATABASE IF NOT EXISTS SecondChanceDB;

USE SecondChanceDB;

CREATE TABLE IF NOT EXISTS Manager
(
    managerID  int         NOT NULL AUTO_INCREMENT,
    first_name varchar(50) NOT NULL,
    last_name  varchar(50) NOT NULL,
    phone      varchar(50) NOT NULL UNIQUE,
    email1     varchar(50) NOT NULL UNIQUE,
    email2     varchar(50) NOT NULL UNIQUE,
    email3     varchar(50) NOT NULL UNIQUE,
    job_title  varchar(50) NOT NULL,
    start_date date,
    reportsTo  int,
    CONSTRAINT pk PRIMARY KEY (managerID),
    CONSTRAINT fk_1 FOREIGN KEY (reportsTo)
        references Manager (managerID)
); 

CREATE TABLE IF NOT EXISTS man_reps
(
    managerID int NOT NULL,
    reports   varchar(200),
    CONSTRAINT pk PRIMARY KEY (managerID, reports),
    CONSTRAINT fk_01 FOREIGN KEY (managerID)
        references Manager (managerID)
);

CREATE TABLE IF NOT EXISTS Customers
(
    email1     varchar(50) UNIQUE,
    email2     varchar(50) UNIQUE,
    email3     varchar(50) UNIQUE,
    customerID int         NOT NULL AUTO_INCREMENT,
    first_name varchar(50) NOT NULL,
    last_name  varchar(50) NOT NULL,
    phone      varchar(50) UNIQUE,
    city       varchar(50),
    state      varchar(50),
    country    varchar(50),
    zip        int NULL,
    managerID  int,
    CONSTRAINT pk PRIMARY KEY (customerID),
    CONSTRAINT fk_02 FOREIGN KEY (managerID)
        references Manager (managerID)
);

CREATE TABLE IF NOT EXISTS Orders
(
    statusID   BOOLEAN,
    orderID    int NOT NULL AUTO_INCREMENT,
    order_date datetime DEFAULT CURRENT_TIMESTAMP,
    city       varchar(50),
    state      varchar(50),
    country    varchar(50),
    zip        int,
    customerID int NOT NULL,
    CONSTRAINT pk PRIMARY KEY (orderID),
    CONSTRAINT fk_05 FOREIGN KEY (customerID)
        references Customers (customerID) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS Sellers
(
    sellerID   int         NOT NULL AUTO_INCREMENT,
    first_name varchar(50) NOT NULL,
    last_name  varchar(50) NOT NULL,
    city       varchar(50),
    state      varchar(50),
    country    varchar(50),
    zip        int,
    email1     varchar(50) UNIQUE,
    email2     varchar(50) UNIQUE,
    email3     varchar(50) UNIQUE,
    phone      varchar(50) UNIQUE,
    CONSTRAINT pk PRIMARY KEY (sellerID)
);

CREATE TABLE IF NOT EXISTS Payments
(
    paymentID    int NOT NULL AUTO_INCREMENT,
    total_price  int,
    type         varchar(50),
    payment_date datetime DEFAULT CURRENT_TIMESTAMP,
    orderID      int NOT NULL,
    sellerID     int NOT NULL,
    CONSTRAINT pk PRIMARY KEY (paymentID),
    CONSTRAINT fk_08 FOREIGN KEY (orderID)
        references Orders (OrderID),
    CONSTRAINT fk_09 FOREIGN KEY (sellerID)
        references Sellers (sellerID) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS Products
(
    productID    int         NOT NULL AUTO_INCREMENT,
    unitPrice    double,
    product_name varchar(50) NOT NULL,
    sellerID     int         NOT NULL,
    descr        varchar(200),
    picture      varchar(100),
    CONSTRAINT pk PRIMARY KEY (productID),
    CONSTRAINT fk_10 FOREIGN KEY (sellerID)
        references Sellers (sellerID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Cart
(
    total_price double,
    cartID      int AUTO_INCREMENT,
    customerID  int NOT NULL,
    CONSTRAINT pk PRIMARY KEY (cartID),
    CONSTRAINT fk_03 FOREIGN KEY (customerID)
        references Customers (customerID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS prod_carts
(
    productID int NOT NULL,
    cartID    int NOT NULL,
    CONSTRAINT pk PRIMARY KEY (cartID, productID),
    CONSTRAINT fk_04 FOREIGN KEY (cartID)
        references Cart (cartID),
    CONSTRAINT fk_07 FOREIGN KEY (productID)
        references Products (productID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Clothing_Type
(
    clothing_name varchar(50) NOT NULL,
    typeID        int         NOT NULL AUTO_INCREMENT,
    productID     int         NOT NULL,
    CONSTRAINT pk PRIMARY KEY (typeID),
    CONSTRAINT fk_11 FOREIGN KEY (productID)
        references Products (productID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS prod_order
(
    productID int NOT NULL,
    orderID   int NOT NULL,
    CONSTRAINT pk PRIMARY KEY (orderID, productID),
    CONSTRAINT fk_12 FOREIGN KEY (productID)
        references Products (productID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_13 FOREIGN KEY (orderID)
        references Orders (OrderID)
);