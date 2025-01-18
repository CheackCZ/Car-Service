import os

import mysql.connector
from dotenv import load_dotenv

class Connection():
    """
    Class for managing database connections and validating configuration values.
    """
    
    def connection():
        """
        Connects to the database based on the provided credentials inside .env file, which are loaded using the load_dotenv() function.
        
        :return mysql.connector.connection.MySQLConnection: The database connection object.
        """
        load_dotenv()
        
        db = mysql.connector.connect(
            host = Connection.validation(os.getenv('DB_HOST')),
            user = Connection.validation(os.getenv('DB_USER')),
            password = Connection.validation(os.getenv('DB_PASSWORD')),
            database=Connection.validation(os.getenv('DB_NAME')),
            port=Connection.port_validation(os.getenv('DB_PORT'))
        )
        return db

    def connect_to_database():
        """
        Attempts to connect to the database and returns a tuple with connection status and message.
        
        :return tuple: A tuple containing a boolean (connection status) and a string message.
        """
        try:
            Connection.connection()
            return True, "Connection successful!"
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False, f"Connection failed due to MySQL connection error!"
        
        
    def validation(value):
        """
        Validates string configuration values, ensuring they are not empty or invalid.
        
        :param value (str): The configuration value to validate.
        
        :return str: The validated and stripped configuration value.
        """
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Invalid configuration -> Update its value inside the .env file.")
        return value.strip()

    def port_validation(port):
        """
        Validates the database port, ensuring it is a valid integer within the range 1-65535.

        :param port (str): The port value to validate.
        
        :return int: The validated port as an integer.
        """
        if not port.isdigit() or not (1 <= int(port) <= 65535):
            raise ValueError("Invalid configuration for port -> Update its value inside the .env file.")
        return int(port)  