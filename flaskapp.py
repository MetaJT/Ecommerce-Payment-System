from flask import Flask, render_template, request, flash, url_for, redirect, request, jsonify
import pymysql
from schema import create_queries

app = Flask(__name__)
app.secret_key = 'key'

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
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `ecommerceDB`.`Users`;" # using Users table instead of users
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                print(i)
    finally:
        connection.close()
    return render_template('Users.html', users=result)

def get_user_names():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT firstName FROM `ecommerceDB`.`Users`;')
    user_names = cursor.fetchall()
    cursor.close()
    connection.close()
    return user_names

# This route is used for the js request, not ideal to keep
# Will try and do something with this
@app.route('/login-user', methods=['GET',])
def login_user():
    userID = request.args.get('userID', default='1')
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

@app.route('/login')
def login():
    user_names = get_user_names()
    return render_template('login.html', user_names=user_names)
    

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
        # password = request.form['password']

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "INSERT INTO ecommerceDB.Users (FirstName, LastName, Username, Email) VALUES (%s, %s, %s, %s)" # Need to add password
                cursor.execute(sql, (first_name, last_name, username, email))
                connection.commit()
                print("Successfully created user.")
        except Exception as e:
            print(f"Error creating user: {str(e)}")
        finally:
            connection.close()
        return redirect(url_for('index')) # Send user back to home page
    return render_template('create_account.html')

if __name__ == '__main__':
    app.run(debug=True)