from src.connection import Connection
from models.repair_type import RepairType

class RepairTypeController:
    """
    Handles database operations for repair types.
    """

    def fetch_all():
        """
        Retrieves all repair types from the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()
            
            cursor.execute("SELECT * FROM repair_type")
            rows = cursor.fetchall()
            
            conn.commit()
            
            return [RepairType(row['id'], row['name'], row['description']) for row in rows]
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_by_id(repair_type_id):
        """
        Fetches a repair type by its ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()

            cursor.execute("SELECT * FROM repair_type WHERE id = %s", (repair_type_id,))
            row = cursor.fetchone()

            conn.commit()

            return RepairType(row['id'], row['name'], row['description']) if row else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def save(repair_type: RepairType):
        """
        Saves a repair type to the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            if repair_type.id is None:
                cursor.execute(
                    "INSERT INTO repair_type (name, description) VALUES (%s, %s)",
                    (repair_type.name, repair_type.description)
                )
                conn.commit()
                repair_type.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE repair_type SET name = %s, description = %s WHERE id = %s",
                    (repair_type.name, repair_type.description, repair_type.id)
                )
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def delete(repair_type_id):
        """
        Deletes a repair type by its ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute("DELETE FROM repair_type WHERE id = %s", (repair_type_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
