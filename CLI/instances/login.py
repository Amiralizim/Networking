import mysql.connector
from mysql.connector import Error
import hashlib
import configparser
import os

'''
This class is specifically used for login related functionalities
'''
class Login:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.config = None

    def initialize_db(self):
        path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(path, 'config.ini'))
        host_name = self.config['database']['host']
        port_number = self.config['database']['port']
        db_user = self.config['database']['username']
        db_password = self.config['database']['password']
        db_name = self.config['database']['database_name']
        self.connection = self.create_connection(host_name, port_number, db_user, db_password, db_name)
        
        self.cursor = self.connection.cursor()
        return self.connection
    
    def create_connection(self, host_name, port_number, user_name, user_password, database_name):
        try:
            self.connection = mysql.connector.connect(
                host=host_name,
                port = port_number,
                user=user_name,
                passwd=user_password,
                database = database_name
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print("The error '{e}' occurred")

        return self.connection

    def hash_password(self, password):
        result = hashlib.sha256(password.encode())
        return result.hexdigest()

    def authenticate(self, username, password):
        query = ("SELECT passwd FROM userinfo WHERE userID = \'{}\';").format(username)
        self.cursor.execute(query)
        query_result = self.cursor.fetchall()
        if len(query_result) == 0:
            return False
        hashed_password_input = self.hash_password(password)
        for x in query_result:
            if x[0] == hashed_password_input:
                return True 
        return False
    
    def get_session_token(self, username):
        query = ("SELECT isadmin FROM userinfo WHERE userID = \'{}\'").format(username)
        self.cursor.execute(query)
        query_result = self.cursor.fetchall()
        return query_result[0][0]

    def add_annotation(self, username, flow_id, annotation):
        query = ("INSERT INTO annotations VALUES ({}, \'{}\', \'{}\');").format(flow_id, username, annotation)
        self.cursor.execute(query)
        count = self.cursor.rowcount
        self.connection.commit() #WHENEVER MAKING CHANGES TO THE DATABASE REMEMBER TO COMMIT TO THE CONNECTION OTHERWISE THEY WILL NOT BE SAVED
        return count