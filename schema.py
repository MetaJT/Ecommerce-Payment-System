# As of now if changes are made to schema, the table needs to be deleted in MySQL workbench first
# then rerun the program with the updated schema
# This will require you to recreate accounts for now
create_queries = [
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.Users (
    UserID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    Password VARCHAR(255) DEFAULT '111',
    PaymentInfo VARCHAR(255),
    Balance DECIMAL(10,2) NOT NULL DEFAULT 0.00
);
''',
'''
CREATE TABLE IF NOT EXISTS Items (
    ItemID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(25) NOT NULL,
    Type VARCHAR(25) NOT NULL,
    Size VARCHAR(10) NOT NULL,
    Description VARCHAR(255) NOT NULL DEFAULT 'None.',
    Quantity INT NOT NULL DEFAULT 5,
    Price DECIMAL(10,2) NOT NULL DEFAULT 0.00
);
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.Invoices (
    InvoicesID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL, 
    ClientName VARCHAR(255),
    InvoiceDate DATE,
    TotalAmount DECIMAL(10,2) NOT NULL DEFAULT 0.00
);
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.InvoiceItems (
    ItemID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    InvoiceID INT NOT NULL,
    ItemDescription VARCHAR(255) NOT NULL DEFAULT 'None.',
    Quantity INT DEFAULT 0,
    LineTotal DECIMAL(10,2) NOT NULL DEFAULT 0.00
);
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.Payments (
    PaymentID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    InvoiceID INT NOT NULL,
    PaymentDate DATE ,
    Amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    PaymentMethod VARCHAR(255)
);
'''
]