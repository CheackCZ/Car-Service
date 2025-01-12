import mysql.connector

import os
from dotenv import load_dotenv

def connection():
    """
    Connects to the database based on the provided credentials inside .env file, which are loaded using the load_dotenv() function.
    """
    load_dotenv()

    db = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def connect_to_database():
    """
    Attempts to connect to the database and returns a tuple with connection status and message.
    """
    try:
        connection()
        return True, "Connection successful!"
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False, f"Connection failed due to MySQL connection error!"
    
print(connect_to_database())