from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Initialize MySQL
def get_db_connection():
    return pymysql.connect(
        host='dbecommerce.c3okqegi6lyw.us-east-2.rds.amazonaws.com',
        user='admin',
        password='DBMS2024!',
        database='ecommerceDB',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `ecommerceDB`.`users`;"
            cursor.execute(sql)
            result = cursor.fetchall()

            for i in result:
                print(i)
    finally:
        connection.close()

    return render_template('users.html', users=result)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/payments')
def payments():
    return render_template('payments.html')

if __name__ == '__main__':
    app.run(debug=True)
