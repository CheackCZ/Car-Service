from src.connection import Connection
from src.models.brand import Brand

class BrandController:
    """
    Handles database operations for 'Brand' - instances of class Brand.
    """
    
    def fetch_all():
        """
        Retrieves all brands from the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()

            cursor.execute("SELECT * FROM brand")
            rows = cursor.fetchall()

            conn.commit()

            return [Brand(row['id'], row['name']) for row in rows]
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_by_id(brand_id):
        """
        Fetches a brand by its ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()

            cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
            row = cursor.fetchone()

            conn.commit()

            return Brand(row['id'], row['name']) if row else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def save(brand: Brand):
        """
        Saves a brand to the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
           
            if brand.id is None:
                cursor.execute(
                    "INSERT INTO brand (name) VALUES (%s)",
                    (brand.name,)
                )
                conn.commit()
                brand.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE brand SET name = %s WHERE id = %s",
                    (brand.name, brand.id)
                )
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def delete(brand_id):
        """
        Deletes a brand by its ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute("DELETE FROM brand WHERE id = %s", (brand_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()