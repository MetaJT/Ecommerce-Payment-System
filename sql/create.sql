CREATE DATABASE IF NOT EXISTS ecommerceDB;

USE ecommerceDB;

CREATE TABLE IF NOT EXISTS Users (
    UserID INT NOT NULL AUTO_INCREMENT,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    Password VARCHAR(255),
    PaymentInfo VARCHAR(255),
    Balance DECIMAL(19,4),
    PRIMARY KEY(UserID)
);

CREATE TABLE IF NOT EXISTS Invoices (
    InvoicesID INT NOT NULL AUTO_INCREMENT,
    UserID INT NOT NULL, 
    ClientName VARCHAR(255),
    InvoiceDate DATE,
    TotalAmount DECIMAL(19,4),
    PRIMARY KEY(InvoicesID)
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
CREATE TABLE IF NOT EXISTS InvoiceItems (
    ItemID INT NOT NULL AUTO_INCREMENT,
    InvoiceID INT NOT NULL,
    ItemDescription VARCHAR(255),
    Quantity INT,
    LineTotal DECIMAL(19,4),
    PRIMARY KEY(ItemID)
    FOREIGN KEY (InvoiceID) REFERENCES Invoices(InvoiceID)
);

CREATE TABLE IF NOT EXISTS Payments (
    PaymentID INT NOT NULL AUTO_INCREMENT,
    InvoiceID INT NOT NULL,
    PaymentDate DATE,
    Amount DECIMAL(19,4),
    PaymentMethod VARCHAR(255),
    PRIMARY KEY(PaymentID)
    FOREIGN KEY (InvoiceID) REFERENCES Invoices(InvoiceID)
);