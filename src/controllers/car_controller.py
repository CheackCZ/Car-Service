from src.connection import Connection

from datetime import datetime
import re
import csv

from ..models.car import Car
from ..models.client import Client
from ..models.brand import Brand


class CarController:
    """
    Handles database operations for car.
    """
    def __init__(self, connection):
        self.conn = connection
        
    def fetch_all(self):
        """
        Retrieves all cars from the database.
        """
        cursor = self.conn.cursor(dictionary=True)
        
        try:
            self.conn.start_transaction()

            query = "SELECT * FROM all_cars"
            cursor.execute(query)
            rows = cursor.fetchall()

            self.conn.commit()

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
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_by_id(self, car_id):
        """
        Fetches a car by its ID.
        """
        cursor = self.conn.cursor(dictionary=True)

        try:
            self.conn.start_transaction()

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

            self.conn.commit()

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
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def fetch_brand_id_by_name(self, brand_name):
        """
        Fetches the brand ID from the database based on the brand name.
        :param brand_name: The name of the brand.
        :return: The ID of the brand.
        """
        cursor = self.conn.cursor(dictionary=True)

        try:
            self.conn.start_transaction()

            query = "SELECT id FROM brand WHERE name = %s"
            cursor.execute(query, (brand_name,))
            result = cursor.fetchone()

            self.conn.commit()

            if result:
                return result["id"]
            else:
                raise ValueError(f"Brand '{brand_name}' not found in the database.")
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def insert(self, car: Car):
        """
        Inserts a new car into the database.
        """
        cursor = self.conn.cursor()
        try:
            self.conn.start_transaction()
            cursor.execute(
                """
                INSERT INTO car (client_id, brand_id, registration_number, registration_date, model) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (car.client.id, car.brand.id, car.registration_number, car.registration_date, car.model)
            )
            self.conn.commit()
            car.id = cursor.lastrowid  # Update the car's ID with the newly inserted row ID
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()


    def update(self, car: Car):
        """
        Updates an existing car in the database.
        """
        cursor = self.conn.cursor()
        try:
            self.conn.start_transaction()
            cursor.execute(
                """
                UPDATE car 
                SET client_id = %s, brand_id = %s, registration_number = %s, registration_date = %s, model = %s 
                WHERE id = %s
                """,
                (car.client.id, car.brand.id, car.registration_number, car.registration_date, car.model, car.id)
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def delete(self, car_id):
        """
        Deletes a car by its ID after ensuring it is not used as a foreign key in the repair table.
        """
        cursor = self.conn.cursor(dictionary=True)

        try:
            self.conn.start_transaction()

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
            self.conn.commit()
            print(f"Car ID {car_id} deleted successfully.")
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
        Validates the imported car data for registration_number, registration_date, and model.

        :param data: List of dictionaries containing car data.
        """
        for idx, row in enumerate(data, start=1):
            registration_number = row.get("registration_number", "").strip()

            if not registration_number:
                raise ValueError(f"Row {idx}: 'registration_number' is required.")
            elif len(registration_number) > 15:
                raise ValueError(f"Row {idx}: 'registration_number' exceeds the maximum length of 15 characters.")
            elif not re.match(r"[A-Z0-9]{1,3}[- ]?[0-9]{1,4}", registration_number):
                raise ValueError(f"Row {idx}: 'registration_number' is invalid. Must match the format.")

            registration_date = row.get("registration_date", "").strip()

            if not registration_date:
                raise ValueError(f"Row {idx}: 'registration_date' is required.")
            else:
                try:
                    datetime.strptime(registration_date, "%Y-%m-%d")
                except ValueError:
                    raise ValueError(f"Row {idx}: 'registration_date' must be in YYYY-MM-DD format.")

            model = row.get("model", "").strip()

            if not model:
                raise ValueError(f"Row {idx}: 'model' is required.")
            elif len(model) > 50:
                raise ValueError(f"Row {idx}: 'model' exceeds the maximum length of 50 characters.")
            elif not re.match(r"^[a-zA-Z0-9á-žÁ-Ž\s]+$", model):
                raise ValueError(f"Row {idx}: 'model' contains invalid characters. Only letters, numbers, and spaces are allowed.")

    def validate_client_and_brand_ids(self, data):
        """
        Validates if client_ids and brand_ids in the data exist in the database.
        """
        cursor = self.conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT id FROM client")
            valid_client_ids = {row["id"] for row in cursor.fetchall()}

            cursor.execute("SELECT id FROM brand")
            valid_brand_ids = {row["id"] for row in cursor.fetchall()}

            invalid_clients = set()
            invalid_brands = set()

            for row in data:
                if int(row["client_id"]) not in valid_client_ids:
                    invalid_clients.add(row["client_id"])
                if int(row["brand_id"]) not in valid_brand_ids:
                    invalid_brands.add(row["brand_id"])

            if invalid_clients or invalid_brands:
                error_message = []
                
                if invalid_clients:
                    error_message.append(f"Invalid Client IDs: {', '.join(map(str, invalid_clients))}")
                if invalid_brands:
                    error_message.append(f"Invalid Brand IDs: {', '.join(map(str, invalid_brands))}")
                raise ValueError("\n".join(error_message))
        finally:
            cursor.close()


    def import_data(self, data):
        """
        Imports car data into the database after validating keys, client_ids, and brand_ids.
        Shows a CTkMessagebox error if validation fails.
        """
        cursor = self.conn.cursor()

        try:
            self.validate_import_data(data)

            self.validate_client_and_brand_ids(data)

            self.conn.start_transaction()

            for row in data:
                cursor.execute(
                    """
                    INSERT INTO car (client_id, brand_id, registration_number, registration_date, model)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (row['client_id'], row['brand_id'], row['registration_number'], row['registration_date'], row['model'])
                )

            self.conn.commit()

            print("Data imported successfully!")
        except ValueError as ve:
            print(f"Validation Error: {ve}")
            self.conn.rollback()
        except Exception as e:
            print(f"Exception: {e}")
            self.conn.rollback()
        finally:
            cursor.close()