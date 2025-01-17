from src.connection import Connection

import csv

from src.models.car import Car
from src.models.client import Client
from src.models.brand import Brand

from CTkMessagebox import CTkMessagebox


class CarController:
    """
    Handles database operations for car.
    """

    def fetch_all():
        """
        Retrieves all cars from the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            conn.start_transaction()

            query = "SELECT * FROM all_cars"
            cursor.execute(query)
            rows = cursor.fetchall()

            conn.commit()

            return [
                Car(
                    id=row['car_id'],
                    client=Client(
                        id=row['client_id'],
                        name=row['client_name'],
                        middle_name=row.get('client_middle_name', ''),
                        last_name=row['client_last_name'],
                        phone=row['client_phone'],
                        email=row['client_email']
                    ),
                    brand=Brand(
                        id=row['brand_id'],
                        name=row['brand_name']
                    ),
                    registration_number=row['registration_number'],
                    registration_date=row['registration_date'],
                    model=row['model']
                )
                for row in rows
            ]
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_by_id(car_id):
        """
        Fetches a car by its ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)

        try:
            conn.start_transaction()

            query = """
                SELECT car.id AS car_id, car.registration_number, car.registration_date, car.model, 
                    client.id AS client_id, client.name AS client_name, client.middle_name AS client_middle_name, client.last_name AS client_last_name, 
                    client.phone AS client_phone, client.email AS client_email, 
                    brand.id AS brand_id, brand.name AS brand_name
                FROM car
                JOIN client ON car.client_id = client.id
                JOIN brand ON car.brand_id = brand.id
                WHERE car.id = %s
            """
            cursor.execute(query, (car_id,))
            row = cursor.fetchone()

            conn.commit()

            if row:
                return Car(
                    id=row['car_id'],
                    client=Client(
                        id=row['client_id'],
                        name=row['client_name'],
                        middle_name=row.get('client_middle_name', ''),
                        last_name=row['client_last_name'],
                        phone=row['client_phone'],
                        email=row['client_email']
                    ),
                    brand=Brand(
                        id=row['brand_id'],
                        name=row['brand_name']
                    ),
                    registration_number=row['registration_number'],
                    registration_date=row['registration_date'],
                    model=row['model']
                )
            return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_brand_id_by_name(brand_name):
        """
        Fetches the brand ID from the database based on the brand name.
        :param brand_name: The name of the brand.
        :return: The ID of the brand.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)

        try:
            conn.start_transaction()

            query = "SELECT id FROM brand WHERE name = %s"
            cursor.execute(query, (brand_name,))
            result = cursor.fetchone()

            conn.commit()

            if result:
                return result["id"]
            else:
                raise ValueError(f"Brand '{brand_name}' not found in the database.")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def insert(car: Car):
        """
        Inserts a new car into the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute(
                """
                INSERT INTO car (client_id, brand_id, registration_number, registration_date, model) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (car.client.id, car.brand.id, car.registration_number, car.registration_date, car.model)
            )
            conn.commit()
            car.id = cursor.lastrowid  # Update the car's ID with the newly inserted row ID
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()


    def update(car: Car):
        """
        Updates an existing car in the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute(
                """
                UPDATE car 
                SET client_id = %s, brand_id = %s, registration_number = %s, registration_date = %s, model = %s 
                WHERE id = %s
                """,
                (car.client.id, car.brand.id, car.registration_number, car.registration_date, car.model, car.id)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def delete(car_id):
        """
        Deletes a car by its ID after ensuring it is not used as a foreign key in the repair table.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)

        try:
            conn.start_transaction()

            # Check if the car ID is referenced in the repair table
            cursor.execute(
                """
                SELECT COUNT(*) AS ref_count
                FROM repair
                WHERE car_id = %s
                """,
                (car_id,)
            )
            result = cursor.fetchone()
            if result["ref_count"] > 0:
                raise ValueError(f"Cannot delete car ID {car_id}: It is referenced in {result['ref_count']} repair(s).")

            # Proceed with deletion if no references are found
            cursor.execute("DELETE FROM car WHERE id = %s", (car_id,))
            conn.commit()
            print(f"Car ID {car_id} deleted successfully.")
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
        required_keys = {"client_id", "brand_id", "registration_number", "registration_date", "model"}
        for row in data:
            # Check for missing keys
            missing_keys = required_keys - row.keys()
            if missing_keys:
                raise ValueError(f"Missing keys in import data: {', '.join(missing_keys)}. Include them in your import data.")

    def validate_client_and_brand_ids(data):
        """
        Validates if client_ids and brand_ids in the data exist in the database.
        Raises a ValueError if any are missing.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Fetch all valid client IDs
            cursor.execute("SELECT id FROM client")
            valid_client_ids = {row["id"] for row in cursor.fetchall()}

            # Fetch all valid brand IDs
            cursor.execute("SELECT id FROM brand")
            valid_brand_ids = {row["id"] for row in cursor.fetchall()}

            # Check each row's client_id and brand_id
            invalid_clients = set()
            invalid_brands = set()

            for row in data:
                if int(row["client_id"]) not in valid_client_ids:
                    invalid_clients.add(row["client_id"])
                if int(row["brand_id"]) not in valid_brand_ids:
                    invalid_brands.add(row["brand_id"])

            # Raise exception with details if invalid entries are found
            if invalid_clients or invalid_brands:
                error_message = []
                if invalid_clients:
                    error_message.append(f"Invalid Client IDs: {', '.join(map(str, invalid_clients))}")
                if invalid_brands:
                    error_message.append(f"Invalid Brand IDs: {', '.join(map(str, invalid_brands))}")
                raise ValueError("\n".join(error_message))
        finally:
            cursor.close()


    def import_data(data):
        """
        Imports car data into the database after validating keys, client_ids, and brand_ids.
        Shows a CTkMessagebox error if validation fails.
        """
        conn = Connection.connection()
        cursor = conn.cursor()

        try:
            # Step 1: Validate required keys
            CarController.validate_import_data(data)

            # Step 2: Validate client_ids and brand_ids
            CarController.validate_client_and_brand_ids(data)

            # Step 3: Import data into the database
            conn.start_transaction()
            for row in data:
                cursor.execute(
                    """
                    INSERT INTO car (client_id, brand_id, registration_number, registration_date, model)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (row['client_id'], row['brand_id'], row['registration_number'], row['registration_date'], row['model'])
                )
            conn.commit()
            CTkMessagebox(title="Success", message="Data imported successfully!", icon="info")
        except ValueError as ve:
            # Show validation errors
            CTkMessagebox(title="Validation Error", message=str(ve), icon="warning")
            conn.rollback()
        except Exception as e:
            # Handle unexpected errors
            CTkMessagebox(title="Error", message=f"Unexpected error: {e}", icon="warning")
            conn.rollback()
        finally:
            cursor.close()