from src.connection import Connection
from src.models.repair_type import RepairType

class RepairTypeController:
    """
    Handles database operations for repair types.
    """
    def __init__(self):
        self.conn = Connection.connection()

    def fetch_all(self):
        """
        Retrieves all repair types from the database.
        """
        cursor = self.conn.cursor(dictionary=True)
        try:
            self.conn.start_transaction()
            
            cursor.execute("SELECT * FROM repair_type")
            rows = cursor.fetchall()
            
            self.conn.commit()
            
            return [RepairType(row['id'], row['name'], row['description']) for row in rows]
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_by_id(self, repair_type_id):
        """
        Fetches a repair type by its ID.
        """
        cursor = self.conn.cursor(dictionary=True)
        try:
            self.conn.start_transaction()

            cursor.execute("SELECT * FROM repair_type WHERE id = %s", (repair_type_id,))
            row = cursor.fetchone()

            self.conn.commit()

            return RepairType(row['id'], row['name'], row['description']) if row else None
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def save(self, repair_type: RepairType):
        """
        Saves a repair type to the database.
        """
        cursor = self.conn.cursor()
        try:
            self.conn.start_transaction()
            if repair_type.id is None:
                cursor.execute(
                    "INSERT INTO repair_type (name, description) VALUES (%s, %s)",
                    (repair_type.name, repair_type.description)
                )
                self.conn.commit()
                repair_type.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE repair_type SET name = %s, description = %s WHERE id = %s",
                    (repair_type.name, repair_type.description, repair_type.id)
                )
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def delete(self, repair_type_id):
        """
        Deletes a repair type by its ID.
        """
        cursor = self.conn.cursor()
        try:
            self.conn.start_transaction()
            cursor.execute("DELETE FROM repair_type WHERE id = %s", (repair_type_id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
