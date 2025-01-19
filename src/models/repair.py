from enum import Enum
from datetime import datetime, date

from src.models.employee import Employee
from src.models.car import Car
from src.models.repair_type import RepairType


class State(Enum):
    """
    Enum representing the possible states of a repair.
    """
    DEFAULT = "Pending"
    IN_PROCESS = "In process"
    COMPLETED = "Completed"
    CANCELED = "Canceled"


class Repair:
    """
    Class representing individual Repairs in the database.
    """

    def __init__(self, id: int = 0, car: Car = None, employee: Employee = None, repair_type: RepairType = None, date_started: date = None, date_finished: date = None, price: float = 0.0, state: State = State.DEFAULT,):
        """
        Initializes Repair instance.
        """
        # Validate id
        if not isinstance(id, int) or id < 0:
            raise ValueError("'id' must be a positive integer.")

        # Validate car
        if not isinstance(car, Car):
            raise TypeError("'car' must be an instance of Car.")

        # Validate employee
        if not isinstance(employee, Employee):
            raise TypeError("'employee' must be an instance of Employee.")

        # Validate repair_type
        if not isinstance(repair_type, RepairType):
            raise TypeError("'repair_type' must be an instance of RepairType.")

        # Validate date_started
        if not isinstance(date_started, date):
            raise TypeError("'date_started' must be a date object.")

        # Validate date_finished
        if date_finished is not None and not isinstance(date_finished, date):
            raise TypeError("'date_finished' must be a date object or None.")
        if date_finished and date_finished < date_started:
            raise ValueError("'date_finished' cannot be earlier than 'date_started'.")

        # Validate price
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("'price' must be a non-negative float or integer.")

        # Validate state
        if not isinstance(state, State):
            raise TypeError("'state' must be an instance of State (Enum).")

        # Assign attributes
        self.id = id
        self.car = car
        self.employee = employee
        self.repair_type = repair_type
        self.date_started = date_started
        self.date_finished = date_finished
        self.price = price
        self.state = state

    def __str__(self):
        """
        Returns a string representation of the Repair instance.
        
        :return str: A formatted string with the repair's details.
        """
        return f"({self.id}) {self.car} | {self.employee} | {self.repair_type} | {self.date_started} -> {self.date_finished or 'N/A'} | {self.price} | {self.state.value}"
        

    def to_dict(self):
        """
        Converts the Repair object into a dictionary representation.
        """
        return {
            "id": self.id,
            "employee_name": self.employee.name,
            "employee_middle_name": self.employee.middle_name,
            "employee_last_name": self.employee.last_name,
            "employee_id": self.employee.id,
            "car_model": self.car.model,
            "car_registration_num": self.car.registration_number,
            "brand_name": self.car.brand.name,
            "repair_type": self.repair_type.name,
            "date_started": self.date_started.strftime("%Y-%m-%d"),
            "date_finished": self.date_finished.strftime("%Y-%m-%d") if self.date_finished else "N/A",
            "price": self.price,
            "state": self.state.value,
        }
