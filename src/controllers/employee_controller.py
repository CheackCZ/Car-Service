import re
import csv

from src.connection import Connection
from src.models.employee import Employee


class EmployeeController:
    """
    Handles database operations for employee.
    """
    def __init__(self, connection):
        self.conn = connection
    
    def fetch_all(self):
        """
        Retrieves all employees from the database.
        """
        cursor = self.conn.cursor(dictionary=True)
        
        try:
            self.conn.start_transaction()

            cursor.execute("SELECT * FROM employee")
            rows = cursor.fetchall()

            self.conn.commit()
            
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
            self.conn.rollback()
            raise e
        
        finally:
            cursor.close()

    def fetch_by_id(self, employee_id):
        """
        Fetches an employee by their ID.
        """
        cursor = self.conn.cursor(dictionary=True)
        
        try:
            self.conn.start_transaction()
            
            cursor.execute("SELECT * FROM employee WHERE id = %s", (employee_id,))
            row = cursor.fetchone()
            
            self.conn.commit()
            
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
            self.conn.rollback()
            raise e
        
        finally:
            cursor.close()

    def insert(self, employee: Employee):
        """
        Inserts a new employee into the database.
        """
        cursor = self.conn.cursor()

        try:
            self.conn.start_transaction()
            
            print("Inserting new employee into the database.") 
            cursor.execute(
                """
                INSERT INTO employee (name, middle_name, last_name, phone, email, is_free)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (employee.name, employee.middle_name, employee.last_name, employee.phone, employee.email, employee.is_free)
            )
            
            self.conn.commit()
            
            employee.id = cursor.lastrowid
        
        except Exception as e:
            print(f"Error during insert operation: {e}") 
            self.conn.rollback()
            raise e
        
        finally:
            cursor.close()

    def update(self, employee: Employee):
        """
        Updates an existing employee in the database.
        """
        cursor = self.conn.cursor()

        try:
            self.conn.start_transaction()
            
            cursor.execute(
                """
                UPDATE employee
                SET name = %s, middle_name = %s, last_name = %s, phone = %s, email = %s, is_free = %s
                WHERE id = %s
                """,
                (employee.name, employee.middle_name, employee.last_name, employee.phone, employee.email, employee.is_free, employee.id)
            )
            
            self.conn.commit()
            
        except Exception as e:
            print(f"Error during update operation: {e}")
            self.conn.rollback()
            raise e
        
        finally:
            cursor.close()

    def delete(self, employee_id):
        """
        Deletes an employee by their ID after ensuring it is not used as a foreign key.
        """
        cursor = self.conn.cursor(dictionary=True)

        try:
            self.conn.start_transaction()

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
            self.conn.commit()
            
            print(f"Employee ID {employee_id} deleted successfully.")
            
        except ValueError as ve:
            self.conn.rollback()
            print(ve)
            raise ve
        
        except Exception as e:
            self.conn.rollback()
            print(f"Error during delete operation: {e}")
            raise e
        
        finally:
            cursor.close()


    def validate_import_data(self, data):
        """
        Validates the imported employee data for name, middle_name, last_name, phone, email, and is_free.

        :param data: List of dictionaries containing employee data.
        :raises ValueError: If any validation check fails.
        """
        for idx, row in enumerate(data, start=1):
            name = row.get("name", "").strip()
            if not name:
                raise ValueError(f"Row {idx}: 'name' is required.")
            elif len(name) > 50:
                raise ValueError(f"Row {idx}: 'name' exceeds the maximum length of 50 characters.")

            middle_name = row.get("middle_name", "").strip()
            if middle_name and (len(middle_name) > 50 or not re.match(r"^[a-zA-Zá-žÁ-Ž\s.]*$", middle_name)):
                raise ValueError(f"Row {idx}: 'middle_name' is invalid.")

            last_name = row.get("last_name", "").strip()
            if not last_name:
                raise ValueError(f"Row {idx}: 'last_name' is required.")
            elif len(last_name) > 50:
                raise ValueError(f"Row {idx}: 'last_name' exceeds the maximum length of 50 characters.")

            phone = row.get("phone", "").strip()
            if not phone:
                raise ValueError(f"Row {idx}: 'phone' is required.")
            elif not re.match(r"^(\+420|420)?[1-9][0-9]{8}$", phone):
                raise ValueError(f"Row {idx}: 'phone' must be a valid Czech number. It must start with +420 or 420, or be a 9-digit number starting with a non-zero digit.")

            email = row.get("email", "").strip()
            if not email:
                raise ValueError(f"Row {idx}: 'email' is required.")
            elif not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
                raise ValueError(f"Row {idx}: 'email' is not valid.")

            is_free = row.get("is_free")
            if isinstance(is_free, str):
                # Convert string representations of booleans
                if is_free.lower() == "true":
                    is_free = True
                elif is_free.lower() == "false":
                    is_free = False
                else:
                    raise ValueError(f"Row {idx}: 'is_free' must be a boolean value (True/False).")

            if not isinstance(is_free, bool):
                raise ValueError(f"Row {idx}: 'is_free' must be a boolean value.")

            # Ensure 'is_free' is stored as a boolean in the row
            row["is_free"] = is_free

    def import_data(self, data):
        """
        Imports employee data into the database after validating keys.
        """
        cursor = self.conn.cursor()

        try:
            self.validate_import_data(data)
            
            self.conn.start_transaction()
            
            for row in data:
                cursor.execute(
                    """
                    INSERT INTO employee (name, middle_name, last_name, phone, email, is_free)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (row['name'], row.get('middle_name', ''), row['last_name'], row['phone'], row['email'], row['is_free'])
                )
            
            self.conn.commit()
        
        except ValueError as ve:
            self.conn.rollback()
            raise ve
        
        except Exception as e:
            self.conn.rollback()
            raise e
        
        finally:
            cursor.close()
            

    def export_data(self, file_path):
        """
        Exports all employees to a CSV file.
        :param file_path: The path to save the CSV file.
        """
        cursor = self.conn.cursor(dictionary=True)

        try:
            self.conn.start_transaction()

            cursor.execute("SELECT * FROM employee")
            rows = cursor.fetchall()

            self.conn.commit()

            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                if not rows:
                    raise ValueError("No data available for export.")

                headers = rows[0].keys()
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)

            print(f"Data exported successfully to {file_path}.")
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()