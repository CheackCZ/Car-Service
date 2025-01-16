from src.connection import Connection
from src.models.employee import Employee

class EmployeeController:
    """
    Handles database operations for employee.
    """
    
    def fetch_all():
        """
        Retrieves all employees from the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()

            cursor.execute("SELECT * FROM employee")
            rows = cursor.fetchall()

            conn.commit()
            return [
                Employee(
                    id=row['id'],
                    name=row['name'],
                    middle_name=row.get('middle_name') or None,  # Normalize NULL/empty values to None
                    last_name=row['last_name'],
                    phone=row['phone'],
                    email=row['email'],
                    is_free=bool(row['is_free'])
                ) 
                for row in rows
            ]
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
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
            
            return Employee(
                id=row['id'],
                name=row['name'],
                middle_name=row.get('middle_name') or None,  # Normalize NULL/empty values to None
                last_name=row['last_name'],
                phone=row['phone'],
                email=row['email'],
                is_free=bool(row['is_free'])
            ) if row else None
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
                    "INSERT INTO employee (name, middle_name, last_name, phone, email, is_free) VALUES (%s, %s, %s, %s, %s, %s)",
                    (employee.name, employee.middle_name, employee.last_name, employee.phone, employee.email, employee.is_free)
                )
                conn.commit()
                employee.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE employee SET name = %s, middle_name = %s, last_name = %s, phone = %s, email = %s, is_free = %s WHERE id = %s",
                    (employee.name, employee.middle_name, employee.last_name, employee.phone, employee.email, employee.is_free, employee.id)
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
