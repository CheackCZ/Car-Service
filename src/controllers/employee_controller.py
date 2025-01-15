from src.connection import Connection
from models.employee import Employee

class EmployeeController:
    """
    Handles database operations for employee.
    """
    
    def fetch_all():
        """
        Retrieves all employee from the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()

            cursor.execute("SELECT * FROM employee")
            rows = cursor.fetchall()

            conn.commit()
            return [
                Employee(row['id'], row['first_name'], row['middle_name'], row['last_name'], row['phone_number'], row['email'], row['is_free']) 
                for row in rows
            ]
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_by_id(employee_id):
        """
        Fetches an employee by their ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()
            
            cursor.execute("SELECT * FROM employee WHERE id = %s", (employee_id,))
            row = cursor.fetchone()
            
            conn.commit()
            
            return Employee(row['id'], row['first_name'], row['middle_name'], row['last_name'], row['phone_number'], row['email'], row['is_free']) if row else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def save(employee: Employee):
        """
        Saves an employee to the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        
        try:
            conn.start_transaction()
            if employee.id is None:
                cursor.execute(
                    "INSERT INTO employee (first_name, middle_name, last_name, phone_number, email, is_free) VALUES (%s, %s, %s, %s, %s, %s)",
                    (employee.first_name, employee.middle_name, employee.last_name, employee.phone_number, employee.email, employee.is_free)
                )
                conn.commit()
                employee.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE employee SET first_name = %s, middle_name = %s, last_name = %s, phone_number = %s, email = %s, is_free = %s WHERE id = %s",
                    (employee.first_name, employee.middle_name, employee.last_name, employee.phone_number, employee.email, employee.is_free, employee.id)
                )
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def delete(employee_id):
        """
        Deletes an employee by their ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute("DELETE FROM employee WHERE id = %s", (employee_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
