from src.connection import Connection
from src.models.brand import Brand

class BrandController:
    """
    Handles database operations for 'Brand' - instances of class Brand.
    """
    def __init__(self, connection):
        self.conn = connection
    
    def fetch_all(self):
        """
        Retrieves all brands from the database.
        """
        cursor = self.conn.cursor(dictionary=True)
        try:
            self.conn.start_transaction()

            cursor.execute("SELECT * FROM brand")
            rows = cursor.fetchall()

            self.conn.commit()

            return [Brand(row['id'], row['name']) for row in rows]
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_by_id(self, brand_id):
        """
        Fetches a brand by its ID.
        """
        self.conn = Connection.connection()
        cursor = self.conn.cursor(dictionary=True)
        try:
            self.conn.start_transaction()

            cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
            row = cursor.fetchone()

            self.conn.commit()

            return Brand(row['id'], row['name']) if row else None
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def save(self, brand: Brand):
        """
        Saves a brand to the database.
        """
        self.conn = Connection.connection()
        cursor = self.conn.cursor()
        try:
            self.conn.start_transaction()
           
            if brand.id is None:
                cursor.execute(
                    "INSERT INTO brand (name) VALUES (%s)",
                    (brand.name,)
                )
                self.conn.commit()
                brand.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE brand SET name = %s WHERE id = %s",
                    (brand.name, brand.id)
                )
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def delete(self, brand_id):
        """
        Deletes a brand by its ID.
        """
        self.conn = Connection.connection()
        cursor = self.conn.cursor()
        try:
            self.conn.start_transaction()
            cursor.execute("DELETE FROM brand WHERE id = %s", (brand_id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()