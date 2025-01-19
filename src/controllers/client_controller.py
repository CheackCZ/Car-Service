from src.connection import Connection
from src.models.client import Client

class ClientController:
    """
    Handles database operations for 'Client' - instances of class Client.
    """
    def __init__(self, connection):
        self.conn = connection
        
    def fetch_all(self):
        """
        Retrieves all client from the database.
        """
        cursor = self.conn.cursor(dictionary=True)
        
        try:
            self.conn.start_transaction()
        
            cursor.execute("SELECT * FROM client")
            rows = cursor.fetchall()

            self.conn.commit()

            return [Client(row['id'], row['name'], row['middle_name'], row['last_name'], row['phone'], row['email']) for row in rows]
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_by_id(self, client_id):
        """
        Fetches a client by their ID.
        """
        self.conn = Connection.connection()
        cursor = self.conn.cursor(dictionary=True)
        
        try:
            self.conn.start_transaction()
        
            cursor.execute("SELECT * FROM client WHERE id = %s", (client_id,))
            row = cursor.fetchone()
        
            self.conn.commit()
            
            return Client(row['id'], row['name'], row['middle_name'], row['last_name'], row['phone'], row['email']) if row else None
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def save(self, client: Client):
        """
        Saves the current Client instance to the database.
        """
        self.conn = Connection.connection()
        cursor = self.conn.cursor()
        
        try:
            self.conn.start_transaction()
        
            if client.id is None:
                cursor.execute(
                    "INSERT INTO client (name, middle_name, last_name, phone, email) VALUES (%s, %s, %s, %s, %s)",
                    (client.name, client.middle_name, client.last_name, client.phone, client.email)
                )
                client.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE client SET name = %s, middle_name = %s, last_name = %s, phone = %s, email = %s WHERE id = %s",
                    (client.name, client.middle_name, client.last_name, client.phone, client.email, client.id)
                )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def delete(self, client_id):
        """
        Deletes a client by their ID.
        """
        self.conn = Connection.connection()
        cursor = self.conn.cursor()
        
        try:
            self.conn.start_transaction()
        
            cursor.execute("DELETE FROM client WHERE id = %s", (client_id,))
        
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()