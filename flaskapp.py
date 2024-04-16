from flask import Flask, render_template, request, flash, url_for, redirect, jsonify 
from flask_login import login_user, logout_user, UserMixin, LoginManager, current_user
import pymysql
from schema import create_queries

app = Flask(__name__)
app.secret_key = 'key'
login_manager = LoginManager(app)

# Stores the current user info
class User(UserMixin):
    def __init__(self, user_info):
        self.id = str(user_info['UserID'])
        self.info = dict(user_info)

# Initialize MySQL
def get_db_connection():
    return pymysql.connect(
        host='dbecommerce.c3okqegi6lyw.us-east-2.rds.amazonaws.com',
        user='admin',
        password='DBMS2024!',
        database='ecommerceDB',
        cursorclass=pymysql.cursors.DictCursor
    )

# Create Tables
def create_tables(sql_file):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            for query in create_queries:
                cursor.execute(query)       
        connection.commit()
    finally:
        connection.close()

# Execute Queries
def execute_query(query, values=None):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        
        if query.strip().split(" ")[0].upper() == "SELECT":
            if cursor.description :  # Checking if there are any results
                result = cursor.fetchall()
                if len(result) == 1 and len(result[0]) == 1:  # If only one row with one column, return the value directly
                    return result[0][0]
                return result
            else:
                return None  # Return None if no results

        else:
            connection.commit()
            return True
    except Exception as e:
        print("Error:", e)
        return False
    finally:
        connection.close()

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    create_tables('schema.py')
    sql = "SELECT * FROM `ecommerceDB`.`Users`;"
    result = execute_query(sql)

    if current_user.is_authenticated: 
        return render_template('users.html', users=result, currUser=current_user.info, items=get_items())
    return render_template('users.html', users=result, items=get_items())

def get_users():
    sql = "SELECT * FROM `ecommerceDB`.`Users`;"
    return execute_query(sql)

def get_items():
    sql = "SELECT * FROM `ecommerceDB`.`Items`;"
    return execute_query(sql)

def get_cart():
    sql = """
    SELECT Items.Name, Items.Type, Items.Size, Items.Price, SUM(Cart.Quantity) AS TotalQuantity, Cart.CartID
    FROM Cart
    INNER JOIN Items ON Cart.ItemID = Items.ItemID
    WHERE Cart.UserID=%s
    GROUP BY 
    Items.ItemID, Items.Name, Items.Type, Items.Size, Items.Price;
    """
    return execute_query(sql, (current_user.info['UserID'],))

def get_order_history():
    sql = "SELECT * FROM ecommerceDB.Orders WHERE UserID=%s"
    return execute_query(sql, (current_user.info['UserID'],))

def get_address_info():
    sql = "SELECT * FROM ecommerceDB.ShippingAddresses WHERE UserID=%s"
    return execute_query(sql, (current_user.info['UserID'],))[0]

# @app.route('/get-')
def get_payment_info():
    sql = "SELECT * FROM ecommerceDB.PaymentMethods WHERE UserID=%s"
    return execute_query(sql, (current_user.info['UserID'],))

@app.route('/get-item', methods=['GET',])
def get_item():
    itemID = request.args.get('itemID')
    sql = "SELECT * FROM `ecommerceDB`.`Items` WHERE ItemID=%s;"
    result = execute_query(sql, (itemID,))
    if result:
        return jsonify({'status': 'success', 'item': result[0]})
    else:
        return jsonify({'status': 'failed'})

@login_manager.user_loader
def load_user(user_id):
    sql = "SELECT * FROM `ecommerceDB`.`Users` WHERE UserID=%s;"
    result = execute_query(sql, (user_id,)) # Fetch one
    if result:
        return User(result[0])
    else:
        return None  # User not found

@app.route('/user-login', methods=['GET',])
def user_login():
    user_id = request.args.get('userID')
    sql = "SELECT * FROM `ecommerceDB`.`Users` WHERE UserID=%s;"
    result = execute_query(sql, (user_id,))# Fetch one
    if result:
        return jsonify({'status': 'success', 'user': result[0]})
    else:
        return jsonify({'status': 'failed'})

@app.route('/login', methods=['GET','POST'])
def login(email=None,password=None):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM `ecommerceDB`.`Users` WHERE Email=%s;" 
        result = execute_query(sql, (email,)) # Fetch one
        user = User(result[0]) 
        if result:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', users=get_users())

