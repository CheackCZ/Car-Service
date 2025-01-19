from src.connection import Connection

from datetime import datetime, date

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
        Inserts a new repair into the database after checking car and employee availability.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)

        try:
            conn.start_transaction()

            # Validate that car is not used somewhere else currently
            cursor.execute(
                """
                SELECT COUNT(*) AS ref_count
                FROM repair
                WHERE car_id = %s AND state IN ('Pending', 'In process')
                """,
                (repair.car.id,)
            )
            
            car_check = cursor.fetchone()
            if car_check["ref_count"] > 0:
                raise ValueError(f"Car ID {repair.car.id} is already under (different) repair.")

            # Validate that employee is not used somewhere else currently
            cursor.execute(
                """
                SELECT is_free 
                FROM employee
                WHERE id = %s
                """,
                (repair.employee.id,)
            )
            
            employee = cursor.fetchone()
            if not employee or not employee["is_free"]:
                raise ValueError(f"Employee ID {repair.employee.id} is currently working on other repair and cannot be assigned to this repair.")
            
            
            # Insert the repair into the database
            cursor.execute(
                """
                INSERT INTO repair (car_id, employee_id, repair_type_id, date_started, date_finished, price, state)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    repair.car.id,
                    repair.employee.id,
                    repair.repair_type.id,
                    repair.date_started,
                    repair.date_finished,
                    repair.price,
                    repair.state.value,
                )
            )

            # Update the employee's status to not free
            if not repair.state.value.capitalize() in ["Completed", "Canceled"]:
                cursor.execute(
                    """
                    UPDATE employee
                    SET is_free = FALSE
                    WHERE id = %s
                    """,
                    (repair.employee.id,)
                )

            conn.commit()
            print(f"Repair added successfully, and Employee ID {repair.employee.id} marked as not free.")
            
        except ValueError as ve:
            print(f"{ve}")
            
        except Exception as e:
            conn.rollback()
            print(f"Error during repair insertion: {e}")
            raise e
        
        finally:
            cursor.close()


    def update_state(repair_id, new_state, cursor):
        """
        Updates the state of a repair and frees the employee if the state is 'Completed' or 'Canceled'.
        """
        try:
            # Update the repair's state
            cursor.execute(
                """
                UPDATE repair
                SET state = %s
                WHERE id = %s
                """,
                (new_state, repair_id)
            )

            # Free the employee if the state is 'Completed' or 'Canceled'
            if new_state.capitalize() in ["Completed", "Canceled"]:
                cursor.execute(
                    """
                    SELECT employee_id
                    FROM repair
                    WHERE id = %s
                    """,
                    (repair_id,)
                )
                result = cursor.fetchone()
                if result:
                    employee_id = result[0]
                    cursor.execute(
                        """
                        UPDATE employee
                        SET is_free = TRUE
                        WHERE id = %s
                        """,
                        (employee_id,)
                    )
                    print(f"Employee ID {employee_id} marked as free due to repair state change to '{new_state}'.")

        except Exception as e:
            print(f"Error during state update: {e}")
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
            
            if type(repair.date_finished) == date:
                date_finished = str(repair.date_finished)
            date_finished = repair.date_finished
            
            cursor.execute(
                """
                UPDATE repair 
                SET car_id = %s, employee_id = %s, repair_type_id = %s, date_started = %s, date_finished = %s, price = %s, state = %s 
                WHERE id = %s
                """,
                (repair.car.id, repair.employee.id, repair.repair_type.id, str(repair.date_started), date_finished, repair.price, repair.state.value, repair.id)
            )
            
            # Update state-specific logic
            RepairController.update_state(repair.id, repair.state.value, cursor)
            
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
        Validates the imported repair data for required keys, data types, and value ranges.

        :param data: List of dictionaries containing repair data.
        :raises ValueError: If any validation check fails.
        """
        required_keys = {"car_id", "employee_id", "repair_type_id", "date_started", "date_finished", "price", "state"}
        valid_states = {"Pending", "In process", "Completed", "Canceled"}

        for idx, row in enumerate(data, start=1):
            missing_keys = required_keys - row.keys()
            if missing_keys:
                raise ValueError(f"Row {idx}: Missing keys: {', '.join(missing_keys)}.")

            car_id = int(row.get("car_id"))
            if not isinstance(car_id, int) or car_id <= 0:
                raise ValueError(f"Row {idx}: 'car_id' must be a positive integer.")

            employee_id = int(row.get("employee_id"))
            if not isinstance(employee_id, int) or employee_id <= 0:
                raise ValueError(f"Row {idx}: 'employee_id' must be a positive integer.")

            repair_type_id = int(row.get("repair_type_id"))
            if not isinstance(repair_type_id, int) or repair_type_id <= 0:
                raise ValueError(f"Row {idx}: 'repair_type_id' must be a positive integer.")

            date_started = row.get("date_started", "").strip()
            try:
                datetime.stpftime(date_started, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Row {idx}: 'date_started' must be in YYYY-MM-DD format.")

            date_finished = row.get("date_finished", "").strip()
            if date_finished:
                try:
                    datetime.strptime(date_finished, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError(f"Row {idx}: 'date_finished' must be in YYYY-MM-DD format.")
                if date_started > date_finished:
                    raise ValueError(f"Row {idx}: 'date_finished' cannot be earlier than 'date_started'.")

            price = float(row.get("price"))
            if not isinstance(price, (int, float)) or price < 0:
                raise ValueError(f"Row {idx}: 'price' must be a non-negative number.")

            state = row.get("state", "").strip().capitalize()
            try:
                State(state)
            except ValueError:
                valid_states = ', '.join([s.value for s in State])
                raise ValueError(f"Row {idx}: 'state' must be one of {valid_states}.")

        print("Validation passed!")
        

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
