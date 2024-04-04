USE ecommerceDB;

-- Create a new user
INSERT INTO Users (FirstName, LastName, Username, Email, Address, Password, PaymentInfo, Balance)
VALUES ('Jane', 'Doe', 'janedoe', 'jane@example.com', '789 Elm St', 'password789', 'Credit Card', 2000);

-- Read all users
SELECT * FROM Users;

-- Update user information
UPDATE Users
SET Balance = 2500
WHERE UserID = 1;

-- Read user with UserID = 1
SELECT * FROM Users WHERE UserID = 1;

-- Create a new invoice
INSERT INTO Invoices (UserID, ClientName, InvoiceDate, TotalAmount)
VALUES (1, 'Client C', '2024-04-03', 1000);

-- Read all invoices
SELECT * FROM Invoices;

-- Update invoice information
UPDATE Invoices
SET TotalAmount = 1200
WHERE InvoicesID = 1;

-- Read invoice with InvoicesID = 1
SELECT * FROM Invoices WHERE InvoicesID = 1;

-- Create a new invoice item
INSERT INTO InvoiceItems (InvoiceID, ItemDescription, Quantity, LineTotal)
VALUES (1, 'Product C', 1, 300);

-- Read all invoice items
SELECT * FROM InvoiceItems;

-- Update invoice item information
UPDATE InvoiceItems
SET Quantity = 2
WHERE ItemID = 1;

-- Read invoice item with ItemID = 1
SELECT * FROM InvoiceItems WHERE ItemID = 1;

-- Create a new payment
INSERT INTO Payments (InvoiceID, PaymentDate, Amount, PaymentMethod)
VALUES (1, '2024-04-07', 1200, 'Credit Card');

-- Read all payments
SELECT * FROM Payments;

-- Update payment information
UPDATE Payments
SET Amount = 1300
WHERE PaymentID = 1;

-- Read payment with PaymentID = 1
SELECT * FROM Payments WHERE PaymentID = 1;

-- Delete the last inserted user
DELETE FROM Users WHERE UserID = (SELECT MAX(UserID) FROM Users);

-- Read all users after deletion
SELECT * FROM Users;