@app.route('/logout')
def logout():
    logout_user() # Logs user out
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create_account', methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = '''
        INSERT INTO `ecommerceDB`.`Users` (`FirstName`, `LastName`, `Username`, `Email`, `Password`) 
        VALUES (%s, %s, %s, %s, %s)
        '''
        execute_query(sql, (first_name, last_name, username, email, password,))
        connection = get_db_connection()
        return redirect(url_for('login'))
    return render_template('create_account.html')

@app.route('/account')
def account():
    return render_template('account.html', user=current_user.info)

@app.route('/account/settings')
def settings():
    return render_template('settings.html', user=current_user.info)

@app.route('/edit-account-details', methods=['POST', 'GET'])
def update_account():
    if request.method == 'POST':
        user_info = request.get_json()
        email = user_info['email']
        password = user_info['password']
        username = user_info['username']
        sql = "UPDATE `ecommerceDB`.`Users` SET `Email`=%s, `Password`=%s, `Username`=%s WHERE `UserID`=%s"
        execute_query(sql, (email, password, username, current_user.info['UserID']))
        return "Account updated.", 200
    else:
        return "Invalid request method", 400

# Need a route to add an address to a user

@app.route('/edit-shipping-details', methods=['POST'])
def update_shipping():
    if request.method == 'POST':
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        postal_code = request.form['postal-code']
        country = request.form['country']
        sql = '''
        INSERT INTO `ShippingAddresses` (UserID, Address, City, State, PostalCode, Country) 
        VALUES (%s, %s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE Address=%s, City=%s, State=%s, PostalCode=%s, Country=%s
        '''
        execute_query(sql,
        (current_user.info['UserID'], address, city, state, postal_code, country, address, 
        city, state, postal_code, country))
        connection = get_db_connection()
        return "Shipping address updated.", 200
    else:
        return "Invalid request method", 400

# Need to add a route to add a payment method for a user

@app.route('/edit-payment-details', methods=['POST'])
def update_payment():
    if request.method == 'POST':
        cardNumber = request.form['card-number']
        cardholderName = request.form['cardholder-name']
        expirationDate = request.form['expiration-date']
        cvv = request.form['cvv']
        sql = '''
        INSERT INTO `PaymentDetails` (UserID, CardNumber, CardholderName, ExpirationDate, CVV) 
        VALUES (%s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE CardNumber=%s, CardholderName=%s, ExpirationDate=%s, CVV=%s
        '''
        execute_query(sql,
        (current_user.info['UserID'], cardNumber, cardholderName, expirationDate, 
        cvv, cardNumber, cardholderName, expirationDate, cvv))
        return "Payment information updated.", 200
    else:
        return "Invalid request method", 400

@app.route('/delete-account', methods=['POST',])
def delete_account():
    if request.method == 'POST':
        sql = "DELETE FROM `ecommerceDB`.`Users` WHERE UserID=%s;"
        execute_query(sql, (current_user.info['UserID'],))
        logout_user()
        return "Account successfully deleted!", 200
    else:
        return "Invalid request method", 400


@app.route('/cart',methods=['GET','POST'])
def cart():
    if request.method == 'POST':
        itemInfo = request.get_json()
        userID = current_user.info['UserID']
        itemID = itemInfo['id']
        quantity = int(itemInfo['quantity'])

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM `Cart` WHERE `UserID`=%s AND `ItemID`=%s"
                cursor.execute(sql_check, (userID, itemID, ))
                existing_item = cursor.fetchone()
                
                if existing_item:
                    # If the item already exists, update its quantity
                    new_quantity = existing_item['Quantity'] + quantity
                    sql_update = "UPDATE `Cart` SET `Quantity`=%s WHERE `UserID`=%s AND `ItemID`=%s"
                    cursor.execute(sql_update, (new_quantity, userID, itemID))
                else:
                    # If the item doesn't exist, insert a new entry
                    sql_insert = "INSERT INTO `ecommerceDB`.`Cart` (`UserID`, `ItemID`, `Quantity`) VALUES (%s, %s, %s)"
                    cursor.execute(sql_insert, (userID, itemID, quantity))
                connection.commit()
        finally:
            connection.close()

    return render_template('cart.html', cart=get_cart(), user=current_user.info)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['item_name']
        type = request.form['item_type']
        size = request.form['size']
        description = request.form['description']
        quantity = request.form['quantity']
        price = request.form['price']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = '''
                INSERT INTO `ecommerceDB`.`Items` (`Name`, `Type`, `Size`, `Description`, `Quantity`,`Price`) 
                VALUES (%s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(sql, (item_name, item_type, size, description, quantity, price))
                print("Successfully added item.")
            connection.commit()
        except Exception as e:
            print(f"Error adding item: {str(e)}")
        finally:
            connection.close()
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/remove-item', methods=['POST'])
def remove_item():
    if request.method == 'POST':
        cart_info = request.get_json()
        userID = current_user.info['UserID']
        cartID = cart_info['cartID']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `ecommerceDB`.`Cart` WHERE `UserID`=%s AND `CartID`=%s;"
                cursor.execute(sql, (userID, cartID))
            connection.commit()
        finally:
            connection.close()
    return 'Item removed.', 200

@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    if request.method == 'POST':
        item_info = request.get_json()
        userID = current_user.info['UserID']
        cartID = item_info['cartID']
        newQuantity = item_info['newQuantity']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `ecommerceDB`.`Cart` SET `Quantity`=%s WHERE `UserID`=%s AND `CartID`=%s"
                cursor.execute(sql, (newQuantity, userID, cartID))
            connection.commit()
        finally:
            connection.close()
    return "Quantity updated.", 200

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    address_info = get_address_info()
    payment_info = get_payment_info()
    return render_template('checkout.html', user=current_user.info, address_info=address_info, payment_info=payment_info)

@app.route('/orders', methods=['GET','POST'])
def orders():
    if request.method == 'POST':
        user_id = current_user.info['UserID']
        order_insert_query = """
            INSERT INTO ecommerceDB.Orders (UserID, OrderDate)
            VALUES (%s, CURRENT_DATE());
        """

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # Insert the order into Orders table
                cursor.execute(order_insert_query, (user_id,))
                connection.commit()

                # Retrieve the OrderID of the newly created order
                order_id_query = "SELECT LAST_INSERT_ID() AS OrderID;"
                cursor.execute(order_id_query)
                order_id = cursor.fetchone()['OrderID']

                # Retrieve items from the cart
                cart_query = """
                    SELECT c.ItemID, c.Quantity, i.Price 
                    FROM ecommerceDB.Cart c
                    JOIN ecommerceDB.Items i ON c.ItemID = i.ItemID
                    WHERE c.UserID = %s;
                """
                cursor.execute(cart_query, (user_id,))
                cart_items = cursor.fetchall()
                print(cart_items)
                total_items = 0
                total_price = 0
                # Insert items into OrderItems table
                for item in cart_items:
                    order_items_insert_query = """
                        INSERT INTO ecommerceDB.OrderItems (OrderID, ItemID, Quantity, Price)
                        VALUES (%s, %s, %s, %s);
                    """
                    total_items += item['Quantity']
                    total_price += item['Quantity'] * item['Price']
                    cursor.execute(order_items_insert_query, (order_id, item['ItemID'], item['Quantity'], item['Price']))
                sql = '''
                INSERT INTO ecommerceDB.Orders (UserID, ItemID, Quantity, Price, OrderDate)
                SELECT c.UserID, c.ItemID, c.Quantity, i.Price, CURDATE()
                FROM ecommerce.Cart c
                JOIN Items i ON c.ItemID = i.ItemID
                GROUP BY c.UserID;
                '''
                execute_query(sql)
                
                # Update the Order table with ItemID, Quantity, and Price
                order_update_query = """
                    UPDATE ecommerceDB.Orders
                    SET TotalItems = %s, TotalAmount = %s
                    WHERE OrderID = %s;
                """
                cursor.execute(order_update_query, (total_items, total_price, order_id))

                # Delete items from the cart
                cart_delete_query = "DELETE FROM ecommerceDB.Cart WHERE UserID = %s;"
                cursor.execute(cart_delete_query, (user_id,))

                connection.commit()

        finally:
            connection.close()
            
@app.route('/orders', methods=['GET','POST'])
def orders():
    return render_template('orders.html',  user=current_user.info)

# renders /deposit.html in order for users to add money to their accounts
@app.route('/deposit')
def deposit():
    return render_template('/deposit.html')

# used so users can add funds to their account
@app.route('/update_balance', methods=['GET', 'POST'])
def update_balance():
    amount = request.form['amount']
    userID = current_user.info['UserID']
    if request.method == 'POST':
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `ecommerceDB`.`Users` SET balance = balance + %s WHERE `UserID`=%s;"
                cursor.execute(sql, (amount, userID))
            connection.commit()
        finally:
            connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)