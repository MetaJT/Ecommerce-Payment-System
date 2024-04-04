# As of now if changes are made to schema, the table needs to be deleted in MySQL workbench first
# then rerun the program with the updated schema
# This will require you to recreate accounts for now
create_queries = [
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.Users (
    UserID INT NOT NULL AUTO_INCREMENT,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    Password VARCHAR(255) DEFAULT '111',
    PaymentInfo VARCHAR(255),
    Balance DECIMAL(10,2) DEFAULT 0.00,
    PRIMARY KEY(UserID)
);
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.Invoices (
    InvoicesID INT NOT NULL AUTO_INCREMENT,
    UserID INT NOT NULL, 
    ClientName VARCHAR(255),
    InvoiceDate DATE,
    TotalAmount DECIMAL(10,2) DEFAULT 0.00,
    PRIMARY KEY(InvoicesID)
);
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.InvoiceItems (
    ItemID INT NOT NULL AUTO_INCREMENT,
    InvoiceID INT NOT NULL,
    ItemDescription VARCHAR(255),
    Quantity INT DEFAULT 0,
    LineTotal DECIMAL(10,2) DEFAULT 0.00,
    PRIMARY KEY(ItemID)
);
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.Payments (
    PaymentID INT NOT NULL AUTO_INCREMENT,
    InvoiceID INT NOT NULL,
    PaymentDate DATE,
    Amount DECIMAL(10,2) DEFAULT 0.00,
    PaymentMethod VARCHAR(255),
    PRIMARY KEY(PaymentID)
);
'''
]