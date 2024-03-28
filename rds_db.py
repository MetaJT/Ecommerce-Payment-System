import pymysql

class AWSRDSDatabase:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_script(self, file_path):
        self.connect()
        with open(file_path, 'r') as sql_file:
            sql_script = sql_file.read()
            self.cursor.execute(sql_script)
        self.connection.commit()
        self.disconnect()
