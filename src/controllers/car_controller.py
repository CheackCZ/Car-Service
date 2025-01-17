from src.connection import Connection

from src.models.car import Car
from src.models.client import Client
from src.models.brand import Brand

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
        Deletes a car by its ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            cursor.execute("DELETE FROM car WHERE id = %s", (car_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()