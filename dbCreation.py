#!/usr/bin/env python3
"""
Functions to create the database
"""

import mysql.connector
from mysql.connector import Error

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': ''
}


def create_database():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = connection.cursor()

        cursor.execute("DROP DATABASE IF EXISTS JoyOfPaintingDB;")
        cursor.execute("CREATE DATABASE JoyOfPaintingDB;")
        print("Database 'JoyOfPaintingDB' created successfully.")

    except Error as error:
        print(f"Error creating database: {error}")

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    create_database()
