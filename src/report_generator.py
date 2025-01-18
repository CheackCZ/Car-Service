from src.connection import Connection

class ReportGenerator:
    """
    Class for generating reports by querying the database.
    """
  
    def generate_summary_report():
        """
        Generates a summary report by querying the `summary_report` view.
        
        :return: List of dictionaries representing the report.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)

        try:
            conn.start_transaction()
            
            query = "SELECT * FROM summary_report"
            cursor.execute(query)
            result = cursor.fetchall()
            
            conn.commit()
            
            return result
        
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()