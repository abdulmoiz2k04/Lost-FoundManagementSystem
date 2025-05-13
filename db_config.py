import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12775243",
        password="xA3WfCDYSy",
        database="sql12775243"
    )
