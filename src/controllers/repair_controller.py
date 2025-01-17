from src.connection import Connection

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
