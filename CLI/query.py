import hashlib
import mysql.connector
from mysql.connector import Error


cursor = None
connection = None

def create_connection(host_name, user_name, user_password):
    #connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            port = '3307',
            user=user_name,
            passwd=user_password,
            database = 'networking'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def initialize_db():
    connection = create_connection('localhost', 'root', 'root')
    cursor = connection.cursor()

def find_flows(sourceip, sourceport, destinationip, destinationport):
    link_id = ("{}-{}-{}-{}").format(sourceip, sourceport, destinationip, destinationport)
    query = ("SELECT * FROM Links WHERE Link_ID = \'{}\' LIMIT 10; ").format(link_id)
    cursor.execute(query)
    for x in cursor.fetchall():
        print (x)
    cursor.close()
    connection.close()

def hash_password(password):
    result = hashlib.sha256(password.encode())
    return result.hexdigest()

def authenticate(username, password):
    query = ("SELECT passwd FROM userinfo WHERE userID = \'{}\';").format(username)
    cursor.execute(query)
    query_result = cursor.fetchall()
    if len(query_result) == 0:
        return False
    hashed_password_input = hash_password(password)
    for x in query_result:
        if x[0] == hashed_password_input:
            return True 
    return False

def get_session_token(username):
    query = ("SELECT isadmin FROM userinfo WHERE userID = \'{}\'").format(username)
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result[0][0]

def add_annotation(username, flow_id, annotation):
    query = ("INSERT INTO annotations VALUES ({}, \'{}\', \'{}\');").format(flow_id, username, annotation)
    cursor.execute(query)
    count = cursor.rowcount
    query_result = cursor.fetchall()
    connection.commit() #WHENEVER MAKING CHANGES TO THE DATABASE REMEMBER TO COMMIT TO THE CONNECTION OTHERWISE THEY WILL NOT BE SAVED
    return count

connection = create_connection('localhost', 'root', 'root')
cursor = connection.cursor()

