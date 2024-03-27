CREATE TABLE Users (
    UserID INT NOT NULL AUTO_INCREMENT , /* Primary Key */
    Email VARCHAR(255),
    ShippingAddress VARCHAR(255),
    PRIMARY KEY(UserID)
);

CREATE TABLE Invoices (
    InvoicesID INT NOT NULL AUTO_INCREMENT, /* Primary Key */
    UserID INT NOT NULL, /* Foreign key from users table */
    ClientName VARCHAR(255),
    InvoiceDate DATE,
    TotalAmount DECIMAL(19,4),
    PRIMARY KEY(InvoicesID)
);

CREATE TABLE InvoiceItems (
    ItemID INT NOT NULL AUTO_INCREMENT, /* Primary Key */
    InvoiceID INT NOT NULL, /* Foreign key from users table */
    ItemDescription VARCHAR(255),
    Quantity INT,
    LineTotal DECIMAL(19,4),
    PRIMARY KEY(ItemID)
);

CREATE TABLE Payments (
    PaymentID INT NOT NULL AUTO_INCREMENT, /* Primary Key */
    InvoiceID INT NOT NULL, /* Foreign key from users table */
    PaymentDate DATE,
    Amount DECIMAL(19,4),
    PaymentMethod VARCHAR(255),
    PRIMARY KEY(PaymentID)
);