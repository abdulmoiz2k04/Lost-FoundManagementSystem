import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
