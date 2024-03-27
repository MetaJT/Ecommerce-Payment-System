from flask import Flask, render_template
import pymysql

app = Flask(__name__)

'''
# Initialize MySQL
db = pymysql.connect(
    host='dbecommerce.c3okqegi6lyw.us-east-2.rds.amazonaws.com',
    user='admin',
    password='DBMS2024!',
    database='ecommerceDB'
)
'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
