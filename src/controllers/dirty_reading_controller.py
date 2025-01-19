from src.connection import Connection

from src.models.dirty_reading import DirtyReading

class DirtyReadingController:
    """
    Handles database operations for Dirty Reading table.
    """
    
    def fetch_by_table_name(table_name):
        """
        Retrieves all records from dirty_reading table in the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            conn.start_transaction()

            cursor.execute("SELECT * FROM dirty_reading where table_name = %s", table_name)
            row = cursor.fetchone()

            conn.commit()
            
            return [
                DirtyReading (
                    table_name=row['table_name'],
                    session_id=row['session_id']
                ) 
            ]
        
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            
    def insert(dirty_reading: DirtyReading):
        """
        Inserts new record for dirty_reading in the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            conn.start_transaction()

            cursor.execute("INSERT INTO dirty_reading (table_name, session_id) values (%s, %s)", dirty_reading.table_name, dirty_reading.session_id)

            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            
    def delete(table_name):
        """
        Deletes a record from dirty_reading table in the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            conn.start_transaction()

            cursor.execute("DELETE FROM dirty_reading WHERE table_name = %s", table_name)

            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            
    def set_transaction_level(state):
        """
        Sets the transaction level based on the state selected.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        
        if state:
            cursor.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;")            
        else:
            cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")