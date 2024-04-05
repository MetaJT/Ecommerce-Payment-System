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
            sql = "SELECT * FROM `ecommerceDB`.`Users`;" # using Users table instead of users
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()
    # If a user is logged in -> pass currUser info to HTML
    print(get_items())
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

# Responsible for loading the user object for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `ecommerceDB`.`Users` WHERE UserID=%s;"
            cursor.execute(sql, (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                # Passes UserID from the DB and then all
                return User(user_data)
            else:
                return None  # User not found
    finally:
        connection.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `ecommerceDB`.`Users` WHERE Email=%s;" # using Users table instead of users
                cursor.execute(sql, (email,))
                connection.commit()
                result = cursor.fetchone()
                # creating user object to pass to Flask-Login::login_user
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

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "INSERT INTO `ecommerceDB`.`Users` (`FirstName`, `LastName`, `Username`, `Email`, `Password`) VALUES (%s, %s, %s, %s, %s)" # Need to add password
                cursor.execute(sql, (first_name, last_name, username, email, password))
                print("Successfully created user.")
            connection.commit()
        except Exception as e:
            print(f"Error creating user: {str(e)}")
        finally:
            connection.close()
        return redirect(url_for('index'))
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
                sql = "INSERT INTO `ecommerceDB`.`Items` (`Name`, `Type`, `Size`, `Description`, `Quantity`,`Price`) VALUES (%s, %s, %s, %s, %s, %s)" # Need to add password
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

if __name__ == '__main__':
    app.run(debug=True)