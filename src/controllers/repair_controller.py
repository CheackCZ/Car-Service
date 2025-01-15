from src.connection import Connection

from models.repair import Repair, State
from models.car import Car
from models.employee import Employee
from models.repair_type import RepairType

class RepairController:
    """
    Handles database operations for repair.
    """

    def fetch_all():
        """
        Retrieves all repair from the database.
        """
        conn = Connection.connection()
        cursor = conn.cursor(dictionary=True)
        try:
            conn.start_transaction()

            query = """
                SELECT repair.id, repair.date_started, repair.date_finished, repair.price, repair.state,
                       cars.id AS car_id, employees.id AS employee_id, repair_types.id AS repair_type_id,
                       cars.registration_number, employees.first_name, employees.last_name, repair_types.name
                FROM repair
                JOIN cars ON repair.car_id = cars.id
                JOIN employees ON repair.employee_id = employees.id
                JOIN repair_types ON repair.repair_type_id = repair_types.id
            """
            cursor.execute(query)
            rows = cursor.fetchall()
      
            conn.commit()
      
            return [
                Repair(
                    id=row['id'],
                    car=Car(id=row['car_id'], registration_number=row['registration_number']),
                    employee=Employee(id=row['employee_id'], first_name=row['first_name'], last_name=row['last_name']),
                    repair_type=RepairType(id=row['repair_type_id'], name=row['name'], description=""),
                    date_started=row['date_started'],
                    date_finished=row['date_finished'],
                    price=row['price'],
                    state=State(row['state'])
                )
                for row in rows
            ]
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
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
                       cars.id AS car_id, employees.id AS employee_id, repair_types.id AS repair_type_id,
                       cars.registration_number, employees.first_name, employees.last_name, repair_types.name
                FROM repair
                JOIN cars ON repair.car_id = cars.id
                JOIN employees ON repair.employee_id = employees.id
                JOIN repair_types ON repair.repair_type_id = repair_types.id
                WHERE repair.id = %s
            """
            cursor.execute(query, (repair_id,))
            row = cursor.fetchone()
           
            conn.commit()
           
            if row:
                return Repair(
                    id=row['id'],
                    car=Car(id=row['car_id'], registration_number=row['registration_number']),
                    employee=Employee(id=row['employee_id'], first_name=row['first_name'], last_name=row['last_name']),
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

    @staticmethod
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
