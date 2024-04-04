-- Insert rows into Users table
INSERT INTO ecommerceDB.Users (FirstName, LastName, Username, Email, Address, Password, PaymentInfo, Balance)
VALUES ('John', 'Doe', 'johndoe', 'john@example.com', '123 Main St', 'password123', 'Credit Card', 1000),
       ('Alice', 'Smith', 'alicesmith', 'alice@example.com', '456 Oak St', 'password456', 'PayPal', 1500);

-- Insert rows into Invoices table
INSERT INTO ecommerceDB.Invoices (UserID, ClientName, InvoiceDate, TotalAmount)
VALUES (1, 'Client A', '2024-04-01', 500),
       (2, 'Client B', '2024-04-02', 750);

-- Insert rows into InvoiceItems table
INSERT INTO ecommerceDB.InvoiceItems (InvoiceID, ItemDescription, Quantity, LineTotal)
VALUES (1, 'Product A', 2, 200),
       (2, 'Product B', 3, 450);

-- Insert rows into Payments table
INSERT INTO ecommerceDB.Payments (InvoiceID, PaymentDate, Amount, PaymentMethod)
VALUES (1, '2024-04-05', 200, 'Credit Card'),
       (2, '2024-04-06', 500, 'PayPal');
