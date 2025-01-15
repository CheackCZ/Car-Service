from src.connection import Connection
from models.client import Client

class ClientController:
    """
    Handles database operations for 'Client' - instances of class Client.
    """
    
    def fetch_all():
        """
        Retrieves all client from the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            conn.start_transaction()
        
            cursor.execute("SELECT * FROM client")
            rows = cursor.fetchall()

            conn.commit()

            return [Client(row['id'], row['first_name'], row['middle_name'], row['last_name'], row['phone_number'], row['email']) for row in rows]
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_by_id(client_id):
        """
        Fetches a client by their ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            conn.start_transaction()
        
            cursor.execute("SELECT * FROM client WHERE id = %s", (client_id,))
            row = cursor.fetchone()
        
            conn.commit()
        
            return Client(row['id'], row['first_name'], row['middle_name'], row['last_name'], row['phone_number'], row['email']) if row else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def save(client: Client):
        """
        Saves the current Client instance to the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        
        try:
            conn.start_transaction()
        
            if client.id is None:
                cursor.execute(
                    "INSERT INTO client (first_name, middle_name, last_name, phone_number, email) VALUES (%s, %s, %s, %s, %s)",
                    (client.first_name, client.middle_name, client.last_name, client.phone_number, client.email)
                )
                client.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE client SET first_name = %s, middle_name = %s, last_name = %s, phone_number = %s, email = %s WHERE id = %s",
                    (client.first_name, client.middle_name, client.last_name, client.phone_number, client.email, client.id)
                )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def delete(client_id):
        """
        Deletes a client by their ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        
        try:
            conn.start_transaction()
        
            cursor.execute("DELETE FROM client WHERE id = %s", (client_id,))
        
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()