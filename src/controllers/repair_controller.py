from src.connection import Connection

import csv

from src.models.repair import Repair, State
from src.models.car import Car
from src.models.brand import Brand
from src.models.employee import Employee
from src.models.repair_type import RepairType

class RepairController:
    """
    Handles database operations for repair.
    """

    def fetch_all():
        """
        Retrieves all repairs from the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()

            query = "SELECT * FROM all_repairs"
            cursor.execute(query)
            rows = cursor.fetchall()

            conn.commit()

            return [
                Repair(
                    id=row['repair_id'],
                    car=Car(id=row['car_id'], brand=Brand(name=row['brand_name']), registration_number=row['car_registration_num'], model=row['car_model']),
                    employee=Employee(id=row['employee_id'], name=row['employee_name']),
                    repair_type=RepairType(name=row['repair_type']),
                    date_started=row['date_started'],
                    date_finished=row['date_finished'],
                    price=row['price'],
                    state=State(row['state'].capitalize()) if row['state'] else State.DEFAULT
                )
                for row in rows
            ]
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_by_id(repair_id):
        """
        Fetches a repair by its ID using the `all_repairs` view.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()

            query = "SELECT * FROM all_repairs WHERE repair_id = %s"
            cursor.execute(query, (repair_id,))
            row = cursor.fetchone()

            conn.commit()

            if row:
                return Repair(
                        id=row['repair_id'],
                        car=Car(id=row['car_id'], brand=Brand(name=row['brand_name']), registration_number=row['car_registration_num'], model=row['car_model']),
                        employee=Employee(id=row['employee_id'], name=row['employee_name']),
                        repair_type=RepairType(name=row['repair_type']),
                        date_started=row['date_started'],
                        date_finished=row['date_finished'],
                        price=row['price'],
                        state=State(row['state'].capitalize()) if row['state'] else State.DEFAULT
                    ) if row else None
            return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()


    def insert(repair: Repair):
        """
        Inserts a new repair into the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute(
                """
                INSERT INTO repair (car_id, employee_id, repair_type_id, date_started, date_finished, price, state) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (repair.car.id, repair.employee.id, repair.repair_type.id, repair.date_started, repair.date_finished, repair.price, repair.state.value)
            )
            conn.commit()
            repair.id = cursor.lastrowid  # Assign the new ID to the repair object
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def update(repair: Repair):
        """
        Updates an existing repair in the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute(
                """
                UPDATE repair 
                SET car_id = %s, employee_id = %s, repair_type_id = %s, date_started = %s, date_finished = %s, price = %s, state = %s 
                WHERE id = %s
                """,
                (repair.car.id, repair.employee.id, repair.repair_type.id, repair.date_started, repair.date_finished, repair.price, repair.state.value, repair.id)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def delete(repair_id):
        """
        Deletes a repair by its ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute("DELETE FROM repair WHERE id = %s", (repair_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()


    def validate_foreign_keys(data):
        """
        Validates that the foreign key IDs in the imported data exist in their respective tables.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Fetch all valid car IDs
            cursor.execute("SELECT id FROM car")
            valid_car_ids = {row["id"] for row in cursor.fetchall()}

            # Fetch all valid employee IDs
            cursor.execute("SELECT id FROM employee")
            valid_employee_ids = {row["id"] for row in cursor.fetchall()}

            # Fetch all valid repair type IDs
            cursor.execute("SELECT id FROM repair_type")
            valid_repair_type_ids = {row["id"] for row in cursor.fetchall()}

            # Validate IDs in the data
            invalid_cars = set()
            invalid_employees = set()
            invalid_repair_types = set()

            for row in data:
                if int(row["car_id"]) not in valid_car_ids:
                    invalid_cars.add(row["car_id"])
                if int(row["employee_id"]) not in valid_employee_ids:
                    invalid_employees.add(row["employee_id"])
                if int(row["repair_type_id"]) not in valid_repair_type_ids:
                    invalid_repair_types.add(row["repair_type_id"])

            # Raise errors for invalid IDs
            error_messages = []
            if invalid_cars:
                error_messages.append(f"Invalid Car IDs: {', '.join(map(str, invalid_cars))}")
            if invalid_employees:
                error_messages.append(f"Invalid Employee IDs: {', '.join(map(str, invalid_employees))}")
            if invalid_repair_types:
                error_messages.append(f"Invalid Repair Type IDs: {', '.join(map(str, invalid_repair_types))}")

            if error_messages:
                raise ValueError("\n".join(error_messages))
        finally:
            cursor.close()

    def validate_import_data(data):
        """
        Validates that the imported data contains all required keys.
        """
        required_keys = {"car_id", "employee_id", "repair_type_id", "date_started", "date_finished", "price", "state"}
        for row in data:
            missing_keys = required_keys - row.keys()
            if missing_keys:
                raise ValueError(f"Missing keys in import data: {', '.join(missing_keys)}. Include them in your import data.")

    def import_data(data):
        """
        Imports repair data into the database after validation.
        """
        conn = Connection.connection()
        cursor = conn.cursor()

        try:
            # Validate required keys
            RepairController.validate_import_data(data)

            # Validate foreign keys
            RepairController.validate_foreign_keys(data)

            conn.start_transaction()
            for row in data:
                cursor.execute(
                    """
                    INSERT INTO repair (car_id, employee_id, repair_type_id, date_started, date_finished, price, state)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (row['car_id'], row['employee_id'], row['repair_type_id'], row['date_started'], row['date_finished'], row['price'], row['state'])
                )
            conn.commit()
            print("Repairs imported successfully!")
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
        Exports all repairs to a CSV file.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)

        try:
            conn.start_transaction()

            query = "SELECT * FROM all_repairs"
            cursor.execute(query)
            rows = cursor.fetchall()

            conn.commit()

            # Write data to CSV
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                if not rows:
                    raise ValueError("No data available for export.")

                headers = rows[0].keys()
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)

            print(f"Repairs exported successfully to {file_path}.")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
