from flask import Flask, render_template, request, flash, url_for, redirect, request, jsonify
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

    # Gets all the info attached to account from the DB
    # Stored as a dictionary
    def info():
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `ecommerceDB`.`Users` WHERE UserID=%s;"
                cursor.execute(sql, (id,))
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

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

@app.route('/')
@app.route('/home')
@app.route('/index')

def index():
    create_tables('schema.py')
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `ecommerceDB`.`Users`;"
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()
    if current_user.is_authenticated: 
        return render_template('users.html', users=result, currUser=current_user.info, items=get_items())
    return render_template('users.html', users=result, items=get_items())

def get_users():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `ecommerceDB`.`Users`;"
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()
    return result

def get_items():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `ecommerceDB`.`Items`;"
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()
    return result

def get_cart():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT Items.Name, Items.Type, Items.Size, Items.Price, Cart.Quantity, Cart.CartID
            FROM Cart
            INNER JOIN Items ON Cart.ItemID = Items.ItemID
            WHERE Cart.UserID = %s
            """
            cursor.execute(sql, (current_user.info['UserID']))
            result = cursor.fetchall()
            print(result)
    finally:
        connection.close()
    return result

# This route is used for the js request, not ideal to keep
# Will try and do something with this
@app.route('/user-login', methods=['GET',])
def user_login():
    userID = request.args.get('userID')
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `ecommerceDB`.`Users` WHERE UserID=%s;"
            cursor.execute(sql, (userID,))
            result = cursor.fetchone()
            if result:
                return jsonify({'status': 'success', 'user': result})
            else:
                return jsonify({'status': 'failed'})
    finally:
        connection.close()

@app.route('/get-item', methods=['GET',])
def get_item():
    itemID = request.args.get('itemID')
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `ecommerceDB`.`Items` WHERE ItemID=%s;"
            cursor.execute(sql, (itemID,))
            result = cursor.fetchone()
            if result:
                return jsonify({'status': 'success', 'item': result})
            else:
                return jsonify({'status': 'failed'})
    finally:
        connection.close()

@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `ecommerceDB`.`Users` WHERE UserID=%s;"
            cursor.execute(sql, (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(user_data)
            else:
                return None  # User not found
    finally:
        connection.close()

@app.route('/login', methods=['GET','POST'])
def login(email=None,password=None):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `ecommerceDB`.`Users` WHERE Email=%s;" 
                cursor.execute(sql, (email,))
                connection.commit()
                result = cursor.fetchone()
                user = User(result) 
                if result:
                    flash('Logged in successfully!', category='success')
                    login_user(user) # Logs user in
                    return redirect(url_for('index'))
                else:
                    flash('No account found with that email!')
        finally:
            connection.close()

    return render_template('login.html', users=get_users())

@app.route('/logout')
def logout():
    logout_user() # Logs user out
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/payments')
def payments():
    return render_template('payments.html')

@app.route('/create_account', methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `ecommerceDB`.`Users` (`FirstName`, `LastName`, `Username`, `Email`, `Password`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (first_name, last_name, username, email, password))
                print("Successfully created user.")
            connection.commit()
        except Exception as e:
            print(f"Error creating user: {str(e)}")
        finally:
            connection.close()
        return redirect(url_for('login'))
    return render_template('create_account.html')

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
                sql = "INSERT INTO `ecommerceDB`.`Items` (`Name`, `Type`, `Size`, `Description`, `Quantity`,`Price`) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (item_name, item_type, size, description, quantity, price))
                print("Successfully added item.")
            connection.commit()
        except Exception as e:
            print(f"Error adding item: {str(e)}")
        finally:
            connection.close()
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/account')
def account():
    return render_template('account.html', user=current_user.info)

@app.route('/account/settings')
def settings():
    return render_template('settings.html', user=current_user.info)

@app.route('/delete-account',methods=['POST'])
def delete_account():
    if request.method == 'POST':
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `ecommerceDB`.`Users` WHERE UserID=%s;"
                cursor.execute(sql, (current_user.info['UserID'],))
            connection.commit()
            return redirect(url_for('index'))
        finally:
            connection.close()

@app.route('/cart',methods=['GET','POST'])
def cart():
    if request.method == 'POST':
        itemInfo = request.get_json()
        userID = current_user.info['UserID']
        itemID = itemInfo['id']
        quantity = itemInfo['quantity']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `ecommerceDB`.`Cart` (`UserID`, `ItemID`, `Quantity`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (userID, itemID, quantity))
            connection.commit()
        finally:
            connection.close()
    return render_template('cart.html', cart=get_cart())

@app.route('/remove-item', methods=['POST'])
def remove_item():
    if request.method == 'POST':
        cart_info = request.get_json()
        user_id = current_user.info['UserID']
        cart_id = cart_info['cartID']
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                print((user_id, cart_id))
                sql = "DELETE FROM `ecommerceDB`.`Cart` WHERE `UserID`=%s AND `CartID`=%s;"
                cursor.execute(sql, (user_id, cart_id))
            connection.commit()
        finally:
            connection.close()
    return 'Item removed.', 200

@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    if request.method == 'POST':
        item_info = request.get_json()
        user_id = current_user.info['UserID']
        cart_id = item_info['cartID']
        new_quantity = item_info['newQuantity']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `ecommerceDB`.`Cart` SET `Quantity`=%s WHERE `UserID`=%s AND `CartID`=%s"
                cursor.execute(sql, (new_quantity, user_id, cart_id))
            connection.commit()
        finally:
            connection.close()
    return "Quantity updated.", 200

if __name__ == '__main__':
    app.run(debug=True)
