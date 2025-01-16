from src.connection import Connection

from src.models.repair import Repair, State
from src.models.car import Car
from src.models.client import Client
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

            query = """
                SELECT repair.id, repair.date_started, repair.date_finished, repair.price, repair.state,
                       car.id AS car_id, car.registration_number, car.registration_date, car.model,
                       client.id AS client_id, client.name AS client_name, client.middle_name as client_middle_name, client.last_name as client_last_name,
                       client.phone as phone, client.email as email,
                       brand.id AS brand_id, brand.name AS brand_name,
                       employee.id AS employee_id, employee.name AS employee_name, employee.last_name, employee.middle_name, employee.phone, employee.email, employee.is_free,
                       repair_type.id AS repair_type_id, repair_type.name
                FROM repair
                JOIN car ON repair.car_id = car.id
                JOIN client ON car.client_id = client.id
                JOIN brand ON car.brand_id = brand.id
                JOIN employee ON repair.employee_id = employee.id
                JOIN repair_type ON repair.repair_type_id = repair_type.id
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            conn.commit()

            return [
                Repair(
                    id=row['id'],
                    car=Car(
                        id=row['car_id'],
                        client=Client(id=row['client_id'], name=row['client_name'], middle_name=row['client_middle_name'], last_name=row['client_last_name'],
                                      phone=row['phone'], email=row['email']),
                        brand=Brand(id=row['brand_id'], name=row['brand_name']),
                        registration_number=row['registration_number'],
                        registration_date=row['registration_date'],
                        model=row['model']
                    ),
                    employee=Employee(id=row['employee_id'], name=row['employee_name'], middle_name=row['middle_name'], last_name=row['last_name'], phone=row['phone'], email=row['email'], is_free=bool(row['is_free'])),
                    repair_type=RepairType(id=row['repair_type_id'], name=row['name']),
                    date_started=row['date_started'],
                    date_finished=row['date_finished'],
                    price=row['price'],
                    state=State(row['state']) if row['state'] else State.DEFAULT
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
        Fetches a repair by its ID.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()

            query = """
                SELECT repair.id, repair.date_started, repair.date_finished, repair.price, repair.state,
                       car.id AS car_id, car.registration_number, car.registration_date, car.model,
                       client.id AS client_id, client.name AS client_name, client.middle_name as client_middle_name, client.last_name as client_last_name,
                       client.phone as phone, client.email as email,
                       brand.id AS brand_id, brand.name AS brand_name,
                       employee.id AS employee_id, employee.name, employee.last_name,
                       repair_type.id AS repair_type_id, repair_type.name
                FROM repair
                JOIN car ON repair.car_id = car.id
                JOIN client ON car.client_id = client.id
                JOIN brand ON car.brand_id = brand.id
                JOIN employee ON repair.employee_id = employee.id
                JOIN repair_type ON repair.repair_type_id = repair_type.id
                WHERE repair.id = %s
            """
            cursor.execute(query, (repair_id,))
            row = cursor.fetchone()

            conn.commit()

            if row:
                return Repair(
                    id=row['id'],
                    car=Car(
                        id=row['car_id'],
                        client=Client(id=row['client_id'], name=row['client_name'], middle_name=row['client_middle_name'], last_name=row['client_last_name'],
                                      phone=row['phone'], email=row['email']),
                        brand=Brand(id=row['brand_id'], name=row['brand_name']),
                        registration_number=row['registration_number'],
                        registration_date=row['registration_date'],
                        model=row['model']
                    ),
                    employee=Employee(id=row['employee_id'], name=row['name'], last_name=row['last_name']),
                    repair_type=RepairType(id=row['repair_type_id'], name=row['name'], description=""),
                    date_started=row['date_started'],
                    date_finished=row['date_finished'],
                    price=row['price'],
                    state=State(row['state'])
                )
            return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def save(repair: Repair):
        """
        Saves a repair to the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            if repair.id is None:
                cursor.execute(
                    """
                    INSERT INTO repair (car_id, employee_id, repair_type_id, date_started, date_finished, price, state) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (repair.car.id, repair.employee.id, repair.repair_type.id, repair.date_started, repair.date_finished, repair.price, repair.state.value)
                )
                conn.commit()
                repair.id = cursor.lastrowid
            else:
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

    @staticmethod
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
