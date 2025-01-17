from src.connection import Connection
from src.models.employee import Employee

import csv

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
                    middle_name=row.get('middle_name', ''),
                    last_name=row['last_name'],
                    phone=row.get('phone', ''),
                    email=row.get('email', ''),
                    is_free=bool(row['is_free'])
                ) 
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
            
            return Employee(
                id=row['id'],
                name=row['name'],
                middle_name=row.get('middle_name', ''),
                last_name=row['last_name'],
                phone=row.get('phone', ''),
                    email=row.get('email', ''),
                is_free=bool(row['is_free'])
            ) if row else None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def insert(employee: Employee):
        """
        Inserts a new employee into the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()

        try:
            conn.start_transaction()
            print("Inserting new employee into the database.") 
            cursor.execute(
                """
                INSERT INTO employee (name, middle_name, last_name, phone, email, is_free)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (employee.name, employee.middle_name, employee.last_name, employee.phone, employee.email, employee.is_free)
            )
            conn.commit()
            employee.id = cursor.lastrowid
        except Exception as e:
            print(f"Error during insert operation: {e}") 
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def update(employee: Employee):
        """
        Updates an existing employee in the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()

        try:
            conn.start_transaction()
            print("Updating existing employee in the database.")  # Debugging
            print(f"Executing query: UPDATE employee SET name={employee.name}, middle_name={employee.middle_name}, "
            f"last_name={employee.last_name}, phone={employee.phone}, email={employee.email}, "
            f"is_free={employee.is_free} WHERE id={employee.id}")
            
            cursor.execute(
                """
                UPDATE employee
                SET name = %s, middle_name = %s, last_name = %s, phone = %s, email = %s, is_free = %s
                WHERE id = %s
                """,
                (employee.name, employee.middle_name, employee.last_name, employee.phone, employee.email, employee.is_free, employee.id)
            )
            conn.commit()
        except Exception as e:
            print(f"Error during update operation: {e}")  # Debugging
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def delete(employee_id):
        """
        Deletes an employee by their ID after ensuring it is not used as a foreign key.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)

        try:
            conn.start_transaction()

            # Check if the employee ID is referenced in other tables
            cursor.execute(
                """
                SELECT COUNT(*) AS ref_count
                FROM repair
                WHERE employee_id = %s
                """,
                (employee_id,)
            )
            result = cursor.fetchone()
            if result and result["ref_count"] > 0:
                raise ValueError(f"Cannot delete employee ID {employee_id}: It is referenced in {result['ref_count']} repair(s).")

            cursor.execute("DELETE FROM employee WHERE id = %s", (employee_id,))
            conn.commit()
            
            print(f"Employee ID {employee_id} deleted successfully.")
        except ValueError as ve:
            conn.rollback()
            print(ve)
            raise ve
        except Exception as e:
            conn.rollback()
            print(f"Error during delete operation: {e}")
            raise e
        finally:
            cursor.close()

    def validate_import_data(data):
        """
        Validates that the imported data contains all required keys.
        """
        required_keys = {"name", "middle_name", "last_name", "phone", "email", "is_free"}
        for row in data:
            # Check for missing keys
            missing_keys = required_keys - row.keys()
            if missing_keys:
                raise ValueError(f"Missing keys in import data: {', '.join(missing_keys)}. Include them in your import data.")

    def import_data(data):
        """
        Imports employee data into the database after validating keys.
        """
        conn = Connection.connection()
        cursor = conn.cursor()

        try:
            # Step 1: Validate required keys
            EmployeeController.validate_import_data(data)

            # Step 2: Import data into the database
            conn.start_transaction()
            for row in data:
                cursor.execute(
                    """
                    INSERT INTO employee (name, middle_name, last_name, phone, email, is_free)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (row['name'], row.get('middle_name', ''), row['last_name'], row['phone'], row['email'], row['is_free'])
                )
            conn.commit()
            print("Data imported successfully!")
        except ValueError as ve:
            conn.rollback()
            raise ve
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def export_data(file_path):
        """
        Exports all employees to a CSV file.
        :param file_path: The path to save the CSV file.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)

        try:
            conn.start_transaction()

            # Fetch all employee data
            cursor.execute("SELECT * FROM employee")
            rows = cursor.fetchall()

            conn.commit()

            # Write to CSV
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                if not rows:
                    raise ValueError("No data available for export.")

                # Get headers from the query result keys
                headers = rows[0].keys()
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)

            print(f"Data exported successfully to {file_path}.")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()