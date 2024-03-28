from flask import Flask, render_template
import pymysql
from rds_db import AWSRDSDatabase

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
    db = AWSRDSDatabase(
        host='dbecommerce.c3okqegi6lyw.us-east-2.rds.amazonaws.com',
        user='admin',
        password='DBMS2024!',
        database='ecommerceDB'
        
    )
    sql_file_path = 'schema.sql'
    db.execute_script(sql_file_path)
    app.run(debug=True)