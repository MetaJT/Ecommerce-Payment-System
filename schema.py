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
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) DEFAULT '111',
    Balance DECIMAL(10,2) NOT NULL DEFAULT 0.00
);
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.Items (
    ItemID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Type VARCHAR(100),
    Size VARCHAR(50),
    Price DECIMAL(10, 2),
    Description TEXT
);
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.Cart (
    CartID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    ItemID INT,
    Quantity INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
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
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.ShippingAddresses (
    AddressID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Address VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(100),
    PostalCode VARCHAR(20),
    Country VARCHAR(100),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.PaymentMethods (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    CardType VARCHAR(50),
    CardNumber VARCHAR(100),
    ExpiryDate DATE,
    CVV VARCHAR(10),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    OrderDate DATE,
    TotalItems INT,
    TotalAmount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    IsComplete BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
''',
'''
CREATE TABLE IF NOT EXISTS ecommerceDB.OrderItems (
    OrderItemID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ItemID INT,
    Quantity INT,
    Price DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);
'''
]

