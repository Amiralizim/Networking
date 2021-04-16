import mysql.connector
from mysql.connector import Error
import hashlib
import os

'''
This class is specifically used for login related functionalities
'''
class Login:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def initialize_db(self):
        db_connection = os.getenv('DB_CONNECTION')
        print(db_connection)
        self.connection = self.create_connection(db_connection, 'root', 'root')
        
        self.cursor = self.connection.cursor()
        return self.connection
    
    def create_connection(self, host_name, user_name, user_password):
        port_number = os.getenv('DB_PORT')
        try:
            self.connection = mysql.connector.connect(
                host=host_name,
                port = port_number,
                user=user_name,
                passwd=user_password,
                database = 'Networking'
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