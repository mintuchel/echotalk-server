import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "ollamap"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)