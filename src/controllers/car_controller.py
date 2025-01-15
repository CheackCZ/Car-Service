from src.connection import Connection

from models.car import Car
from models.client import Client
from models.brand import Brand

class CarController:
    """
    Handles database operations for car.
    """
    
    def fetch_all():
        """
        Retrieves all car from the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()
            
            query = """
                SELECT car.id, car.registration_number, car.registration_date, car.model, 
                       clients.id AS client_id, clients.first_name, clients.last_name, 
                       brands.id AS brand_id, brands.name AS brand_name
                FROM car
                JOIN clients ON car.client_id = clients.id
                JOIN brands ON car.brand_id = brands.id
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            conn.commit()
            
            return [
                Car(
                    id=row['id'],
                    client=Client(id=row['client_id'], first_name=row['first_name'], last_name=row['last_name']),
                    brand=Brand(id=row['brand_id'], name=row['brand_name']),
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
                SELECT car.id, car.registration_number, car.registration_date, car.model, 
                       clients.id AS client_id, clients.first_name, clients.last_name, 
                       brands.id AS brand_id, brands.name AS brand_name
                FROM car
                JOIN clients ON car.client_id = clients.id
                JOIN brands ON car.brand_id = brands.id
                WHERE car.id = %s
            """
            cursor.execute(query, (car_id,))
            row = cursor.fetchone()

            conn.commit()

            if row:
                return Car(
                    id=row['id'],
                    client=Client(id=row['client_id'], first_name=row['first_name'], last_name=row['last_name']),
                    brand=Brand(id=row['brand_id'], name=row['brand_name']),
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

    def save(car: Car):
        """
        Saves a car to the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            if car.id is None:
                cursor.execute(
                    """
                    INSERT INTO car (client_id, brand_id, registration_number, registration_date, model) 
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (car.client.id, car.brand.id, car.registration_number, car.registration_date, car.model)
                )
                conn.commit()
                car.id = cursor.lastrowid
            else:
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
